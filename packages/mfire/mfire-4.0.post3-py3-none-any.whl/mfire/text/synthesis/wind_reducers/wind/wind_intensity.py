from __future__ import annotations

from functools import cached_property
from typing import Optional

import numpy as np

import mfire.utils.mfxarray as xr
from mfire.settings import get_logger
from mfire.text.synthesis.wind_reducers.wind.helpers import BaseWindPeriod
from mfire.utils.date import Datetime
from mfire.utils.string import _

# Logging
LOGGER = get_logger(name=__name__, bind="wind_intensity")


class WindIntensity:
    """WindIntensity class."""

    PERCENTILE_NUM: int = 95

    def __init__(self, wind_force: float) -> None:
        self._interval: tuple[int, int] = (0, 0)
        self._interval_from_wind_force(wind_force)

    @property
    def mapping(self) -> dict[tuple, str]:
        # We shall declare this attribute as a class attribute, but we don't in order to
        # have the translation in the unit tests of tests/text/test_manager.py
        return {
            (20, 30): _("assez fort"),
            (30, 45): _("fort"),
            (45, 70): _("très fort"),
            (70, None): _("tempétueux"),
        }

    @property
    def interval(self) -> tuple[int, int]:
        return self._interval

    @property
    def as_text(self) -> str:
        return self.mapping[self._interval]

    @cached_property
    def speed_min(self) -> float:
        wi_interval: list = list(self.mapping.keys())
        wi_interval.sort()
        return float(wi_interval[0][0])

    @classmethod
    def data_array_to_value(cls, data_array: xr.DataArray) -> float:
        """Find the value which represents the input DataArray."""
        return round(np.nanpercentile(data_array.values, cls.PERCENTILE_NUM), 2)

    @classmethod
    def from_term_data_array(cls, data_array: xr.DataArray) -> WindIntensity:
        """Instantiate a WindIntensity from a DataArray."""
        return cls(cls.data_array_to_value(data_array))

    def _interval_from_wind_force(self, wind_force: float) -> None:
        for bound_inf, bound_sup in self.mapping:
            if (bound_inf <= wind_force) and (
                bound_sup is None or wind_force < bound_sup
            ):
                self._interval = bound_inf, bound_sup
                return

        raise ValueError(f"Wind intensity not found for wind force {wind_force} !")

    def __eq__(self, other: WindIntensity) -> bool:
        return isinstance(other, WindIntensity) and self.interval == other.interval

    def __le__(self, other: WindIntensity) -> bool:
        return self.interval[0] <= other.interval[0]

    def __lt__(self, other: WindIntensity) -> bool:
        return self.interval[0] < other.interval[0]

    def __ge__(self, other: WindIntensity) -> bool:
        return self.interval[0] >= other.interval[0]

    def __gt__(self, other: WindIntensity) -> bool:
        return self.interval[0] > other.interval[0]

    def __hash__(self) -> int:
        return hash(self.interval)

    def __repr__(self):
        return f"WindIntensity(interval={self._interval})"


class Pci(BaseWindPeriod):
    """Period with common Intensity (Pci) class."""

    def __init__(self, begin_time: Datetime, end_time: Datetime, wi: WindIntensity):
        super().__init__(begin_time, end_time)
        self.wi: WindIntensity = wi

    def __eq__(self, other: Pci) -> bool:
        return super().__eq__(other) and self.wi == other.wi

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.wi))

    def has_same_intensity_than(self, other: Pci) -> bool:
        return self.wi == other.wi

    def update(self, other: Pci) -> bool:
        """Try to update the period with another period."""
        if self.has_same_intensity_than(other) and self.end_time <= other.begin_time:
            self.end_time = other.end_time
            return True

        return False

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(begin_time={self.begin_time}, "
            f"end_time={self.end_time}), wi={self.wi}"
        )

    def summarize(self, reference_datetime: Datetime) -> dict:
        """Summarize the Pci instance."""
        summary: dict = super().summarize(reference_datetime)
        summary[self.WI_K] = self.wi.as_text

        return summary


class PciFinder:
    def __init__(self, initial_periods: list[Pci]):
        """Initialize a PciFinder instance."""
        self._initial_periods: list[Pci] = initial_periods

    @classmethod
    def from_dataset(cls, dataset: xr.Dataset) -> PciFinder:
        """Initialize a period finder from its term-periods."""

        term_periods: list[Pci] = []

        for valid_time in dataset.valid_time:
            term_dataset: xr.Dataset = dataset.sel(valid_time=valid_time)

            term_periods.append(
                Pci(
                    Datetime(term_dataset.previous_time.values),
                    Datetime(term_dataset.valid_time.values),
                    WindIntensity(term_dataset.wind_q95.values),
                )
            )

        return cls(term_periods)

    def run(self) -> list[Pci]:
        """Find all periods as a list."""
        periods: list[Pci] = []
        cnt: int = len(self._initial_periods)
        period: Optional[Pci]
        period = self._initial_periods[0] if cnt else None

        for i in range(1, cnt):
            period_cur: Pci = self._initial_periods[i]
            res: bool = period.update(period_cur)

            # If res is True, period has been updated with period_cur times
            if res is False:
                periods.append(period)
                period = period_cur

        if period is not None:
            periods.append(period)

        return periods
