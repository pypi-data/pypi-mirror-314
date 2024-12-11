from collections import defaultdict
from itertools import product

import numpy as np
import pytest

import mfire.utils.mfxarray as xr
from mfire.composite.operator import ComparisonOperator
from mfire.settings import Settings
from mfire.text.risk.rep_value import (
    AltitudeRepValueReducer,
    FFRafRepValueBuilder,
    FFRafRepValueReducer,
    FFRepValueBuilder,
    FFRepValueReducer,
    LpnRepValueBuilder,
    LpnRepValueReducer,
    PrecipitationRepValueBuilder,
    PrecipitationRepValueReducer,
    RainRepValueBuilder,
    RainRepValueReducer,
    RepValueBuilder,
    RepValueReducer,
    SnowRepValueBuilder,
    SnowRepValueReducer,
    TemperatureRepValueBuilder,
    TemperatureRepValueReducer,
)
from mfire.utils.date import Datetime
from mfire.utils.string import _
from tests.composite.factories import (
    FieldCompositeFactory,
    LevelCompositeFactory,
    RiskComponentCompositeFactory,
)
from tests.text.base.factories import BaseBuilderFactory
from tests.text.risk.factories import (
    AccumulationRepValueBuilderFactory,
    AccumulationRepValueReducerFactory,
    AltitudeRepValueBuilderFactory,
    AltitudeRepValueReducerFactory,
    FFRafRepValueBuilderFactory,
    FFRafRepValueReducerFactory,
    FFRepValueBuilderFactory,
    FFRepValueReducerFactory,
    LpnRepValueBuilderFactory,
    LpnRepValueReducerFactory,
    PrecipitationRepValueBuilderFactory,
    PrecipitationRepValueReducerFactory,
    RainRepValueBuilderFactory,
    RainRepValueReducerFactory,
    RepValueBuilderFactory,
    RepValueReducerFactory,
    RepValueTestFactory,
    SnowRepValueBuilderFactory,
    SnowRepValueReducerFactory,
    TemperatureRepValueBuilderFactory,
    TemperatureRepValueReducerFactory,
    create_rep_value_test_data_altitude,
)

# Test data
REP_VALUE_TEST_DATA: list[dict] = RepValueTestFactory().run()
REP_VALUE_TEST_DATA_ALTITUDE: list[dict] = create_rep_value_test_data_altitude(
    REP_VALUE_TEST_DATA
)
IDX_TEST_DATA = list(range(len(REP_VALUE_TEST_DATA)))


def format_data(data: dict, units: str) -> dict:
    data = data.copy()
    if "plain" in data:
        data["plain"]["units"] = units
    if "mountain" in data:
        data["mountain"]["units"] = units
    return data


def build_expected_result(input_data: dict, output_data: dict) -> dict:
    res = {}
    res.update({"input": input_data})
    res.update({"output": output_data})
    return res


class TestRepValueReducer:
    factory = RepValueReducerFactory(phenomenon_factory="phen")

    @pytest.mark.parametrize(
        "reducer_class",
        [
            FFRepValueReducer,
            FFRafRepValueReducer,
            TemperatureRepValueReducer,
            PrecipitationRepValueReducer,
            RainRepValueReducer,
            SnowRepValueReducer,
        ],
    )
    def test_initialization_failure(self, reducer_class):
        """Test that KeyError raised if if 'var_name' key is missing in data arg."""
        with pytest.raises(KeyError):
            reducer_class(data={})

    def test_phenomenon(self):
        assert RepValueReducerFactory().phenomenon == ""

    def test_def_article(self, assert_equals_result):
        result = defaultdict(lambda: {})
        for feminine in [True, False]:
            for plural in [True, False]:
                factory = RepValueReducerFactory(
                    phenomenon_factory="phen", feminine=feminine, plural=plural
                )
                for language in Settings.iter_languages():
                    result[f"{feminine=},{plural=}"][language] = factory.def_article
        assert_equals_result(result)

    def test_indef_article(self, assert_equals_result):
        result = defaultdict(lambda: {})
        for feminine in [True, False]:
            for plural in [True, False]:
                factory = RepValueReducerFactory(
                    phenomenon_factory="phen", feminine=feminine, plural=plural
                )
                for language in Settings.iter_languages():
                    result[f"{feminine=},{plural=}"][language] = factory.indef_article
        assert_equals_result(result)

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            # Plain cases only
            (
                {"plain": {"value": 2.0, "operator": ComparisonOperator.SUP}},
                {"plain": {"value": 1.5}},
                True,
            ),
            (
                {"plain": {"value": 2.0, "operator": ComparisonOperator.INF}},
                {"plain": {"value": 2.5}},
                True,
            ),
            (
                {"plain": {"value": 2.0, "operator": ComparisonOperator.INF}},
                {"plain": {"value": 1.5}},
                False,
            ),
            (
                {"plain": {"value": 2.0, "operator": ComparisonOperator.SUP}},
                {"plain": {"value": 2.5}},
                False,
            ),
            # Plain and mountain cases
            (
                {
                    "plain": {"value": 2.0, "operator": ComparisonOperator.INFEGAL},
                    "mountain": {"value": 1.0, "operator": ComparisonOperator.SUP},
                },
                {"plain": {"value": 2.0}, "mountain": {"value": 0.5}},
                True,
            ),
            (
                {
                    "plain": {"value": 2.0, "operator": ComparisonOperator.INFEGAL},
                    "mountain": {"value": 1.0, "operator": ComparisonOperator.INF},
                },
                {"plain": {"value": 2.0}, "mountain": {"value": 1.5}},
                True,
            ),
            (
                {
                    "plain": {"value": 2.0, "operator": ComparisonOperator.INFEGAL},
                    "mountain": {"value": 1.0, "operator": ComparisonOperator.INF},
                },
                {"plain": {"value": 2.0}, "mountain": {"value": 0.5}},
                False,
            ),
            (
                {
                    "plain": {"value": 2.0, "operator": ComparisonOperator.INFEGAL},
                    "mountain": {"value": 1.0, "operator": ComparisonOperator.SUP},
                },
                {"plain": {"value": 2.0}, "mountain": {"value": 1.5}},
                False,
            ),
            # Mountain cases only
            (
                {"mountain": {"value": 2.0, "operator": ComparisonOperator.SUP}},
                {"mountain": {"value": 1.5}},
                True,
            ),
            (
                {"mountain": {"value": 2.0, "operator": ComparisonOperator.INF}},
                {"mountain": {"value": 2.5}},
                True,
            ),
            (
                {"mountain": {"value": 2.0, "operator": ComparisonOperator.INF}},
                {"mountain": {"value": 1.5}},
                False,
            ),
            (
                {"mountain": {"value": 2.0, "operator": ComparisonOperator.SUP}},
                {"mountain": {"value": 2.5}},
                False,
            ),
            # Special cases
            (
                {"plain": {"value": 2.0, "operator": ComparisonOperator.SUP}},
                {"mountain": {"value": 3.0}},
                True,
            ),
            ({"mountain": {"value": 3.0}}, {"plain": {"value": 2.0}}, False),
            (
                {
                    "plain": {"value": 2.0, "operator": ComparisonOperator.INFEGAL},
                    "mountain": {"value": 1.0, "operator": ComparisonOperator.SUP},
                },
                {"plain": {"value": 2.0}},
                True,
            ),
            (
                {"plain": {"value": 2.0, "operator": ComparisonOperator.INFEGAL}},
                {"plain": {"value": 2.0}, "mountain": {"value": 1.0}},
                False,
            ),
        ],
    )
    def test_compare(self, a, b, expected):
        assert RepValueReducer.compare(a, b) == expected

    @pytest.mark.parametrize("unit,expected", [("cm", "cm"), (None, "")])
    def test_units(self, unit, expected):
        assert self.factory.units(unit) == expected

    @pytest.mark.parametrize(
        "x,expected",
        [(None, None), (1e-7, None), (1e-5, "1e-05"), (10, "10"), (100.258, "100.258")],
    )
    def test_round(self, x, expected):
        assert self.factory.round(x) == expected

    def test_around_word(self, assert_equals_result):
        np.random.seed(1)
        assert_equals_result(
            {
                language: self.factory.around_word
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize(
        "dict_in,expected",
        [  # no operator
            ({"operator": None, "next_critical": 12, "value": 10}, (None, None)),
            # no value
            (
                {
                    "operator": ComparisonOperator.SUP,
                    "next_critical": 12,
                    "value": None,
                },
                (None, None),
            ),
            # no next_critical
            (
                {
                    "operator": ComparisonOperator.SUP,
                    "next_critical": None,
                    "value": 10,
                },
                (10, None),
            ),
            # value < next_critical
            (
                {"operator": ComparisonOperator.SUP, "next_critical": 12, "value": 10},
                (10, None),
            ),
            # value < next_critical
            (
                {"operator": ComparisonOperator.SUP, "next_critical": 10, "value": 12},
                (9, 12),
            ),
        ],
    )
    def test_replace_critical(self, dict_in, expected):
        assert RepValueReducer.replace_critical(dict_in) == expected

    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        reducer = RepValueReducerFactory(
            phenomenon_factory="phen", data=format_data(data, units="UNITS")
        )
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestFFRepValueReducer:
    factory = FFRepValueReducerFactory()

    def test_definite_var_name(self, assert_equals_result):
        assert_equals_result(
            {
                language: self.factory.definite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_indefinite_var_name(self, assert_equals_result):
        assert_equals_result(
            {
                language: self.factory.indefinite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_round(self, assert_equals_result):
        assert_equals_result(
            {
                language: {
                    value: self.factory.round(value)
                    for value in [None, 1e-7, 1e-5, 7.5, 12.5]
                }
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        reducer = FFRepValueReducerFactory(data=format_data(data, units="km/h"))
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestTemperatureRepValueReducer:
    factory = TemperatureRepValueReducerFactory()

    def test_definite_var_name(self, assert_equals_result):
        assert_equals_result(
            {
                language: self.factory.definite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_indefinite_var_name(self, assert_equals_result):
        assert_equals_result(
            {
                language: self.factory.indefinite_var_name
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize(
        "x,operator,expected",
        [
            (None, ComparisonOperator.INF, None),
            (None, ComparisonOperator.SUP, None),
            (1e-7, ComparisonOperator.INF, "0"),
            (1e-7, ComparisonOperator.SUP, "1"),
            (7.5, ComparisonOperator.INF, "7"),
            (7.5, ComparisonOperator.SUP, "8"),
        ],
    )
    def test_round(self, x, operator, expected):
        assert self.factory.round(x, operator=operator) == expected

    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        reducer = TemperatureRepValueReducerFactory(data=format_data(data, units="°C"))
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestFFRafRepValueReducer:
    factory = FFRafRepValueReducerFactory()

    def test_definite_var_name(self, assert_equals_result):
        assert_equals_result(
            {
                language: self.factory.definite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_indefinite_var_name(self, assert_equals_result):
        assert_equals_result(
            {
                language: self.factory.indefinite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_round(self, assert_equals_result):
        values = [
            (None, None),
            (1e-7, None),
            (1e-5, None),
            (7.5, None),
            (7.5, _("comprises entre")),
        ]
        assert_equals_result(
            {
                language: {
                    str((x, around)): self.factory.round(x, around=around)
                    for x, around in values
                }
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        reducer = FFRafRepValueReducerFactory(data=format_data(data, units="km/h"))
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestAccumulationRepValueReducer:
    @pytest.mark.parametrize("var_name", ["NEIPOT1__SOL", "NEIPOT6__SOL", "EAU1__SOL"])
    def test_accumulated_hours(self, var_name, assert_equals_result):
        reducer = AccumulationRepValueReducerFactory(var_name=var_name)
        assert_equals_result(reducer.accumulated_hours)

    def test_check_data(self):
        with pytest.raises(
            ValueError, match="No accumulation found for 'NEIPOT__SOL' var_name"
        ):
            _ = AccumulationRepValueReducerFactory(var_name="NEIPOT__SOL")


class TestSnowRepValueReducer:
    factory = SnowRepValueReducerFactory()

    @pytest.mark.parametrize("var_name", ["NEIPOT1__SOL", "NEIPOT24__SOL"])
    def test_definite_var_name(self, var_name, assert_equals_result):
        assert_equals_result(
            {
                language: SnowRepValueReducerFactory(
                    var_name=var_name
                ).definite_var_name
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("var_name", ["NEIPOT1__SOL", "NEIPOT24__SOL"])
    def test_indefinite_var_name(self, var_name, assert_equals_result):
        assert_equals_result(
            {
                language: SnowRepValueReducerFactory(
                    var_name=var_name
                ).indefinite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_round(self, assert_equals_result):
        values = [None, 1e-7, 1e-5, 1.5, 4.5, 6.5, 7.5, 12.5, 17.5, 28.1, 113.4]
        assert_equals_result(
            {
                language: {x: self.factory.round(x) for x in values}
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        reducer = SnowRepValueReducerFactory(data=format_data(data, units="cm"))
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestPrecipitationRepValueReducer:
    factory = PrecipitationRepValueReducerFactory()

    @pytest.mark.parametrize("var_name", ["PRECIP3__SOL", "PRECIP1__SOL"])
    def test_definite_var_name(self, var_name, assert_equals_result):
        assert_equals_result(
            {
                language: PrecipitationRepValueReducerFactory(
                    var_name=var_name
                ).definite_var_name
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("var_name", ["PRECIP3__SOL", "PRECIP1__SOL"])
    def test_indefinite_var_name(self, var_name, assert_equals_result):
        assert_equals_result(
            {
                language: PrecipitationRepValueReducerFactory(
                    var_name=var_name
                ).indefinite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_round(self, assert_equals_result):
        values = [
            None,
            1e-7,
            1e-5,
            1.5,
            4.5,
            7.5,
            12.5,
            17.5,
            22,
            27,
            35,
            45,
            55,
            70,
            90,
            112.2,
            1218.5,
        ]
        assert_equals_result(
            {
                language: {x: self.factory.round(x) for x in values}
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        reducer = PrecipitationRepValueReducerFactory(
            data=format_data(data, units="mm")
        )
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestRainRepValueReducer:
    factory = RainRepValueReducerFactory()

    @pytest.mark.parametrize("var_name", ["EAU24__SOL", "EAU1__SOL"])
    def test_definite_var_name(self, var_name, assert_equals_result):
        assert_equals_result(
            {
                language: RainRepValueReducerFactory(
                    var_name=var_name
                ).definite_var_name
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("var_name,", ["EAU24__SOL", "EAU1__SOL"])
    def test_indefinite_var_name(self, var_name, assert_equals_result):
        assert_equals_result(
            {
                language: RainRepValueReducerFactory(
                    var_name=var_name
                ).indefinite_var_name
                for language in Settings.iter_languages()
            }
        )

    def test_round(self, assert_equals_result):
        values = [
            None,
            1e-7,
            1e-5,
            1.5,
            4.5,
            7.5,
            12.5,
            17.5,
            22,
            27,
            35,
            45,
            55,
            70,
            90,
            115,
            1215,
        ]
        assert_equals_result(
            {
                language: {x: self.factory.round(x) for x in values}
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        reducer = RainRepValueReducerFactory(data=format_data(data, units="cm"))
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )


class TestLpnRepValueReducer:
    @pytest.mark.parametrize(
        "lpn,wwmf,spatial_risk",
        [
            # No LPN
            (None, None, None),
            ([np.nan], [60], None),
            # No snow points but snow risk - see #41799
            ([110], [50], None),
            # No snow points and sometimes no snow risk + see #42568
            ([110, 2000], [50, 51], [np.nan, 1.0]),
            ([110, 2000], [50, 51], [0.0, 1.0]),
            # Lpn without variation
            ([110], [60], None),
            ([100, 199], [60, 60], None),
            ([100, 330, 450, 670], [60, 50, 50, 50], None),
            # One variation
            ([100, 330, 450, 670], [60, 60, 60, 60], None),
            ([560, 330, 45], [60, 60, 60], None),
            # Two variations
            ([120, 220, 320, 420, 320, 220, 180], [60, 60, 60, 60, 60, 60, 60], None),
            # More than 3 variations
            ([120, 500, 470, 460, 800, 820, 530], [60, 60, 60, 60, 60, 60, 60], None),
        ],
    )
    def test_compute(self, lpn, wwmf, spatial_risk, assert_equals_result):
        if lpn is None:
            params, levels = {}, []
        else:
            valid_time = [
                Datetime(2023, 3, 1, 3 * i).as_np_dt64 for i in range(len(lpn))
            ]
            if spatial_risk is None:
                spatial_risk = [1] * len(valid_time)
            lpn = xr.DataArray(
                [[lpn, [v + 5 for v in lpn]]],  # test minimal value taken over space
                coords={
                    "latitude": [30],
                    "longitude": [40, 41],
                    "valid_time": valid_time,
                },
            )
            wwmf = xr.DataArray(
                [[wwmf, wwmf]],
                coords={
                    "latitude": [30],
                    "longitude": [40, 41],
                    "valid_time": valid_time,
                },
            )
            params = {
                "LPN__SOL": FieldCompositeFactory(compute_factory=lambda: lpn),
                "WWMF__SOL": FieldCompositeFactory(compute_factory=lambda: wwmf),
            }
            levels = [
                LevelCompositeFactory(
                    level=2,
                    spatial_risk_da_factory=xr.DataArray(
                        [[[spatial_risk] * 2]],
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
            params=params,
            geo_factory=lambda _: xr.DataArray(
                [[True, True]], coords={"latitude": [30], "longitude": [40, 41]}
            ),
            final_risk_max_level_factory=lambda _: 2,
            levels=levels,
        )
        assert_equals_result(
            {
                language: LpnRepValueReducerFactory(
                    geo_id="geo_id", composite=composite
                ).compute()
                for language in Settings.iter_languages()
            }
        )


class TestAltitudeRepValueReducer:
    @pytest.mark.parametrize(
        "var_name",
        [
            "FF__HAUTEUR10",
            "T__HAUTEUR2",
            "RAF__HAUTEUR10",
            "NEIPOT1__SOL",
            "PRECIP1__SOL",
            "EAU12__SOL",
            "OTHER__OTHER",
        ],
    )
    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, var_name, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        reducer = AltitudeRepValueReducerFactory(data={var_name: data})
        assert_equals_result(
            build_expected_result(
                data,
                {language: reducer.compute() for language in Settings.iter_languages()},
            )
        )

    @pytest.mark.parametrize(
        "var_name,expected_class",
        [
            ("FF__HAUTEUR10", FFRepValueReducer),
            ("T__HAUTEUR2", TemperatureRepValueReducer),
            ("RAF__HAUTEUR10", FFRafRepValueReducer),
            ("PRECIP1__SOL", PrecipitationRepValueReducer),
            ("EAU12__SOL", RainRepValueReducer),
            ("NEIPOT1__SOL", SnowRepValueReducer),
            ("LPN__SOL", LpnRepValueReducer),
            ("OTHER__OTHER", None),
        ],
    )
    def test_get_reducer(self, var_name, expected_class):
        result = AltitudeRepValueReducer.get_reducer(var_name)
        if expected_class is not None:
            assert result == expected_class
        else:
            assert result is None


class TestRepValueBuilder:
    @pytest.mark.parametrize(
        "var_name,expected_class",
        [
            ("FF__HAUTEUR10", FFRepValueBuilder),
            ("RAF__HAUTEUR10", FFRafRepValueBuilder),
            ("T__HAUTEUR2", TemperatureRepValueBuilder),
            ("PRECIP1__SOL", PrecipitationRepValueBuilder),
            ("EAU12__SOL", RainRepValueBuilder),
            ("NEIPOT1__SOL", SnowRepValueBuilder),
            ("LPN__SOL", LpnRepValueBuilder),
            ("OTHER__OTHER", None),
        ],
    )
    def test_get_builder(self, var_name, expected_class):
        result = RepValueBuilder.get_builder(
            {"var_name": var_name},
            builder=BaseBuilderFactory(composite=RiskComponentCompositeFactory()),
        )
        if expected_class is not None:
            assert isinstance(result, expected_class)
        else:
            assert result is None

    def test_template_name(self):
        builder = RepValueBuilderFactory()
        assert builder.template_name == "rep_value_generic"

    @pytest.mark.parametrize(
        "reduction,expected",
        [
            ({}, ""),
            ({"plain_value": ...}, "plain"),
            ({"mountain_value": ...}, "mountain"),
            ({"plain_value": ..., "local_plain_value": ...}, "local_plain"),
            ({"mountain_value": ..., "local_mountain_value": ...}, "local_mountain"),
            ({"plain_value": ..., "mountain_value": ...}, "plain_mountain"),
            (
                {"plain_value": ..., "local_plain_value": ..., "mountain_value": ...},
                "local_plain_mountain",
            ),
            (
                {
                    "plain_value": ...,
                    "mountain_value": ...,
                    "local_mountain_value": ...,
                },
                "plain_local_mountain",
            ),
            (
                {
                    "plain_value": ...,
                    "local_plain_value": ...,
                    "mountain_value": ...,
                    "local_mountain_value": ...,
                },
                "local_plain_local_mountain",
            ),
        ],
    )
    def test_template_key_not_accumulated(self, reduction, expected):
        builder = RepValueBuilderFactory(
            reducer=RepValueReducerFactory(reduction=reduction)
        )
        assert builder.template_key == expected

    @pytest.mark.parametrize(
        "data, reduction, expected",
        [
            ({}, {}, ""),
            ({"plain": ...}, {}, "no_acc_plain"),
            ({"plain": ...}, {"plain_value": ...}, "plain"),
            ({"plain": ...}, {"local_plain_value": ...}, "no_acc_plain_local_plain"),
            (
                {"plain": ...},
                {"plain_value": ..., "local_plain_value": ...},
                "local_plain",
            ),
            ({"mountain": ...}, {}, "no_acc_mountain"),
            ({"mountain": ...}, {"mountain_value": ...}, "mountain"),
            (
                {"mountain": ...},
                {"local_mountain_value": ...},
                "no_acc_mountain_local_mountain",
            ),
            (
                {"mountain": ...},
                {"mountain_value": ..., "local_mountain_value": ...},
                "local_mountain",
            ),
            ({"plain": ..., "mountain": ...}, {}, "no_acc_plain_no_acc_mountain"),
            (
                {"plain": ..., "mountain": ...},
                {"plain_value": ...},
                "plain_no_acc_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"mountain_value": ...},
                "no_acc_plain_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"local_plain_value": ...},
                "no_acc_plain_local_plain_no_acc_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"local_mountain_value": ...},
                "no_acc_plain_no_acc_mountain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"plain_value": ..., "mountain_value": ...},
                "plain_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"plain_value": ..., "local_plain_value": ...},
                "local_plain_no_acc_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"plain_value": ..., "local_mountain_value": ...},
                "plain_no_acc_mountain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"mountain_value": ..., "local_plain_value": ...},
                "no_acc_plain_local_plain_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"mountain_value": ..., "local_mountain_value": ...},
                "no_acc_plain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"local_plain_value": ..., "local_mountain_value": ...},
                "no_acc_plain_local_plain_no_acc_mountain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {"plain_value": ..., "mountain_value": ..., "local_plain_value": ...},
                "local_plain_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {
                    "plain_value": ...,
                    "mountain_value": ...,
                    "local_mountain_value": ...,
                },
                "plain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {
                    "plain_value": ...,
                    "local_plain_value": ...,
                    "local_mountain_value": ...,
                },
                "local_plain_no_acc_mountain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {
                    "mountain_value": ...,
                    "local_plain_value": ...,
                    "local_mountain_value": ...,
                },
                "no_acc_plain_local_plain_local_mountain",
            ),
            (
                {"plain": ..., "mountain": ...},
                {
                    "plain_value": ...,
                    "mountain_value": ...,
                    "local_plain_value": ...,
                    "local_mountain_value": ...,
                },
                "local_plain_local_mountain",
            ),
        ],
    )
    def test_template_key_accumulated_var_name(self, data, reduction, expected):
        builder = AccumulationRepValueBuilderFactory(
            reducer=AccumulationRepValueReducerFactory(data=data, reduction=reduction)
        )
        assert builder.template_key == expected

    def test_pre_process(self):
        reduction = {
            "indefinite_var_name": "un cumul de précipitation sur 3 heures",
            "plain_value": "au maximum 3 mm",
            "around": "aux alentours de",
        }
        builder = RepValueBuilderFactory(
            text="On attend {indefinite_var_name} {around} {value}.",
            reducer=RepValueReducerFactory(
                reduction=reduction, data={"var_name": "TEST__VARNAME"}
            ),
        )
        builder.pre_process()

        assert builder.text == "On attend {indefinite_var_name} {around}{value}."
        assert builder.reduction == {
            "indefinite_var_name": "un cumul de précipitation sur 3 heures",
            "plain_value": "au maximum 3 mm",
            "around": "d'",
        }

    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: RepValueBuilderFactory(
                        data=format_data(data, units="UNITS")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )

    @pytest.mark.parametrize(
        "data",
        [
            # Empty data
            {},
            # rep value > next_critical
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 1,
                        "next_critical": 2,
                    },
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                        "next_critical": 7,
                    },
                    "mountain_altitude": 1300,
                }
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 1,
                        "next_critical": 2,
                    },
                    "RAF__HAUTEUR10": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                        "next_critical": 7,
                    },
                    "mountain_altitude": 1300,
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 1,
                        "next_critical": 2,
                    },
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                        "next_critical": 7,
                    },
                    "mountain_altitude": 1300,
                },
            },
            # rep value < threshold
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 10,
                        "occurrence": False,
                    },
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 15,
                        "occurrence": False,
                    },
                    "mountain_altitude": 1300,
                }
            },
            {
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 10,
                        "occurrence": True,
                    },
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 15,
                        "occurrence": True,
                    },
                    "mountain_altitude": 1300,
                }
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 10,
                        "occurrence": True,
                    },
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 15,
                        "occurrence": True,
                    },
                    "mountain_altitude": 1300,
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 10,
                        "occurrence": True,
                    },
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 1,
                        "threshold": 15,
                        "occurrence": True,
                    },
                    "mountain_altitude": 1300,
                },
            },
            # Altitude builder same prefixes
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 1,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "T__HAUTEUR2": {
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 1,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 1,
                    },
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
            },
            # Altitude builder different prefixes
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 1,
                    },
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    },
                    "mountain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 5,
                        "threshold": 1,
                    },
                    "mountain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 10,
                        "threshold": 5,
                    },
                    "mountain_altitude": 1200,
                },
            },
            # No mountain_altitude
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    }
                }
            },
            {
                "T__HAUTEUR2": {
                    "plain": {
                        "units": "celsius",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    }
                },
                "FF__HAUTEUR10": {
                    "plain": {
                        "units": "km/h",
                        "operator": ComparisonOperator.SUPEGAL,
                        "value": 2,
                        "threshold": 1,
                    }
                },
            },
            {"T__HAUTEUR2": {}, "FF__HAUTEUR10": {}},
        ],
    )
    def test_compute_all(self, data, assert_equals_result):
        np.random.seed(1)
        assert_equals_result(
            {
                language: RepValueBuilder.compute_all(
                    data, builder=BaseBuilderFactory()
                )
                for language in Settings.iter_languages()
            }
        )

    @pytest.mark.parametrize("data", [{}, {"mountain_altitude": 500}])
    def test_compute_all_with_lpn(self, data, assert_equals_result):
        np.random.seed(1)
        valid_time = [Datetime(2023, 3, 1, 3 * i).as_np_dt64 for i in range(7)]
        lpn = xr.DataArray(
            [[[120, 500, 470, 460, 800, 820, 530]]],
            coords={"latitude": [30], "longitude": [40], "valid_time": valid_time},
        )
        wwmf = xr.DataArray(
            [[[60] * 7]],
            coords={"latitude": [30], "longitude": [40], "valid_time": valid_time},
        )
        composite = RiskComponentCompositeFactory(
            params={
                "LPN__SOL": FieldCompositeFactory(compute_factory=lambda: lpn),
                "WWMF__SOL": FieldCompositeFactory(compute_factory=lambda: wwmf),
            },
            geo_factory=lambda _: xr.DataArray(
                xr.DataArray([[True]], coords={"latitude": [30], "longitude": [40]})
            ),
        )
        assert_equals_result(
            {
                language: RepValueBuilder.compute_all(
                    {"LPN__SOL": data}, builder=BaseBuilderFactory(composite=composite)
                )
                for language in Settings.iter_languages()
            }
        )


class TestFFRepValueBuilder:
    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: FFRepValueBuilderFactory(
                        data=format_data(data, units="km/h")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )


class TestTemperatureRepValueBuilder:
    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: TemperatureRepValueBuilderFactory(
                        data=format_data(data, units="°C")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )


class TestFFRafRepValueBuilder:
    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: FFRafRepValueBuilderFactory(
                        data=format_data(data, units="km/h")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )


class TestSnowRepValueBuilder:
    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: SnowRepValueBuilderFactory(
                        data=format_data(data, units="cm")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )


class TestPrecipitationRepValueBuilder:
    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: PrecipitationRepValueBuilderFactory(
                        data=format_data(data, units="mm")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )


class TestRainRepValueBuilder:
    @pytest.mark.parametrize("idx", IDX_TEST_DATA)
    def test_compute(self, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA[idx]
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: RainRepValueBuilderFactory(
                        data=format_data(data, units="mm")
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )


class TestLpnRepValueBuilder:
    def test_template_name(self):
        assert (
            LpnRepValueBuilderFactory(reducer=LpnRepValueReducerFactory()).template_name
            == "rep_value_lpn"
        )

    def test_template_key(self):
        assert (
            LpnRepValueBuilderFactory(
                reducer=LpnRepValueReducerFactory(), reduction_factory={}
            ).template_key
            is None
        )
        assert (
            LpnRepValueBuilderFactory(
                reducer=LpnRepValueReducerFactory(),
                reduction_factory={"key": "template_key"},
            ).template_key
            == "template_key"
        )

    @pytest.mark.parametrize(
        "reduction",
        [
            {
                "key": "1xlpn",
                "lpn": [100],
                "temp": ["ce milieu de nuit de mardi à mercredi"],
            },
            {
                "key": "2xlpn+",
                "lpn": [100, 700],
                "temp": [
                    "ce milieu de nuit de mardi à mercredi",
                    "ce mercredi fin de matinée",
                ],
            },
            {
                "key": "2xlpn-",
                "lpn": [600, 0],
                "temp": [
                    "ce milieu de nuit de mardi à mercredi",
                    "ce mercredi début de matinée",
                ],
            },
            {
                "key": "3xlpn+",
                "lpn": [100, 800, 500],
                "temp": [
                    "ce milieu de nuit de mardi à mercredi",
                    "ce mercredi après-midi",
                    "ce mercredi soir",
                ],
            },
        ],
    )
    def test_compute(self, reduction, assert_equals_result):
        np.random.seed(0)

        assert_equals_result(
            {
                language: LpnRepValueBuilderFactory(
                    reducer=LpnRepValueReducerFactory(
                        compute_factory=lambda: None, reduction=reduction
                    )
                ).compute()
                for language in Settings.iter_languages()
            }
        )


class TestAltitudeRepValueBuilder:
    @pytest.mark.parametrize(
        "var_name, unit",
        [
            ("FF__HAUTEUR10", "km/h"),
            ("T__HAUTEUR2", "°C"),
            ("RAF__HAUTEUR10", "km/h"),
            ("NEIPOT1__SOL", "cm"),
            ("PRECIP1__SOL", "cm"),
            ("EAU12__SOL", "cm"),
            ("OTHER__OTHER", "cm"),
        ],
    )
    @pytest.mark.parametrize("idx", range(len(REP_VALUE_TEST_DATA_ALTITUDE)))
    def test_compute(self, var_name, unit, idx, assert_equals_result):
        np.random.seed(1)
        data = REP_VALUE_TEST_DATA_ALTITUDE[idx]
        assert_equals_result(
            build_expected_result(
                data,
                {
                    language: AltitudeRepValueBuilderFactory(
                        data={var_name: format_data(data, units=unit)}
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )

    @pytest.mark.parametrize(
        "idx1,idx2", product(range(len(REP_VALUE_TEST_DATA_ALTITUDE)), repeat=2)
    )
    def test_compute_both(self, idx1, idx2, assert_equals_result):
        np.random.seed(1)
        data1 = REP_VALUE_TEST_DATA_ALTITUDE[idx1]
        data2 = REP_VALUE_TEST_DATA_ALTITUDE[idx2]
        assert_equals_result(
            build_expected_result(
                {"NEIPOT1__SOL": data1, "NEIPOT24__SOL": data2},
                {
                    language: AltitudeRepValueBuilderFactory(
                        data={"NEIPOT1__SOL": data1, "NEIPOT24__SOL": data2}
                    ).compute()
                    for language in Settings.iter_languages()
                },
            )
        )
