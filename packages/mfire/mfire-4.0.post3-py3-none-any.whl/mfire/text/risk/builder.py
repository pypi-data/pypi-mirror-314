from __future__ import annotations

from typing import Optional, Tuple, Union

import numpy as np
import pandas as pd
from pydantic import model_validator

import mfire.utils.mfxarray as xr
from mfire.composite.base import precached_property
from mfire.composite.component import RiskComponentComposite
from mfire.composite.operator import ComparisonOperator
from mfire.settings import get_logger
from mfire.text.base.builder import BaseBuilder
from mfire.text.risk.reducer import RiskReducer
from mfire.text.risk.rep_value import RepValueBuilder, RepValueReducer
from mfire.utils.string import clean_text

# Logging
LOGGER = get_logger(name="text.risk.builder.mod", bind="risk.builder")


class RiskBuilder(BaseBuilder):
    """
    This class enables to manage all text for representative values. It chooses which
    class needs to be used for each case.
    """

    geo_id: str
    reducer_class: type = RiskReducer
    reducer: Optional[RiskReducer] = None
    composite: Optional[RiskComponentComposite] = None

    module_name: str = "risk"

    @model_validator(mode="after")
    def init_reducer(self):
        if self.reducer is None:
            self.reducer = self.reducer_class(
                geo_id=self.geo_id, data=self.data, composite=self.composite
            )
        return self

    @property
    def is_multizone(self):
        return self.reducer.is_multizone

    @property
    def template_name(self) -> str:
        if self.composite.hazard_name == "Neige":
            return "snow"
        if self.is_multizone:
            return f"multizone_{self.reducer.localisation.template_type}"
        if self.reduction["type"] == "general":
            return "monozone_generic"
        return "monozone_precip"

    @property
    def template_key(self) -> Union[str, np.ndarray]:
        """
        Get the template key.

        Returns:
            str: The template key.
        """
        if self.composite.hazard_name == "Neige":
            return self.reduction["key"]
        if self.is_multizone:
            return self.reducer.localisation.unique_name
        if self.reduction["type"] != "general":
            return self.reduction["type"]
        return self.reducer.strategy.norm_risk

    @staticmethod
    def extract_critical_values(
        da: xr.DataArray, operator: ComparisonOperator
    ) -> Tuple[float, str]:
        """
        Get the most critical values over time

        Args:
            da (xr.DataArray): The dataArray to look at
            operator (str): The comparison operator

        Raises:
            ValueError: If the comparison operator is not an order operator

        Returns:
            (float, str): The critical values as well as the impacted area.
        """
        values: np.ndarray

        if operator.is_increasing_order:
            values = da.max(["valid_time", "id"]).values
            area_id = da.isel(id=da.max("valid_time").argmax("id"))["id"].item()
        elif operator.is_decreasing_order:
            values = da.min(["valid_time", "id"]).values
            area_id = da.isel(id=da.min("valid_time").argmin("id"))["id"].item()
        else:
            raise ValueError(
                "Operator is not understood when trying to find the critical "
                "representative values."
            )

        # Set value
        value: float = float(values) if values.ndim == 0 else float(values[0])

        return value, area_id

    @precached_property
    def risk_level(self) -> int:
        return self.composite.final_risk_max_level(self.geo_id)

    @precached_property
    def comparison(self) -> dict:
        """
        Get the comparison dictionary for the specified risk level as follows:

            {
                "T__HAUTEUR2": {
                    "plain": Threshold(...),
                    "mountain": Threshold(...),
                    "category": ...,
                    "mountain_altitude": ...,
                    "aggregation": ...,
                },
                "NEIPOT1__SOL": {...},
            }

        Args:
            level (int, optional): The risk level. Defaults to 1.

        Returns:
            dict: Comparison dictionary
        """
        # Retrieve the comparison dictionary for the desired level
        if self.risk_level == 0:
            return {}

        d1_comp = self.composite.risks_of_level(level=self.risk_level)[
            0
        ].get_comparison()

        # Iterate over each variable and check for identical variables in other levels
        for variable in d1_comp:
            other_level = self.composite.risks_of_level(level=self.risk_level + 1)
            if not other_level:
                continue

            d2_comp = other_level[0].get_comparison()
            if variable in d1_comp and variable in d2_comp:
                if "plain" in d1_comp[variable] and "plain" in d2_comp[variable]:
                    d1_comp[variable]["plain"].update_next_critical(
                        d2_comp[variable]["plain"]
                    )
                if "mountain" in d1_comp[variable] and "mountain" in d2_comp[variable]:
                    d1_comp[variable]["mountain"].update_next_critical(
                        d2_comp[variable]["mountain"]
                    )
        return d1_comp

    def _compute_critical_values(
        self, evt_ds: xr.Dataset, dict_comp: dict, kind: str
    ) -> dict:
        key = f"rep_value_{kind}"
        if key not in evt_ds or kind not in dict_comp or np.isnan(evt_ds[key]).all():
            return {}

        value, area = self.extract_critical_values(
            evt_ds[key], dict_comp[kind].comparison_op
        )
        return {
            kind: {
                "id": area,
                "operator": ComparisonOperator(dict_comp[kind].comparison_op),
                "threshold": dict_comp[kind].threshold,
                "units": dict_comp[kind].units,
                "next_critical": dict_comp[kind].next_critical,
                "value": value,
                "occurrence": evt_ds[f"occurrence_{kind}"].item(),
            }
        }

    @property
    def critical_values(self) -> dict:
        """
        Get the critical values.

        Returns:
            dict: A dictionary containing the critical values, keyed by variable name.
        """
        if not self.comparison:
            return {}

        # Get the risk dataset
        risk_ds = (
            self.reducer.localisation.spatial_localisation.localised_risk_ds
            if self.is_multizone
            else self.composite.risk_ds.sel(id=self.geo_id).expand_dims({"id": 1})
        ).sel(risk_level=self.risk_level)

        # Create a dictionary to store the critical values.
        critical_values = {}

        # Iterate over the events in the spatial table_localisation.
        for evt in risk_ds.evt:
            # Get the variable name for the event.
            evt_ds = risk_ds.sel(evt=evt)
            variable = evt_ds.weatherVarName.item()
            if pd.isna(variable):
                continue

            # Get the dictionary of comparison for the concerned variable.
            dict_comp = self.comparison[variable]

            # Create a dictionary to store the critical values for the event.
            event_critical_values = self._compute_critical_values(
                evt_ds, dict_comp, "plain"
            ) | self._compute_critical_values(evt_ds, dict_comp, "mountain")

            mountain_altitude = dict_comp.get("mountain_altitude")
            if mountain_altitude is not None:
                event_critical_values["mountain_altitude"] = mountain_altitude

            # If there are any critical values for the event, add them to the
            # dictionary of critical values.
            if bool(event_critical_values) and variable not in critical_values:
                critical_values[variable] = event_critical_values

        # Return the dictionary of critical values.
        return critical_values

    def _post_process_monozone_generic(self, rep_value_table: dict):
        final_rep_value = {
            key: RepValueBuilder.compute_all(
                {k: v for k, v in value.items() if k != "level"}, builder=self
            )
            for key, value in rep_value_table.items()
            if len(value) > 1
        }
        self.text = clean_text(self.text.format(**final_rep_value))

    def _post_process_monozone_precip(self, rep_value_table: dict):
        max_val = {}
        for data in rep_value_table.values():
            if data["level"] == self.reducer.final_risk_max:
                for key, param in data.items():
                    if key != "level" and (
                        key not in max_val
                        or RepValueReducer.compare(param, max_val[key])
                    ):
                        max_val[key] = param
        if max_val:
            self.text += " " + RepValueBuilder.compute_all(max_val, builder=self)

    def post_process_monozone(self):
        """Processes the representative values for the monozone comment."""
        rep_value_table = {}
        for bloc, data in self.reduction.items():
            if isinstance(data, dict):
                data_dict = {
                    k: v
                    for k, v in data.items()
                    if k not in ["start", "stop", "centroid", "period"]
                }

                if not data_dict.get("level"):
                    data_dict["level"] = -1
                if bool(data_dict) and data_dict["level"] != 0:
                    rep_value_table[f"{bloc}_val"] = data_dict

        if self.reduction["type"] == "PRECIP":
            self._post_process_monozone_precip(rep_value_table)
        else:
            self._post_process_monozone_generic(rep_value_table)

    def post_process_multizone(self):
        """Processes the representative values for the multizone comment."""
        self.text += " " + RepValueBuilder.compute_all(
            self.critical_values, builder=self
        )

    def post_process_snow(self):
        """Processes the representative values for the snow comment."""
        self.text += " " + RepValueBuilder.compute_all(
            self.critical_values, builder=self
        )

        # Put the LPN (if present) at the 2nd line (#41905)
        if "LPN__SOL" in self.critical_values:
            text = self.text.split("\n")
            self.text = "\n".join([text[0], text[-1]] + text[1:-1])

    def post_process(self):
        """Make a post-process operation on the text."""
        if self.composite.hazard_name == "Neige":
            self.post_process_snow()
        elif self.is_multizone:
            self.post_process_multizone()
        else:
            self.post_process_monozone()
        super().post_process()
