import traceback
from functools import cached_property
from typing import Optional

import numpy as np

import mfire.utils.mfxarray as xr
from mfire.composite.component import SynthesisComposite
from mfire.settings import get_logger
from mfire.text.synthesis.wind_reducers.base_param_summary_builder import (
    BaseParamSummaryBuilder,
)
from mfire.text.synthesis.wind_reducers.exceptions import WindSynthesisError
from mfire.text.synthesis.wind_reducers.mixins import BaseSummaryBuilderMixin
from mfire.text.synthesis.wind_reducers.utils import add_previous_time_in_dataset
from mfire.utils.date import Datetime
from mfire.utils.period import Period

from .gust_enum import GustCase

# Logging
LOGGER = get_logger(name=__name__, bind="gust")


class GustSummaryBuilder(BaseSummaryBuilderMixin, BaseParamSummaryBuilder):
    FORCE_MIN: float = 50.0
    GUST: str = "gust"
    INTERVAL_PERCENT: float = 20.0
    INTERVAL_SIZE: int = 20
    PERCENTILE_NUM: int = 90
    CACHED_EXCEPTIONS: tuple[Exception] = (WindSynthesisError,)

    def __init__(self, compo: SynthesisComposite, dataset: xr.Dataset):
        # Call SummaryBuilderMixin.__init__ and create the summary attribute
        super().__init__()

        self.units: str = self._get_composite_units(compo, self.GUST)

        # Get gust data: nan values will be kept
        self.dataset: xr.Dataset = dataset[["gust"]]

        self._process_param_data(self.dataset, "gust", units=self.units)

        # Add the `previous_time` variable in dataset
        self.dataset = add_previous_time_in_dataset(self.dataset)

        self._preprocess()

    @property
    def gust_da(self) -> xr.DataArray:
        """Get the gust DataArray."""
        return self.dataset.gust

    @cached_property
    def gust_max_da(self) -> xr.DataArray:
        """Get the gust max DataArray along the valid_time dim."""
        return self.dataset.gust.max(dim="valid_time")

    @property
    def gust_max(self) -> int:
        return self.dataset.attrs["gust_max"]

    @cached_property
    def mask(self) -> np.ndarray:
        """Get the mask.

        It comes only from the 1st term.
        """
        return ~np.isnan(
            self.dataset.gust.sel(valid_time=self.dataset.valid_time[0]).values
        )

    def _compute_gust_max(self) -> int:
        """Compute the representative value of gust max."""
        # If gust max raw is nan, return 0
        if np.isnan(self.dataset.attrs["gust_max_raw"]):
            return 0

        # Keep only points where gust max > 50
        data_array = self.gust_max_da.where(self.gust_max_da > self.FORCE_MIN)

        if np.isnan(data_array).all():
            return 0

        # Compute the 90th percentile of max gust > 50
        q90: float = round(np.nanpercentile(data_array, 90), 2)

        # And then round it to the closest tenth (ex: 94.9 => 90, 95.0 => 100)
        q90_floor: int = int(np.floor(q90))
        rounded_to_10: int = (q90_floor // 10) * 10  # rounded to 10 inf
        if q90_floor - rounded_to_10 >= 5:
            rounded_to_10 += 10  # rounded to 10 sup

        return rounded_to_10

    def _preprocess(self) -> None:
        # Compute the number of masked points
        self.dataset.attrs["points_nbr"] = int(np.count_nonzero(self.mask))

        # Get raw gust max
        gust_max_raw: float = float(np.round(self.gust_max_da.max(), decimals=2))
        self.dataset.attrs["gust_max_raw"] = gust_max_raw
        self.dataset.attrs["gust_max"] = self._compute_gust_max()

    def count_points(self, term_data: xr.DataArray, condition) -> tuple[int, float]:
        """Count the points of a term regarding a particular condition."""
        mask = term_data.where(condition)
        count: int = int(mask.count())

        if count == 0:
            return 0, 0

        return count, round(count * 100.0 / int(self.dataset.attrs["points_nbr"]), 1)

    def compute_percent_coverage_of_interval(
        self, bound_inf: float, bound_sup: float
    ) -> float:
        _, percent = self.count_points(
            self.gust_max_da,
            (self.gust_max_da >= bound_inf) & (self.gust_max_da <= bound_sup),
        )
        return percent

    def _set_case1(
        self, bound_inf: int, bound_sup: int, reference_datetime: Datetime
    ) -> None:
        """Set case 1 and fill summary in this way."""
        self._summary.update(
            {
                "bound_inf": bound_inf,
                "bound_sup": bound_sup,
                "period": self._find_gust_period(bound_inf).describe(
                    reference_datetime
                ),
            }
        )
        self._set_summary_case(GustCase.CASE_1.value)

    def _set_case2(
        self, bound_inf: int, bound_sup: int, reference_datetime: Datetime
    ) -> None:
        """Set case 2 and fill summary in this way."""
        self._summary.update(
            {
                "bound_inf": bound_inf,
                "bound_sup": bound_sup,
                "gust_max": self.gust_max,
                "period": self._find_gust_period(bound_inf).describe(
                    reference_datetime
                ),
            }
        )

        self._set_summary_case(GustCase.CASE_2.value)

    def _set_case3(self, reference_datetime: Datetime) -> None:
        """Set case 3 and fill summary in this way."""
        self._summary.update(
            {
                "gust_max": self.gust_max,
                "period": self._find_gust_period(50).describe(reference_datetime),
            }
        )

        self._set_summary_case(GustCase.CASE_3.value)

    def _initialize_bound_inf(self) -> Optional[int]:
        """Initialize the bound inf of the interval."""
        # If gust_max is nan or is <= 50 km/h, it means that there is no gust to
        # describe, so no bound_inf
        if self.gust_max < self.FORCE_MIN:
            return None

        if self.gust_max <= self.FORCE_MIN + self.INTERVAL_SIZE:
            return int(self.FORCE_MIN)

        return self.gust_max - self.INTERVAL_SIZE

    def _generate_summary(self, reference_datetime: Datetime) -> None:
        """Compute the gust summary."""
        # Find the best interval containing gust_max
        bound_inf: Optional[int] = self._initialize_bound_inf()

        # If interval not found, meaning gust_max is nan or <= 50 km/h, this is
        # the case 0
        if bound_inf is None:
            self._set_summary_case(GustCase.CASE_0.value)
            return

        # Add the case and the unit in the summary
        self._summary["units"] = self.units

        if bound_inf < self.FORCE_MIN:
            self._set_case3(reference_datetime)
            return

        bound_sup: int = bound_inf + self.INTERVAL_SIZE
        percent: float = self.compute_percent_coverage_of_interval(bound_inf, bound_sup)

        # Case 1
        if percent >= self.INTERVAL_PERCENT:
            self._set_case1(bound_inf, bound_sup, reference_datetime)
            return

        bound_inf -= 10
        bound_sup -= 10

        while bound_inf >= self.FORCE_MIN:
            percent: float = self.compute_percent_coverage_of_interval(
                bound_inf, bound_sup
            )

            # Case 2
            if percent >= self.INTERVAL_PERCENT:
                self._set_case2(bound_inf, bound_sup, reference_datetime)

                break

            bound_inf -= 10
            bound_sup -= 10

        # If no interval found => case 3
        if self.case is None:
            self._set_case3(reference_datetime)

    def _find_gust_period(self, bound_inf: float) -> Period:
        gust_q90: list[float] = []
        valid_times: list[np.datetime64] = []

        for valid_time in self.dataset.valid_time.values:
            term_data: xr.DataArray = self.gust_da.sel(valid_time=valid_time)
            term_data = term_data.where(term_data > self.FORCE_MIN)
            gust_q90_cur: float = (
                round(np.nanpercentile(term_data.values, self.PERCENTILE_NUM), 2)
                if term_data.count() > 0
                else float("nan")
            )
            gust_q90.append(gust_q90_cur)

            if gust_q90_cur >= bound_inf:
                valid_times.append(valid_time)

        self.dataset["gust_q90"] = xr.DataArray(
            data=gust_q90, coords=[self.dataset.valid_time], dims=["valid_time"]
        )

        # this case should never happen
        if not valid_times:
            raise ValueError(f"No term with Q90 >= bound_inf '{bound_inf}' found !")

        return Period(
            Datetime(self.dataset.previous_time.sel(valid_time=valid_times[0]).values),
            Datetime(valid_times[-1]),
        )

    def compute(self, reference_datetime: Datetime) -> dict:
        """Compute the gust summary."""
        try:
            self._generate_summary(reference_datetime)
        except self.CACHED_EXCEPTIONS as exp:
            msg: str = (
                f"{exp.__class__.__name__}: problem detected in GustSummaryBuilder -> "
                f"{traceback.format_exc()}"
            )

            self._add_error_case_in_summary(self._summary, msg)

        return {self.GUST: self._summary}
