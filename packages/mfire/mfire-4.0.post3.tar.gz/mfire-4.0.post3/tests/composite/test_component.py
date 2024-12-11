from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

import mfire.utils.mfxarray as xr
from mfire.composite.aggregation import AggregationMethod, AggregationType
from mfire.composite.component import (
    RiskComponentComposite,
    SynthesisComponentComposite,
)
from mfire.composite.event import Category, Threshold
from mfire.composite.level import LocalisationConfig
from mfire.composite.operator import ComparisonOperator, LogicalOperator
from mfire.composite.period import PeriodComposite
from mfire.utils.date import Datetime
from mfire.utils.json import JsonFile
from mfire.utils.period import Period, PeriodDescriber
from tests.composite.factories import (
    AggregationFactory,
    AltitudeCompositeFactory,
    EventCompositeFactory,
    FieldCompositeFactory,
    GeoCompositeFactory,
    LevelCompositeFactory,
    PeriodCompositeFactory,
    RiskComponentCompositeFactory,
    SynthesisComponentCompositeFactory,
    SynthesisCompositeFactory,
)
from tests.functions_test import assert_identically_close

# COMPONENTS


class TestAbstractComponentComposite:
    @pytest.mark.parametrize(
        "component_class",
        [SynthesisComponentCompositeFactory, RiskComponentCompositeFactory],
    )
    def test_init_dates(self, component_class):
        component = component_class(
            production_datetime="2023-03-01", configuration_datetime="2023-03-02"
        )
        assert component.production_datetime == Datetime(2023, 3, 1)
        assert component.configuration_datetime == Datetime(2023, 3, 2)

    @pytest.mark.parametrize(
        "component_class",
        [SynthesisComponentCompositeFactory, RiskComponentCompositeFactory],
    )
    def test_period_describer(self, component_class):
        component = component_class(
            period=PeriodCompositeFactory(
                start=Datetime(2023, 3, 1, 1), stop=Datetime(2023, 3, 1, 12)
            ),
            production_datetime=Datetime(2023, 3, 1),
        )
        assert component.period_describer == PeriodDescriber(
            cover_period=Period(Datetime(2023, 3, 1, 1), Datetime(2023, 3, 1, 12)),
            request_time=Datetime(2023, 3, 1),
        )


class TestRiskComponentComposite:
    inputs_dir: Path = Path(__file__).parent / "inputs"

    def test_is_risks_empty(self):
        risk_compo = RiskComponentCompositeFactory()
        assert risk_compo.is_risks_empty is True

        risk_compo = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset({"A": ("B", [1])}, coords={"B": [2]})
        )
        assert risk_compo.is_risks_empty is False

    def test_risks_of_level(self):
        risk_compo = RiskComponentCompositeFactory(
            levels=[LevelCompositeFactory(level=1)] * 3
            + [LevelCompositeFactory(level=2)] * 5
        )
        assert len(risk_compo.risks_of_level(1)) == 3
        assert len(risk_compo.risks_of_level(2)) == 5
        assert len(risk_compo.risks_of_level(3)) == 0

    def test_final_risk_max_level(self):
        # Empty risk
        risk_compo = RiskComponentCompositeFactory()
        assert risk_compo.final_risk_max_level(geo_id="id") == 0

        # Non-empty risk
        risk_compo = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset({"A": ("B", [...])}, coords={"B": [...]}),
            final_risk_da_factory=xr.DataArray(
                [[1, 2], [4, 5]], coords={"id": ["id_1", "id_2"], "A": [..., ...]}
            ),
        )
        assert risk_compo.final_risk_max_level(geo_id="id_1") == 2
        assert risk_compo.final_risk_max_level(geo_id="id_2") == 5

    def test_final_risk_min_level(self):
        # Empty risk
        risk_compo = RiskComponentCompositeFactory()
        assert risk_compo.final_risk_min_level(geo_id="id") == 0

        # Non-empty risk
        risk_compo = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset({"A": ("B", [...])}, coords={"B": [...]}),
            final_risk_da_factory=xr.DataArray(
                [[1, 2], [4, 5]], coords={"id": ["id_1", "id_2"], "A": [..., ...]}
            ),
        )

        assert risk_compo.final_risk_min_level(geo_id="id_1") == 1
        assert risk_compo.final_risk_min_level(geo_id="id_2") == 4

    def test_alt_area_name(self):
        # Empty risk
        risk_compo = RiskComponentCompositeFactory()
        assert risk_compo.area_name(geo_id="id") == "N.A"

        # Non-empty risk
        risk_compo = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset(
                {"altAreaName": (["id"], ["area1", "area2"])},
                coords={"id": ["id1", "id2"]},
            )
        )
        assert risk_compo.alt_area_name(geo_id="id1") == "area1"
        assert risk_compo.alt_area_name(geo_id="id2") == "area2"

    def test_area_name(self):
        # Empty risk
        risk_compo = RiskComponentCompositeFactory()
        assert risk_compo.area_name(geo_id="id") == "N.A"

        # Non-empty risk
        risk_compo = RiskComponentCompositeFactory(
            risk_ds=xr.Dataset(
                {"areaName": (["id"], ["area1", "area2"])},
                coords={"id": ["id1", "id2"]},
            )
        )
        assert risk_compo.area_name(geo_id="id1") == "area1"
        assert risk_compo.area_name(geo_id="id2") == "area2"

    def test_get_comparison(self):
        levels = [
            LevelCompositeFactory(
                level=1,
                events=[
                    EventCompositeFactory(
                        plain=Threshold(
                            threshold=13,
                            comparison_op=ComparisonOperator.SUP,
                            units="mm",
                        ),
                        mountain=Threshold(
                            threshold=13,
                            comparison_op=ComparisonOperator.INF,
                            units="mm",
                        ),
                    )
                ],
            ),
            LevelCompositeFactory(
                level=2,
                events=[
                    EventCompositeFactory(
                        plain=Threshold(
                            threshold=1.5,
                            comparison_op=ComparisonOperator.SUP,
                            units="cm",
                        ),
                        mountain=Threshold(
                            threshold=1.0,
                            comparison_op=ComparisonOperator.INF,
                            units="cm",
                        ),
                    )
                ],
            ),
            LevelCompositeFactory(
                level=3,
                events=[
                    EventCompositeFactory(
                        plain=Threshold(
                            threshold=20,
                            comparison_op=ComparisonOperator.SUPEGAL,
                            units="mm",
                        ),
                        mountain=Threshold(
                            threshold=0.5,
                            comparison_op=ComparisonOperator.INFEGAL,
                            units="cm",
                        ),
                    )
                ],
            ),
        ]

        risk_compo = RiskComponentCompositeFactory(levels=levels)
        assert risk_compo.get_comparison(1) == {
            "field_name": {
                "plain": Threshold(
                    threshold=13,
                    comparison_op=ComparisonOperator.SUP,
                    units="mm",
                    next_critical=15.0,
                ),
                "category": Category.BOOLEAN,
                "mountain": Threshold(
                    threshold=13,
                    comparison_op=ComparisonOperator.INF,
                    units="mm",
                    next_critical=10.0,
                ),
                "aggregation": {"kwargs": {}, "method": AggregationMethod.MEAN},
            }
        }
        assert risk_compo.get_comparison(2) == {
            "field_name": {
                "plain": Threshold(
                    threshold=1.5,
                    comparison_op=ComparisonOperator.SUP,
                    units="cm",
                    next_critical=2.0,
                ),
                "category": Category.BOOLEAN,
                "mountain": Threshold(
                    threshold=1,
                    comparison_op=ComparisonOperator.INF,
                    units="cm",
                    next_critical=0.5,
                ),
                "aggregation": {"kwargs": {}, "method": AggregationMethod.MEAN},
            }
        }
        assert risk_compo.get_comparison(3) == {
            "field_name": {
                "plain": Threshold(
                    threshold=20, comparison_op=ComparisonOperator.SUPEGAL, units="mm"
                ),
                "category": Category.BOOLEAN,
                "mountain": Threshold(
                    threshold=0.5, comparison_op=ComparisonOperator.INFEGAL, units="cm"
                ),
                "aggregation": {"kwargs": {}, "method": AggregationMethod.MEAN},
            }
        }

    @pytest.mark.parametrize(
        "axis,expected",
        [
            (0, [5.0, 1.0, 4.0]),
            (1, [2.0, 4.0, 4.0]),
            ((0,), [5.0, 1.0, 4.0]),
            ((1,), [2.0, 4.0, 4.0]),
        ],
    )
    def test_replace_middle(self, axis, expected):
        x = np.array([[2.0, 1.0, 2.0], [5.0, 1.0, 4.0], [4.0, 4.0, 1.0]])
        result = RiskComponentComposite._replace_middle(x, axis=axis)
        assert_identically_close(result, np.array(expected))

    def test_special_merge(self):
        d1 = xr.Dataset(
            {
                "summarized_density": (["valid_time", "risk_level"], [[0.1, 0.2]]),
                "risk_summarized_density": (["valid_time", "risk_level"], [[0.1, 0.2]]),
                "occurrence": (["valid_time", "risk_level"], [[False, True]]),
                "occurrence_plain": (["valid_time", "risk_level"], [[False, True]]),
                "occurrence_mountain": (["valid_time", "risk_level"], [[False, True]]),
            },
            coords={
                "risk_level": [1, 2],
                "valid_time": [
                    np.datetime64("2024-02-01T00:00:00").astype("datetime64[ns]")
                ],
            },
        )
        d2 = xr.Dataset(
            {
                "summarized_density": (
                    ["valid_time", "risk_level"],
                    [[0.2, 0.1], [0.4, 0.3]],
                ),
                "risk_summarized_density": (
                    ["valid_time", "risk_level"],
                    [[0.2, 0.1], [0.4, 0.3]],
                ),
                "occurrence": (
                    ["valid_time", "risk_level"],
                    [[True, False], [True, False]],
                ),
                "occurrence_plain": (
                    ["valid_time", "risk_level"],
                    [[True, False], [False, True]],
                ),
                "occurrence_mountain": (
                    ["valid_time", "risk_level"],
                    [[True, False], [False, True]],
                ),
            },
            coords={
                "risk_level": [1, 2],
                "valid_time": [
                    np.datetime64("2024-02-01T00:00:00").astype("datetime64[ns]"),
                    np.datetime64("2024-02-02T04:00:00").astype("datetime64[ns]"),
                ],
            },
        )

        result = RiskComponentComposite._special_merge(d1, d2)

        assert_identically_close(
            result,
            xr.Dataset(
                {
                    "summarized_density": (
                        ["valid_time", "risk_level"],
                        [[0.2, 0.2], [0.4, 0.3]],
                    ),
                    "risk_summarized_density": (
                        ["valid_time", "risk_level"],
                        [[0.2, 0.2], [0.4, 0.3]],
                    ),
                    "occurrence": (
                        ["valid_time", "risk_level"],
                        [[True, True], [True, False]],
                    ),
                    "occurrence_plain": (
                        ["valid_time", "risk_level"],
                        [[True, True], [False, True]],
                    ),
                    "occurrence_mountain": (
                        ["valid_time", "risk_level"],
                        [[True, True], [False, True]],
                    ),
                },
                coords={
                    "risk_level": [1, 2],
                    "valid_time": [
                        np.datetime64("2024-02-01T00:00:00").astype("datetime64[ns]"),
                        np.datetime64("2024-02-02T04:00:00").astype("datetime64[ns]"),
                    ],
                },
            ),
        )

    def test_compute(self, assert_equals_result):
        lon, lat = [15], [30, 31, 32, 33]
        ids = ["id"]

        altitude = AltitudeCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [[10, np.nan, 20, 30]], coords={"longitude": lon, "latitude": lat}
            )
        )
        geos1 = GeoCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [[[False, True, True, True]]],
                coords={"id": ids, "longitude": lon, "latitude": lat},
            ),
            mask_id=ids,
        )
        geos2 = GeoCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [[[False, True, False, True]]],
                coords={"id": ids, "longitude": lon, "latitude": lat},
            ),
            mask_id=ids,
        )

        field1 = FieldCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [
                    [
                        [1000, 2000],  # masked values by geos
                        [1500, 3000],  # masked values by altitude
                        [1.7, 1.9],  # isn't risked with threshold and geos
                        [1.8, 1.9],
                    ]
                ],
                coords={
                    "longitude": lon,
                    "latitude": lat,
                    "valid_time": [
                        Datetime(2023, 3, i).as_np_dt64 for i in range(1, 3)
                    ],
                },
                attrs={"units": "cm"},
                name="NEIPOT24__SOL",
            )
        )
        field2 = FieldCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [
                    [
                        [1500],  # masked values by geos
                        [2000],  # masked values by altitude
                        [1.6],  # isn't risked with threshold
                        [1.9],
                    ]
                ],
                coords={
                    "longitude": lon,
                    "latitude": lat,
                    "valid_time": [Datetime(2023, 3, 3).as_np_dt64],
                },
                attrs={"units": "cm"},
                name="NEIPOT1__SOL",
            )
        )
        evt1 = EventCompositeFactory(
            field=field1,
            geos=geos1,
            altitude=altitude,
            category=Category.QUANTITATIVE,
            plain=Threshold(
                threshold=2.0, comparison_op=ComparisonOperator.SUPEGAL, units="cm"
            ),
        )
        evt2 = EventCompositeFactory(
            field=field1,
            geos=geos2,
            altitude=altitude,
            category=Category.QUANTITATIVE,
            plain=Threshold(
                threshold=15, comparison_op=ComparisonOperator.SUPEGAL, units="mm"
            ),
        )
        evt3 = EventCompositeFactory(
            field=field2,
            geos=geos2,
            altitude=altitude,
            category=Category.QUANTITATIVE,
            plain=Threshold(
                threshold=2.0, comparison_op=ComparisonOperator.SUPEGAL, units="cm"
            ),
            mountain=Threshold(
                threshold=12, comparison_op=ComparisonOperator.SUPEGAL, units="mm"
            ),
            mountain_altitude=15,
        )

        lvl1 = LevelCompositeFactory(
            level=1,
            events=[evt1, evt2],
            logical_op_list=[LogicalOperator.OR],
            aggregation_type=AggregationType.DOWN_STREAM,
            aggregation=AggregationFactory(),
        )
        lvl2 = LevelCompositeFactory(
            level=2,
            events=[evt1, evt2],
            logical_op_list=[LogicalOperator.AND],
            aggregation_type=AggregationType.DOWN_STREAM,
            aggregation=AggregationFactory(),
        )
        lvl3 = LevelCompositeFactory(
            level=3,
            events=[evt3],
            aggregation_type=AggregationType.DOWN_STREAM,
            aggregation=AggregationFactory(),
        )
        risk_compo = RiskComponentCompositeFactory(levels=[lvl1, lvl2, lvl3])

        risk_compo.compute()
        assert_equals_result(
            {
                "risk_ds": risk_compo.risk_ds.to_dict(),
                "final_risk_da": risk_compo.final_risk_da.to_dict(),
            }
        )

    @patch("os.environ", {"MFIRE_DISABLE_PRECACHING": True})
    def test_integration(self, assert_equals_result, root_path_cwd):
        data = JsonFile(self.inputs_dir / "small_conf_risk.json").load()
        data_prod = next(iter(data.values()))
        component = data_prod["components"][0]
        compo = RiskComponentComposite(**component)

        assert_equals_result(compo)

    @pytest.mark.parametrize(
        "final_risk_da,expected",
        [
            # No information about fog
            (None, None),
            (
                xr.DataArray(
                    [[1]], coords={"valid_time": [Datetime(2023, 3, 1)], "id": ["id3"]}
                ),
                None,
            ),
            (
                xr.DataArray(
                    [[1]], coords={"valid_time": [Datetime(2023, 2, 1)], "id": ["id1"]}
                ),
                None,
            ),
            # Mist without occurrence
            (
                xr.DataArray(
                    [[0]], coords={"valid_time": [Datetime(2023, 3, 1)], "id": ["id1"]}
                ),
                False,
            ),
            # Mist with occurrence
            (
                xr.DataArray(
                    [[1, 0]],
                    coords={"valid_time": [Datetime(2023, 3, 1)], "id": ["id1", "id2"]},
                ),
                True,
            ),
            (
                xr.DataArray(
                    [[0, 1]],
                    coords={"valid_time": [Datetime(2023, 3, 1)], "id": ["id1", "id2"]},
                ),
                True,
            ),
        ],
    )
    def test_has_risk(self, final_risk_da, expected):
        valid_time_slice = slice(Datetime(2023, 3, 1), Datetime(2023, 3, 1, 2))
        assert (
            RiskComponentCompositeFactory(final_risk_da_factory=final_risk_da).has_risk(
                ids=["id1", "id2"], valid_time_slice=valid_time_slice
            )
            == expected
        )

    @pytest.mark.parametrize(
        "field,ids,expected",
        [
            ("F1", ["id1"], True),
            ("F2", ["id2"], True),
            ("F2", ["id1", "id2"], True),
            ("F1", ["id2"], False),
        ],
    )
    def test_has_field(self, field, ids, expected):
        level = LevelCompositeFactory(
            events=[
                EventCompositeFactory(
                    field=FieldCompositeFactory(name="F1"), geos_id_factory=["id1"]
                ),
                EventCompositeFactory(
                    field=FieldCompositeFactory(name="F2"), geos_id_factory=["id2"]
                ),
            ]
        )
        compo = RiskComponentCompositeFactory(levels=[level])
        assert compo.has_field(field, ids) == expected

    def test_geo(self):
        risk = RiskComponentCompositeFactory(
            levels=[
                LevelCompositeFactory(
                    events=[
                        EventCompositeFactory(
                            geos=xr.DataArray(coords={"id": ["id1"]}, dims=["id"])
                        )
                    ]
                ),
                LevelCompositeFactory(
                    events=[
                        EventCompositeFactory(
                            geos=xr.DataArray(
                                coords={"id": ["id1", "id2"]}, dims=["id"]
                            )
                        )
                    ]
                ),
            ]
        )
        assert risk.geo("id1").id == "id1"
        assert risk.geo("id2").id == "id2"
        assert risk.geo("id3") is None


class TestSynthesisComponentComposite:
    inputs_dir: Path = Path(__file__).parent / "inputs"

    def test_init_weather_component(self):
        composite = SynthesisCompositeFactory(component=None)
        assert composite.component is None

        component = SynthesisComponentCompositeFactory(weathers=[composite])
        assert component.weathers[0].component is not None

    def test_weather_period(self):
        compo = SynthesisComponentCompositeFactory()
        assert compo.weather_period == PeriodComposite(
            id="period_id", start=Datetime(2023, 3, 1), stop=Datetime(2023, 3, 5)
        )

    def test_alt_area_name(self):
        ds = xr.Dataset(
            {"altAreaName": (["id"], ["area1", "area2"]), "id": ["id1", "id2"]}
        )
        text_compo = SynthesisComponentCompositeFactory(compute_factory=lambda: ds)

        assert text_compo.alt_area_name("id1") == "area1"
        assert text_compo.alt_area_name("id2") == "area2"

    def test_area_name(self):
        ds = xr.Dataset(
            {"areaName": (["id"], ["area1", "area2"]), "id": ["id1", "id2"]}
        )
        text_compo = SynthesisComponentCompositeFactory(compute_factory=lambda: ds)

        assert text_compo.area_name("id1") == "area1"
        assert text_compo.area_name("id2") == "area2"

    def test_compute(self, assert_equals_result):
        lon, lat = [35], [40, 41, 42]
        ids = ["id"]

        # First weather risk_component
        field1 = FieldCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [[1.0, 2.0, 3.0]], coords={"longitude": lon, "latitude": lat}
            ),
            name="T__HAUTEUR2",
        )
        geos1 = GeoCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [[[True, False, False]]],
                coords={"id": ids, "longitude": lon, "latitude": lat},
            ),
            mask_id=ids,
        )

        weather_compo1 = SynthesisCompositeFactory(
            id="tempe", params={"tempe": field1}, geos=geos1
        )

        # Second weather risk_component
        field2 = FieldCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [[4.0, 5.0, 6.0]], coords={"longitude": lon, "latitude": lat}
            ),
            name="T__SOL",
        )
        geos2 = GeoCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [[[False, True, False]]],
                coords={"id": ids, "longitude": lon, "latitude": lat},
            ),
            mask_id=ids,
        )

        weather_compo2 = SynthesisCompositeFactory(
            id="tempe", params={"tempe": field2}, geos=geos2
        )

        # Text Component
        component = SynthesisComponentCompositeFactory(
            geos=["id"], weathers=[weather_compo1, weather_compo2]
        )
        assert_equals_result(component.compute().to_dict())

    @patch("os.environ", {"MFIRE_DISABLE_PRECACHING": True})
    def test_integration(self, assert_equals_result, root_path_cwd):
        data = JsonFile(self.inputs_dir / "small_conf_text.json").load()
        data_prod = next(iter(data.values()))
        component = data_prod["components"][0]
        compo = SynthesisComponentComposite(**component)

        assert_equals_result(compo)


# COMPONENT COMPOSITES


class TestSynthesisComposite:
    def test_wrong_field(self):
        with pytest.raises(
            ValueError,
            match="Wrong field: [], expected ['wwmf', 'precip', 'rain', 'snow', "
            "'lpn']",
        ):
            SynthesisCompositeFactory(id="weather", params={})

    def test_check_condition_without_condition(self):
        weather_compo = SynthesisCompositeFactory()
        assert weather_compo.check_condition("geo_id") is True

    def test_check_condition(self):
        assert SynthesisCompositeFactory().check_condition("...") is True

        synthesis_compo = SynthesisCompositeFactory(
            condition=EventCompositeFactory(
                compute_factory=lambda: xr.DataArray([False, True]),
                geos=GeoCompositeFactory(mask_id=None),
            )
        )
        assert synthesis_compo.check_condition("geo_id") is True
        assert synthesis_compo.condition.geos.mask_id == "geo_id"

        assert (
            SynthesisCompositeFactory(
                condition=EventCompositeFactory(
                    compute_factory=lambda: xr.DataArray([False, False])
                )
            ).check_condition("...")
            is False
        )

    def test_altitude(self):
        weather_compo = SynthesisCompositeFactory(
            id="tempe", params={"tempe": FieldCompositeFactory(grid_name="franxl1s100")}
        )

        assert weather_compo.altitude("weather") is None

        alt = weather_compo.altitude("tempe")
        assert isinstance(alt, xr.DataArray)
        assert alt.name == "franxl1s100"

    def test_geos_data(self):
        geos = GeoCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [1, 2], coords={"id": ["id_1", "id_2"]}
            ),
            mask_id=["id_1", "id_2"],
        )
        weather_compo = SynthesisCompositeFactory(geos=geos)
        assert_identically_close(
            weather_compo.geos_data(),
            xr.DataArray([1, 2], coords={"id": ["id_1", "id_2"]}),
        )
        assert_identically_close(
            weather_compo.geos_data(geo_id="id_1"),
            xr.DataArray(1, coords={"id": "id_1"}),
        )

    @pytest.mark.parametrize("test_file", [{"extension": "nc"}], indirect=True)
    def test_geos_descriptive(self, test_file):
        lon, lat = [31], [40]
        ids = ["id_axis", "id_1", "id_2", "id_axis_altitude", "id_axis_compass"]
        ds = xr.Dataset(
            {
                "A": (
                    ["longitude", "latitude", "id"],
                    [[[True, True, False, True, False]]],
                )
            },
            coords={
                "id": ids,
                "longitude": lon,
                "latitude": lat,
                "areaType": (
                    ["id"],
                    ["areaTypeAxis", "areaType1", "areaType2", "Altitude", "compass"],
                ),
            },
        )
        ds.to_netcdf(test_file)

        weather_compo = SynthesisCompositeFactory(
            geos=GeoCompositeFactory(file=test_file, grid_name="A"),
            localisation=LocalisationConfig(
                geos_descriptive=["id_1", "id_2"],
                compass_split=True,
                altitude_split=True,
            ),
        )
        assert_identically_close(
            weather_compo.geos_descriptive("id_axis"),
            xr.DataArray(
                [[[1.0, np.nan, 1.0, np.nan]]],
                coords={
                    "id": ["id_1", "id_2", "id_axis_altitude", "id_axis_compass"],
                    "longitude": lon,
                    "latitude": lat,
                    "areaName": (["id"], ["unknown", "unknown", "unknown", "unknown"]),
                    "altAreaName": (
                        ["id"],
                        ["unknown", "unknown", "unknown", "unknown"],
                    ),
                    "areaType": (
                        ["id"],
                        ["areaType1", "areaType2", "Altitude", "compass"],
                    ),
                },
                dims=["longitude", "latitude", "id"],
                name="A",
            ),
        )

        weather_compo.localisation.compass_split = False
        weather_compo.localisation.altitude_split = False
        assert_identically_close(
            weather_compo.geos_descriptive("id_axis"),
            xr.DataArray(
                [[[1.0, np.nan]]],
                coords={
                    "id": ["id_1", "id_2"],
                    "longitude": lon,
                    "latitude": lat,
                    "areaName": (["id"], ["unknown", "unknown"]),
                    "altAreaName": (["id"], ["unknown", "unknown"]),
                    "areaType": (["id"], ["areaType1", "areaType2"]),
                },
                dims=["longitude", "latitude", "id"],
                name="A",
            ),
        )

    def test_compute(self, assert_equals_result):
        lon, lat = [35], [40, 41, 42]
        ids = ["id"]

        field = FieldCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [[1.0, 2.0, 3.0]], coords={"longitude": lon, "latitude": lat}
            )
        )
        geos = GeoCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [[[True, False, True]]],
                coords={"id": ids, "longitude": lon, "latitude": lat},
            ),
            mask_id=ids,
        )

        weather_compo = SynthesisCompositeFactory(
            id="tempe", params={"tempe": field}, geos=geos
        )

        assert_equals_result(weather_compo.compute().to_dict())

    def test_compute_with_small_geos(self, assert_equals_result):
        lon, lat = [35], [40, 41, 42]
        ids = ["id"]

        field = FieldCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [[1.0, 2.0, 3.0]], coords={"longitude": lon, "latitude": lat}
            )
        )
        geos = GeoCompositeFactory(
            compute_factory=lambda: xr.DataArray(
                [[[True]]], coords={"id": ids, "longitude": lon, "latitude": [41]}
            ),
            mask_id=ids,
        )

        weather_compo = SynthesisCompositeFactory(
            id="tempe", params={"tempe": field}, geos=geos
        )

        assert_equals_result(weather_compo.compute().to_dict())
