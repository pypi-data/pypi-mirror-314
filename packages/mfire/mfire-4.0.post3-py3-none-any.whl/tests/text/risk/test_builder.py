import numpy as np
import pytest

import mfire.utils.mfxarray as xr
from mfire.composite.event import Threshold
from mfire.composite.operator import ComparisonOperator
from mfire.settings import Settings
from mfire.text.risk.builder import RiskBuilder
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
    SpatialLocalisationFactory,
    TableLocalisationFactory,
)
from tests.text.risk.factories import RiskBuilderFactory, RiskReducerFactory


class TestRiskBuilder:
    def test_init_reducer(self):
        builder = RiskBuilderFactory()
        assert builder.reducer.geo_id == "geo_id"

    def test_is_multizone(self):
        reducer = RiskReducerFactory(is_multizone_factory=True)
        builder = RiskBuilderFactory(reducer=reducer)
        assert builder.is_multizone is True

        reducer = RiskReducerFactory(is_multizone_factory=False)
        builder = RiskBuilderFactory(reducer=reducer)
        assert builder.is_multizone is False

    def test_template_name(self):
        # Snow case
        assert (
            RiskBuilderFactory(
                composite=RiskComponentCompositeFactory(hazard_name="Neige")
            ).template_name
            == "snow"
        )

        # Monozone non-general case
        reducer = RiskReducerFactory(
            reduction={"type": "other"}, is_multizone_factory=False
        )
        builder = RiskBuilderFactory(reducer=reducer)
        assert builder.template_name == "monozone_precip"

        # Monozone general case
        reducer = RiskReducerFactory(
            reduction={"type": "general"}, is_multizone_factory=False
        )
        builder = RiskBuilderFactory(reducer=reducer)
        assert builder.template_name == "monozone_generic"

        # Multizone cases
        reducer = RiskReducerFactory(
            localisation=RiskLocalisationFactory(template_type_factory="test")
        )
        builder = RiskBuilderFactory(is_multizone_factory=True, reducer=reducer)
        assert builder.template_name == "multizone_test"

    def test_template_key(self):
        # Snow case
        assert (
            RiskBuilderFactory(
                composite=RiskComponentCompositeFactory(hazard_name="Neige"),
                reduction_factory={"key": "template_key"},
            ).template_key
            == "template_key"
        )

        # Monozone non-general case
        reducer = RiskReducerFactory(
            reduction={"type": "other"}, is_multizone_factory=False
        )
        builder = RiskBuilderFactory(reducer=reducer)
        assert builder.template_key == "other"

        # Monozone general case
        valid_time = [Datetime(2023, 3, 1, i).as_np_dt64 for i in range(3)]
        composite = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset(coords={"B": [1], "risk_level": [1, 2]}),
            final_risk_da_factory=xr.DataArray(
                [[2, 1, 2]], coords={"id": ["geo_id"], "valid_time": valid_time}
            ),
            final_risk_max_level_factory={"geo_id": 2},
        )
        reducer = RiskReducerFactory(
            reduction={"type": "general"},
            is_multizone_factory=False,
            composite=composite,
        )
        builder = RiskBuilderFactory(reducer=reducer)
        assert_identically_close(builder.template_key, np.array([1.0, 1.0, 1.0]))

        # Multizone case
        reducer = RiskReducerFactory(
            localisation=RiskLocalisationFactory(unique_name_factory="test")
        )
        builder = RiskBuilderFactory(is_multizone_factory=True, reducer=reducer)
        assert builder.template_key == "test"

    def test_extract_critical_value(self):
        da = xr.DataArray(
            [[1, 2, 3], [4, 5, 6]],
            coords={
                "id": ["id1", "id2"],
                "valid_time": [Datetime(2023, 3, 1, i) for i in range(3)],
            },
        )
        assert RiskBuilder.extract_critical_values(da, ComparisonOperator.SUP) == (
            6.0,
            "id2",
        )
        assert RiskBuilder.extract_critical_values(da, ComparisonOperator.INF) == (
            1.0,
            "id1",
        )
        with pytest.raises(
            ValueError,
            match="Operator is not understood when trying to find the critical "
            "representative values.",
        ):
            _ = RiskBuilder.extract_critical_values(da, ComparisonOperator.ISIN)


class TestRiskBuilderMonozone:
    @pytest.mark.parametrize(
        "reduction",
        [
            {
                "B0": {
                    "level": ...,
                    "T__HAUTEUR2": {
                        "plain": {
                            "units": "celsius",
                            "operator": ComparisonOperator.SUPEGAL,
                            "value": 2,
                        },
                        "mountain_altitude": 1200,
                    },
                    "RAF__HAUTEUR10": {
                        "mountain": {
                            "units": "cm",
                            "operator": ComparisonOperator.SUPEGAL,
                            "value": 10,
                        },
                        "mountain_altitude": 1200,
                    },
                }
            },
            {
                "B0": {
                    "level": ...,
                    "FF__HAUTEUR10": {
                        "plain": {
                            "units": "cm",
                            "operator": ComparisonOperator.SUPEGAL,
                            "value": 2,
                        },
                        "mountain": {
                            "units": "cm",
                            "operator": ComparisonOperator.SUPEGAL,
                            "value": 5,
                        },
                        "mountain_altitude": 1200,
                    },
                    "NEIPOT24__SOL": {
                        "plain": {
                            "units": "cm",
                            "operator": ComparisonOperator.SUPEGAL,
                            "value": 5,
                        },
                        "mountain": {
                            "units": "cm",
                            "operator": ComparisonOperator.SUPEGAL,
                            "value": 10,
                        },
                        "mountain_altitude": 1200,
                    },
                }
            },
            {
                "B0": {
                    "level": ...,
                    "PRECIP1__SOL": {
                        "plain": {
                            "units": "cm",
                            "operator": ComparisonOperator.SUPEGAL,
                            "value": 2,
                        },
                        "mountain_altitude": 1200,
                    },
                    "EAU24__SOL": {
                        "mountain": {
                            "units": "cm",
                            "operator": ComparisonOperator.SUPEGAL,
                            "value": 10,
                        },
                        "mountain_altitude": 1200,
                    },
                }
            },
            {
                "B0": {
                    "level": ...,
                    "PRECIP12__SOL": {
                        "plain": {
                            "units": "cm",
                            "operator": ComparisonOperator.SUPEGAL,
                            "value": 2,
                        },
                        "mountain_altitude": 1200,
                    },
                    "EAU24__SOL": {
                        "mountain": {
                            "units": "cm",
                            "operator": ComparisonOperator.SUPEGAL,
                            "value": 10,
                        },
                        "mountain_altitude": 1200,
                    },
                }
            },
            {
                "B0": {
                    "level": ...,
                    "NEIPOT1__SOL": {
                        "plain": {
                            "units": "cm",
                            "operator": ComparisonOperator.SUPEGAL,
                            "value": 2,
                        }
                    },
                }
            },
            {
                "B0": {
                    "level": ...,
                    "NEIPOT1__SOL": {
                        "plain": {
                            "units": "cm",
                            "operator": ComparisonOperator.SUPEGAL,
                            "value": 2,
                        }
                    },
                    "NEIPOT24__SOL": {
                        "plain": {
                            "units": "cm",
                            "operator": ComparisonOperator.SUPEGAL,
                            "value": 2,
                        }
                    },
                }
            },
            {"B0": {"level": ..., "NEIPOT1__SOL": {}, "RAF__HAUTEUR10": {}}},
        ],
    )
    def test_post_process_general(self, reduction, assert_equals_result):
        np.random.seed(0)
        reducer = RiskReducerFactory(reduction=reduction | {"type": "OTHER"})
        builder = RiskBuilderFactory(
            is_multizone_factory=False,
            reducer=reducer,
            template_factory="Template du monozone. {B0_val}",
        )
        assert_equals_result(builder.compute())

    @pytest.mark.parametrize("final_risk_max", [2, 3])
    def test_post_process_precip(self, final_risk_max, assert_equals_result):
        np.random.seed(0)
        assert_equals_result(
            {
                language: RiskBuilderFactory(
                    reducer=RiskReducerFactory(
                        final_risk_max_factory=final_risk_max,
                        reduction={
                            "alt_area_name": _("sur le domaine"),
                            "type": "PRECIP",
                            "B0": {
                                "centroid": 1.0,
                                "level": 2,
                                "EAU1__SOL": {
                                    "plain": {
                                        "min": 1.0,
                                        "max": 1.2,
                                        "value": 1.1,
                                        "units": "cm",
                                        "operator": "supegal",
                                    }
                                },
                                "EAU24__SOL": {
                                    "plain": {
                                        "min": 50.0,
                                        "max": 52.0,
                                        "value": 51.0,
                                        "units": "mm",
                                        "operator": "sup",
                                    },
                                    "mountain": {
                                        "min": 53.0,
                                        "max": 55.0,
                                        "value": 54.0,
                                        "units": "mm",
                                        "operator": "inf",
                                    },
                                },
                            },
                        },
                    ),
                    is_multizone_factory=False,
                ).compute()
                for language in Settings.iter_languages()
            }
        )

    def test_compute_simple_generic(self, assert_equals_result):
        np.random.seed(0)
        assert_equals_result(
            RiskBuilderFactory(
                reducer=RiskReducerFactory(
                    reduction={
                        "type": "OTHER",
                        "B0": {
                            "start": "en début de nuit de mardi à mercredi",
                            "centroid": 1.0,
                            "level": 2,
                            "T__HAUTEUR": {
                                "plain": {
                                    "min": 1.0,
                                    "max": 1.2,
                                    "value": 1.1,
                                    "units": "celsius",
                                    "operator": "supegal",
                                }
                            },
                            "FF__HAUTEUR10": {
                                "plain": {
                                    "min": 50.0,
                                    "max": 52.0,
                                    "value": 51.0,
                                    "units": "km/h",
                                    "operator": "sup",
                                },
                                "mountain": {
                                    "min": 53.0,
                                    "max": 55.0,
                                    "value": 54.0,
                                    "units": "km/h",
                                    "operator": "inf",
                                },
                            },
                            "stop": "ce milieu de nuit de mardi à mercredi",
                            "period": "la nuit de mardi à mercredi",
                        },
                        "level_max": {
                            "RAF__HAUTEUR10": {
                                "plain": {
                                    "min": 4.0,
                                    "max": 4.2,
                                    "value": 4.1,
                                    "units": "km/h",
                                    "operator": "supegal",
                                }
                            },
                            "EAU12__SOL": {
                                "plain": {
                                    "min": 80.0,
                                    "max": 82.0,
                                    "value": 81.0,
                                    "units": "mm",
                                    "operator": "sup",
                                },
                                "mountain": {
                                    "min": 83.0,
                                    "max": 85.0,
                                    "value": 84.0,
                                    "units": "mm",
                                    "operator": "inf",
                                },
                            },
                        },
                        "level_int": {
                            "PRECIP1__SOL": {
                                "plain": {
                                    "min": 20.0,
                                    "max": 32.0,
                                    "value": 31.0,
                                    "units": "mm",
                                    "operator": "supegal",
                                }
                            }
                        },
                    }
                ),
                is_multizone_factory=False,
                template_factory="Risque à partir de {B0_start} jusqu’à {B0_stop}. "
                "{B0_val}. Level max : {level_max_val}. Level int : "
                "{level_int_val}.",
            ).compute()
        )

    @pytest.mark.parametrize(
        "evt1_name,evt2_name,unit_evt1,unit_evt2",
        [
            ("EAU24__SOL", "EAU12__SOL", "mm", "mm"),  # Type PRECIP
            ("EAU24__SOL", "FF__HAUTEUR", "mm", "km/h"),  # Type general
            ("FF__HAUTEUR", "RAF__HAUTEUR", "km/h", "km/h"),  # Type general
        ],
    )
    def test_compute(
        self, evt1_name, evt2_name, unit_evt1, unit_evt2, assert_equals_result
    ):
        np.random.seed(0)

        valid_time = [Datetime(2023, 3, 1, 3 * i).as_np_dt64 for i in range(4)]

        lvl1 = LevelCompositeFactory(
            level=1,
            events=[
                EventCompositeFactory(
                    field=FieldCompositeFactory(name=evt1_name),
                    plain=Threshold(
                        threshold=2.0,
                        comparison_op=ComparisonOperator.SUP,
                        units=unit_evt1,
                    ),
                )
            ],
        )
        lvl2 = LevelCompositeFactory(
            level=2,
            events=[
                # only plain event
                EventCompositeFactory(
                    field=FieldCompositeFactory(name=evt1_name),
                    plain=Threshold(
                        threshold=1.5,
                        comparison_op=ComparisonOperator.SUP,
                        units=unit_evt1,
                    ),
                ),
                # plain and mountain event
                EventCompositeFactory(
                    field=FieldCompositeFactory(name=evt2_name),
                    plain=Threshold(
                        threshold=20,
                        comparison_op=ComparisonOperator.SUP,
                        units=unit_evt2,
                    ),
                    mountain=Threshold(
                        threshold=30,
                        comparison_op=ComparisonOperator.SUPEGAL,
                        units=unit_evt2,
                    ),
                ),
            ],
        )
        composite = RiskComponentCompositeFactory(
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
                    "threshold_plain": (["risk_level", "evt"], [[5, 10], [15, 20]]),
                    "threshold_mountain": (["risk_level", "evt"], [[15, 20], [25, 30]]),
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
                    "id": ["geo_id"],
                    "evt": [0, 1],
                    "risk_level": [1, 2],
                    "valid_time": valid_time,
                    "units": (
                        ["risk_level", "evt"],
                        [[unit_evt1, np.nan], [unit_evt1, unit_evt2]],
                    ),
                    "altAreaName": (["id"], [_("sur tout le domaine")]),
                },
            ),
            final_risk_da_factory=xr.DataArray(
                [[2, 1, 1, 2]], coords={"id": ["geo_id"], "valid_time": valid_time}
            ),
            levels=[lvl1, lvl2],
        )

        assert_equals_result(
            {
                language: RiskBuilderFactory(
                    reducer=RiskReducerFactory(
                        is_multizone_factory=False, composite=composite
                    )
                ).compute()
                for language in Settings.iter_languages()
            }
        )


class TestRiskBuilderMultizone:
    @pytest.mark.parametrize(
        "template_name_factory", ["multizone_generic", "multizone_precip"]
    )
    def test_template(self, template_name_factory, assert_equals_result):
        np.random.seed(0)

        keys = [
            "P1_0_1",
            "P2_1_2",
            "P2_1_3",
            "P2_2_3",
            "P2_0_1_2",
            "P2_0_1_3",
            "P2_0_2_3",
            "P2_1_2_3",
            "P3_2_5",
            "P3_2_7",
            "P3_3_5",
            "P3_3_6",
            "P3_5_6",
            "P3_5_7",
            "P3_0_2_5",
            "P3_0_2_7",
            "P3_0_3_5",
            "P3_0_3_6",
            "P3_0_5_6",
            "P3_0_5_7",
            "P3_1_2_4",
            "P3_1_2_5",
            "P3_1_2_6",
            "P3_1_2_7",
            "P3_1_3_4",
            "P3_1_3_5",
            "P3_1_3_6",
            "P3_1_3_7",
            "P3_1_4_6",
            "P3_1_4_7",
            "P3_1_5_6",
            "P3_1_5_7",
            "P3_2_3_4",
            "P3_2_3_5",
            "P3_2_3_6",
            "P3_2_3_7",
            "P3_2_4_5",
            "P3_2_4_7",
            "P3_2_5_6",
            "P3_2_5_7",
            "P3_2_6_7",
            "P3_3_4_5",
            "P3_3_4_6",
            "P3_3_5_6",
            "P3_3_5_7",
            "P3_3_6_7",
            "P3_4_5_6",
            "P3_4_5_7",
            "P3_4_6_7",
            "P3_5_6_7",
        ]

        result = {}
        for language in Settings.iter_languages():
            result[language] = {}
            for key in keys:
                result[language][key] = RiskBuilderFactory(
                    is_multizone_factory=True,
                    template_key_factory=key,
                    template_name_factory=template_name_factory,
                ).template.format(
                    alt_area_name=_("sur le domaine"),
                    zone1="Zone 1",
                    zone2="Zone 2",
                    zone3="Zone 3",
                    zone1_2="Zone 1 et 2",
                    zone1_3="Zone 1 et 3",
                    zone2_3="Zone 2 et 3",
                    zone1_2_3="Zone 1, 2 et 3",
                    periode1="Periode 1",
                    periode2="Periode 2",
                    periode3="Periode 3",
                    periode1_2="Periodes 1 et 2",
                    periode1_3="Periodes 1 et 3",
                    periode2_3="Periodes 2 et 3",
                    periode1_2_3="Periodes 1, 2 et 3",
                )

        assert_equals_result(result)

    @pytest.mark.parametrize(
        "data",
        [
            # Empty data
            {},
            # Altitude builder
            {
                "NEIPOT1__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                    },
                    "mountain_altitude": 1200,
                },
                "NEIPOT24__SOL": {
                    "mountain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "NEIPOT1__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                    },
                    "mountain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                    },
                    "mountain_altitude": 1200,
                },
                "NEIPOT24__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                    },
                    "mountain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "NEIPOT1__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                    },
                    "mountain_altitude": 1200,
                },
                "EAU24__SOL": {
                    "mountain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "PRECIP12__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                    },
                    "mountain_altitude": 1200,
                },
                "EAU24__SOL": {
                    "mountain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                    },
                    "mountain_altitude": 1200,
                },
            },
            # No mountain_altitude
            {
                "NEIPOT1__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                    }
                }
            },
            # Homogeneous var_name
            {
                "NEIPOT1__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                    }
                },
                "NEIPOT24__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                    }
                },
            },
            # Not homogeneous var_name
            {"NEIPOT1__SOL": {}, "RAF__HAUTEUR10": {}},
        ],
    )
    def test_post_process(self, data, assert_equals_result):
        np.random.seed(0)
        assert_equals_result(
            RiskBuilderFactory(
                is_multizone_factory=True,
                critical_values_factory=data,
                template_factory="Template du multizone.",
            ).compute()
        )

    @pytest.mark.parametrize(
        "evt1_name,evt2_name,unit_evt1,unit_evt2",
        [
            ("EAU24__SOL", "EAU12__SOL", "mm", "mm"),  # Type PRECIP
            ("EAU24__SOL", "FF__HAUTEUR", "mm", "km/h"),  # Type general
            ("FF__HAUTEUR", "RAF__HAUTEUR", "km/h", "km/h"),  # Type general
        ],
    )
    def test_compute(
        self, evt1_name, evt2_name, unit_evt1, unit_evt2, assert_equals_result
    ):
        np.random.seed(0)

        valid_time = [Datetime(2023, 3, 1, 3 * i).as_np_dt64 for i in range(4)]
        lvl1 = LevelCompositeFactory(
            level=1,
            events=[
                EventCompositeFactory(
                    field=FieldCompositeFactory(name=evt1_name),
                    plain=Threshold(
                        threshold=2.0,
                        comparison_op=ComparisonOperator.SUP,
                        units=unit_evt1,
                    ),
                )
            ],
        )
        lvl2 = LevelCompositeFactory(
            level=2,
            events=[
                # only plain event
                EventCompositeFactory(
                    field=FieldCompositeFactory(name=evt1_name),
                    plain=Threshold(
                        threshold=1.5,
                        comparison_op=ComparisonOperator.SUP,
                        units=unit_evt1,
                    ),
                ),
                # plain and mountain event
                EventCompositeFactory(
                    field=FieldCompositeFactory(name=evt2_name),
                    plain=Threshold(
                        threshold=20,
                        comparison_op=ComparisonOperator.SUP,
                        units=unit_evt2,
                    ),
                    mountain=Threshold(
                        threshold=30,
                        comparison_op=ComparisonOperator.SUPEGAL,
                        units=unit_evt2,
                    ),
                ),
            ],
        )

        ids = ["id1"]

        result = {}
        for language in Settings.iter_languages():
            risk_ds = xr.Dataset(
                {
                    "occurrence_plain": (
                        ["risk_level", "evt"],
                        [[True, True], [True, True]],
                    ),
                    "occurrence_mountain": (
                        ["risk_level", "evt"],
                        [[True, True], [True, True]],
                    ),
                    "threshold_plain": (["risk_level", "evt"], [[5, 10], [15, 20]]),
                    "threshold_mountain": (["risk_level", "evt"], [[15, 20], [25, 30]]),
                    "weatherVarName": (
                        ["risk_level", "evt"],
                        [[evt1_name, np.nan], [evt1_name, evt2_name]],
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
                        [[unit_evt1, np.nan], [unit_evt1, unit_evt2]],
                    ),
                    "altAreaName": (["id"], [_("sur tout le domaine")]),
                },
            )
            risk_component = RiskComponentCompositeFactory(
                risk_ds=risk_ds,
                levels=[lvl1, lvl2],
                final_risk_max_level_factory=lambda _: 2,
            )

            localisation = RiskLocalisationFactory(
                risk_component=risk_component,
                geo_id="id1",
                periods_name_factory=[
                    "20230301060000_to_20230301080000",
                    "20230301120000_to_20230301160000",
                    "20230302180000_to_20230302230000",
                ],
                table_localisation=TableLocalisationFactory(
                    table={"zone1": "sur la zone 1", "zone2": "sur la zone 2"}
                ),
                spatial_localisation=SpatialLocalisationFactory(
                    risk_component=risk_component, localised_risk_ds_factory=risk_ds
                ),
                unique_name_factory="P3_2_5",
            )
            result[language] = RiskBuilderFactory(
                composite=risk_component,
                is_multizone_factory=True,
                reducer=RiskReducerFactory(
                    geo_id=ids[0], composite=risk_component, localisation=localisation
                ),
            ).compute()

        assert_equals_result(result)


class TestRiskBuilderSnow:
    @pytest.mark.parametrize(
        "data",
        [
            # Altitude builder
            {
                "NEIPOT1__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                    },
                    "mountain_altitude": 1200,
                },
                "NEIPOT24__SOL": {
                    "mountain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "NEIPOT1__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                    },
                    "mountain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                    },
                    "mountain_altitude": 1200,
                },
                "NEIPOT24__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                    },
                    "mountain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                    },
                    "mountain_altitude": 1200,
                },
            },
            # No mountain_altitude
            {
                "NEIPOT1__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                    }
                }
            },
            # Homogeneous var_name
            {
                "NEIPOT1__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                    }
                },
                "NEIPOT24__SOL": {
                    "plain": {
                        "units": "cm",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                    }
                },
            },
        ],
    )
    @pytest.mark.parametrize("has_lpn", [True, False])
    def test_post_process(self, data, has_lpn, assert_equals_result):
        np.random.seed(0)

        lpn = [100, 500, 200, 1000]
        valid_time = [Datetime(2023, 3, 1, 3 * i).as_np_dt64 for i in range(len(lpn))]
        lpn = xr.DataArray(
            [[lpn, [v + 5 for v in lpn]]],  # test minimal value taken over space
            coords={"latitude": [30], "longitude": [40, 41], "valid_time": valid_time},
        )
        wwmf = xr.DataArray(
            [[[60] * 4] * 2],
            coords={"latitude": [30], "longitude": [40, 41], "valid_time": valid_time},
        )
        params = {
            "LPN__SOL": FieldCompositeFactory(compute_factory=lambda: lpn),
            "WWMF__SOL": FieldCompositeFactory(compute_factory=lambda: wwmf),
        }
        levels = [
            LevelCompositeFactory(
                level=2,
                spatial_risk_da_factory=xr.DataArray(
                    [[[[True] * len(valid_time)] * 2]],
                    coords={
                        "id": ["geo_id"],
                        "latitude": [30],
                        "longitude": [40, 41],
                        "valid_time": valid_time,
                    },
                ),
            )
        ]

        composite = RiskComponentCompositeFactory(
            hazard_name="Neige",
            params=params,
            geo_factory=lambda _: xr.DataArray(
                [[True, True]], coords={"latitude": [30], "longitude": [40, 41]}
            ),
            levels=levels,
        )

        if has_lpn:
            data = data.copy() | {"LPN__SOL": {}}

        assert_equals_result(
            RiskBuilderFactory(
                composite=composite,
                critical_values_factory=data,
                template_factory="L1\nL2\nL3",
            ).compute()
        )
