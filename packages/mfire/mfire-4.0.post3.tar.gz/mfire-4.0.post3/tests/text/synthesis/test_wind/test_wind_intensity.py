"""Unit tests of wind intensity classes."""

import copy

import numpy as np
import pytest

import mfire.utils.mfxarray as xr
from mfire.text.synthesis.wind_reducers.wind.wind_intensity import (
    Pci,
    PciFinder,
    WindIntensity,
)
from mfire.utils.date import Datetime
from tests.text.utils import generate_valid_times, generate_valid_times_v2

from .factories import CompositeFactory1x100
from .mixins import Data1x1


class TestWindIntensity:
    @pytest.mark.parametrize(
        "force", [20.0, 29.9, 30.0, 44.9, 45.0, 69.9, 70.0, 80.0, 90.0]
    )
    def test_creation(self, force, assert_equals_result):
        wi = WindIntensity(force)

        result: dict = {
            "force": force,
            "wi_interval": str(wi.interval),
            "wi_as_text": wi.as_text,
        }

        # Check text
        assert_equals_result(result)

    @pytest.mark.parametrize("force", [0.0, 14.0, 19.9])
    def test_creation_exception(self, force):
        with pytest.raises(ValueError):
            WindIntensity(force)

    def test_speed_min(self):
        assert WindIntensity(30).speed_min == 20.0
        assert WindIntensity(70.0).speed_min == 20.0

    @pytest.mark.parametrize(
        "valid_times, data_wf, wind_intensity_exp",
        [
            (
                generate_valid_times(periods=1),
                np.arange(1.0, 101.0, 1, dtype=np.float64),
                WindIntensity(70.0),
            )
        ],
    )
    def test_creation_from_term(self, valid_times, data_wf, wind_intensity_exp):
        composite = CompositeFactory1x100().get(
            valid_times=valid_times, data_wind=data_wf
        )
        dataset = composite.compute()
        data_array: xr.DataArray = dataset["wind"].sel(valid_time=valid_times[0])
        wind_intensity: WindIntensity = WindIntensity.from_term_data_array(data_array)
        assert wind_intensity == wind_intensity_exp

    def test_comparison(self):
        assert WindIntensity(20.0) == WindIntensity(29.9)
        assert WindIntensity(31.0) == WindIntensity(44.9)
        assert WindIntensity(45.0) == WindIntensity(69.9)
        assert WindIntensity(70.2) == WindIntensity(90.8)

        assert WindIntensity(25.0) <= WindIntensity(30.0)
        assert WindIntensity(25.0) <= WindIntensity(35.0)
        assert WindIntensity(50.0) >= WindIntensity(40.0)
        assert WindIntensity(50.0) >= WindIntensity(54.0)

        assert WindIntensity(25.0) < WindIntensity(35.0)
        assert WindIntensity(50.0) > WindIntensity(44.0)
        assert WindIntensity(80.0) > WindIntensity(67.6)


class TestPci:
    WIND_INTENSITY = WindIntensity(32.0)
    WIND_PCI = Pci(
        Datetime(2023, 1, 1, 10, 0, 0), Datetime(2023, 1, 1, 11, 0, 0), WIND_INTENSITY
    )

    @pytest.mark.parametrize(
        "begin_time, end_time",
        [
            (Datetime(2023, 1, 1, 11, 0, 0), Datetime(2023, 1, 1, 10, 0, 0)),
            (Datetime(2023, 1, 1, 11, 0, 0), Datetime(2023, 1, 1, 11, 59, 59)),
            (Datetime(2023, 1, 1, 11, 0, 0), Datetime(2023, 1, 1, 11, 0, 0)),
        ],
    )
    def test_creation_exception(self, begin_time, end_time):
        with pytest.raises(ValueError):
            Pci(begin_time, end_time, self.WIND_INTENSITY)

    @pytest.mark.parametrize(
        "period, res_exp, period_exp",
        [
            (
                Pci(
                    Datetime(2023, 1, 1, 11, 0, 0),
                    Datetime(2023, 1, 1, 12, 0, 0),
                    WindIntensity(30.0),
                ),
                True,
                Pci(
                    Datetime(2023, 1, 1, 10, 0, 0),
                    Datetime(2023, 1, 1, 12, 0, 0),
                    WIND_INTENSITY,
                ),
            ),
            (
                Pci(
                    Datetime(2023, 1, 1, 11, 0, 0),
                    Datetime(2023, 1, 1, 12, 0, 0),
                    WindIntensity(39.9),
                ),
                True,
                Pci(
                    Datetime(2023, 1, 1, 10, 0, 0),
                    Datetime(2023, 1, 1, 12, 0, 0),
                    WIND_INTENSITY,
                ),
            ),
            (
                Pci(
                    Datetime(2023, 1, 1, 9, 0, 0),
                    Datetime(2023, 1, 1, 10, 0, 0),
                    WindIntensity(34.1),
                ),
                False,
                WIND_PCI,
            ),
            (
                Pci(
                    Datetime(2023, 1, 1, 8, 0, 0),
                    Datetime(2023, 1, 1, 9, 0, 0),
                    WindIntensity(45.0),
                ),
                False,
                WIND_PCI,
            ),
        ],
    )
    def test_update(self, period: Pci, res_exp: bool, period_exp: Pci):
        pci = copy.deepcopy(self.WIND_PCI)
        res = pci.update(period)
        assert res == res_exp
        assert pci == period_exp

    @pytest.mark.parametrize(
        "wi_p1, wi_p2, check_exp",
        [
            (
                Pci(
                    Datetime(2023, 1, 1, 0, 0, 0),
                    Datetime(2023, 1, 1, 4, 0, 0),
                    WindIntensity(20.0),
                ),
                Pci(
                    Datetime(2023, 1, 1, 6, 0, 0),
                    Datetime(2023, 1, 1, 10, 0, 0),
                    WindIntensity(20.0),
                ),
                True,
            ),
            (
                Pci(
                    Datetime(2023, 1, 1, 0, 0, 0),
                    Datetime(2023, 1, 1, 4, 0, 0),
                    WindIntensity(45.0),
                ),
                Pci(
                    Datetime(2023, 1, 1, 6, 0, 0),
                    Datetime(2023, 1, 1, 10, 0, 0),
                    WindIntensity(69.9),
                ),
                True,
            ),
            (
                Pci(
                    Datetime(2023, 1, 1, 0, 0, 0),
                    Datetime(2023, 1, 1, 4, 0, 0),
                    WindIntensity(29.9),
                ),
                Pci(
                    Datetime(2023, 1, 1, 6, 0, 0),
                    Datetime(2023, 1, 1, 10, 0, 0),
                    WindIntensity(46.0),
                ),
                False,
            ),
        ],
    )
    def test_has_same_intensity(self, wi_p1, wi_p2, check_exp):
        assert wi_p1.has_same_intensity_than(wi_p2) == check_exp


class TestPciFinder(Data1x1):
    @pytest.mark.parametrize(
        "data, valid_times, periods_exp",
        [
            (
                [25.0],
                generate_valid_times(periods=1),
                [
                    Pci(
                        Datetime(2023, 1, 1, 23, 0, 0),
                        Datetime(2023, 1, 2, 0, 0, 0),
                        WindIntensity(20.0),
                    )
                ],
            ),
            (
                [20.0, 27.0],
                generate_valid_times(periods=2),
                [
                    Pci(
                        Datetime(2023, 1, 1, 23, 0, 0),
                        Datetime(2023, 1, 2, 1, 0, 0),
                        WindIntensity(20.0),
                    )
                ],
            ),
            (
                [20.0, 30.0, 45.0],
                generate_valid_times(periods=3),
                [
                    Pci(
                        Datetime(2023, 1, 1, 23, 0, 0),
                        Datetime(2023, 1, 2, 0, 0, 0),
                        WindIntensity(20.0),
                    ),
                    Pci(
                        Datetime(2023, 1, 2, 0, 0, 0),
                        Datetime(2023, 1, 2, 1, 0, 0),
                        WindIntensity(30.0),
                    ),
                    Pci(
                        Datetime(2023, 1, 2, 1, 0, 0),
                        Datetime(2023, 1, 2, 2, 0, 0),
                        WindIntensity(45.0),
                    ),
                ],
            ),
            (
                [20.0, 22.6, 31.5, 32.0, 33],
                generate_valid_times(periods=5),
                [
                    Pci(
                        Datetime(2023, 1, 1, 23, 0, 0),
                        Datetime(2023, 1, 2, 1, 0, 0),
                        WindIntensity(20.0),
                    ),
                    Pci(
                        Datetime(2023, 1, 2, 1, 0, 0),
                        Datetime(2023, 1, 2, 4, 0, 0),
                        WindIntensity(30.0),
                    ),
                ],
            ),
            (
                [20.0, 22.6, 33.0],
                generate_valid_times_v2("2023-01-02", (2, "H"), (1, "3H")),
                [
                    Pci(
                        Datetime(2023, 1, 1, 23, 0, 0),
                        Datetime(2023, 1, 2, 1, 0, 0),
                        WindIntensity(20.0),
                    ),
                    Pci(
                        Datetime(2023, 1, 2, 1, 0, 0),
                        Datetime(2023, 1, 2, 4, 0, 0),
                        WindIntensity(30.0),
                    ),
                ],
            ),
            (
                [75.0] * 5,
                generate_valid_times_v2("2023-01-02", (2, "H"), (3, "3H")),
                [
                    Pci(
                        Datetime(2023, 1, 1, 23, 0, 0),
                        Datetime(2023, 1, 2, 10, 0, 0),
                        WindIntensity(70.0),
                    )
                ],
            ),
        ],
    )
    def test_period_finder(self, data, valid_times: list | np.ndarray, periods_exp):
        dataset: xr.Dataset = self._create_dataset(
            valid_times, data_wind=np.array(data)
        )

        wind_q95: list[float] = []
        for valid_time in dataset.valid_time:
            dataset_cur: xr.Dataset = dataset.sel(valid_time=valid_time)
            wind_q95.append(
                round(WindIntensity.data_array_to_value(dataset_cur.wind), 2)
            )

        # Add the `wind_q95` variable
        dataset["wind_q95"] = xr.DataArray(
            data=wind_q95, coords=[dataset.valid_time], dims=["valid_time"]
        )

        period_finder = PciFinder.from_dataset(dataset)
        periods = period_finder.run()
        assert periods == periods_exp
