from __future__ import annotations

from itertools import combinations
from typing import Dict, Optional

import numpy as np
from dateutil.parser import ParserError

import mfire.utils.mfxarray as xr
from mfire.composite.base import BaseModel
from mfire.localisation.altitude import rename_alt_min_max
from mfire.localisation.area_algebra import compute_iou
from mfire.localisation.spatial_localisation import SpatialLocalisation
from mfire.settings import get_logger
from mfire.utils.calc import bin_to_int
from mfire.utils.period import Period
from mfire.utils.string import concatenate_string

# Logging
LOGGER = get_logger(name="table_localisation.mod", bind="table_localisation")


class TableLocalisation(BaseModel):
    """
    A class to generate summary tables.
    """

    data: xr.DataArray
    spatial_localisation: SpatialLocalisation

    alt_min: int
    alt_max: int

    table: Optional[Dict[str, str]] = {}

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = self.data.copy()

    @property
    def name(self) -> str:
        """Compute the name of the reduced form"""
        base = str(self.data.period.size)
        nums = sorted(set(self.data["raw"].data))
        return f"P{base}_{'_'.join(nums)}"

    def _merge_similar_areas(self, da: xr.DataArray) -> xr.DataArray:
        """
        Merge similar areas.

        Args:
            da (xr.DataArray): The data array to merge.

        Returns:
            xr.DataArray: The merged data array.
        """

        # Concatenation of the name of the merged areas
        areas_id = list({v for ids in da.id.values for v in ids.split("_+_")})
        areas = self.spatial_localisation.completed_areas.sel(id=areas_id)
        area_name = concatenate_string(sorted(areas.areaName.values))

        # Calculation of the type of the merged areas
        area_type = np.unique(areas.areaType)
        area_type = area_type[0] if len(area_type) == 1 else "unknown"

        # Rename the area name to include the minimum and maximum altitudes.
        if area_type == "Altitude":
            area_name = rename_alt_min_max(
                area_name=area_name, alt_min=self.alt_min, alt_max=self.alt_max
            )

        # Check the IoU between the sum of the merged areas and the domain.
        if compute_iou(areas.max("id"), self.spatial_localisation.domain) > 0.98:
            # If the IoU is greater than 0.98, then use the name and type of the
            # domain.
            area_name = self.spatial_localisation.domain.areaName.item()
            area_type = "domain"

        # Create a new data array for the merged area.
        merged_area = (
            da.max("id")
            .expand_dims({"id": ["_+_".join(da.id.values)]})
            .assign_coords({"raw": (["id"], [da.raw.max().item()])})
        )
        merged_area["areaName"] = ("id", [str(area_name)])
        merged_area["areaType"] = ("id", [area_type])

        return merged_area

    def _squeeze_empty_period(self):
        """Remove empty periods from the beginning and end of the table_localisation."""
        i = 0
        squeeze_list = []

        # Remove empty periods from the beginning of the table_localisation
        while self.data.isel(period=[i]).sum().values == 0:
            squeeze_list.append(i)
            i += 1

        # Remove empty periods from the end of the table_localisation
        i = self.data.period.size - 1
        while self.data.isel(period=[i]).sum().values == 0:
            squeeze_list.append(i)
            i += -1

        # Create a set of all periods that are not empty
        select = set(list(range(self.data.period.size)))
        to_select = sorted(select.difference(set(squeeze_list)))

        # Select the periods that are not empty
        self.data = self.data.isel(period=to_select)

    def _clean_periods(self):
        """Clean periods of data."""

        # Make a clean
        to_merge = True
        while to_merge:
            to_merge = (
                self._clean_similar_period() or self._clean_period_with_same_name()
            )

        # Update the raw values of the table
        self.data["raw"] = (
            ("id",),
            [str(bin_to_int(self.data.sel({"id": id}).values)) for id in self.data.id],
        )

    def _clean_similar_period(self) -> bool:
        """
        Clean similar period: two period are similar if they are adjacent and risk
        values are the same. This function should work for any number of period.

        Returns:
            bool: True if any periods were merged. False if no periods were merged.
        """
        index_to_remove = []
        period_name = [self.data.period.isel(period=0).values]
        if self.data.period.size > 0:
            for p in range(1, self.data.period.size):
                if (
                    self.data.isel(period=[p]).data
                    == self.data.isel(period=[p - 1]).data
                ).all():
                    index_to_remove.append(p)
                    # Update the period name to reflect the merged periods.
                    period_name[-1] = (
                        str(period_name[-1])
                        + "_+_"
                        + str(self.data.isel(period=[p])["period"].values[0])
                    )
                else:
                    period_name.append(self.data.period.isel(period=p).values)

        if index_to_remove:
            # Create a set of all the period indices.
            index = set(list(range(self.data.period.size)))

            # Remove the indices of the periods to be removed.
            index = index.difference(set(index_to_remove))

            # Sort the remaining indices.
            keep_list = sorted(index)

            # Select the remaining periods from the table_localisation.
            self.data = self.data.isel(period=keep_list)

            # Update the period names in the table_localisation.
            self.data["period"] = period_name
        return bool(index_to_remove)

    def _clean_period_with_same_name(self) -> bool:
        """
        Clean periods with the same name.

        Returns:
            bool: True if any periods were merged. False if no periods were merged.
        """

        # Check if all periods are valid datetimes
        period_describer = self.spatial_localisation.risk_component.period_describer
        period_descriptions = []
        for period in self.data["period"].values:
            time_list = period.split("_to_")
            try:
                period_obj = Period(time_list[0], time_list[-1])
                LOGGER.debug(
                    f"Period = {period_obj} "
                    f"({period_describer.describe(period_obj)})"
                )
            except ParserError:
                # Log a warning and return False if any period is not a valid datetime
                LOGGER.warning(
                    f"At least one period value is not a datetime {period}. "
                    "We will not merge period by name."
                )
                return False
            period_descriptions += [period_describer.describe(period_obj)]

        # Create a new column with the period names
        self.data["period_name"] = (("period"), period_descriptions)

        # Identify the periods that need to be merged
        to_merge = len(set(period_descriptions)) != len(period_descriptions)
        if to_merge:
            # Merge the periods
            tmp_list = []
            for pname in set(period_descriptions):
                table_to_reduce = self.data.where(
                    self.data.period_name == pname, drop=True
                )
                if table_to_reduce.period.size > 1:
                    reduced_table = table_to_reduce.max("period")
                    first_period = str(
                        table_to_reduce["period"].isel(period=0).values
                    ).split("_to_")
                    last_period = str(
                        table_to_reduce["period"].isel(period=-1).values
                    ).split("_to_")
                    reduced_table["period"] = first_period[0] + "_to_" + last_period[-1]
                    reduced_table = reduced_table.expand_dims("period")
                    tmp_list += [reduced_table]
                else:
                    tmp_list += [table_to_reduce]

            # Update the table with the merged periods
            self.data = xr.merge(tmp_list)[self.data.name]

        # Drop the period_name column
        self.data = self.data.drop_vars("period_name", errors="ignore")

        return to_merge

    def compute(self) -> TableLocalisation:
        """
        Compute a reduced table from the original table.

        Returns:
            TableLocalisation: The reduced table.
        """

        # Clean periods
        self._squeeze_empty_period()
        self._clean_periods()

        # Merge similar areas
        final_list = []
        areas_ids = []  # to be sure of the order after merging operation
        for elt in sorted(set(self.data["raw"].data)):
            area = self._merge_similar_areas(
                self.data.sel({"id": self.data["raw"] == elt})
            )
            areas_ids.append(area["id"].values[0])
            final_list.append(area)

        # Update the table with the merged areas
        self.data = xr.merge(final_list).sel({"id": areas_ids})[self.data.name]

        # Compute the table
        self._compute_table()

        # Check for merged areas
        area_values = set(self.table.values())
        if len(area_values) != len(self.table):
            merged_ids = set()
            for area_name in area_values:
                keys_for_area = [
                    key for key, val in self.table.items() if val == area_name
                ]
                if len(keys_for_area) > 1:
                    merged_ids |= {
                        self.data.id.data[int(area_id) - 1]
                        for area in keys_for_area
                        for area_id in area.replace("zone", "").split("_")
                    }

            # Keep the same order for the merged areas
            merged_ids = [id for id in areas_ids if id in merged_ids]

            # Merge the reduced table with the merged areas
            self.data = xr.merge(
                [
                    self.data.sel(id=[id for id in areas_ids if id not in merged_ids]),
                    self._merge_similar_areas(self.data.sel(id=merged_ids)),
                ]
            )[self.data.name].sortby("raw")

            # Recompute the table
            self._compute_table()

        return self

    def _compute_table(self):
        """Computes internally the table."""
        self._clean_periods()
        self.table.clear()

        elements = range(len(self.data.id))
        for i in elements:
            for combination in combinations(elements, i + 1):
                keys, vals = [], []
                for j in combination:
                    keys += [str(j + 1)]
                    vals += [str(self.data.id.data[j])]

                self.table["zone" + "_".join(keys)] = self._merge_similar_areas(
                    self.data.sel(id=vals)
                ).areaName.data[0]
