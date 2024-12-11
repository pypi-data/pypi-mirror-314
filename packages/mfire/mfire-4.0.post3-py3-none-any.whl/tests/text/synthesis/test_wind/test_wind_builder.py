from __future__ import annotations

from abc import ABC, abstractmethod
from unittest.mock import patch

import numpy as np
import pytest

from mfire.text.synthesis.wind import WindBuilder, WindReducer
from mfire.text.synthesis.wind_reducers.mixins import BaseSummaryBuilderMixin
from tests.composite.factories import SynthesisCompositeFactory
from tests.text.utils import generate_valid_times

from .factories import CompositeFactory1x1, CompositeFactory5x2
from .test_gust_summary_builder import COMPLEX_CASES_PARAMS as GUST_COMPLEX_CASES_PARAMS
from .test_wind_summary_builder import TEST_CASE3_PARAMS

ERROR_CASE: str = BaseSummaryBuilderMixin.ERROR_CASE


class BaseTestBuilderForOneParam(ABC):
    """BaseTestBuilderForOneParam class."""

    TESTED_PARAM: str = ""

    @staticmethod
    @abstractmethod
    def _process_data(data_gust, data_wf, data_wd):
        pass

    @abstractmethod
    def _build_composite(self, valid_times, data_gust, data_wf, data_wd):
        pass

    def _check(self, valid_times, data_gust, data_wf, data_wd, assert_equals_result):
        """Check WindBuilder process by testing param data, produced summary and text.

        Param can be the wind or the gust.
        """
        # Get or set data
        data_gust, data_wf, data_wd = self._process_data(data_gust, data_wf, data_wd)

        # Create composite
        composite = self._build_composite(valid_times, data_gust, data_wf, data_wd)

        # Create WindBuilder
        builder: WindBuilder = WindBuilder(geo_id="", composite=composite)

        # Compute
        text: str = builder.compute()

        # Check WindCaseNbr
        param_summary = builder.reducer.reduction[self.TESTED_PARAM]
        case_value: str = param_summary["case"]

        result: dict = {
            "input": {
                "valid_times": [str(v) for v in valid_times],
                "data_gust": data_gust,
                "data_wf": data_wf,
                "data_wd": data_wd,
            },
            "case": case_value,
            "text": text,
        }

        # Check text
        assert_equals_result(result)


class TestBuilderGust(BaseTestBuilderForOneParam):
    """TestBuilderGust class."""

    TESTED_PARAM = "gust"

    def _build_composite(self, valid_times, data_gust, data_wf, data_wd):
        # Create composite
        composite = CompositeFactory5x2.get(
            valid_times=valid_times,
            data_wind=data_wf,
            data_dir=data_wd,
            data_gust=data_gust,
        )

        return composite

    @staticmethod
    def _process_data(data_gust, data_wf, data_wd):
        if data_gust is None:
            data_wf = np.array(data_wf)
            data_gust = np.full_like(data_wf, 0.0)
        elif data_wf is None and data_wd is None:
            data_gust = np.array(data_gust)
            data_wf = np.full_like(data_gust, 0.0)
        else:
            raise ValueError("data_gust or data_wf has parameter to be set !")

        if data_wf is not None and data_wd is None:
            data_wd = np.full_like(data_wf, np.nan)

        return data_gust, data_wf, data_wd

    @pytest.mark.parametrize(
        "valid_times, data_gust",
        [
            # No gust => case 0
            (
                generate_valid_times(periods=4),
                [[[0.0, 0.0]] * 5] * 2 + [[[np.nan, np.nan]] * 5] + [[[0.0, 0.0]] * 5],
            ),
            # All gust <= 50 km/h => case 0
            (
                generate_valid_times(periods=4),
                [[[40.0, 40.0]] * 5] * 2 + [[[50.0, 50.0]] * 5] * 2,
            ),
        ]
        + GUST_COMPLEX_CASES_PARAMS,
    )
    def test(self, valid_times, data_gust, assert_equals_result):
        """Test function which calls _check method.

        We reuse parameters from test_gust_summary_builder.GUST_COMPLEX_CASES_PARAMS.
        """
        self._check(valid_times, data_gust, None, None, assert_equals_result)


class TestBuilderWind(BaseTestBuilderForOneParam):
    """TestBuilderWind class."""

    TESTED_PARAM = "wind"

    @staticmethod
    def _process_data(data_gust, data_wf, data_wd):
        if data_gust is None:
            data_gust = [0.0] * len(data_wf)
        elif data_wf is None and data_wd is None:
            data_wf = [0.0] * len(data_gust)
        else:
            raise ValueError("data_gust or data_wf has parameter to be set !")

        if data_wf is not None and data_wd is None:
            data_wd = [np.nan] * len(data_wf)

        return data_gust, data_wf, data_wd

    def _build_composite(self, valid_times, data_gust, data_wf, data_wd):
        # Create composite
        composite = CompositeFactory1x1.get_composite_when_term_data_is_one_number(
            valid_times=valid_times,
            data_wind=data_wf,
            data_dir=data_wd,
            data_gust=data_gust,
        )

        return composite


class TestBuilderWindCase1(TestBuilderWind):
    """Test WindBuilder with wind data for case 1."""

    @pytest.mark.parametrize(
        "valid_times, data_wf, data_wd",
        [
            (
                # type 1 terms (Case 1)
                generate_valid_times(periods=3),
                [5.0, 8.0, 9.9],
                [0.1, 1.0, 2.0],
            )
        ],
    )
    def test(self, valid_times, data_wf, data_wd, assert_equals_result):
        """Test function which calls _check method."""
        self._check(valid_times, None, data_wf, data_wd, assert_equals_result)


class TestBuilderWindCase2(TestBuilderWind):
    """Test WindBuilder with wind data for case 2."""

    @pytest.mark.parametrize(
        "valid_times, data_wf",
        [
            (
                # Only type 2 terms:
                generate_valid_times(periods=3),
                [10.0, 15.0, 19.9],
            ),
            (
                # Type 1 and type 2 terms are present:
                generate_valid_times(periods=3),
                [1.0, 16.0, 19.9],
            ),
        ],
    )
    def test(self, valid_times, data_wf, assert_equals_result):
        """Test function which calls _check method."""
        self._check(valid_times, None, data_wf, None, assert_equals_result)


class TestBuilderWindCase3OneBlock(TestBuilderWind):
    """Test WindBuilder with wind data for case 3 with one block."""

    @patch(
        "mfire.text.synthesis.wind_reducers.wind.WindSummaryBuilder."
        "WF_PERCENTILE_NUM",
        50,
    )
    @pytest.mark.parametrize(
        "valid_times, data_wf, data_wd",
        [
            (
                # Case 3_1B_1_1
                # - 1 PCI with [20, 30[ intensity
                # - 1 PCD with (320, 80) angle
                generate_valid_times(periods=12),
                [20.0] * 11 + [29.9],
                [360.0] * 12,
            ),
            (
                # Case 3_1B_1_2
                # - 1 PCI with [30, 45[ intensity
                # - 2 PCD with (320, 80) and (0, 80) angles
                generate_valid_times(periods=12),
                [30.0] * 11 + [44.9],
                [360.0] * 4 + [90.0] * 4 + [40.0] * 4,
            ),
            (
                # Case 3_1B_1_0
                # - 1 PCI with [45, 70[ intensity
                # - 0 PCD
                generate_valid_times(periods=12),
                [69.0] * 12,
                [np.nan] * 12,
            ),
            (
                # Case 3_1B_2_1
                # - 2 PCI with [20, 30[ and [30, 45[ intensities
                # - 1 PCD with (140, 80) angles
                generate_valid_times(periods=12),
                [25.0] * 4 + [1.0] * 4 + [30.0] * 4,
                [180.0] * 12,
            ),
            (
                # Case 3_1B_2_2
                # - 2 PCI with [20, 30[ and [30, 45[ intensities
                # - 2 PCD with (50, 80) and (140, 80) angles
                generate_valid_times(periods=12),
                [25.0] * 4 + [30.0] * 8,
                [90.0] * 6 + [180.0] * 6,
            ),
            (
                # Case 3_1B_2_2_simultaneous_change
                # - 2 PCI with [20, 30[ and [30, 45[ intensities
                # - 2 PCD with (50, 80) and (140, 80) angles
                generate_valid_times(periods=12),
                [25.0] * 4 + [30.0] * 8,
                [90.0] * 4 + [180.0] * 8,
            ),
            (
                # Case 3_1B_2_0
                # - 2 PCI with [20, 30[ and [30, 45[ intensities
                # - 0 PCD
                generate_valid_times(periods=12),
                [25.0] * 4 + [30.0] * 8,
                [np.nan] * 12,
            ),
            (
                # Case 3_1B_>2_1
                # - 4 PCI: [20, 30[, [30, 45[, [20, 30[ and [45, 70[
                # intensities ==> [20, 30[ wi min to [45, 70[ wi max in PCI
                # - 1 PCD with (230, 80) angle
                generate_valid_times(periods=12),
                [28.0] * 5 + [30.0] + [28.0] * 5 + [45.0],
                [270.0] * 12,
            ),
            (
                # Case 3_1B_>2_2
                # - 4 PCI: [30, 45[, [45, 70[, [30, 45[ and [70, ...[
                # intensities ==> [30, 45[ wi min to [70, ...[ wi max in PCI
                # - 2 PCD with (230, 80) and (320, 80) angles
                generate_valid_times(periods=12),
                [30] * 5 + [45.0] + [30.0] * 5 + [70.0],
                [270.0] * 4 + [np.nan] * 4 + [360.0] * 4,
            ),
            (
                # Case 3_1B_>2_0
                # - 4 PCI: [30, 45[, [45, 70[, [30, 45[ and [70, ...[
                # intensities ==> [30, 45[ wi min to [70, ...[ wi max in PCI
                # - 0 PCD
                generate_valid_times(periods=12),
                [30] * 5 + [45.0] + [30.0] * 5 + [70.0],
                [np.nan] * 6 + [160] * 2 + [np.nan] * 4,
            ),
        ],
    )
    def test(self, valid_times, data_wf, data_wd, assert_equals_result):
        """Test when there is 1 WIndBlock."""
        self._check(valid_times, None, data_wf, data_wd, assert_equals_result)


class TestBuilderWindCase3TwoBlocks(TestBuilderWind):
    """Test WindBuilder with wind data for case 3 with two blocks."""

    @patch(
        "mfire.text.synthesis.wind_reducers.wind.WindSummaryBuilder."
        "WF_PERCENTILE_NUM",
        50,
    )
    @pytest.mark.parametrize(
        "valid_times, data_wf, data_wd",
        [
            (
                # Case 3_2B_1_1_1_1
                # - 1 PCI with [20, 30[ intensity
                # - 1 PCD with (320, 80) angle
                generate_valid_times(periods=24),
                [20.0] * 6 + [10.0] * 8 + [1.0] * 4 + [29.9] * 6,
                [360.0] * 24,
            ),
            (
                # Case 3_2B_1_2_1_1
                # - 1 PCI with [20, 30[ intensity
                # - 2 PCD with (320, 80) and (50, 80) angles
                generate_valid_times(periods=24),
                [20.0] * 6 + [10.0] * 8 + [1.0] * 4 + [29.9] * 6,
                [360.0] * 12 + [np.nan] * 2 + [90.0] * 10,
            ),
            (
                # Case 3_2B_1_1_1_0
                # - 1 PCI with [20, 30[ intensity
                # - 1 PCD with (320, 80) angle
                generate_valid_times(periods=24),
                [20.0] * 6 + [10.0] * 8 + [1.0] * 4 + [29.9] * 6,
                [360.0] * 12 + [np.nan] * 12,
            ),
            (
                # Case 3_2B_1_1_0_1
                # - 2 PCI with [45, 70[ and [70, ...[ intensities
                # - 1 PCD with (320, 80) angle
                generate_valid_times(periods=24),
                [70.0] * 6 + [10.0] * 8 + [1.0] * 4 + [71.0] * 6,
                [np.nan] * 12 + [180.0] * 12,
            ),
            (
                # Case 3_2B_1_3_2_1
                # - B1: 1 PCI with [70, ...[ intensity, 2 PCD with (320, 80), (50, 80)
                # - B2: 1 PCI with [70, ...[ intensity, 1 PCD with (95, 80)
                # - 1 PCI with [70, ...[ intensity
                # - 3 PCD with (320, 80), (50, 80) and (95, 80) angles
                generate_valid_times(periods=24),
                [70.0] * 9 + [10.0] * 6 + [90.0] * 9,
                [360.0] * 4 + [90.0] * 11 + [140.0] * 9,
            ),
            (
                # Case 3_2B_1_2_2_0
                # - B1: 1 PCI with [70, ...[ intensity, 2 PCD with (320, 80), (50, 80)
                # - B2: 1 PCI with [70, ...[ intensity, 0 PCD
                # - 1 PCI with [70, ...[ intensity
                # - 2 PCD with (320, 80) and (50, 80) angles
                generate_valid_times(periods=24),
                [70.0] * 9 + [10.0] * 6 + [90.0] * 9,
                [360.0] * 4 + [90.0] * 5 + [np.nan] * 15,
            ),
            (
                # Case 3_2B_1_3_1_2
                # - B1: 1 PCI with [30, 45[ intensity, 1 PCD with (320, 65)
                # - B2: 1 PCI with [30, 45[ intensity, 2 PCD with (95, 80) and (50, 80)
                # - 1 PCI with [30, 45[ intensity
                # - 3 PCD with (320, 80), (50, 80) and (100, 80) angles
                generate_valid_times(periods=24),
                [30.0] * 9 + [10.0] * 6 + [44.0] * 9,
                [360.0] * 9 + [np.nan] * 6 + [90.0] * 4 + [140.0] * 5,
            ),
            (
                # Case 3_2B_1_2_0_2
                # - B1: 1 PCI with [70, ...[ intensity, 0 PCD
                # - B2: 1 PCI with [70, ...[ intensity, 2 PCD with (320, 80), (50, 80)
                # - 1 PCI with [70, ...[ intensity
                # - 2 PCD with (320, 80) and (50, 80) angles
                generate_valid_times(periods=24),
                [90.0] * 9 + [10.0] * 6 + [70.0] * 9,
                [np.nan] * 15 + [360.0] * 4 + [90.0] * 5,
            ),
            (
                # Case 3_2B_1_0_0_0
                # - B1: 1 PCI with [20, 30[ intensity, 0 PCD
                # - B2: 1 PCI with [20, 30[ intensity, 0 PCD
                # - 1 PCI with [20, 30[ intensity
                # - 0 PCD
                generate_valid_times(periods=24),
                [25.0] * 9 + [10.0] * 6 + [25.0] * 9,
                [np.nan] * 24,
            ),
            (
                # Case 3_2B_2_1_1_1
                # - B1: 1 PCI with [20, 30[ intensity, 1 PCD with (320, 80) angle
                # - B2: 1 PCI with [45, 70[ intensity, 1 PCD with (320, 80) angle
                # - 2 PCI with [20, 30[ and [45, 70[ intensities
                # - 1 PCD with (320, 80) angle
                generate_valid_times(periods=24),
                [20.0] * 6 + [10.0] * 8 + [1.0] * 4 + [45.0] * 6,
                [360.0] * 24,
            ),
            (
                # Case 3_2B_2_1_1_0
                # - B1: 1 PCI with [20, 30[ intensity, 1 PCD with (90, 80) angle
                # - B2: 1 PCI with [45, 70[ intensity, 0 PCD
                # - 2 PCI with [20, 30[ and [45, 70[ intensities
                # - 1 PCD with (90, 80) angle
                generate_valid_times(periods=24),
                [20.0] * 10 + [10.0] * 4 + [45.0] * 10,
                [90.0] * 10 + [np.nan] * 14,
            ),
            (
                # Case 3_2B_2_1_0_1
                # - B1: 1 PCI with [20, 30[ intensity, 0 PCD
                # - B2: 1 PCI with [45, 70[ intensity, 1 PCD with (90, 80) angle
                # - 2 PCI with [20, 30[ and [45, 70[ intensities
                # - 1 PCD with (90, 80) angle
                generate_valid_times(periods=24),
                [20.0] * 10 + [10.0] * 4 + [45.0] * 10,
                [np.nan] * 14 + [90.0] * 10,
            ),
            (
                # Case 3_2B_2_3_2_1
                # - B1: 1 PCI with [20, 30[ intensity, 2 PCD with (320, 80), (50, 80)
                # - B2: 1 PCI with [45, 70[ intensity, 1 PCD with (95, 80)
                # - 2 PCI with [20, 30[ and [45, 70[ intensities
                # - 3 PCD with (320, 80), (50, 80) and (95, 80) angles
                generate_valid_times(periods=24),
                [20.0] * 10 + [10.0] * 4 + [45.0] * 10,
                [360.0] * 4 + [90.0] * 6 + [np.nan] * 4 + [140.0] * 10,
            ),
            (
                # Case 3_2B_2_2_2_0
                # - B1: 1 PCI with [20, 30[ intensity, 2 PCD with (320, 80), (50, 80)
                # - B2: 1 PCI with [70, ...[ intensity, 0 PCD
                # - 2 PCI with [20, 30[ and [70, ...[ intensities
                # - 2 PCD with (320, 80) and (50, 80) angles
                generate_valid_times(periods=24),
                [20.0] * 10 + [10.0] * 4 + [70.0] * 10,
                [360.0] * 6 + [90.0] * 4 + [np.nan] * 14,
            ),
            (
                # Case 3_2B_2_3_1_2
                # - B1: 1 PCI with [20, 30[ intensity, 1 PCD with (320, 65)
                # - B2: 1 PCI with [70, ...[ intensity, 2 PCD with (95, 80) and (50, 80)
                # - 2 PCI with [20, 30[ and [70, ...[ intensities
                # - 3 PCD with (320, 80), (50, 80) and (100, 80) angles
                generate_valid_times(periods=24),
                [20.0] * 10 + [10.0] * 4 + [70.0] * 10,
                [360.0] * 10 + [np.nan] * 4 + [90.0] * 4 + [140.0] * 6,
            ),
            (
                # Case 3_2B_2_2_0_2
                # - B1: 1 PCI with [20, 30[ intensity, 0 PCD
                # - B2: 1 PCI with [70, ...[ intensity, 2 PCD with (320, 80), (50, 80)
                # - 2 PCI with [20, 30[ and [70, ...[ intensities
                # - 2 PCD with (320, 80) and (50, 80) angles
                generate_valid_times(periods=24),
                [20.0] * 10 + [10.0] * 4 + [70.0] * 10,
                [np.nan] * 14 + [360.0] * 4 + [90.0] * 6,
            ),
            (
                # Case 3_2B_2_0_0_0
                # - B1: 1 PCI with [70, ...[ intensity, 0 PCD
                # - B2: 1 PCI with [45, 70[ intensity, 0 PCD
                # - 2 PCI with [70, ...[ and [45, 70[ intensities
                # - 0 PCD
                generate_valid_times(periods=24),
                [90.0] * 10 + [10.0] * 4 + [69.0] * 10,
                [np.nan] * 24,
            ),
            (
                # Case 3_2B_>2_1_1_1
                # - B1: 2 PCI with [20, 30[ and [30, 45[ intensities, 1 PCD (320, 80)
                # - B2: 2 PCI with [20, 30[ and [45, 70[ intensities, 1 PCD (320, 80)
                # - 2 PCI min et max: [20, 30[ and [45, 70[
                # - 1 PCD with (320, 80) angle
                generate_valid_times(periods=24),
                [20.0] * 6 + [30.0] * 4 + [10.0] * 4 + [21.0] * 4 + [60.0] * 6,
                [360.0] * 24,
            ),
            (
                # Case 3_2B_>2_2_1_1
                # - B1: 2 PCI with [20, 30[ and [30, 45[ intensities, 1 PCD (320, 80)
                # - B2: 2 PCI with [20, 30[ and [45, 70[ intensities, 1 PCD (50, 80)
                # - 2 PCI min et max: [20, 30[ and [45, 70[
                # - 1 PCD with (320, 80) and (50, 80) angles
                generate_valid_times(periods=24),
                [20.0] * 6 + [30.0] * 4 + [10.0] * 4 + [21.0] * 4 + [60.0] * 6,
                [360.0] * 12 + [90.0] * 12,
            ),
            (
                # Case 3_2B_>2_1_1_0
                # - B1: 2 PCI with [20, 30[ and [30, 45[ intensities, 1 PCD (320, 80)
                # - B2: 2 PCI with [20, 30[ and [45, 70[ intensities, 0 PCD
                # - 2 PCI min et max: [20, 30[ and [45, 70[
                # - 1 PCD with (320, 80) angle
                generate_valid_times(periods=24),
                [20.0] * 6 + [30.0] * 4 + [10.0] * 4 + [21.0] * 4 + [60.0] * 6,
                [360.0] * 10 + [np.nan] * 14,
            ),
            (
                # Case 3_2B_>2_1_0_1
                # - B1: 2 PCI with [20, 30[ and [30, 45[ intensities, 0 PCD
                # - B2: 2 PCI with [20, 30[ and [45, 70[ intensities, 1 PCD (230, 80)
                # - 2 PCI min et max: [20, 30[ and [45, 70[
                # - 1 PCD with (230, 80) angle
                generate_valid_times(periods=24),
                [20.0] * 6 + [30.0] * 4 + [10.0] * 4 + [21.0] * 4 + [60.0] * 6,
                [np.nan] * 14 + [230.0] * 10,
            ),
            (
                # Case 3_2B_>2_3_2_1
                # - B1: 2 PCI with [20, 30[ and [30, 45[ intensities, 2 PCD
                # - B2: 2 PCI with [20, 30[ and [45, 70[ intensities, 1 PCD
                # - 2 PCI min et max: [20, 30[ and [45, 70[
                # - 3 PCD with (320, 80), (230, 80) and (50, 80) angles
                generate_valid_times(periods=24),
                [20.0] * 6 + [30.0] * 4 + [10.0] * 4 + [21.0] * 4 + [60.0] * 6,
                [360.0] * 5 + [270.0] * 5 + [np.nan] * 4 + [90.0] * 10,
            ),
            (
                # Case 3_2B_>2_2_2_0
                # - B1: 2 PCI with [20, 30[ and [30, 45[ intensities, 2 PCD
                # - B2: 2 PCI with [20, 30[ and [45, 70[ intensities, 0 PCD
                # - 2 PCI min et max: [20, 30[ and [45, 70[
                # - 2 PCD with (320, 80), (230, 80) and (50, 80) angles
                generate_valid_times(periods=24),
                [20.0] * 6 + [30.0] * 4 + [10.0] * 4 + [21.0] * 4 + [60.0] * 6,
                [360.0] * 5 + [270.0] * 5 + [np.nan] * 14,
            ),
            (
                # Case 3_2B_>2_3_1_2
                # - B1: 2 PCI with [20, 30[ and [30, 45[ intensities, 1 PCD
                # - B2: 2 PCI with [20, 30[ and [45, 70[ intensities, 2 PCD
                # - 2 PCI min et max: [20, 30[ and [45, 70[
                # - 3 PCD with (320, 80), (50, 80) and (100, 80) angles
                generate_valid_times(periods=24),
                [20.0] * 6 + [30.0] * 4 + [10.0] * 4 + [21.0] * 4 + [60.0] * 6,
                [360.0] * 10 + [np.nan] * 4 + [90.0] * 3 + [140.0] * 7,
            ),
            (
                # Case 3_2B_>2_2_0_2
                # - B1: 2 PCI with [20, 30[ and [30, 45[ intensities, 0 PCD
                # - B2: 2 PCI with [20, 30[ and [45, 70[ intensities, 2 PCD
                # - 2 PCI min et max: [20, 30[ and [45, 70[
                # - 2 PCD with (50, 80) and (100, 80) angles
                generate_valid_times(periods=24),
                [20.0] * 6 + [30.0] * 4 + [10.0] * 4 + [21.0] * 4 + [60.0] * 6,
                [np.nan] * 14 + [90.0] * 3 + [140.0] * 7,
            ),
            (
                # Case 3_2B_>2_0_0_0
                # - B1: 2 PCI with [20, 30[ and [30, 45[ intensities, 0 PCD
                # - B2: 2 PCI with [20, 30[ and [45, 70[ intensities, 0 PCD
                # - 2 PCI min et max: [20, 30[ and [45, 70[
                # - 0 PCD
                generate_valid_times(periods=24),
                [20.0] * 6 + [30.0] * 4 + [10.0] * 4 + [21.0] * 4 + [60.0] * 6,
                [np.nan] * 24,
            ),
        ],
    )
    def test(self, valid_times, data_wf, data_wd, assert_equals_result):
        """Test when there are 2 WindBlocks."""
        self._check(valid_times, None, data_wf, data_wd, assert_equals_result)


class TestBuilderWindCase3Tricky(TestBuilderWind):
    """Test WindBuilder with wind data for case 3 on tricky situations.

    Tricky situations (1 or 2 WindBlocks) come from TEST_CASE3_PARAMS of
    test_wind_summary_builder.
    """

    @patch(
        "mfire.text.synthesis.wind_reducers.wind.WindSummaryBuilder."
        "WF_PERCENTILE_NUM",
        50,
    )
    @pytest.mark.parametrize("valid_times, data_wf, data_wd", TEST_CASE3_PARAMS)
    def test(self, valid_times, data_wf, data_wd, assert_equals_result):
        """Test when there is 1 WIndBlock."""
        self._check(valid_times, None, data_wf, data_wd, assert_equals_result)


class TestWindBuilder:
    """TestWindBuilder class."""

    COMPOSITE_FACTORY: CompositeFactory1x1 = CompositeFactory1x1

    def _check(self, valid_times, data_gust, data_wf, data_wd, assert_equals_result):
        """Check builder resulting text with both wind and gust input data."""

        # Create composite
        composite = self.COMPOSITE_FACTORY.get_composite_when_term_data_is_one_number(
            valid_times=valid_times,
            data_wind=data_wf,
            data_dir=data_wd,
            data_gust=data_gust,
        )

        # Create WindBuilder
        builder: WindBuilder = WindBuilder(geo_id="", composite=composite)

        # Check the generated text
        assert_equals_result(builder.compute())

    @pytest.mark.parametrize(
        "valid_times, data_gust, data_wf, data_wd",
        [
            (
                # No wind, no gust
                generate_valid_times(periods=12),
                [0.0] * 12,
                [0.0] * 12,
                [np.nan] * 12,
            ),
            (
                # Wind with type 1 and gust
                generate_valid_times(periods=12),
                [50.1] * 12,
                [9.0] * 12,
                [np.nan] * 12,
            ),
            (
                # Wind with type 2 and gust
                generate_valid_times(periods=12),
                [60.0] * 12,
                [12.0] * 12,
                [np.nan] * 12,
            ),
            (
                # Wind with type 1 and 2 and gust
                generate_valid_times(periods=12),
                [61.0] * 12,
                [5.0] * 6 + [13.0] * 6,
                [np.nan] * 12,
            ),
            (
                # Wind with type 3 and gust
                generate_valid_times(periods=12),
                [99.0] + [40.0] * 11,
                [5.0] * 6 + [70.0] * 6,
                [np.nan] * 12,
            ),
        ],
    )
    def test(self, valid_times, data_gust, data_wf, data_wd, assert_equals_result):
        """Test function which calls _check method."""
        self._check(valid_times, data_gust, data_wf, data_wd, assert_equals_result)


class TestWindBuilderFromParamSummary:
    @staticmethod
    def generate_text_from_reduction(reduction: dict) -> str:
        class Reducer(WindReducer):
            def _compute(self) -> dict:
                """Return reduction."""
                self.reduction = reduction
                return reduction

        class WindBuilderTest(WindBuilder):
            reducer_class: type = Reducer

        builder = WindBuilderTest(
            geo_id="", composite=SynthesisCompositeFactory(id="wind")
        )
        text: str = builder.compute()
        return text

    def check_builder_with_bad_reduction(self, reduction: dict):
        text: str = self.generate_text_from_reduction(reduction)
        assert text == (
            "Ce commentaire n'a pas pu être produit à cause d'un incident technique."
        )

    def check_builder(self, reduction: dict, assert_equals_result):
        assert_equals_result(self.generate_text_from_reduction(reduction))

    @pytest.mark.parametrize(
        "reduction",
        [
            # Unknown case for wind
            (
                {
                    "gust": {
                        "bound_inf": 80,
                        "bound_sup": 100,
                        "gust_max": 110,
                        "period": "lundi après-midi",
                        "case": "2",
                        "units": "km/h",
                    },
                    "wind": {"case": "unknown_case"},
                }
            ),
            # Error case for wind
            (
                {
                    "gust": {
                        "bound_inf": 80,
                        "bound_sup": 100,
                        "gust_max": 110,
                        "period": "lundi après-midi",
                        "case": "2",
                        "units": "km/h",
                    },
                    "wind": {"case": ERROR_CASE},
                }
            ),
            # Unknown selector for wind
            (
                {
                    "gust": {
                        "bound_inf": 80,
                        "bound_sup": 100,
                        "gust_max": 110,
                        "period": "lundi après-midi",
                        "case": "2",
                        "units": "km/h",
                    },
                    "wind": {"unknown_selector": "2"},
                }
            ),
            # Unknown case for gust
            (
                {
                    "gust": {"case": "unknown_case"},
                    "wind": {
                        "case": "2",
                        "units": "km/h",
                        "wi": "modéré",
                        "wd_periods": [],
                    },
                }
            ),
            # Error case for gust
            (
                {
                    "gust": {"case": ERROR_CASE},
                    "wind": {
                        "case": "2",
                        "units": "km/h",
                        "wi": "modéré",
                        "wd_periods": [],
                    },
                }
            ),
            # Unknown selector for gust
            (
                {
                    "gust": {"unknown_selector": "2"},
                    "wind": {
                        "case": "2",
                        "units": "km/h",
                        "wi": "modéré",
                        "wd_periods": [],
                    },
                }
            ),
            # Gust summary is missing
            (
                {
                    "wind": {
                        "case": "2",
                        "units": "km/h",
                        "wi": "modéré",
                        "wd_periods": [],
                    }
                }
            ),
            # Wind summary is missing
            (
                {
                    "gust": {
                        "bound_inf": 80,
                        "bound_sup": 100,
                        "gust_max": 110,
                        "period": "lundi après-midi",
                        "case": "2",
                        "units": "km/h",
                    }
                }
            ),
        ],
    )
    def test_wind_builder_with_bad_reduction(self, reduction):
        self.check_builder_with_bad_reduction(reduction)

    @pytest.mark.parametrize(
        "wind_summary",
        [{"case": "unknown_case"}, {"case": ERROR_CASE}, {"unknown_selector": "2"}],
    )
    def test_builder_with_bad_wind_summary(self, wind_summary):
        reduction = dict()
        reduction["gust"] = {"case": "0"}
        reduction["wind"] = wind_summary
        self.check_builder_with_bad_reduction(reduction)

    @pytest.mark.parametrize(
        "gust_summary",
        [{"case": "unknown_case"}, {"case": ERROR_CASE}, {"unknown_selector": "2"}],
    )
    def test_builder_with_bad_gust_summary(self, gust_summary):
        reduction = dict()
        reduction["wind"] = {"case": "1"}
        reduction["wind"] = gust_summary
        self.check_builder_with_bad_reduction(reduction)

    def test_wind_builder(self, assert_equals_result):
        reduction = {
            "gust": {
                "bound_inf": 80,
                "bound_sup": 100,
                "gust_max": 110,
                "period": "lundi après-midi",
                "case": "2",
                "units": "km/h",
            },
            "wind": {"case": "2", "units": "km/h", "wi": "modéré", "wd_periods": []},
        }

        self.check_builder(reduction, assert_equals_result)
