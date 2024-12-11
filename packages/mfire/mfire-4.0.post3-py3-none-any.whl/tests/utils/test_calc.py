import numpy as np
import pytest

import mfire.utils.mfxarray as xr
from mfire.utils.calc import (
    all_close,
    all_combinations_and_remaining,
    bin_to_int,
    combinations_and_remaining,
    compute_accumulation,
    round_to_closest_multiple,
    round_to_next_multiple,
    round_to_previous_multiple,
)
from mfire.utils.date import Datetime
from tests.functions_test import assert_identically_close


class TestCalcFunctions:
    def test_compute_accumulationn(self):
        lon, lat = [30], [40]
        valid_times = [Datetime(2023, 3, 1, i).as_np_dt64 for i in range(12)]
        field = xr.DataArray(
            name="name",
            data=[[[1, 4, 6, 7, 5, 3, 0, 0, 1, 0, 0, 0]]],
            dims=["latitude", "longitude", "valid_time"],
            coords={"latitude": lat, "longitude": lon, "valid_time": valid_times},
        )

        result = compute_accumulation(field)
        expected = xr.DataArray(
            name="name",
            data=[[[26.0, 25.0, 21.0, 16.0, 9.0, 4.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0]]],
            dims=["latitude", "longitude", "valid_time"],
            coords={"latitude": lat, "longitude": lon, "valid_time": valid_times},
            attrs={"accum_hour": 6},
        )
        assert_identically_close(result, expected)

    @pytest.mark.parametrize(
        "x,m,expected",
        [
            (1.3, 0.5, 1.5),
            (1.6, 0.5, 1.5),
            (22, 10, 20),
            (27, 10, 30),
            (np.array([1.3, 1.6]), 0.5, np.array([1.5, 1.5])),
            (np.array([22, 27]), 10, np.array([20, 30])),
        ],
    )
    def test_round_to_closest_multiple(self, x, m, expected):
        assert all_close(round_to_closest_multiple(x, m), expected)

    @pytest.mark.parametrize(
        "x,m,expected",
        [
            (1.3, 0.5, 1.5),
            (1.6, 0.5, 2),
            (22, 10, 30),
            (27, 10, 30),
            (np.array([1.3, 1.6]), 0.5, np.array([1.5, 2])),
            (np.array([22, 27]), 10, np.array([30, 30])),
        ],
    )
    def test_round_to_next_multiple(self, x, m, expected):
        assert all_close(round_to_next_multiple(x, m), expected)

    @pytest.mark.parametrize(
        "x,m,expected",
        [
            (1.3, 0.5, 1),
            (1.6, 0.5, 1.5),
            (22, 10, 20),
            (27, 10, 20),
            (np.array([1.3, 1.6]), 0.5, np.array([1, 1.5])),
            (np.array([22, 27]), 10, np.array([20, 20])),
        ],
    )
    def test_round_to_previous_multiple(self, x, m, expected):
        assert all_close(round_to_previous_multiple(x, m), expected)

    def test_combinations_and_remaining(self):
        obj = [1, 2, 3]
        result = list(combinations_and_remaining(obj, r=2))
        expected = [([1, 2], [3]), ([1, 3], [2]), ([2, 3], [1])]
        assert result == expected

    def test_all_combinations_and_remaining(self):
        # With symmetric
        obj = [1, 2, 3, 4]
        result = list(all_combinations_and_remaining(obj, is_symmetric=True))
        expected = [
            ([1], [2, 3, 4]),
            ([2], [1, 3, 4]),
            ([3], [1, 2, 4]),
            ([4], [1, 2, 3]),
            ([1, 2], [3, 4]),
            ([1, 3], [2, 4]),
            ([1, 4], [2, 3]),
            ([2, 3], [1, 4]),
            ([2, 4], [1, 3]),
            ([3, 4], [1, 2]),
        ]
        assert result == expected

        # Without symmetric
        obj = [1, 2, 3]
        result = list(all_combinations_and_remaining(obj, is_symmetric=False))
        expected = [
            ([1], [2, 3]),
            ([2], [1, 3]),
            ([3], [1, 2]),
            ([1, 2], [3]),
            ([1, 3], [2]),
            ([2, 3], [1]),
            ([1, 2, 3], []),
        ]
        assert result == expected

    def test_bin_to_int(self):
        assert bin_to_int([1, 0, 1]) == 5
        assert bin_to_int("110") == 6

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (None, None, True),
            (None, 2, False),
            (-2, None, False),
            (1.0, 1.0000000001, True),
            (1.0, 2.0, False),
            ("s1", "s2", False),
            ("s1", "s1", True),
            ([1.0, 2.0], [1.0000000001, 1.9999999999], True),
            ([1.0, 2.0], [1.0, 2.1], False),
            (["s1", "s1"], ["s1", "s2"], False),
            (["s1", "s1"], ["s1", "s1"], True),
            ("s1", 1.0, False),
            (1.0, "s1", False),
        ],
    )
    def test_all_close(self, a, b, expected):
        assert all_close(a, b) == expected
