from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from functools import cached_property
from itertools import combinations
from typing import Dict, List, Optional, Union, cast

import numpy as np
from pydantic import model_validator

import mfire.utils.mfxarray as xr
from mfire.composite.base import BaseModel, precached_property
from mfire.composite.component import RiskComponentComposite
from mfire.composite.operator import ComparisonOperator
from mfire.localisation.risk_localisation import RiskLocalisation
from mfire.settings import SPACE_DIM, get_logger
from mfire.text.base.reducer import BaseReducer
from mfire.text.risk.rep_value import RepValueReducer
from mfire.utils.date import Datetime, Timedelta
from mfire.utils.exception import LocalisationWarning
from mfire.utils.period import Period, Periods
from mfire.utils.string import split_var_name
from mfire.utils.template import CentroidTemplateRetriever, TemplateRetriever
from mfire.utils.unit_converter import unit_conversion
from mfire.utils.wwmf import Wwmf

# Logging
LOGGER = get_logger(name="text_reducer.mod", bind="text_reducer")


class RiskReducer(BaseReducer):
    composite: Optional[RiskComponentComposite] = None
    localisation: Optional[RiskLocalisation] = None
    geo_id: str

    @cached_property
    def strategy(self) -> RiskReducerStrategy:
        """Decides which comment generation module to use."""
        if self.composite.hazard_name == "Neige":
            return RiskReducerStrategySnow(reducer=self)
        elif self.is_multizone:
            return RiskReducerStrategyMultizone(reducer=self)
        return RiskReducerStrategyMonozone(reducer=self)

    @model_validator(mode="after")
    def init_localisation(self):
        if self.localisation is None:
            try:
                self.localisation = RiskLocalisation(
                    risk_component=cast(RiskComponentComposite, self.composite),
                    geo_id=self.geo_id,
                )
                self.localisation.compute()
            except LocalisationWarning:
                self.localisation = None
        return self

    @property
    def is_multizone(self) -> bool:
        return self.localisation is not None and self.localisation.is_multizone

    @precached_property
    def final_risk_da(self) -> xr.DataArray:
        return self.composite.final_risk_da.sel(id=self.geo_id)

    @precached_property
    def final_risk_max(self) -> int:
        return self.final_risk_da.max().item()

    @precached_property
    def risk_ds(self) -> xr.Dataset:
        return self.composite.risk_ds

    def post_process(self):
        """Make a post-process operation in the reduction."""
        super().post_process()
        self.strategy.process_period()

    def _compute(self) -> dict:
        """Decides which comment generation module to use."""
        self.reduction = self.strategy.compute()
        self.reduction["alt_area_name"] = self.composite.alt_area_name(self.geo_id)
        return self.reduction


class RiskReducerStrategy(BaseModel, ABC):
    reducer: RiskReducer

    @property
    def reduction(self):
        return self.reducer.reduction

    @reduction.setter
    def reduction(self, value):
        self.reducer.reduction = value

    @abstractmethod
    def compute(self):
        pass

    @abstractmethod
    def process_period(self):
        pass


class RiskReducerStrategySnow(RiskReducerStrategy):
    def compute(self):
        """Make the reduction in the case of snow risk - see #40981"""
        final_risk_max = self.reducer.final_risk_max
        if final_risk_max == 0:
            return {"key": "RAS"}

        wwmf = self.reducer.composite.params["WWMF__SOL"].compute()
        wwmf = Wwmf.is_snow(wwmf) & (wwmf != 58)

        density = wwmf.sum(dim=SPACE_DIM) / wwmf.sum()
        density = (density[:-1].to_numpy() + density[1:].to_numpy()) >= 0.05
        if density.sum() == 0:
            return {"key": "RAS"}

        stops = [Datetime(vt) for vt in wwmf.valid_time]
        if len(stops) == 1:
            starts = [wwmf.valid_time[0] - Timedelta(hours=1)] + stops[:-1]
        else:
            starts = [
                wwmf.valid_time[0] - (wwmf.valid_time[1] - wwmf.valid_time[0])
            ] + stops[:-1]

        density = np.concatenate(([False], density, [False]))
        starts = [starts[idx] for idx in (density[1:] & ~density[:-1]).nonzero()[0]]
        stops = [stops[idx] for idx in (~density[1:] & density[:-1]).nonzero()[0]]

        periods = Periods([Period(start, stop) for start, stop in zip(starts, stops)])

        spatial_risk_da = xr.concat(
            [
                lvl.spatial_risk_da.sel(id=self.reducer.geo_id)
                for lvl in self.reducer.composite.risks_of_level(final_risk_max)
            ],
            dim="valid_time",
        )
        intensity = (
            self.reducer.composite.params["NEIPOT3__SOL"].compute() * spatial_risk_da
        )
        intensity = unit_conversion(intensity, "cm")

        if self.reducer.is_multizone:
            localisation = self.reducer.localisation.all_name
        else:
            localisation = self.reducer.composite.alt_area_name(self.reducer.geo_id)

        return {
            "periods": self.reducer.composite.period_describer.describe(periods),
            "key": "low" if intensity.max().item() < 5 else "high",
            "localisation": localisation,
        }

    def process_period(self):
        """Process the period."""
        pass


class RiskReducerStrategyMonozone(RiskReducerStrategy):
    def process_value(self, param: str, evts_ds: List, kind: str) -> Optional[Dict]:
        """
        Retrieves all significant values (min, max, rep_value, units, etc.)
        for plain or mountain (kind argument).

        Args:
            param (str): Parameter (e.g. NEIPOT24__SOL).
            evts_ds (List): List of datasets containing events for a parameter.
            kind (str): Plain or mountain.

        Returns:
            Dict: Dictionary containing the information or None if the information is
                not available (e.g., for a qualitative parameter or when kind is
                mountain but no mountain is available).
        """
        occurrence_evt = False
        data_vars = evts_ds[0].data_vars
        threshold, min_v, max_v, rep_value = np.NaN, np.NaN, np.NaN, np.NaN
        if all(
            (
                f"min_{kind}" in data_vars,
                f"max_{kind}" in data_vars,
                f"rep_value_{kind}" in data_vars,
                kind in self.operator_dict[param],
            )
        ):
            ev_values = []
            for ev in evts_ds:
                occurrence_evt = occurrence_evt or ev[f"occurrence_{kind}"].item()
                if ev[f"min_{kind}"].values < min_v or np.isnan(min_v):
                    min_v = ev[f"min_{kind}"].values

                if ev[f"max_{kind}"].values > max_v or np.isnan(max_v):
                    max_v = ev[f"max_{kind}"].values

                ev_values.append(ev[f"rep_value_{kind}"].values)

            rep_value = self.operator_dict[param][kind].critical_value(ev_values)
            threshold = evts_ds[0][f"threshold_{kind}"].item()

        def format_func(x):
            return float(x) if not np.isnan(x) else None

        values_dict = {
            "min": format_func(min_v),
            "max": format_func(max_v),
            "value": format_func(rep_value),
            "units": str(evts_ds[0].units.data),
            "operator": self.operator_dict[param].get(kind),
            "threshold": threshold,
            "occurrence": occurrence_evt,
        }

        return values_dict if None not in values_dict.values() else None

    def infos(self, data: Union[List[xr.Dataset], List[xr.DataArray]]) -> Dict:
        """
        Retrieves the information for each block Bi.

        Args:
            data (Union[List[xr.Dataset], List[xr.DataArray]]): List of DataArray or
                    Dataset for the same level.

        Returns:
            dict: Dictionary summarizing the desired information.
        """
        if isinstance(data[0], xr.DataArray):
            return {
                "centroid": data[0].centroid.item(),
                "level": 0,
                "start": Datetime(min(data)),
                "stop": Datetime(max(data)),
            }

        time = []
        level = int(data[0].risk_level.values)
        bloc = {"centroid": data[0].centroid.item(), "level": level}

        event_dict = defaultdict(lambda: [])
        for ech in data:
            time.append(ech.valid_time.values)
            for ev in ech.evt:
                event = ech.sel(evt=ev)
                key_event = str(event.weatherVarName.values)
                # to handle no condition for some event for some level
                # e.g. lvl1 with evt1 and evt2 but lvl2 with only evt1
                if key_event != "nan":
                    event_dict[str(event.weatherVarName.data)].append(event)

        for param, evt_ds in event_dict.items():
            bloc[param] = {}
            plain = self.process_value(param, evt_ds, "plain")
            if plain:
                bloc[param]["plain"] = {**plain}

            mountain = self.process_value(param, evt_ds, "mountain")
            if mountain:
                bloc[param]["mountain"] = {**mountain}
            if (
                mountain_altitude := self.reducer.composite.risks_of_level(level=level)[
                    0
                ]
                .events[0]
                .mountain_altitude
            ) is not None:
                bloc[param]["mountain_altitude"] = mountain_altitude

        bloc["start"], bloc["stop"] = Datetime(min(time)), Datetime(max(time))
        return bloc

    @property
    def final_risk_da(self) -> xr.DataArray:
        # Handling of 3h blocs to avoid to repeat same period name - see #34947
        final_risk_da = self.reducer.final_risk_da.resample(valid_time="3h").max()
        final_risk_da = final_risk_da.reindex(
            valid_time=self.reducer.final_risk_da.valid_time, method="ffill"
        )

        # Handling of beginning and ending blocs to avoid to repeat same period name
        # - see #34947
        final_risk_da.values[:3] = max(final_risk_da[:3])
        final_risk_da.values[-3:] = max(final_risk_da[-3:])
        return final_risk_da

    @property
    def norm_risk(self) -> np.ndarray:
        """
        Returns normalized risk levels in the range 0 to 1.

        Returns:
            np.ndarray: Normalized risk levels.
        """
        final_risk = self.final_risk_da.values
        if (max_level := self.reducer.risk_ds.risk_level.max().item()) > 1:
            # Normalize risk levels
            final_risk = np.where(
                final_risk, 1 - (((max_level - final_risk) * 0.5) / (max_level - 1)), 0
            )
        return final_risk

    @precached_property
    def operator_dict(self) -> Dict[str, Dict[str, ComparisonOperator]]:
        """Get the comparison operators used for rounding the representative values.

        Returns:
            operator_dict (Dict): Dictionary containing the comparison operators per
                event.
        """
        operator_dict = {}
        for level in self.reducer.composite.levels:
            for ev in level.events:
                operator_dict[ev.field.name] = {}
                try:
                    operator_dict[ev.field.name]["plain"] = ev.plain.comparison_op
                except AttributeError:
                    pass
                try:
                    operator_dict[ev.field.name]["mountain"] = ev.mountain.comparison_op
                except AttributeError:
                    pass
        return operator_dict

    def find_template_type(self):
        """
        Determines the template type (general, snow or precip) based on the variables
        included in the reduction block.

        Returns:
            str: The template type.
        """
        template_type = "general"

        if self.reducer.final_risk_max > 0:
            # Iterate over the reduction blocks
            for key, bloc in self.reduction.items():
                # Skip blocks that don't start with "B" or don't have the maximum risk
                # level.
                if (
                    not key.startswith("B")
                    or bloc["level"] != self.reducer.final_risk_max
                ):
                    continue

                # Get the variable names of the reduction block, excluding the keys that
                # are not relevant.
                keys = {
                    split_var_name(var_name, full_var_name=False)[0]
                    for var_name in bloc.keys()
                    if var_name not in ["level", "start", "stop", "centroid"]
                }

                # Determine the template type based on the variable names.
                if keys.issubset({"PRECIP", "EAU"}):
                    template_type = "PRECIP"
                    break

        self.reduction["type"] = template_type

    def _find_levels_data_loop(self, data: dict):
        # Determine the level key based on the centroid value.
        if data["centroid"] == 1:
            level_key = "level_max"
        elif data["level"] != 0:
            level_key = "level_int"
        else:
            return

        for key, param in data.items():
            # Skip keys that are not relevant to the level comparison
            if key in ["level", "start", "stop", "centroid"]:
                continue

            # If the key is already present in the level dictionary and the
            # representative values is not better than the stored one, skip the
            # parameter.
            if key in self.reduction[level_key] and RepValueReducer.compare(
                self.reduction[level_key][key], param
            ):
                continue

            # Otherwise, add the parameter to the level dictionary.
            self.reduction[level_key][key] = param

    def find_levels(self):
        """
        Add information about the maximum and intermediate levels to the reduction.

        This function iterates over the blocks in the reduction and adds information
        about the maximum and intermediate levels to the `level_max` and `level_int`
        dictionaries.

        The maximum level is determined by the centroid value. The intermediate levels
        are determined by comparing the representative values of the same parameter for
        the same level.
        """

        # Initialize the maximum and intermediate level dictionaries.
        self.reduction["level_max"] = {}
        self.reduction["level_int"] = {}

        # Iterate over the blocks in the reduction.
        for bloc, data in self.reduction.items():
            if bloc.startswith("B"):
                self._find_levels_data_loop(data)

    def process_period(self):
        """Process period-related tags in the comment for monozone case."""
        # Process each key-value pair in the reduction dictionary
        if self.reduction is None:
            return

        for key, val in self.reduction.items():
            # Check if the value is a dictionary with 'start' and 'stop' keys
            if isinstance(val, dict) and "start" in val and "stop" in val:
                # Add the period elements to the period table_localisation
                period_describer = self.reducer.composite.period_describer
                self.reduction[key]["period"] = period_describer.describe(
                    Period(val["start"], val["stop"])
                )
                self.reduction[key]["start"] = period_describer.describe(
                    Period(val["start"])
                )
                self.reduction[key]["stop"] = period_describer.describe(
                    Period(val["stop"])
                )

    def compute(self) -> dict:
        """
        Reduces the risk into blocks based on the blocks found after using dtw.

        Returns:
            Union[List, dict]: Reduced risk as a list and a dictionary containing
                information for each block.
        """
        final_risk_da = self.final_risk_da

        self.reduction = CentroidTemplateRetriever.read_file(
            TemplateRetriever.path_by_name("risk/monozone_generic"),
            index_col=["0", "1", "2", "3", "4"],
        ).get_by_dtw(self.norm_risk)

        final_risk_da["blocks"] = ("valid_time", [v[1] for v in self.reduction["path"]])
        centroid_list = []
        last = final_risk_da["blocks"].values[0]
        for x in final_risk_da["blocks"].values:
            if last == x:
                centroid_list.append(self.reduction["centroid"][last])
            else:
                centroid_list.append(self.reduction["centroid"][last + 1])
            last = x
        final_risk_da["centroid"] = ("valid_time", centroid_list)

        # Construction of B blocks
        same_level_list = []
        for idx, risk in enumerate(final_risk_da):
            if (
                idx > 0
                and risk["centroid"].data != final_risk_da["centroid"].data[idx - 1]
            ):
                previous_block = risk["blocks"].data - 1
                self.reduction[f"B{previous_block}"] = self.infos(same_level_list)
                same_level_list.clear()

            if risk["centroid"].values == 0:
                same_level_list.append(risk["valid_time"])
            elif risk.values in self.reducer.risk_ds.risk_level.values:
                same_level_list.append(
                    self.reducer.risk_ds.sel(
                        id=self.reducer.geo_id,
                        valid_time=risk["valid_time"],
                        risk_level=risk.values,
                    )
                )
        last_block = final_risk_da[-1]["blocks"].data
        self.reduction[f"B{last_block}"] = self.infos(same_level_list)
        self.find_template_type()
        self.find_levels()

        return self.reduction


class RiskReducerStrategyMultizone(RiskReducerStrategy):
    def process_period(self):
        """Process period-related tags in the comment for multizone case."""
        periods = []
        for period_name in self.reducer.localisation.periods_name:
            time_list = period_name.split("_to_")
            periods += [Period(time_list[0], time_list[-1])]

        elements = range(len(periods))

        for i in elements:
            for combin in combinations(elements, i + 1):
                keys, values = [], Periods()
                for j in combin:
                    keys += [str(j + 1)]
                    values += [periods[j]]
                key = "periode" + "_".join(keys)
                self.reduction[key] = self.reducer.composite.period_describer.describe(
                    values
                )

    def compute(self) -> dict:
        self.reduction = self.reducer.localisation.table_localisation.table
        return self.reduction
