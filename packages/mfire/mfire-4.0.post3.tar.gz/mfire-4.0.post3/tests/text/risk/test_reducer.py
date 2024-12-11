import numpy as np
import pytest

import mfire.utils.mfxarray as xr
from mfire.composite.event import Threshold
from mfire.composite.operator import ComparisonOperator
from mfire.settings import Settings
from mfire.text.risk.reducer import (
    RiskReducerStrategyMonozone,
    RiskReducerStrategyMultizone,
    RiskReducerStrategySnow,
)
from mfire.utils.date import Datetime
from mfire.utils.string import _
from tests.composite.factories import (
    EventCompositeFactory,
    FieldCompositeFactory,
    LevelCompositeFactory,
    RiskComponentCompositeFactory,
)
from tests.functions_test import assert_identically_close
from tests.localisation.factories import (
    RiskLocalisationFactory,
    TableLocalisationFactory,
)
from tests.text.risk.factories import RiskReducerFactory


class TestRiskReducer:
    def test_strategy(self):
        pass

    def test_is_multizone(self):
        reducer = RiskReducerFactory(localisation=None)
        assert reducer.is_multizone is False

        reducer = RiskReducerFactory(
            localisation=RiskLocalisationFactory(is_multizone_factory=False)
        )
        assert reducer.is_multizone is False

        reducer = RiskReducerFactory(
            localisation=RiskLocalisationFactory(is_multizone_factory=True)
        )
        assert reducer.is_multizone is True

    @pytest.mark.parametrize("level_max", list(range(4)))
    def test_final_risk_max(self, level_max):
        all_levels = list(range(level_max + 1))
        risk_compo = RiskComponentCompositeFactory(
            final_risk_da_factory=xr.DataArray(
                [all_levels],
                coords={
                    "id": ["geo_id"],
                    "valid_time": [Datetime(2023, 1, 1, i) for i in all_levels],
                },
            )
        )
        reducer = RiskReducerFactory(composite=risk_compo)
        assert reducer.final_risk_max == level_max


class TestRiskReducerStrategySnow:
    def test_compute(self):
        # Test with final risk max level = 0
        strategy = RiskReducerStrategySnow(
            reducer=RiskReducerFactory(final_risk_max_factory=0)
        )
        assert strategy.compute() == {"key": "RAS"}

        # Test without density
        strategy = RiskReducerStrategySnow(
            reducer=RiskReducerFactory(
                final_risk_max_factory=1,
                composite=RiskComponentCompositeFactory(
                    params={
                        "WWMF__SOL": FieldCompositeFactory(
                            compute_factory=lambda: xr.DataArray(
                                [[[0, 0]]],
                                coords={
                                    "longitude": [30],
                                    "latitude": [40],
                                    "valid_time": [
                                        Datetime(2023, 3, 1),
                                        Datetime(2023, 3, 2),
                                    ],
                                },
                                dims=["longitude", "latitude", "valid_time"],
                            )
                        )
                    }
                ),
            )
        )
        assert strategy.compute() == {"key": "RAS"}

        # Test with low intensity and monozone
        strategy = RiskReducerStrategySnow(
            reducer=RiskReducerFactory(
                is_multizone_factory=False,
                final_risk_max_factory=1,
                first_time_factory=Datetime(2023, 3, 1),
                composite=RiskComponentCompositeFactory(
                    levels=[
                        LevelCompositeFactory(
                            level=1,
                            spatial_risk_da_factory=xr.DataArray(
                                [[[[True, True, True, True]]]],
                                coords={
                                    "id": ["geo_id"],
                                    "longitude": [30],
                                    "latitude": [40],
                                    "valid_time": [
                                        Datetime(2023, 3, 1, i) for i in range(4)
                                    ],
                                },
                            ),
                        )
                    ],
                    params={
                        "WWMF__SOL": FieldCompositeFactory(
                            compute_factory=lambda: xr.DataArray(
                                [[[0, 60, 60, 0]]],
                                coords={
                                    "longitude": [30],
                                    "latitude": [40],
                                    "valid_time": [
                                        Datetime(2023, 3, 1, i) for i in range(4)
                                    ],
                                },
                                dims=["longitude", "latitude", "valid_time"],
                            )
                        ),
                        "NEIPOT3__SOL": FieldCompositeFactory(
                            compute_factory=lambda: xr.DataArray(
                                [[[0, 10, 10, 0]]],
                                coords={
                                    "longitude": [30],
                                    "latitude": [40],
                                    "valid_time": [
                                        Datetime(2023, 3, 1, i) for i in range(4)
                                    ],
                                },
                                dims=["longitude", "latitude", "valid_time"],
                                attrs={"units": "mm"},
                            )
                        ),
                    },
                ),
            )
        )
        assert strategy.compute() == {
            "key": "low",
            "localisation": "N.A",
            "periods": "en début de période",
        }

        # Test with low intensity and multizone
        strategy = RiskReducerStrategySnow(
            reducer=RiskReducerFactory(
                is_multizone_factory=True,
                final_risk_max_factory=1,
                first_time_factory=Datetime(2023, 3, 1),
                composite=RiskComponentCompositeFactory(
                    levels=[
                        LevelCompositeFactory(
                            level=1,
                            spatial_risk_da_factory=xr.DataArray(
                                [[[[True, True, True, True]]]],
                                coords={
                                    "id": ["geo_id"],
                                    "longitude": [30],
                                    "latitude": [40],
                                    "valid_time": [
                                        Datetime(2023, 3, 1, i) for i in range(4)
                                    ],
                                },
                            ),
                        )
                    ],
                    params={
                        "WWMF__SOL": FieldCompositeFactory(
                            compute_factory=lambda: xr.DataArray(
                                [[[0, 60, 60, 0]]],
                                coords={
                                    "longitude": [30],
                                    "latitude": [40],
                                    "valid_time": [
                                        Datetime(2023, 3, 1, i) for i in range(4)
                                    ],
                                },
                                dims=["longitude", "latitude", "valid_time"],
                            )
                        ),
                        "NEIPOT3__SOL": FieldCompositeFactory(
                            compute_factory=lambda: xr.DataArray(
                                [[[0, 10, 10, 0]]],
                                coords={
                                    "longitude": [30],
                                    "latitude": [40],
                                    "valid_time": [
                                        Datetime(2023, 3, 1, i) for i in range(4)
                                    ],
                                },
                                dims=["longitude", "latitude", "valid_time"],
                                attrs={"units": "cm"},
                            )
                        ),
                    },
                ),
                localisation=RiskLocalisationFactory(all_name_factory="Lieu Multizone"),
            )
        )
        assert strategy.compute() == {
            "key": "high",
            "localisation": "Lieu Multizone",
            "periods": "en début de période",
        }

    def test_process_period(self):
        strategy = RiskReducerStrategySnow(reducer=RiskReducerFactory())
        strategy.process_period()
        assert strategy.reduction is None


class TestRiskReducerStrategyMonozone:
    @pytest.mark.parametrize(
        "final_risk,offset,expected",
        [
            # Test with correction for bloc of 3h and offset
            ([3, 2, 1, 1, 2, 1, 1, 1, 0], 0, [3, 3, 3, 2, 2, 2, 1, 1, 1]),
            ([3, 2, 1, 1, 2, 1, 1, 1, 0], 1, [3, 3, 3, 2, 2, 1, 1, 1, 1]),
            ([3, 2, 1, 1, 2, 1, 1, 1, 0], 2, [3, 3, 3, 2, 2, 2, 2, 2, 2]),
        ],
    )
    def test_final_risk_da(self, final_risk, offset, expected):
        valid_time = [
            Datetime(2023, 3, 1, i + offset).as_np_dt64 for i in range(len(final_risk))
        ]

        composite = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset(
                {"risk_level": range(max(final_risk) + 1)}, coords={"id": ["geo_id"]}
            ),
            final_risk_da_factory=xr.DataArray(
                [final_risk], coords={"id": ["geo_id"], "valid_time": valid_time}
            ),
        )
        strategy = RiskReducerStrategyMonozone(
            reducer=RiskReducerFactory(composite=composite)
        )
        assert_identically_close(
            strategy.final_risk_da,
            xr.DataArray(
                expected,
                coords={"id": "geo_id", "valid_time": valid_time},
                dims=["valid_time"],
            ),
        )

    @pytest.mark.parametrize(
        "final_risk,offset,expected",
        [
            # Test with max_level=2
            (
                [2, 2, 2, 1, 1, 1, 2, 2, 2],
                0,
                [1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0],
            ),
            # Test with max_level=1
            ([1] * 9, 0, [1] * 9),
            # Test with max_level=0
            ([0] * 9, 0, [0] * 9),
            # Test with correction for bloc of 3h and offset
            (
                [3, 2, 1, 1, 2, 1, 1, 1, 0],
                0,
                [1.0, 1.0, 1.0, 0.75, 0.75, 0.75, 0.5, 0.5, 0.5],
            ),
            (
                [3, 2, 1, 1, 2, 1, 1, 1, 0],
                1,
                [1.0, 1.0, 1.0, 0.75, 0.75, 0.5, 0.5, 0.5, 0.5],
            ),
            (
                [3, 2, 1, 1, 2, 1, 1, 1, 0],
                2,
                [1.0, 1.0, 1.0, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            ),
        ],
    )
    def test_norm_risk(self, final_risk, offset, expected):
        valid_time = [
            Datetime(2023, 3, 1, i + offset).as_np_dt64 for i in range(len(final_risk))
        ]

        composite = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset(
                {"risk_level": range(max(final_risk) + 1)}, coords={"id": ["geo_id"]}
            ),
            final_risk_da_factory=xr.DataArray(
                [final_risk], coords={"id": ["geo_id"], "valid_time": valid_time}
            ),
        )
        strategy = RiskReducerStrategyMonozone(
            reducer=RiskReducerFactory(composite=composite)
        )
        assert_identically_close(strategy.norm_risk, np.array(expected))

    def test_operator_dict(self):
        lvl1 = LevelCompositeFactory(
            events=[
                EventCompositeFactory(
                    field=FieldCompositeFactory(name="evt1"),
                    plain=Threshold(threshold=15, comparison_op=ComparisonOperator.SUP),
                ),
                EventCompositeFactory(
                    field=FieldCompositeFactory(name="evt2"),
                    plain=Threshold(threshold=15, comparison_op=ComparisonOperator.SUP),
                    mountain=Threshold(
                        threshold=15, comparison_op=ComparisonOperator.INF
                    ),
                ),
            ]
        )
        lvl2 = LevelCompositeFactory(
            events=[
                EventCompositeFactory(
                    field=FieldCompositeFactory(name="evt3"),
                    plain=Threshold(
                        threshold=15, comparison_op=ComparisonOperator.EGAL
                    ),
                )
            ]
        )
        composite = RiskComponentCompositeFactory(levels=[lvl1, lvl2])
        strategy = RiskReducerStrategyMonozone(
            reducer=RiskReducerFactory(composite=composite)
        )
        assert strategy.operator_dict == {
            "evt1": {"plain": ComparisonOperator.SUP},
            "evt2": {
                "plain": ComparisonOperator.SUP,
                "mountain": ComparisonOperator.INF,
            },
            "evt3": {"plain": ComparisonOperator.EGAL},
        }

    def test_process_value(self):
        lvl = LevelCompositeFactory(
            level=1,
            events=[
                EventCompositeFactory(
                    field=FieldCompositeFactory(name="evt"),
                    plain=Threshold(threshold=15, comparison_op=ComparisonOperator.SUP),
                    mountain=Threshold(
                        threshold=15, comparison_op=ComparisonOperator.INF
                    ),
                )
            ],
        )
        strategy = RiskReducerStrategyMonozone(
            reducer=RiskReducerFactory(
                composite=RiskComponentCompositeFactory(levels=[lvl])
            )
        )

        # Test without data
        evts_ds = [
            xr.Dataset(
                {
                    "risk_level": 1,
                    "units": ...,
                    "threshold_plain": ...,
                    "threshold_mountain": ...,
                }
            )
        ]
        assert strategy.process_value("evt", evts_ds=evts_ds, kind="plain") is None
        assert strategy.process_value("evt", evts_ds=evts_ds, kind="mountain") is None

        evts_ds = [
            xr.Dataset(
                {
                    "risk_level": 1,
                    "threshold_plain": 10.0,
                    "min_plain": 10.0,
                    "max_plain": 20.0,
                    "rep_value_plain": 15.0,
                    "threshold_mountain": 30.0,
                    "min_mountain": 30.0,
                    "max_mountain": 40.0,
                    "rep_value_mountain": 35.0,
                    "occurrence_plain": True,
                    "occurrence_mountain": False,
                },
                coords={"units": "cm"},
            ),
            xr.Dataset(
                {
                    "risk_level": 1,
                    "threshold_plain": 10.0,
                    "min_plain": 15.0,
                    "max_plain": 17.0,
                    "rep_value_plain": 16.0,
                    "threshold_mountain": 30.0,
                    "min_mountain": 35.0,
                    "max_mountain": 53.0,
                    "rep_value_mountain": 41.0,
                    "occurrence_plain": False,
                    "occurrence_mountain": True,
                },
                coords={"units": "cm"},
            ),
        ]
        assert strategy.process_value("evt", evts_ds=evts_ds, kind="plain") == {
            "threshold": 10.0,
            "min": 10.0,
            "max": 20.0,
            "value": 16.0,
            "units": "cm",
            "operator": ComparisonOperator.SUP,
            "occurrence": True,
        }
        assert strategy.process_value("evt", evts_ds=evts_ds, kind="mountain") == {
            "threshold": 30.0,
            "min": 30.0,
            "max": 53.0,
            "value": 35.0,
            "units": "cm",
            "operator": ComparisonOperator.INF,
            "occurrence": True,
        }

        # Test with only plain event
        lvl = LevelCompositeFactory(
            level=1,
            events=[
                EventCompositeFactory(
                    field=FieldCompositeFactory(name="evt"),
                    plain=Threshold(threshold=15, comparison_op=ComparisonOperator.SUP),
                )
            ],
        )
        strategy = RiskReducerStrategyMonozone(
            reducer=RiskReducerFactory(
                composite=RiskComponentCompositeFactory(levels=[lvl])
            )
        )
        assert strategy.process_value("evt", evts_ds=evts_ds, kind="plain") == {
            "threshold": 10.0,
            "min": 10.0,
            "max": 20.0,
            "value": 16.0,
            "units": "cm",
            "operator": ComparisonOperator.SUP,
            "occurrence": True,
        }
        assert strategy.process_value("evt", evts_ds=evts_ds, kind="mountain") is None

        # Test with only mountain event
        lvl = LevelCompositeFactory(
            level=1,
            events=[
                EventCompositeFactory(
                    field=FieldCompositeFactory(name="evt"),
                    plain=None,
                    mountain=Threshold(
                        threshold=15, comparison_op=ComparisonOperator.SUP
                    ),
                )
            ],
        )
        strategy = RiskReducerStrategyMonozone(
            reducer=RiskReducerFactory(
                composite=RiskComponentCompositeFactory(levels=[lvl])
            )
        )

        assert strategy.process_value("evt", evts_ds=evts_ds, kind="plain") is None
        assert strategy.process_value("evt", evts_ds=evts_ds, kind="mountain") == {
            "threshold": 30.0,
            "min": 30.0,
            "max": 53.0,
            "value": 41.0,
            "units": "cm",
            "operator": ComparisonOperator.SUP,
            "occurrence": True,
        }

    def test_infos(self, assert_equals_result):
        # Test with DataArray
        da1 = xr.DataArray(Datetime(2023, 3, 1, 6).as_np_dt64, coords={"centroid": 0.2})
        da2 = xr.DataArray(Datetime(2023, 3, 1, 7).as_np_dt64)
        da3 = xr.DataArray(Datetime(2023, 3, 1, 8).as_np_dt64)
        strategy = RiskReducerStrategyMonozone(reducer=RiskReducerFactory())
        assert strategy.infos([da1, da2, da3]) == {
            "level": 0,
            "start": Datetime(2023, 3, 1, 6),
            "stop": Datetime(2023, 3, 1, 8),
            "centroid": 0.2,
        }

        # Test with Dataset
        ds1 = xr.Dataset(
            {
                "centroid": 0.2,
                "threshold_plain": (["evt"], [5.0, 50.0]),
                "min_plain": (["evt"], [1.0, 20.0]),
                "max_plain": (["evt"], [11.0, 120.0]),
                "rep_value_plain": (["evt"], [6.0, 70.0]),
                "threshold_mountain": (["evt"], [np.nan, 100.0]),
                "min_mountain": (["evt"], [np.nan, 40.0]),
                "max_mountain": (["evt"], [np.nan, 240.0]),
                "rep_value_mountain": (["evt"], [np.nan, 140.0]),
                "occurrence_plain": (["evt"], [True, True]),
                "occurrence_mountain": (["evt"], [True, True]),
            },
            coords={
                "evt": [0, 1],
                "units": (["evt"], ["cm", "mm"]),
                "risk_level": 1,
                "valid_time": Datetime(2023, 3, 1, 6).as_np_dt64,
                "weatherVarName": (["evt"], ["NEIPOT1__SOL", "NEIPOT24__SOL"]),
            },
        )
        ds2 = xr.Dataset(
            {
                "threshold_plain": (["evt"], [10.0, 100.0]),
                "min_plain": (["evt"], [3.0, 40.0]),
                "max_plain": (["evt"], [13.0, 140.0]),
                "rep_value_plain": (["evt"], [8.0, 90.0]),
                "threshold_mountain": (["evt"], [np.nan, 600.0]),
                "min_mountain": (["evt"], [np.nan, 80.0]),
                "max_mountain": (["evt"], [np.nan, 280.0]),
                "rep_value_mountain": (["evt"], [np.nan, 180.0]),
                "occurrence_plain": (["evt"], [True, True]),
                "occurrence_mountain": (["evt"], [True, True]),
            },
            coords={
                "evt": [0, 1],
                "units": (["evt"], ["cm", "mm"]),
                "valid_time": Datetime(2023, 3, 1, 7).as_np_dt64,
                "weatherVarName": (["evt"], ["NEIPOT1__SOL", "NEIPOT24__SOL"]),
            },
        )
        ds3 = xr.Dataset(
            {
                "threshold_plain": (["evt"], [20.0, 200.0]),
                "min_plain": (["evt"], [5.0, 60.0]),
                "max_plain": (["evt"], [15.0, 160.0]),
                "rep_value_plain": (["evt"], [10.0, 110.0]),
                "threshold_mountain": (["evt"], [np.nan, 600.0]),
                "min_mountain": (["evt"], [np.nan, 120.0]),
                "max_mountain": (["evt"], [np.nan, 360.0]),
                "rep_value_mountain": (["evt"], [np.nan, 220.0]),
                "occurrence_plain": (["evt"], [False, False]),
                "occurrence_mountain": (["evt"], [False, False]),
            },
            coords={
                "evt": [0, 1],
                "units": (["evt"], ["cm", "mm"]),
                "valid_time": Datetime(2023, 3, 1, 8).as_np_dt64,
                "weatherVarName": (["evt"], ["NEIPOT1__SOL", "NEIPOT24__SOL"]),
            },
        )

        lvl = LevelCompositeFactory(
            level=1,
            events=[
                # only plain event
                EventCompositeFactory(
                    field=FieldCompositeFactory(name="NEIPOT1__SOL"),
                    mountain_altitude=600,
                ),
                # plain and mountain event
                EventCompositeFactory(
                    field=FieldCompositeFactory(name="NEIPOT24__SOL"),
                    mountain=Threshold(
                        threshold=30, comparison_op=ComparisonOperator.SUPEGAL
                    ),
                    mountain_altitude=600,
                ),
            ],
        )
        strategy = RiskReducerStrategyMonozone(
            reducer=RiskReducerFactory(
                composite=RiskComponentCompositeFactory(levels=[lvl])
            )
        )
        assert_equals_result(strategy.infos([ds1, ds2, ds3]))

    @pytest.mark.parametrize(
        "level_max,expected_type",
        [
            (0, "general"),
            (1, "PRECIP"),
            (2, "PRECIP"),
            (3, "PRECIP"),
            (4, "general"),
            (5, "general"),
            (6, "general"),
        ],
    )
    def test_find_template_type(self, level_max, expected_type):
        strategy = RiskReducerStrategyMonozone(
            reducer=RiskReducerFactory(
                final_risk_max_factory=level_max,
                reduction={
                    "C": ...,
                    "B1": {
                        "level": 1,
                        "start": ...,
                        "stop": ...,
                        "centroid": ...,
                        "PRECIP1__SOL": ...,
                    },
                    "B2": {
                        "level": 2,
                        "start": ...,
                        "stop": ...,
                        "centroid": ...,
                        "EAU24__SOL": ...,
                    },
                    "B3": {
                        "level": 3,
                        "start": ...,
                        "stop": ...,
                        "centroid": ...,
                        "PRECIP1__SOL": ...,
                        "EAU24__SOL": ...,
                    },
                    "B4": {
                        "level": 4,
                        "start": ...,
                        "stop": ...,
                        "centroid": ...,
                        "NEIPOT12__SOL": ...,
                    },
                    "B5": {
                        "level": 5,
                        "PRECIP1__SOL": ...,
                        "EAU24__SOL": ...,
                        "NEIPOT12__SOL": ...,
                    },
                    "B6": {
                        "level": 6,
                        "PRECIP1__SOL": ...,
                        "EAU24__SOL": ...,
                        "NEIPOT12__SOL": ...,
                        "OTHER__OTHER": ...,
                    },
                },
            )
        )

        strategy.find_template_type()
        assert strategy.reduction["type"] == expected_type

    def test_find_levels(self):
        reduction = {
            "C": ...,
            "B1": {
                "level": ...,
                "start": ...,
                "stop": ...,
                "centroid": 1,  # => level_max
                "EAU24__SOL": {
                    "plain": {"operator": ComparisonOperator.SUP, "value": 10}
                },  # won't be kept
                "PRECIP1__SOL": {
                    "plain": {"operator": ComparisonOperator.INF, "value": 10}
                },  # will be kept
            },
            "B2": {
                "level": ...,
                "start": ...,
                "stop": ...,
                "centroid": 1,  # => level_max
                "EAU24__SOL": {
                    "plain": {"operator": ComparisonOperator.SUP, "value": 20}
                },  # will be kept
                "PRECIP1__SOL": {
                    "plain": {"operator": ComparisonOperator.INF, "value": 20}
                },  # won't be kept
            },
            "B3": {
                "level": 3,  # => level_int
                "start": ...,
                "stop": ...,
                "centroid": ...,
                "NEIPOT12__SOL": {
                    "plain": {"operator": ComparisonOperator.SUP, "value": 10},
                    "mountain": {"operator": ComparisonOperator.INF, "value": 10},
                },  # won't be kept
            },
            "B4": {
                "level": 2,  # => level_int
                "start": ...,
                "stop": ...,
                "centroid": ...,
                "NEIPOT12__SOL": {
                    "plain": {"operator": ComparisonOperator.SUP, "value": 10},
                    "mountain": {"operator": ComparisonOperator.INF, "value": 5},
                },  # will be kept
            },
        }
        strategy = RiskReducerStrategyMonozone(
            reducer=RiskReducerFactory(reduction=reduction)
        )
        strategy.find_levels()
        assert strategy.reduction == reduction | {
            "level_max": {
                "EAU24__SOL": {
                    "plain": {"operator": ComparisonOperator.SUP, "value": 20}
                },
                "PRECIP1__SOL": {
                    "plain": {"operator": ComparisonOperator.INF, "value": 10}
                },
            },
            "level_int": {
                "NEIPOT12__SOL": {
                    "plain": {"operator": ComparisonOperator.SUP, "value": 10},
                    "mountain": {"operator": ComparisonOperator.INF, "value": 5},
                }
            },
        }

    def test_process_period(self, assert_equals_result):
        # Test for "Neige" hazard_name
        strategy = RiskReducerStrategyMonozone(
            reducer=RiskReducerFactory(
                is_multizone_factory=False,
                composite=RiskComponentCompositeFactory(hazard_name="Neige"),
            )
        )
        strategy.process_period()
        assert strategy.reduction is None

        # Test for other hazard_name
        reduction = {
            "not_dict_value": 3,
            "no_start": {"stop": Datetime(2023, 3, 1, 8)},
            "no_stop": {"start": Datetime(2023, 3, 1, 6)},
            "B0": {"start": Datetime(2023, 3, 1, 0), "stop": Datetime(2023, 3, 1, 12)},
            "B1": {"start": Datetime(2023, 3, 2, 12), "stop": Datetime(2023, 3, 2, 18)},
        }
        strategy = RiskReducerStrategyMonozone(
            reducer=RiskReducerFactory(reduction=reduction, is_multizone_factory=False)
        )
        strategy.process_period()
        assert_equals_result(strategy.reduction)

    @pytest.mark.parametrize(
        "evt1_name,evt2_name",
        [
            ("NEIPOT1__SOL", "NEIPOT24__SOL"),  # type SNOW
            ("NEIPOT1__SOL", "EAU12__SOL"),  # Type PRECIP_SNOW
            ("EAU24__SOL", "EAU12__SOL"),  # Type PRECIP
            ("NEIPOT1__SOL", "FF__HAUTEUR"),  # Type general
            ("NEIPOT1__SOL", "RAF__HAUTEUR"),  # Type general
        ],
    )
    def test_compute(self, evt1_name, evt2_name, assert_equals_result):
        np.random.seed(1)
        valid_time = [Datetime(2023, 3, 1, 3 * i).as_np_dt64 for i in range(4)]

        lvl1 = LevelCompositeFactory(
            level=1,
            events=[
                EventCompositeFactory(
                    field=FieldCompositeFactory(name=evt1_name),
                    plain=Threshold(
                        threshold=2.0, comparison_op=ComparisonOperator.SUP, units="mm"
                    ),
                )
            ],
        )
        lvl2 = LevelCompositeFactory(
            level=2,
            events=[
                # only plain event
                EventCompositeFactory(field=FieldCompositeFactory(name=evt1_name)),
                # plain and mountain event
                EventCompositeFactory(
                    field=FieldCompositeFactory(name=evt2_name),
                    plain=Threshold(threshold=15, comparison_op=ComparisonOperator.SUP),
                    mountain=Threshold(
                        threshold=30,
                        comparison_op=ComparisonOperator.SUPEGAL,
                        units="cm",
                    ),
                ),
            ],
        )

        assert_equals_result(
            {
                language: RiskReducerFactory(
                    composite=RiskComponentCompositeFactory(
                        risk_ds=xr.Dataset(
                            {
                                "occurrence_plain": (
                                    ["risk_level", "evt"],
                                    [[True, True], [True, True]],
                                ),
                                "occurrence_mountain": (
                                    ["risk_level", "evt"],
                                    [[True, True], [True, True]],
                                ),
                                "threshold_plain": (
                                    ["risk_level", "evt"],
                                    [[5, 10], [15, 20]],
                                ),
                                "threshold_mountain": (
                                    ["risk_level", "evt"],
                                    [[15, 20], [25, 30]],
                                ),
                                "weatherVarName": (
                                    ["risk_level", "evt"],
                                    [[evt1_name, np.nan], [evt1_name, evt2_name]],
                                ),
                                "min_plain": (
                                    ["id", "risk_level", "evt", "valid_time"],
                                    [
                                        [
                                            [[10.0, 20.0, 30.0, 40.0], 4 * [np.nan]],
                                            [
                                                [1.0, 2.0, 3.0, 4.0],
                                                [50.0, 60.0, 70.0, 80.0],
                                            ],
                                        ]
                                    ],
                                ),
                                "max_plain": (
                                    ["id", "risk_level", "evt", "valid_time"],
                                    [
                                        [
                                            [[12.0, 22.0, 32.0, 42.0], 4 * [np.nan]],
                                            [
                                                [1.2, 2.2, 3.2, 4.2],
                                                [52.0, 62.0, 72.0, 82.0],
                                            ],
                                        ]
                                    ],
                                ),
                                "rep_value_plain": (
                                    ["id", "risk_level", "evt", "valid_time"],
                                    [
                                        [
                                            [[11.0, 21.0, 31.0, 41.0], 4 * [np.nan]],
                                            [
                                                [1.1, 2.1, 3.1, 4.1],
                                                [51.0, 61.0, 71.0, 81.0],
                                            ],
                                        ]
                                    ],
                                ),
                                "min_mountain": (
                                    ["id", "risk_level", "evt", "valid_time"],
                                    [
                                        [
                                            2 * [4 * [np.nan]],
                                            [4 * [np.nan], [53.0, 63.0, 73.0, 83.0]],
                                        ]
                                    ],
                                ),
                                "max_mountain": (
                                    ["id", "risk_level", "evt", "valid_time"],
                                    [
                                        [
                                            2 * [4 * [np.nan]],
                                            [4 * [np.nan], [55.0, 65.0, 75.0, 85.0]],
                                        ]
                                    ],
                                ),
                                "rep_value_mountain": (
                                    ["id", "risk_level", "evt", "valid_time"],
                                    [
                                        [
                                            2 * [4 * [np.nan]],
                                            [4 * [np.nan], [54.0, 64.0, 74.0, 84.0]],
                                        ]
                                    ],
                                ),
                            },
                            coords={
                                "id": ["geo_id"],
                                "evt": [0, 1],
                                "risk_level": [1, 2],
                                "valid_time": valid_time,
                                "units": (
                                    ["risk_level", "evt"],
                                    [["mm", np.nan], ["cm", "mm"]],
                                ),
                                "altAreaName": (["id"], [_("sur tout le domaine")]),
                            },
                        ),
                        final_risk_da_factory=xr.DataArray(
                            [[2, 1, 1, 2]],
                            coords={"id": ["geo_id"], "valid_time": valid_time},
                        ),
                        levels=[lvl1, lvl2],
                    )
                ).compute()
                for language in Settings.iter_languages()
            }
        )


class TestRiskReducerStrategyMultizone:
    def test_process_period(self, assert_equals_result):
        strategy = RiskReducerStrategyMultizone(
            reducer=RiskReducerFactory(
                reduction={},
                is_multizone_factory=True,
                localisation=RiskLocalisationFactory(
                    periods_name_factory=[
                        "20230301060000_to_20230301080000",
                        "20230301120000_to_20230301160000",
                        "20230302180000_to_20230302230000",
                    ]
                ),
            )
        )
        strategy.process_period()
        assert_equals_result(strategy.reduction)

    @pytest.mark.parametrize(
        "evt1_name,evt2_name",
        [
            ("NEIPOT1__SOL", "NEIPOT24__SOL"),  # type SNOW
            ("NEIPOT1__SOL", "EAU12__SOL"),  # Type PRECIP_SNOW
            ("EAU24__SOL", "EAU12__SOL"),  # Type PRECIP
            ("NEIPOT1__SOL", "FF__HAUTEUR"),  # Type general
            ("NEIPOT1__SOL", "RAF__HAUTEUR"),  # Type general
        ],
    )
    def test_compute(self, evt1_name, evt2_name, assert_equals_result):
        np.random.seed(1)
        valid_time = [Datetime(2023, 3, 1, 3 * i).as_np_dt64 for i in range(4)]

        lvl1 = LevelCompositeFactory(
            level=1,
            events=[
                EventCompositeFactory(
                    field=FieldCompositeFactory(name=evt1_name),
                    plain=Threshold(
                        threshold=2.0, comparison_op=ComparisonOperator.SUP, units="mm"
                    ),
                )
            ],
        )
        lvl2 = LevelCompositeFactory(
            level=2,
            events=[
                # only plain event
                EventCompositeFactory(field=FieldCompositeFactory(name=evt1_name)),
                # plain and mountain event
                EventCompositeFactory(
                    field=FieldCompositeFactory(name=evt2_name),
                    plain=Threshold(threshold=20, comparison_op=ComparisonOperator.SUP),
                    mountain=Threshold(
                        threshold=30,
                        comparison_op=ComparisonOperator.SUPEGAL,
                        units="mm",
                    ),
                ),
            ],
        )

        ids = ["id1"]

        result = {}
        for language in Settings.iter_languages():
            composite = RiskComponentCompositeFactory(
                risk_ds=xr.Dataset(
                    {
                        "weatherVarName": (
                            ["risk_level", "evt"],
                            [[evt1_name, np.nan], [evt1_name, evt2_name]],
                        ),
                        "min_plain": (
                            ["id", "risk_level", "evt", "valid_time"],
                            [
                                [
                                    [[10.0, 20.0, 30.0, 40.0], 4 * [np.nan]],
                                    [[1.0, 2.0, 3.0, 4.0], [50.0, 60.0, 70.0, 80.0]],
                                ]
                            ],
                        ),
                        "max_plain": (
                            ["id", "risk_level", "evt", "valid_time"],
                            [
                                [
                                    [[12.0, 22.0, 32.0, 42.0], 4 * [np.nan]],
                                    [[1.2, 2.2, 3.2, 4.2], [52.0, 62.0, 72.0, 82.0]],
                                ]
                            ],
                        ),
                        "rep_value_plain": (
                            ["id", "risk_level", "evt", "valid_time"],
                            [
                                [
                                    [[11.0, 21.0, 31.0, 41.0], 4 * [np.nan]],
                                    [[1.1, 2.1, 3.1, 4.1], [51.0, 61.0, 71.0, 81.0]],
                                ]
                            ],
                        ),
                        "min_mountain": (
                            ["id", "risk_level", "evt", "valid_time"],
                            [
                                [
                                    2 * [4 * [np.nan]],
                                    [4 * [np.nan], [53.0, 63.0, 73.0, 83.0]],
                                ]
                            ],
                        ),
                        "max_mountain": (
                            ["id", "risk_level", "evt", "valid_time"],
                            [
                                [
                                    2 * [4 * [np.nan]],
                                    [4 * [np.nan], [55.0, 65.0, 75.0, 85.0]],
                                ]
                            ],
                        ),
                        "rep_value_mountain": (
                            ["id", "risk_level", "evt", "valid_time"],
                            [
                                [
                                    2 * [4 * [np.nan]],
                                    [4 * [np.nan], [54.0, 64.0, 74.0, 84.0]],
                                ]
                            ],
                        ),
                    },
                    coords={
                        "id": ids,
                        "evt": [0, 1],
                        "risk_level": [1, 2],
                        "valid_time": valid_time,
                        "units": (
                            ["risk_level", "evt"],
                            [["mm", np.nan], ["cm", "mm"]],
                        ),
                        "altAreaName": (["id"], [_("sur tout le domaine")]),
                    },
                ),
                final_risk_da_factory=xr.DataArray(
                    [[2, 1, 1, 2]], coords={"id": ids, "valid_time": valid_time}
                ),
                levels=[lvl1, lvl2],
            )

            result[language] = RiskReducerFactory(
                geo_id=ids[0],
                composite=composite,
                localisation=RiskLocalisationFactory(
                    table_localisation=TableLocalisationFactory(
                        table={"zone1": "Zone 1", "zone2": "Zone 2"}
                    ),
                    periods_name_factory=[
                        "20230301060000_to_20230301080000",
                        "20230301120000_to_20230301160000",
                        "20230302180000_to_20230302230000",
                    ],
                ),
            ).compute()

        assert_equals_result(result)
