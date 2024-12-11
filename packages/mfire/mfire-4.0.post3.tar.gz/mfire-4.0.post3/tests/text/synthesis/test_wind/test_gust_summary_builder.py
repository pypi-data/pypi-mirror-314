from typing import Callable

import numpy as np
import pytest

from mfire.text.synthesis.wind_reducers.gust.gust_summary_builder import (
    GustSummaryBuilder,
)
from mfire.utils.date import Datetime
from tests.text.utils import generate_valid_times

from .factories import (
    CompositeFactory1x1,
    CompositeFactory1x2,
    CompositeFactory1x7,
    CompositeFactory2x2,
    CompositeFactory5x2,
)

COMPLEX_CASES_PARAMS = [
    # Case 1:
    # gust_max_raw = 99.0
    # The Q90 is computed from [60, 70, 75, 98, 99] => Q90 = 98.6
    # => gust_max = 100.0
    # I_0 = [80, 100] contains 2/10 = 20% of data_max_da points => OK
    # Q90 >= 80 for the terms 0 and
    (
        generate_valid_times(periods=4),
        [
            [[10.0, 20.0], [30.0, 40.0], [50.0, 60.0], [70.0, 75.0], [90.0, 99.0]],
            [[10.0, 20.0], [30.0, 40.0], [50.0, 60.0], [70.0, 75.0], [20.0, 31.0]],
            [[11.0, 12.0], [13.0, 14.0], [15.0, 16.0], [17.0, 74.0], [98.0, 90.0]],
            [[10.0, 20.0], [30.0, 40.0], [50.0, 60.0], [61.0, 62.0], [63.0, 64.0]],
        ],
    ),
    # Case 2:
    # gust_max_raw = 99.0
    # The Q90 is computed from [51, 60, 76, 77, 89, 109] => Q90 = 99.0
    # => gust_max = 100.0
    # I_0 = [80, 100] contains 1/10 = 10% of data_max_da points => NOK
    # I_1 = [70, 90] contains raf_max and 3/10 = 30% of data_max_da points => OK
    # Q90 >= 70 for the 2first term
    (
        generate_valid_times(periods=4),
        [
            [[10.0, 20.0], [30.0, 40.0], [50.0, 60.0], [70.0, 75.0], [71.0, 109.0]],
            [[10.0, 20.0], [30.0, 40.0], [50.0, 60.0], [76.0, 77.0], [89.0, 79.0]],
            [[1.0, 2.0], [3.0, 4.0], [51.0, 6.0], [1.0, 0.0], [2.0, 70.0]],
            [[10.0, 20.0], [30.0, 40.0], [50.0, 60.0], [61.0, 62.0], [63.0, 64.0]],
        ],
    ),
    # Case 2:
    # gust_max_raw = 120.0
    # The Q90 is computed from [51, 55, 56, 59, 71, 120] => Q90 = 95.5
    # => gust_max = 100.0
    # I_0 = [80, 100] contains 0/10 = 10% of data_max_da points => NOK
    # I_1 = [70, 90] contains 1/10 = 20% of data_max_da points => NOK
    # I_2 = [60, 80] contains 0/10 = 20% of data_max_da points => NOK
    # I_3 = [50, 70] contains 4/10 = 40% of data_max_da points => OK
    # Q90 >= 50 for all terms 3
    (
        generate_valid_times(periods=4),
        [
            [[10.0, 20.0], [30.0, 40.0], [51.0, 55.0], [56.0, 59.0], [66.0, 120.0]],
            [[10.0, 20.0], [30.0, 40.0], [51.0, 52.0], [53.0, 54.0], [71.0, 58.0]],
            [[1.0, 2.0], [3.0, 4.0], [51.0, 6.0], [1.0, 0.0], [2.0, 45.0]],
            [[10.0, 20.0], [30.0, 40.0], [51.0, 51.0], [52.0, 51.0], [56.0, 64.0]],
        ],
    ),
    # Case 3:
    # gust_max_raw = 99.0
    # The Q90 is computed from [99] => Q90 = 99.0
    # => gust_max = 100.0
    # [80, 100] contains 1/10 = 20% of data_max_da points => NOK
    # [70, 90] contains 0/10 = 20% of data_max_da points => NOK
    # [60, 80] contains 0/10 = 20% of data_max_da points => NOK
    # [50, 70] contains 0/10 = 40% of data_max_da points => NOK
    # => no interval found
    # Q90 >= 50 for the 2 first terms
    (
        generate_valid_times(periods=4),
        [
            [[10.0, 20.0], [30.0, 40.0], [41.0, 45.0], [46.0, 49.0], [46.0, 99.0]],
            [[10.0, 20.0], [30.0, 40.0], [41.0, 42.0], [43.0, 44.0], [41.0, 58.0]],
            [[1.0, 2.0], [3.0, 4.0], [41.0, 6.0], [1.0, 0.0], [2.0, 45.0]],
            [[10.0, 20.0], [30.0, 40.0], [41.0, 31.0], [22.0, 21.0], [26.0, 24.0]],
        ],
    ),
]


class TestGustSummaryBuilder:
    @pytest.mark.parametrize(
        "valid_times, data, units_compo, units_data, data_exp, unit_exp",
        [
            (
                generate_valid_times(periods=2),
                [[[0.0, 1.0], [np.nan, 20.0]], [[4.0, np.nan], [15.0, 18.0]]],
                {"gust": "km/h"},
                {"gust": "km/h"},
                [[[0.0, 1.0], [np.nan, 20.0]], [[4.0, np.nan], [15.0, 18.0]]],
                "km/h",
            ),
            (
                generate_valid_times(periods=2),
                [[[0.0, 1.0], [np.nan, 20.0]], [[4.0, np.nan], [15.0, 18.0]]],
                {"gust": "km/h"},
                {"gust": "m s**-1"},
                3.6
                * np.array(
                    [[[0.0, 1.0], [np.nan, 20.0]], [[4.0, np.nan], [15.0, 18.0]]]
                ),
                "km/h",
            ),
        ],
    )
    def test_units_conversion(
        self, valid_times, data, units_compo, units_data, data_exp, unit_exp
    ):
        """Test the conversion of the gust unit which has to be km/h."""
        composite = CompositeFactory2x2().get(
            valid_times=valid_times,
            data_gust=data,
            units_compo=units_compo,
            units_data=units_data,
        )
        dataset = composite.compute()
        summary_builder = GustSummaryBuilder(composite, dataset)

        assert summary_builder.gust_da.units == unit_exp

        values = summary_builder.gust_da.sel(valid_time=valid_times).values
        np.testing.assert_allclose(values, data_exp)

    @pytest.mark.parametrize(
        "valid_times, data",
        [
            (
                generate_valid_times(periods=2),
                [[[0.0, 40.0], [np.nan, 10.5]], [[20.0, 30.0], [np.nan, 40.0]]],
            ),
            (
                generate_valid_times(periods=2),
                [[[0.0, 40.0], [np.nan, 10.5]], [[20.0, 30.0], [40.0, np.nan]]],
            ),
        ],
    )
    def test_mask(self, valid_times, data, assert_equals_result):
        composite = CompositeFactory2x2().get(valid_times=valid_times, data_gust=data)
        dataset = composite.compute()
        summary_builder = GustSummaryBuilder(composite, dataset)

        res: dict = {
            "data": data,
            "points_nbr": summary_builder.dataset.attrs["points_nbr"],
            "mask": summary_builder.mask,
        }

        assert_equals_result(res)

    @pytest.mark.parametrize(
        "valid_times, data",
        [
            (generate_valid_times(periods=1), [np.nan]),
            (generate_valid_times(periods=1), [0.0]),
            (generate_valid_times(periods=1), [50.0]),
            (generate_valid_times(periods=1), [40.0, 110.0]),  # Q90 = 110.0
            (generate_valid_times(periods=1), [54.0, 94.0]),  # Q90 = 90.0
            (generate_valid_times(periods=1), [58.0, 99.0]),  # S90 = 94.9
            (generate_valid_times(periods=1), [59.0, 99.0]),  # S90 = 95.0
            (generate_valid_times(periods=1), [72.0, 103.0]),  # Q90 = 99.9
            (generate_valid_times(periods=1), [51.0, 72.2]),  # Q90 = 69.9
            (generate_valid_times(periods=1), [52.2, 72.2]),  # Q90 = 70.0
            (generate_valid_times(periods=1), [53.0, 72.2]),  # Q90 = 70.1
            (generate_valid_times(periods=1), [51.0, 61.0]),  # Q90 = 60.0
            (
                # The Q90 is computed only y from 60.0, 61.0, 71.0, 80.0, 90.0, 132.0
                # => Q90 = 111.2
                # I_0 = [100, 120] contains 16.7 % of points < 20 %
                # I_1 = [90, 110] contains 16.7 % of points < 20 %
                # I_1 = [80, 100] contains 33.3 % of points >= 20 % => interval found
                generate_valid_times(periods=1),
                [40.0, 60.0, 61.0, 71.0, 80.0, 90.0, 132.0],  # Q90 = 111.2
            ),
        ],
    )
    def test_gust_metadata(self, valid_times, data, assert_equals_result):
        func: Callable

        if len(data) == 1:
            func = CompositeFactory1x1().get_composite_when_term_data_is_one_number
        elif len(data) == 2:
            func = CompositeFactory1x2.get
        else:
            func = CompositeFactory1x7.get

        composite = func(valid_times=valid_times, data_gust=data)

        dataset = composite.compute()
        summary_builder = GustSummaryBuilder(composite, dataset)

        res: dict = {
            "data": data,
            "gust_max_raw": summary_builder.dataset.attrs["gust_max_raw"],
            "gust_max": summary_builder.gust_max,
            "bound_inf_init": summary_builder._initialize_bound_inf(),
        }

        assert_equals_result(res)

    @staticmethod
    def check_compute(
        composite_factory, valid_times, data: list | np.ndarray, assert_equals_result
    ):
        composite = composite_factory().get(valid_times=valid_times, data_gust=data)
        dataset = composite.compute()
        summary_builder = GustSummaryBuilder(composite, dataset)
        summary_builder.compute(Datetime(2023, 1, 2, 0, 0, 0))

        res: dict = {
            "input": {"valid_times": [str(v) for v in valid_times], "data": data},
            "output": {
                "points_nbr": summary_builder.dataset.attrs["points_nbr"],
                "gust_max_da": summary_builder.gust_max_da.values,
                "gust_max_raw": summary_builder.dataset.attrs["gust_max_raw"],
                "gust_max": summary_builder.gust_max,
                "summary": summary_builder.summary,
            },
        }

        case = summary_builder.case

        # If case 0, then assert_equals_result
        if case == "0":
            assert_equals_result(res)
            return

        # Else add more elements in output before comparing
        bound_inf = summary_builder.summary.get("bound_inf")
        if bound_inf is not None:
            res["output"].update(
                {
                    "gust_q90": summary_builder.dataset["gust_q90"].values,
                    "period": str(summary_builder._find_gust_period(bound_inf)),
                    "percent": summary_builder.compute_percent_coverage_of_interval(
                        bound_inf, summary_builder.summary.get("bound_sup")
                    ),
                }
            )
        else:
            bound_inf = 50.0
            res["output"].update(
                {
                    "gust_q90": summary_builder.dataset["gust_q90"].values,
                    "period": str(summary_builder._find_gust_period(bound_inf)),
                }
            )

        assert_equals_result(res)

    @pytest.mark.parametrize(
        "valid_times, data",
        [
            # Case 0
            (
                generate_valid_times(periods=2),
                [[[0.0, 40.0], [np.nan, 10.5]], [[20.0, 30.0], [np.nan, 20.5]]],
            ),
            # Case 0
            (generate_valid_times(periods=1), [[0.0, 40.1], [np.nan, 10.5]]),
            # Case 0
            (generate_valid_times(periods=1), [[0.0, 20.0], [49.9, 10.5]]),
            # Case 0
            (generate_valid_times(periods=1), [[0.0, 20.0], [50.0, 10.5]]),
        ],
    )
    def test_compute_2x2(
        self, valid_times, data: list | np.ndarray, assert_equals_result
    ):
        self.check_compute(CompositeFactory2x2, valid_times, data, assert_equals_result)

    @pytest.mark.parametrize("valid_times, data", COMPLEX_CASES_PARAMS)
    def test_compute_5x2(
        self, valid_times, data: list | np.ndarray, assert_equals_result
    ):
        self.check_compute(CompositeFactory5x2, valid_times, data, assert_equals_result)
