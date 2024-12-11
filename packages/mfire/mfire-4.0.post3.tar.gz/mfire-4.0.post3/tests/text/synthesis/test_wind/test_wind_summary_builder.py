from datetime import datetime
from unittest.mock import patch

import numpy as np
import pytest

import mfire.utils.mfxarray as xr
from mfire.text.synthesis.wind_reducers.exceptions import WindSynthesisError
from mfire.text.synthesis.wind_reducers.mixins import BaseSummaryBuilderMixin
from mfire.text.synthesis.wind_reducers.wind import WindSummaryBuilder
from mfire.text.synthesis.wind_reducers.wind.case3 import (
    BlockSummaryBuilder,
    Case3SummaryBuilder,
    TwoBlocksSummaryBuilder,
)
from mfire.text.synthesis.wind_reducers.wind.wind_intensity import Pci, WindIntensity
from mfire.utils.date import Datetime
from tests.text.utils import generate_valid_times, generate_valid_times_v2

from .factories import (
    CompositeFactory1x1,
    CompositeFactory2x2,
    CompositeFactory2x2Type1,
    CompositeFactory5x2,
    CompositeFactory6x2,
    CompositeFactory6x4,
)

ERROR_CASE: str = BaseSummaryBuilderMixin.ERROR_CASE


class TestWindDataConversion:
    @pytest.mark.parametrize(
        "valid_times, data, units_compo, units_data, data_exp, unit_exp",
        [
            # All parametrization produce examples with only type 1 terms: then the
            # data is not filtered
            (
                generate_valid_times(periods=2),
                [[[0.0, 1.0], [np.nan, 10.0]], [[4.0, np.nan], [11.0, 14.0]]],
                {"wind": "km/h"},
                {"wind": "km/h"},
                [[[0.0, 1.0], [np.nan, 10.0]], [[4.0, np.nan], [11.0, 14.0]]],
                "km/h",
            ),
            (
                generate_valid_times(periods=2),
                [[[0.0, 1.0], [0.0, 10.0]], [[4.0, 0.0], [11.0, 14.0]]],
                {"wind": "km/h"},
                {"wind": "km/h"},
                [[[0.0, 1.0], [0.0, 10.0]], [[4.0, 0.0], [11.0, 14.0]]],
                "km/h",
            ),
            (
                generate_valid_times(periods=2),
                [[[0.0, 1.0], [np.nan, 1.0]], [[1.0, 0.0], [1.0, 1.0]]],
                {"wind": "km/h"},
                {"wind": "m s**-1"},
                3.6 * np.array([[[0.0, 1.0], [np.nan, 1.0]], [[1.0, 0.0], [1.0, 1.0]]]),
                "km/h",
            ),
            (
                generate_valid_times(periods=2),
                [[[0.0, 1.0], [0.0, 1.0]], [[1.0, 0.0], [1.0, 1.0]]],
                {"wind": "km/h"},
                {"wind": "m s**-1"},
                3.6 * np.array([[[0.0, 1.0], [0.0, 1.0]], [[1.0, 0.0], [1.0, 1.0]]]),
                "km/h",
            ),
        ],
    )
    def test_wind_units_conversion(
        self, valid_times, data, units_compo, units_data, data_exp, unit_exp
    ):
        """Test wind force initialization and conversion.

        Nan values are replaced by 0 and the wind force unit has to be km/h.
        """
        composite = CompositeFactory2x2().get(
            valid_times=valid_times,
            data_wind=data,
            units_compo=units_compo,
            units_data=units_data,
        )
        dataset = composite.compute()
        summary_builder = WindSummaryBuilder(composite, dataset)

        # Check unit
        data_array: xr.DataArray = summary_builder.wind
        assert data_array.units == unit_exp

        # Check value after conversion
        np.testing.assert_allclose(data_array.values, data_exp)

    @pytest.mark.parametrize(
        "valid_times, data, units_compo, units_data, data_exp, unit_exp",
        [
            (
                generate_valid_times(periods=2),
                [[[0.1, 1.0], [np.nan, 20.0]], [[4.0, np.nan], [15.0, 18.0]]],
                {"direction": "deg"},
                {"direction": "deg"},
                [[[0.1, 1.0], [np.nan, 20.0]], [[4.0, np.nan], [15.0, 18.0]]],
                "deg",
            ),
            (
                generate_valid_times(periods=2),
                [[[0.1, 1.0], [0.0, 20.0]], [[4.0, np.nan], [15.0, 18.0]]],
                {"direction": "deg"},
                {"direction": "°"},
                [[[0.1, 1.0], [np.nan, 20.0]], [[4.0, np.nan], [15.0, 18.0]]],
                "deg",
            ),
        ],
    )
    def test_direction_units_conversion(
        self, valid_times, data, units_compo, units_data, data_exp, unit_exp
    ):
        """Test wind direction initialization and conversion.

        The wind direction unit has to be km/h.
        """
        composite = CompositeFactory2x2Type1().get(
            valid_times=valid_times,
            data_dir=data,
            units_compo=units_compo,
            units_data=units_data,
        )
        dataset = composite.compute()
        summary_builder = WindSummaryBuilder(composite, dataset)

        # Check unit
        data_array: xr.DataArray = summary_builder.direction
        assert data_array.units == unit_exp

        # Check value after conversion
        np.testing.assert_allclose(data_array.values, data_exp)


class TestWindSummaryInitialization:
    def test_points_nbr(self):
        valid_times = generate_valid_times(periods=1)

        composite = CompositeFactory5x2().get(
            valid_times=valid_times, data_wind=np.full((5, 2), 20.0)
        )
        dataset = composite.compute()
        summary_builder = WindSummaryBuilder(composite, dataset)

        points_nbr_exp = 5 * 2
        assert summary_builder.dataset.attrs["points_nbr"] == points_nbr_exp

    @pytest.mark.parametrize(
        "term_data, lower_bound, count_exp, percent_exp",
        [
            (
                [[1.0, 2.0], [3.0, 3.0], [4.0, 5.0], [30.0, 31.0], [32.0, 33.0]],
                20.0,
                4,
                40.0,
            ),
            (
                [
                    [np.nan, np.nan],
                    [np.nan, np.nan],
                    [30.0, 31.0],
                    [32.0, 33.0],
                    [34.0, 35.0],
                ],
                20.0,
                6,
                100.0,
            ),
            (
                [
                    [np.nan, np.nan],
                    [np.nan, np.nan],
                    [1.0, 2.0],
                    [3.0, 33.0],
                    [34.0, 35.0],
                ],
                20.0,
                3,
                50.0,
            ),
            (np.full((5, 2), np.nan), 30.0, 0, 0.0),
            (np.full((5, 2), 0.0), 30.0, 0, 0.0),
        ],
    )
    def test_count_points(self, term_data, lower_bound, count_exp, percent_exp):
        valid_times = generate_valid_times(periods=1)
        valid_time = valid_times[0]

        composite = CompositeFactory5x2().get(
            valid_times=valid_times, data_wind=term_data
        )
        dataset = composite.compute()
        summary_builder = WindSummaryBuilder(composite, dataset)

        data = summary_builder.wind.sel(valid_time=valid_time)
        count, percent = summary_builder.count_points(data, data >= lower_bound)

        assert count == count_exp
        assert percent == percent_exp

    @staticmethod
    @patch(
        "mfire.text.synthesis.wind_reducers.wind.WindSummaryBuilder."
        "WF_TYPE_SEPARATORS",
        [15.0, 30.0],
    )  # We mock the wind types separator to easily simulate the wind situations
    def _check_wind_summary_builder(
        composite_factory, valid_times, data_wf, data_wd, assert_equals_result
    ):
        """Test WindSummaryBuilder.

        We mock the wind types separator to easily simulate the wind situations.

        Test the most sensitive data from the initialization to the summary dictionary
        generation:
        - term types
        - case
        - dataset.attrs
        - wind data
        - direction data
        """
        # Compute the composite
        composite = composite_factory.get(
            valid_times=valid_times, data_wind=data_wf, data_dir=data_wd
        )
        dataset = composite.compute()
        summary_builder = WindSummaryBuilder(composite, dataset)

        # Generate summary
        reference_datetime: Datetime = Datetime(datetime.now())
        summary_builder.compute(reference_datetime)

        # Build result
        result: dict = {
            "input": {
                "valid_times": [str(v) for v in valid_times],
                "data_wf": data_wf,
                "data_wd": data_wd,
            },
            "wind_type": summary_builder.wind_type.values.tolist(),
            "dataset_attrs": summary_builder._get_sorted_dataset_attrs(),
            "data_wf": summary_builder.wind.values.tolist(),
            "data_wd": summary_builder.direction.values.tolist(),
        }

        assert_equals_result(result)

    @pytest.mark.parametrize(
        "valid_times, data_wf, data_wd",
        [
            # All point have no wind force
            # --> term of type 1
            (
                generate_valid_times(periods=1),  # valid_times
                np.full((5, 2), np.nan),  # data_wf
                np.full((5, 2), np.nan),  # data_wd
            ),
            # Each point has a wind force < 15 --> term of type 1
            (
                generate_valid_times(periods=1),
                [[1.0, 2.0], [4.0, 5.0], [6.0, 7.0], [np.nan, np.nan], [8.0, 14.9]],
                [
                    [10.0, 11.0],
                    [12.0, 13.0],
                    [14.0, 15.0],
                    [np.nan, np.nan],
                    [18.0, 19.0],
                ],
            ),
            # The wind force are in [1, 15] --> type 2
            (
                generate_valid_times(periods=1),
                [[1.0, 2.0], [4.0, 5.0], [6.0, 7.0], [np.nan, np.nan], [8.0, 15.0]],
                [
                    [10.0, 11.0],
                    [12.0, 13.0],
                    [14.0, 15.0],
                    [np.nan, np.nan],
                    [18.0, 19.0],
                ],
            ),
            # A point has a wind force >= 30 and the threshold is 10.5
            # 1/10 points (10. %) with a wind force >= 30 --> possibly a type 3
            # 1/10 points (10. %) with a wind force >= threshold --> type 3
            (
                generate_valid_times(periods=1),
                [[1.0, 2.0], [4.0, 5.0], [6.0, 7.0], [8.0, 9.0], [8.0, 30.0]],
                [
                    [10.0, 11.0],
                    [12.0, 13.0],
                    [14.0, 15.0],
                    [np.nan, np.nan],
                    [18.0, 19.0],
                ],
            ),
            # All points have a wind force equal to 20.0  --> type 2
            (generate_valid_times(periods=1), [[20.0, 20.0]] * 5, [[10.0, 11.0]] * 5),
            # All points have a wind force  >= 30  --> type 3
            (generate_valid_times(periods=1), [[30.0, 40.0]] * 5, [[10.0, 11.0]] * 5),
        ],
    )
    def test_wind_summary_builder_5x2(
        self, valid_times, data_wf, data_wd, assert_equals_result
    ):
        """Test the WindSummaryBuilder with terms of 5x2 size."""
        self._check_wind_summary_builder(
            CompositeFactory5x2, valid_times, data_wf, data_wd, assert_equals_result
        )

    @pytest.mark.parametrize(
        "valid_times, data_wf, data_wd",
        [
            # A point has a wind force equal to 30.0 and the threshold is 4.0
            # 1/11 points (9.1 %) with a wind force >= 30 --> possibly a type 3
            # 1/12 points (9.1 %) with a wind force >= threshold --> type 2
            (
                generate_valid_times(periods=1),
                [
                    [1.0, 1.0],
                    [np.nan, 1.0],
                    [1.0, 1.0],
                    [1.0, 1.0],
                    [1.0, 1.0],
                    [1.0, 30.0],
                ],
                [
                    [10.0, 11.0],
                    [np.nan, 13.0],
                    [14.0, 15.0],
                    [16.0, 17.0],
                    [18.0, 19.0],
                    [20.0, 21.0],
                ],
            ),
            # A point has a wind force equal to 30.0 and the threshold is 20.4
            # 2/10 points (20.0 %) with a wind force >= 30 --> possibly a type 3
            # 2/10 points (20.0 %) with a wind force >= threshold --> type 3
            (
                generate_valid_times(periods=1),
                [
                    [1.0, 2.0],
                    [np.nan, 3.0],
                    [np.nan, 5.0],
                    [6.0, 7.0],
                    [8.0, 9.0],
                    [31.0, 30.0],
                ],
                [
                    [10.0, 11.0],
                    [np.nan, 13.0],
                    [np.nan, 15.0],
                    [16.0, 17.0],
                    [18.0, 19.0],
                    [20.0, 21.0],
                ],
            ),
            # Threshold = 11.8
            # - term 0: all points < 15 --> type 1
            # - term 1: 4/12 (33.3 %) points with wind >= 15 --> type 2
            # - term 2: 2/12 (16.7 %) points with wind force >= 30 --> possibly a type 3
            # 4/12 points (33.3 %) with a wind force >= threshold --> type 3
            (
                generate_valid_times(periods=3),
                [
                    [
                        [1.0, 2.0],
                        [3.0, 3.0],
                        [4.0, 5.0],
                        [6.0, 7.0],
                        [8.0, 9.0],
                        [10.0, 11.0],
                    ],
                    [
                        [1.0, 2.0],
                        [3.0, 3.0],
                        [4.0, 5.0],
                        [6.0, 7.0],
                        [16.0, 17.0],
                        [18.0, 19.0],
                    ],
                    [
                        [1.0, 2.0],
                        [3.0, 3.0],
                        [4.0, 5.0],
                        [6.0, 7.0],
                        [16.0, 17.0],
                        [30.0, 30.0],
                    ],
                ],
                [
                    [
                        [1.0, 2.0],
                        [3.0, 3.0],
                        [4.0, 5.0],
                        [6.0, 7.0],
                        [16.0, 17.0],
                        [18.0, 19.0],
                    ],
                    [
                        [10.0, 11.0],
                        [12.0, 13.0],
                        [14.0, 15.0],
                        [16.0, 17.0],
                        [18.0, 19.0],
                        [20.0, 21.0],
                    ],
                    [
                        [22.0, 23.0],
                        [24.0, 25.0],
                        [26.0, 27.0],
                        [28.0, 29.0],
                        [30.0, 31.0],
                        [32.0, 33.0],
                    ],
                ],
            ),
            # Threshold = 8.2
            # - term 0: all points < 15 --> type 1
            # - term 1: 4/12 (33.3 %) points with wind >= 15 --> type 2
            # - term 2: 1/12 (8.3 %) points with wind force >= 30 --> possibly a type 3
            # 1/12 points (8.3 %) with a wind force >= threshold --> type 2
            (
                generate_valid_times(periods=3),
                [
                    [
                        [1.0, 2.0],
                        [3.0, 3.0],
                        [4.0, 5.0],
                        [6.0, 7.0],
                        [8.0, 9.0],
                        [10.0, 11.0],
                    ],
                    [
                        [1.0, 2.0],
                        [3.0, 3.0],
                        [4.0, 5.0],
                        [6.0, 7.0],
                        [16.0, 17.0],
                        [18.0, 19.0],
                    ],
                    [
                        [1.0, 1.0],
                        [1.0, 1.0],
                        [1.0, 1.0],
                        [1.0, 1.0],
                        [1.0, 5.0],
                        [np.nan, 30.0],
                    ],
                ],
                [
                    [
                        [1.0, 2.0],
                        [3.0, 3.0],
                        [4.0, 5.0],
                        [6.0, 7.0],
                        [16.0, 17.0],
                        [18.0, 19.0],
                    ],
                    [
                        [10.0, 11.0],
                        [12.0, 13.0],
                        [14.0, 15.0],
                        [16.0, 17.0],
                        [18.0, 19.0],
                        [20.0, 21.0],
                    ],
                    [
                        [22.0, 23.0],
                        [24.0, 25.0],
                        [26.0, 27.0],
                        [28.0, 29.0],
                        [30.0, 31.0],
                        [32.0, 33.0],
                    ],
                ],
            ),
        ],
    )
    def test_wind_summary_builder_6x2(
        self, valid_times, data_wf, data_wd, assert_equals_result
    ):
        """Test the WindSummaryBuilder with terms of 5x2 size."""
        self._check_wind_summary_builder(
            CompositeFactory6x2, valid_times, data_wf, data_wd, assert_equals_result
        )

    @pytest.mark.parametrize(
        "valid_times, data_wf, data_wd",
        [
            # Threshold = 4.0
            # There is point >= 15 --> --> possibly a type 2
            # 1/24 points (4.1 %) with a wind force >= 15 --> type 1
            (
                generate_valid_times(periods=1),
                [
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 20.0],
                ],
                [
                    [1.0, 2.0, 3.0, 3.0],
                    [5.0, 6.0, 7.0, 8.0],
                    [9.0, 10.0, 11.0, 12.0],
                    [13.0, 14.0, 15.0, 16.0],
                    [17.0, 18.0, 19.0, 20.0],
                    [21.0, 22.0, 23.0, 24.0],
                ],
            ),
            # Threshold = 4.0
            # There is point >= 30 --> --> possibly a type 3
            # - 1/24 points (4.1 %) with a wind force >= 30 --> not a type 3
            # - 1/24 points (4.1 %) with a wind force >= 15 --> not a type 2
            # so this is a term of type 1
            (
                generate_valid_times(periods=1),
                [
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 30.0],
                ],
                [
                    [1.0, 2.0, 3.0, 3.0],
                    [5.0, 6.0, 7.0, 8.0],
                    [9.0, 10.0, 11.0, 12.0],
                    [13.0, 14.0, 15.0, 16.0],
                    [17.0, 18.0, 19.0, 20.0],
                    [21.0, 22.0, 23.0, 24.0],
                ],
            ),
            # Threshold = 4.0
            # There is point >= 30 --> --> possibly a type 3
            # - 1/24 points (4.1 %) with a wind force >= 30 --> not a type 3
            # - 2/24 points (8.3 %) with a wind force >= 15 --> type 2
            (
                generate_valid_times(periods=1),
                [
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 1.0, 1.0],
                    [1.0, 1.0, 20.0, 30.0],
                ],
                [
                    [1.0, 2.0, 3.0, 3.0],
                    [5.0, 6.0, 7.0, 8.0],
                    [9.0, 10.0, 11.0, 12.0],
                    [13.0, 14.0, 15.0, 16.0],
                    [17.0, 18.0, 19.0, 20.0],
                    [21.0, 22.0, 23.0, 24.0],
                ],
            ),
        ],
    )
    def test_wind_summary_builder_6x4(
        self, valid_times, data_wf, data_wd, assert_equals_result
    ):
        """Test the WindSummaryBuilder with terms of 5x2 size."""
        self._check_wind_summary_builder(
            CompositeFactory6x4, valid_times, data_wf, data_wd, assert_equals_result
        )


class TestGenerateSummary:
    @staticmethod
    def _compare_summary(summary: dict, summary_exp: dict):
        assert summary == summary_exp


class TestGenerateSummaryCase1(TestGenerateSummary):
    class CompositeFactory(CompositeFactory2x2):
        LON = [30, 31]
        LAT = [40, 41]

    def test(self):
        valid_times = generate_valid_times(periods=1)

        composite = self.CompositeFactory().get(
            valid_times=valid_times, data_wind=np.full((2, 2), 9.0)
        )
        dataset = composite.compute()
        summary_builder = WindSummaryBuilder(composite, dataset)
        reference_datetime: Datetime = Datetime(datetime.now())
        summary = summary_builder.compute(reference_datetime)

        summary_exp = {"wind": {"case": "1"}}
        self._compare_summary(summary, summary_exp)


TEST_CASE3_PARAMS: list = [
    (
        # Input Fingerprint: 111222222233333333333333
        # The last group is the only one type 3 group and then has the wind force
        # max [20, 30[.
        # WindBlock with 1 PCI, 1 PCD
        generate_valid_times(periods=24),
        [5.0] * 3 + [10.0] * 7 + [20.0] * 10 + [25.0] * 4,
        [90.0] * 24,
    ),
    (
        # Input Fingerprint: 333333332233333333333333
        # The type 2 group hase size 2 between 2 type 3 groups
        # => we will get only one merged WindBlock
        # 1 WindBlock with 1 PCI, no PCD
        generate_valid_times(periods=24),
        [20.0] * 8 + [10.0] * 2 + [21.0] * 14,
        [np.nan] * 24,
    ),
    (
        # Input Fingerprint: 333222222233333333333333
        # 2 type 3 groups:
        # - 1st is < 4h => not kept
        # - the last which is >= 4 and has the wind force max
        # 1 WindBlocks: 1 PCI, no PCD
        generate_valid_times(periods=24),
        [20.0] * 3 + [10.0] * 7 + [21.0] * 14,
        [np.nan] * 24,
    ),
    (
        # Input Fingerprint: 322222222222222222222222
        # Only the 1st term has the type 3
        # 1 WindBlock: 1 PCI, no PCD (because
        # dir period of 1h < 3h)
        generate_valid_times(periods=24),
        [20.0] * 1 + [10.0] * 23,
        [10.0] * 24,
    ),
    (
        # Input Fingerprint: 332222222222222222222222
        # Only one type 3 group with the 1srt 2 terms.
        # 1 WindBlock: 1 PCI, no PCD (because dir period of 2h < 3h)
        generate_valid_times(periods=24),
        [20.0] * 2 + [10.0] * 22,
        [10.0] * 24,
    ),
    (
        # Input Fingerprint: 333222222222222222222222
        # Only one type 3 group with the first 3 terms.
        # 1 WindBlock: 1 PCI, 1 PCD
        generate_valid_times(periods=24),
        [20.0] * 3 + [10.0] * 21,
        [10.0] * 24,
    ),
    (
        # Input Fingerprint: 222222223223223223223223
        # Type 3 terms are separated by 2-terms groups. The Last has the type 3.
        # 1 WindBlock: 1 PCI, 1 PCD
        generate_valid_times(periods=24),
        [10.0] * 8 + [20.0, 10.0, 10.0] * 5 + [20.0],
        [90] * 24,
    ),
    (
        # Input Fingerprint: 222222223223223223223222
        # Type 3 terms are separated by 2-terms groups. The Last has the type 2.
        # 1 WindBlock: 1 PCI, 1 PCD
        generate_valid_times(periods=24),
        [10.0] * 8 + [20.0, 10.0, 12.0] * 5 + [10.0],
        [180.0] * 24,
    ),
    (
        # Input Fingerprint: 22222222222222222222223
        # Only the last term has the type 3
        # 1 WindBlock: 1 PCI, no PCD (because dir period of 1h < 3h)
        generate_valid_times(periods=24),
        [12.0] * 23 + [20.0],
        [10] * 24,
    ),
    (
        # Input Fingerprint: 333322222233333333333333
        # 2 type 3 groups (1st and last), wind force max is in the last
        # 2 WindBlocks
        generate_valid_times(periods=24),
        [20.0] * 4 + [12.0] * 6 + [21.0] * 14,
        [np.nan] * 24,
    ),
    (
        # Input Fingerprint: 333222222233333333333333
        # 2 type 3 groups (1st and last), wind force max is in the 1st
        # 2 WindBlocks
        generate_valid_times(periods=24),
        [25.0] * 3 + [11.0] * 7 + [20.0] * 14,
        [np.nan] * 24,
    ),
    (
        # Input Fingerprint: 333222222233333333333333
        # 2 type 3 groups (1st and last), wind force max in all type 3 group
        # 2 WindBlocks
        generate_valid_times(periods=24),
        [21.0] * 3 + [10.0] * 7 + [21.0] * 14,
        [np.nan] * 24,
    ),
    (
        # Input Fingerprint: 22222222223222222222222
        # Max wind force is on the only one type 3 term
        # 1 WindBlocks: 1 PCI, 0 PCD
        generate_valid_times(periods=24),
        [11.0] * 10 + [21.0] * 1 + [12.0] * 13,
        [150.0] * 24,
    ),
    (
        # Input Fingerprint: 333322222233333322223333
        # Max wind force is in the first type 3 group
        # There are 3 WindBlocks => the 2 last are the closest and will be
        # merged. So there will stay only 2 WindBlocks.
        generate_valid_times(periods=24),
        [22.0] * 4 + [10.0] * 6 + [21.0] * 6 + [11.0] * 4 + [21.0] * 4,
        [np.nan] * 24,
    ),
    (
        # Input Fingerprint: 333322222233333322223333
        # Max wind force is in all type 3 group
        # There are 3 WindBlocks => the 2 last are the closest and will be
        # merged. So there will stay only 2 WindBlocks.
        generate_valid_times(periods=24),
        [21.0] * 4 + [10.0] * 6 + [21.0] * 6 + [11.0] * 4 + [21.0] * 4,
        [np.nan] * 24,
    ),
    (
        # Input Fingerprint: 222222222333222222222223
        # 2 type 3 groups, wind force max is in 1st type 3 group, the last is so
        # short
        # 1 WindBlock: PCI, no PCD
        generate_valid_times(periods=24),
        [10.0] * 9 + [21.0] * 3 + [11.0] * 11 + [20.0] * 1,
        [360.0] * 24,
    ),
    (
        # Input Fingerprint: 333333333333333333333333
        # All terms are of type 3
        # Same WindDirection in the 1st and the last PCD
        # 1 WindBlock: 1 PCI, 2 PCD
        generate_valid_times(periods=24),
        [21.0] * 24,
        [0.1] * 4 + [150.0] * 12 + [0.1] * 8,
    ),
    (
        # Input Fingerprint: 333333333333333333333333
        # All terms are of type 3
        # The 1st and the last direction are opposite => no PCD
        # 1 WindBlock: 1 PCI, 0 PCD
        generate_valid_times(periods=24),
        [20.0] * 24,
        [180.0] * 4 + [np.nan] * 12 + [0.1] * 8,
    ),
    (
        # Input Fingerprint: 322222222333222222222222
        # Only short type 3 groups, wind force max 31 is in 2nd so is kept
        # 1 WindBlock: 1 PCI, no PCD
        generate_valid_times(periods=24),
        [20.0] * 1 + [10.0] * 8 + [21.0] * 3 + [10.0] * 12,
        [50.0] * 24,
    ),
    (
        # Input Fingerprint: 322222222333222222222222
        # Only short type 3 groups, wind force max 60 is in 2nd so is kept
        # 1 WindBlock: 1 PCI, no PCD
        generate_valid_times(periods=24),
        [20.0] * 1 + [10.0] * 8 + [40.0] * 3 + [15.0] * 12,
        [np.nan] * 24,
    ),
    (
        # Input Fingerprint: 22233222
        # 3-hours terms => 1 type group of 6 hours
        # 1 WindBlock: 1 PCI, 2 PCD
        generate_valid_times(periods=8, freq="3h"),
        [10.0] * 3 + [20.0] * 2 + [11.0] * 3,
        [np.nan] * 3 + [0.1] * 1 + [150.0] * 1 + [np.nan] * 3,
    ),
    (
        # Input Fingerprint: 222222222222222333333
        # 1 type 3 group at the end
        # 1 WindBlock: 1 PCI, 1 PCD
        generate_valid_times_v2("2023-01-02", (16, "h"), (5, "3h")),
        [10.0] * 15 + [20.0] * 6,
        [0.1] * 21,
    ),
    (
        # Input Fingerprint: 333322222222222222222322
        # 2 type 3 groups, wind force max in the 1st, the 2nd is so short
        # 1 WindBlock: 1 PCI, 1 PCD
        generate_valid_times(periods=24),
        [21.0] * 4 + [10.0] * 17 + [20.0] * 1 + [11.0] * 2,
        [0.1] * 24,
    ),
    (
        # Input Fingerprint: 333322222222222222223222
        # 2 type 3 groups, wind force max in the 2nd: all kept
        # 2 WindBlock
        generate_valid_times(periods=24),
        [20.0] * 4 + [10.0] * 16 + [21.0] * 1 + [10.0] * 3,
        [0.1] * 24,
    ),
    (
        # Input Fingerprint: 2323233332323222
        # 1 WindBlock
        generate_valid_times(periods=16),
        [10.0] + [20.0, 10.0] * 2 + [24.0] * 4 + [10.0, 20.0] * 2 + [10.0] * 3,
        [0.1] * 16,
    ),
    (
        # Input Fingerprint: only one term of type 3
        # 1 WindBlock
        generate_valid_times(periods=1),
        [40.0],
        [0.1],
    ),
    (
        # Input Fingerprint: 333222222222333333333222222222333333
        # The 2 first WindBlocks should be merged
        # 2 Windblocks: 3 changing and unordered WindIntensity
        generate_valid_times(periods=36),
        [75.0] * 3 + [10.0] * 9 + [65.0] * 9 + [10.0] * 9 + [75.0] * 6,
        [np.nan] * 36,
    ),
    (
        # Input Fingerprint: 333111111111333333333111111111333333
        # Same result as previous test: the 2 first WindBlocks should be merged
        # 2 Windblocks: 3 changing and unordered WindIntensity
        generate_valid_times(periods=36),
        [75.0] * 3 + [1.0] * 9 + [65.0] * 9 + [1.0] * 9 + [75.0] * 6,
        [np.nan] * 36,
    ),
    (
        # Input Fingerprint: 333222222233333333333333
        # 2 type 3 blocks: 1st so short, wind force max in the last
        # 1 Windblock: 1 PCI, no PCD
        generate_valid_times(periods=24),
        [20.0] * 3 + [15.0] * 7 + [29.0] * 14,
        [np.nan] * 24,
    ),
    (
        # Input Fingerprint: 333222222233333333333333
        # 2 type 3 blocks: wind force max in the 1st, 2nd enough long then kept
        # 2 Windblocks
        generate_valid_times(periods=24),
        [24.0] * 3 + [15.0] * 7 + [21.0] * 14,
        [5.0] * 24,
    ),
    (
        # Input Fingerprint: 333322222233333322223333
        # There are 3 WindBlocks => the 2 last are the closest and will be
        # merged. So there will stay only 2 WindBlocks.
        generate_valid_times(periods=24),
        [21.0] * 4 + [15.0] * 6 + [21.0] * 6 + [15.0] * 4 + [24.9] * 4,
        [90.0] * 12 + [180.0] * 12,
    ),
    (
        # Input Fingerprint: 222222222333222222222223
        # Max wind force is in 1st type 3 group (last type 3 term no kept)
        # 1 WindBlock: 1 PCI, no PCD
        generate_valid_times(periods=24),
        [15.0] * 9 + [29.0] * 3 + [15.0] * 11 + [20.0] * 1,
        [0.1] * 24,
    ),
    (
        # Input Fingerprint: 322222222333222222222222
        # Max wind force is in the 2 WindBlocks
        # 2 WindBlocks
        generate_valid_times(periods=24),
        [21.0] * 1 + [15.0] * 8 + [21.0] * 3 + [15.0] * 12,
        [np.nan] * 24,
    ),
    (
        # Input Fingerprint: 333322222222222222222322
        # Max wind force is in the 1st WindBlock
        # 1 WindBlock: 1 PCI, 1 PCD
        generate_valid_times(periods=24),
        [29.0] * 4 + [15.0] * 17 + [20.0] * 1 + [15.0] * 2,
        [0.1] * 24,
    ),
    (
        # Input Fingerprint: 333333333333333333333333
        # More than 3 wi but they are ordered from the min to the max
        # 1 WindBlock:
        # - 3 PCI with [20, 30[, [30, 45[ and [70, ...[ wi
        # => only [20, 30[ and [70, ...[ wi are kept
        # - 1 PCD
        # case: case 3_1B_2_1
        generate_valid_times(periods=24),
        [20.0] * 20 + [30.0] * 2 + [70.0] * 2,
        [360.0] * 24,
    ),
    (
        # Input Fingerprint: 333333333333333333333333
        # More than 3 wi but they are ordered from the max to the min
        # 1 WindBlock:
        # - 3 PCI with [70, ...[, [45, 70[ and [20, 30[ wi
        # => only [70, ...[ and [20, 30[ wi are kept
        # - same wind direction for the 2 blocks => 1 PCD
        # case: case 3_1B_2_1
        generate_valid_times(periods=24),
        [70.0] * 2 + [45.0] * 2 + [20.0] * 20,
        [360.0] * 24,
    ),
    (
        # Input Fingerprint: 333333333322223333333333
        # More than 3 wi but they are ordered from the min to the max
        # 2 WindBlocks
        # - B1: 1 PCI with [20, 30[ wi
        # - B2: 2 PCI with [30, 45[ and [70, ...[ wi
        # - same wind direction for the 2 blocks
        # => only [20, 30[ and [70, ...[ wi are kept
        # - same wind direction for the 2 blocks => 1 PCD
        # case: case 3_2B_2_1_1_1
        generate_valid_times(periods=24),
        [20.0] * 16 + [np.nan] * 4 + [30.0] * 2 + [70.0] * 2,
        [360.0] * 24,
    ),
    (
        # Input Fingerprint: 333333333322223333333333
        # More than 3 wi but they are ordered from the max to the min
        # 2 WindBlocks
        # - B1: 1 PCI with [70, ...[ and [30, 45[ wi
        # - B2: 2 PCI with[20, 30[ wi
        # - same wind direction for the 2 blocks => 1 PCD
        # => only [70, ...[ and [20, 30[ wi are kept
        # case: case 3_2B_2_1_1_1
        generate_valid_times(periods=24),
        [70.0] * 2 + [30.0] * 2 + [np.nan] * 4 + [20.0] * 16,
        [360.0] * 24,
    ),
    (
        # Input Fingerprint: 333333333333333333333333
        # More than 2 unordered wi with 1 WindBlock:
        # 3 PCI with [30, 45[, [20, 30[ and [70, ...[ wi
        # => only min = [20, 30[ and max [70, ...[ wi are kept
        # case: case 3_1B_>2_1
        generate_valid_times(periods=24),
        [30.0] * 2 + [20.0] * 20 + [70.0] * 2,
        [360.0] * 24,
    ),
    (
        # Input Fingerprint: 333333333322223333333333
        # More than 2 unordered wi with 2 WindBlocks
        # - B1: 1 PCI with [30, 45[ and [70, ...[ wi
        # - B2: 2 PCI with[20, 30[ wi
        # - same wind direction for the 2 blocks => 1 PCD
        # => only min = [20, 30[ and max [70, ...[ wi are kept
        # case: case 3_2B_>2_2_1_1
        generate_valid_times(periods=24),
        [30.0] * 2 + [70.0] * 2 + [np.nan] * 4 + [20.0] * 16,
        [360.0] * 4 + [np.nan] * 4 + [90.0] * 16,
    ),
    (
        # Input Fingerprint: 333333333333333333333333
        # 1 PCI
        # 2 opposite directions => no PCD
        # case: 3_1B_1_0
        generate_valid_times(periods=12),
        [40.0] * 12,
        [360.0] * 6 + [180.0] * 6,
    ),
    (
        # Input Fingerprint: 333333333333333333333333
        # 2 PCI
        # 2 opposite directions => no PCD
        # case: 3_1B_2_0
        generate_valid_times(periods=12),
        [30.0] * 9 + [45.0] * 3,
        [360.0] * 6 + [180.0] * 6,
    ),
    (
        # Input Fingerprint: 333333333333333333333333
        # 3 unordered PCI
        # 2 opposite directions => no PCD
        # case: 3_1B_>2_0
        generate_valid_times(periods=24),
        [30.0] * 2 + [20.0] * 20 + [70.0] * 2,
        [360.0] * 12 + [180.0] * 12,
    ),
    (
        # Input Fingerprint: 333333333333333333333333
        # 1 PCI
        # The 1st and last directions are opposite => no PCD
        # case: 3_1B_1_0
        generate_valid_times(periods=12),
        [30.0] * 12,
        [360.0] * 4 + [90.0] * 4 + [180.0] * 4,
    ),
    (
        # Input Fingerprint: 333333333333333333333333
        # 2 PCI
        # 2 opposite directions => no PCD
        # case: 3_1B_2_0
        generate_valid_times(periods=12),
        [30.0] * 9 + [45.0] * 3,
        [360.0] * 4 + [90.0] * 4 + [180.0] * 4,
    ),
    (
        # Input Fingerprint: 333333333333333333333333
        # 3 unordered PCI
        # 2 opposite directions => no PCD
        # case: 3_1B_>2_0
        generate_valid_times(periods=24),
        [30.0] * 2 + [20.0] * 20 + [70.0] * 2,
        [360.0] * 8 + [90.0] * 8 + [180.0] * 8,
    ),
    (
        # Input Fingerprint: 333333333322223333333333
        # 1 PCI
        # 2 opposite directions => no PCD
        # case: case 3_2B_1_0_0_0
        generate_valid_times(periods=24),
        [30.0] * 10 + [np.nan] * 4 + [30.0] * 10,
        [360.0] * 10 + [np.nan] * 4 + [180.0] * 10,
    ),
    (
        # Input Fingerprint: 333333333322223333333333
        # 2 PCI
        # 2 opposite directions => no PCD
        # case: case 3_2B_2_0_0_0
        generate_valid_times(periods=24),
        [40.0] * 10 + [np.nan] * 4 + [60.0] * 10,
        [360.0] * 10 + [np.nan] * 4 + [180.0] * 10,
    ),
    (
        # Input Fingerprint: 333333333322223333333333
        # 3 unordered PCI
        # 2 opposite directions => no PCD
        # case: case 3_2B_>2_0_0_0
        generate_valid_times(periods=24),
        [50.0] * 1 + [25.0] * 15 + [np.nan] * 4 + [30.0] * 4,
        [360.0] * 16 + [np.nan] * 4 + [180.0] * 4,
    ),
    (
        # Input Fingerprint: 333333333322223333333333
        # 1 PCI
        # 2 dir periods: the 1st and last directions are equals
        # => 1 PCD
        # case: case 3_2B_1_1_1_1
        generate_valid_times(periods=24),
        [30.0] * 10 + [np.nan] * 4 + [35.0] * 10,
        [360.0] * 10 + [np.nan] * 4 + [360.0] * 10,
    ),
    (
        # Input Fingerprint: 333333333322223333333333
        # 2 PCI
        # 2 dir periods: the 1st and last directions are equals
        # => 1 PCD
        # case: case 3_2B_2_1_1_1
        generate_valid_times(periods=24),
        [40.0] * 10 + [np.nan] * 4 + [45.0] * 10,
        [360.0] * 10 + [np.nan] * 4 + [360.0] * 10,
    ),
    (
        # Input Fingerprint: 333333333322223333333333
        # 3 unordered PCI
        # 2 dir periods: the 1st and last directions are equals
        # => 1 PCD
        # case: case 3_2B_>2_1_1_1
        generate_valid_times(periods=24),
        [44.0] * 9 + [70.0] * 1 + [np.nan] * 4 + [45.0] * 10,
        [360.0] * 10 + [np.nan] * 4 + [360.0] * 10,
    ),
    (
        # Input Fingerprint: 333333333322223333333333
        # 2 PCI
        # 3 dir periods: the 1st and last directions are equals
        # => no PCD
        # case: case 3_2B_2_1_1_1
        generate_valid_times(periods=24),
        [40.0] * 10 + [np.nan] * 4 + [45.0] * 10,
        [360.0] * 5 + [90.0] * 5 + [np.nan] * 4 + [360.0] * 10,
    ),
    (
        # Input Fingerprint: 333333333322223333333333
        # 3 unordered PCI
        # 3 dir periods: the 1st and last directions are equals
        # => no PCD
        # case: case 3_2B_>2_1_1_1
        generate_valid_times(periods=24),
        [40.0] * 9 + [70.0] * 1 + [np.nan] * 4 + [45.0] * 10,
        [360.0] * 5 + [90.0] * 5 + [np.nan] * 4 + [360.0] * 10,
    ),
    (
        # Input Fingerprint: 222233333333333333333333
        # 1 PCI
        # The period starting from the 1st long enough PCD and finishing by the last
        # long enough PCD is 45 % of the monitoring period
        # => < 50 % => no PCD
        # case: case 3_1B_1_0
        generate_valid_times(periods=24),
        [15.0] * 4 + [40.0] * 20,
        [np.nan] * 8 + [90.0] * 4 + [np.nan] + [180.0] * 4 + [np.nan] * 7,
    ),
    (
        # Input Fingerprint: 222233333333333333333333
        # 1 PCI
        # The period starting from the 1st long enough PCD and finishing by the last
        # long enough PCD is 50 % of the block period
        # => 2 PCD
        # case: case 3_1B_1_2
        generate_valid_times(periods=24),
        [15.0] * 4 + [40.0] * 20,
        [np.nan] * 8 + [90.0] * 4 + [np.nan] * 2 + [180.0] * 4 + [np.nan] * 6,
    ),
    (
        # Input Fingerprint: 222233333333333322223333
        # 2 WindBlocks
        # In the 1st block: the PCD is 41.6 % of the block period
        # => no PCD for the 1st block
        # 1 PCD fot the 2nd block
        # case: case 3_2B_2_1_0_1
        generate_valid_times(periods=24),
        [15.0] * 4 + [44.0] * 12 + [15.0] * 4 + [80.0] * 4,
        [np.nan] * 4 + [np.nan] + [180.0] * 5 + [np.nan] * 6 + [45.0] * 8,
    ),
    (
        # Input Fingerprint: 222233333333333322223333
        # 2 WindBlocks
        # In the 1st block: the period starting from the 1st long enough PCD and
        # finishing by the last long enough PCD is 50 % of the block period
        # => 2 PCD for the 1st block
        # 1 PCD fot the 2nd block
        # case: case 3_2B_2_3_2_1
        generate_valid_times(periods=24),
        [15.0] * 4 + [40.0] * 12 + [15.0] * 4 + [80.0] * 4,
        [np.nan] * 4 + [180.0] * 3 + [90.0] * 3 + [np.nan] * 6 + [45.0] * 8,
    ),
    (
        # Input Fingerprint: 333333333322223333333333
        # - B1: 1 PCI with [30, 50[ intensity, 1 PCD with (90, 80) angle
        # - B2: 1 PCI with [65, 75[ intensity, 1 PCD with (320, 80) angle
        # - 2 PCI with [30, 50[ and [65, 75[ intensities
        # - 2 PCD with (50, 80) and (320, 80) angles
        # PCI and PCD change at the same time
        # case: 3_2B_2_2_1_1_simultaneous_change
        generate_valid_times(periods=24),
        [20.0] * 10 + [15.0] * 4 + [45.0] * 10,
        [90.0] * 10 + [np.nan] * 4 + [360.0] * 10,
    ),
    (
        # Input Fingerprint: 333333333322223333333333
        # - B1: 1 PCI with [30, 50[ intensity, 1 PCD with (90, 80) angle
        # - B2: 1 PCI with [65, 75[ intensity, 1 PCD with (320, 80) angle
        # - 2 PCI with [30, 50[ and [65, 75[ intensities
        # - 2 PCD with (50, 80) and (320, 80) angles
        # PCI and PCD don't change at the same time
        # case: 3_2B_2_2_1_1
        generate_valid_times(periods=24),
        [20.0] * 10 + [15.0] * 4 + [50.0] * 10,
        [90.0] * 10 + [np.nan] * 8 + [360.0] * 6,
    ),
]


class TestGenerateSummaryCase3:
    @staticmethod
    def _create_summary_builder_from_composite(composite) -> WindSummaryBuilder:
        """Create a WindSummaryBuilder from a composite."""
        dataset = composite.compute()
        summary_builder: WindSummaryBuilder = WindSummaryBuilder(composite, dataset)
        return summary_builder

    def _run_case3_summary_builder_from_composite(
        self, composite
    ) -> Case3SummaryBuilder:
        """Run Case3SummaryBuilder from the dataset of a summary builder."""
        reference_datetime: Datetime = Datetime(datetime.now())
        summary_builder: WindSummaryBuilder
        summary_builder = self._create_summary_builder_from_composite(composite)
        case3_summary_builder: Case3SummaryBuilder = Case3SummaryBuilder(
            summary_builder.dataset
        )
        case3_summary_builder.run(reference_datetime)
        return case3_summary_builder

    def build_wind_blocks(self, composite):
        """Build WindBlocks from composite."""
        case3_summary_builder: Case3SummaryBuilder
        case3_summary_builder = self._run_case3_summary_builder_from_composite(
            composite
        )
        block_summary_builder: BlockSummaryBuilder
        block_summary_builder = case3_summary_builder.block_summary_builder

        expected: dict = {
            "wind_blocks": [
                str(b) for b in case3_summary_builder.blocks_builder.blocks
            ],
            "pci": [str(p) for p in block_summary_builder.pci],
            "pcd": [str(p) for p in block_summary_builder.pcd],
            "counters": case3_summary_builder.block_summary_builder.counters,
            "case": case3_summary_builder.summary["case"],
        }

        if isinstance(block_summary_builder, TwoBlocksSummaryBuilder):
            expected.update(
                {
                    "pcd_g0": [str(p) for p in block_summary_builder.pcd_g0],
                    "pcd_g1": [str(p) for p in block_summary_builder.pcd_g1],
                }
            )

        return expected

    def test_pci_sorted_key(self, assert_equals_result):
        pci: list[Pci] = [
            Pci(
                Datetime(2023, 2, 2, 3, 0, 0),
                Datetime(2023, 2, 2, 6, 0, 0),
                WindIntensity(70),
            ),
            Pci(
                Datetime(2023, 2, 2, 9, 0, 0),
                Datetime(2023, 2, 2, 12, 0, 0),
                WindIntensity(30),
            ),
            Pci(
                Datetime(2023, 2, 2, 6, 0, 0),
                Datetime(2023, 2, 2, 9, 0, 0),
                WindIntensity(20),
            ),
            Pci(
                Datetime(2023, 2, 2, 3, 0, 0),
                Datetime(2023, 2, 2, 6, 0, 0),
                WindIntensity(30),
            ),
        ]

        pci.sort(key=BlockSummaryBuilder.pci_sorted_key)

        assert_equals_result([str(p) for p in pci])

    @patch(
        "mfire.text.synthesis.wind_reducers.wind.WindSummaryBuilder."
        "WF_PERCENTILE_NUM",
        50,
    )
    @pytest.mark.parametrize("valid_times, data_wf, data_wd", TEST_CASE3_PARAMS)
    def test_block_builder_grid_1x1(
        self, valid_times, data_wf, data_wd, assert_equals_result
    ):
        """Test resulting WindBlocks built from 1x1 grid data."""
        composite = CompositeFactory1x1.get_composite_when_term_data_is_one_number(
            valid_times=valid_times, data_wind=data_wf, data_dir=data_wd
        )

        result: dict = {
            "input": {
                "valid_times": [str(v) for v in valid_times],
                "data_wf": data_wf,
                "data_wd": data_wd,
            }
        }

        result.update(self.build_wind_blocks(composite))

        assert_equals_result(result)

    @patch(
        "mfire.text.synthesis.wind_reducers.wind.WindSummaryBuilder."
        "WF_TYPE3_CONFIRMATION_PERCENT",
        5,
    )
    @pytest.mark.parametrize(
        "valid_times, data_wf, data_wd",
        [
            (
                # Input Fingerprint: 23
                # 3h step between terms
                # Q95 max for each term: 19.9 and 20.0
                # => Q95 max is 20 (and not 65). which is the wind force max but not the
                # Q95 max
                # Wind direction of each term: (320, 80) and (110, 80)
                # => 1 WindBlock containing the 2nd term
                generate_valid_times_v2("2023-01-02", (2, "3h")),
                [
                    [
                        [9.9, 19.9, 19.9, 19.9],
                        [19.9, 19.9, 19.9, 19.9],
                        [19.9, 19.9, 19.9, 19.9],
                        [19.9, 19.9, 19.9, 19.9],
                        [19.9, 19.9, 19.9, 19.9],
                        [19.9, 19.9, 19.9, 65.0],
                    ],
                    [
                        [19.9, 20.0, 20.0, 20.0],
                        [20.0, 20.0, 20.0, 20.0],
                        [20.0, 20.0, 20.0, 20.0],
                        [20.0, 20.0, 20.0, 20.0],
                        [20.0, 20.0, 20.0, 20.0],
                        [20.0, 20.0, 20.0, 21.0],
                    ],
                ],
                [np.full((6, 4), 0.1), np.full((6, 4), 150.0)],
            ),
            (
                # Input Fingerprint: 323
                # monitoring period: 8h
                # Q95 max for each term: 20.0, 11.0 and 36.85
                # => the Q95 max is 36.85 (and not 50. which are in the 2nd term)
                # => only the last term are kept
                # Wind direction of each term: (320, 80), (110, 80) and (110, 80)
                # => 1 WindBlock containing the 2nd type3-term
                generate_valid_times_v2("2023-01-02", (1, "2h"), (1, "3h"), (1, "4h")),
                [
                    [
                        [20.0, 20.0, 20.0, 20.0],
                        [20.0, 20.0, 20.0, 20.0],
                        [20.0, 20.0, 20.0, 20.0],
                        [20.0, 20.0, 20.0, 20.0],
                        [20.0, 20.0, 20.0, 20.0],
                        [20.0, 20.0, 20.0, 60.0],
                    ],  # Q95 = 20.0
                    [
                        [11.0, 11.0, 11.0, 11.0],
                        [11.0, 11.0, 11.0, 11.0],
                        [11.0, 11.0, 11.0, 11.0],
                        [11.0, 11.0, 11.0, 11.0],
                        [11.0, 11.0, 11.0, 11.0],
                        [11.0, 11.0, 11.0, 65.0],
                    ],  # Q95 = 11.0
                    [
                        [30.0, 30.0, 30.0, 30.0],
                        [30.0, 30.0, 30.0, 30.0],
                        [30.0, 30.0, 30.0, 30.0],
                        [30.0, 30.0, 30.0, 30.0],
                        [30.0, 30.0, 30.0, 30.0],
                        [35.0, 36.0, 37.0, 38.0],
                    ],  # Q95 = 36.85
                ],
                [np.full((6, 4), 0.1), np.full((6, 4), 150.0), np.full((6, 4), 150.0)],
            ),
            (
                # Input Fingerprint: 33 => Case 3
                # The 1st term has the type 3, but with a Q95 equal to 18.73 which
                # is < 20 => it is replaced by 20 when the WindIntensity is computed
                # in BlocksBuilder._compute_periods
                generate_valid_times_v2("2023-01-02", (2, "3h")),
                [
                    [
                        [20.1, 20.1, 11.0, 11.0],
                        [11.0, 11.0, 11.0, 11.0],
                        [11.0, 11.0, 11.0, 11.0],
                        [11.0, 11.0, 11.0, 11.0],
                        [11.0, 11.0, 11.0, 11.0],
                        [11.0, 11.0, 11.0, 11.0],
                    ],
                    [
                        [20.1, 20.1, 20.1, 20.1],
                        [0.1, 0.1, 0.1, 0.1],
                        [0.1, 0.1, 0.1, 0.1],
                        [0.1, 0.1, 0.1, 0.1],
                        [0.1, 0.1, 0.1, 0.1],
                        [0.1, 0.1, 0.1, 0.1],
                    ],
                ],
                [np.full((6, 4), 0.1), np.full((6, 4), 150.0)],
            ),
        ],
    )
    def test_block_builder_grid_6x2(
        self, valid_times, data_wf, data_wd, assert_equals_result
    ):
        """Test resulting WindBlocks built from 6x2 grid data."""
        composite = CompositeFactory6x4.get(
            valid_times=valid_times, data_wind=data_wf, data_dir=data_wd
        )

        result: dict = {
            "input": {
                "valid_times": [str(v) for v in valid_times],
                "data_wf": data_wf,
                "data_wd": data_wd,
            }
        }

        result.update(self.build_wind_blocks(composite))

        assert_equals_result(result)

    @pytest.mark.parametrize(
        "valid_times, data_wf",
        [
            (
                generate_valid_times("2023-01-02", 3),
                [
                    [
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 1.0, 1.0, 65.0],
                    ],
                    [
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 25.0, 30.0, 60.0],
                    ],  # Q95 of filtered data is 57.0
                    [
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 1.0, 1.0, 1.0],
                        [1.0, 25.0, 30.0, 32.0],
                    ],  # Q95 of filtered data is 31.8
                ],
            )
        ],
    )
    def test_block_builder_q95_max_6x4(self, valid_times, data_wf):
        """Test resulting WindBlocks built from 6x2 grid data."""
        composite = CompositeFactory6x4.get(valid_times=valid_times, data_wind=data_wf)

        case3_summary_builder = self._run_case3_summary_builder_from_composite(
            composite
        )

        # Test wind_q95 values
        dataset: xr.Dataset = case3_summary_builder.blocks_builder.dataset
        np.array_equal(
            dataset.wind_q95.values, np.array([np.nan, 57.0, 31.8]), equal_nan=True
        )

        # Test the value of the wind_q95_max's attribute
        assert dataset.attrs["wind_q95_max"] == 57.0

    @pytest.mark.parametrize(
        "valid_times, data_wf, data_wd",
        [
            (
                # Input Fingerprint: 111111222222222222222222 => no type 3 terms
                generate_valid_times(periods=24),
                [10.0] * 6 + [15.0] * 18,
                [np.nan] * 24,
            )
        ],
    )
    def test_summary_builder_error(self, valid_times, data_wf, data_wd):
        reference_datetime: Datetime = Datetime(datetime.now())
        composite = CompositeFactory1x1.get_composite_when_term_data_is_one_number(
            valid_times=valid_times, data_wind=data_wf, data_dir=data_wd
        )
        summary_builder = self._create_summary_builder_from_composite(composite)

        case3_summary_builder: Case3SummaryBuilder = Case3SummaryBuilder(
            summary_builder.dataset
        )

        with pytest.raises(WindSynthesisError):
            case3_summary_builder.run(reference_datetime)


class TestGenerateSummaryError(TestGenerateSummary):
    class CompositeFactory(CompositeFactory2x2):
        LON = [30, 31]
        LAT = [40, 41]

    def get_summary(self, wind_summary_builder_class) -> dict:
        valid_times = generate_valid_times(periods=1)

        composite = self.CompositeFactory().get(
            valid_times=valid_times, data_wind=np.full((2, 2), 10.0)
        )
        dataset = composite.compute()
        summary_builder = wind_summary_builder_class(composite, dataset)
        reference_datetime: Datetime = Datetime(datetime.now())
        summary = summary_builder.compute(reference_datetime)

        return summary

    def test_summary_with_error_case(self):
        for error in WindSummaryBuilder.CACHED_EXCEPTIONS:

            class BadWindSummaryBuilder(WindSummaryBuilder):
                def _generate_summary(self, reference_datetime: Datetime) -> None:
                    raise error

            summary = self.get_summary(BadWindSummaryBuilder)
            assert summary["wind"]["case"] == ERROR_CASE
            assert summary["wind"].get("msg") is not None
