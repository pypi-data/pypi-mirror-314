import xarray as xr

from mfire.utils.date import Datetime
from tests.composite.factories import (
    GeoCompositeFactory,
    SynthesisComponentCompositeFactory,
    SynthesisCompositeFactory,
    SynthesisCompositeInterfaceFactory,
)
from tests.functions_test import assert_identically_close
from tests.text.synthesis.factories import SynthesisReducerFactory
from tests.utils.factories import PeriodDescriberFactory


class TestSynthesisReducer:
    def test_period_describer(self):
        period_describer = PeriodDescriberFactory()
        reducer = SynthesisReducerFactory(
            composite=SynthesisCompositeFactory(
                component=SynthesisComponentCompositeFactory(
                    period_describer_factory=period_describer
                )
            )
        )
        assert reducer.period_describer == period_describer

    def test_has_risk(self):
        weather_compo = SynthesisCompositeFactory(
            compute_factory=lambda **_kwargs: xr.DataArray(
                [0, 1, 2],
                coords={
                    "valid_time": [Datetime(2023, 3, 1, i).as_np_dt64 for i in range(3)]
                },
            ),
            geos=GeoCompositeFactory(all_sub_areas_factory=lambda _: ["Sub Areas"]),
            interface=SynthesisCompositeInterfaceFactory(
                has_risk=lambda x, y, z: (x, y, z)
            ),
        )
        reducer = SynthesisReducerFactory(composite=weather_compo)

        assert_identically_close(
            reducer.has_risk("Risk name"),
            (
                "Risk name",
                ["Sub Areas"],
                slice(
                    Datetime(2023, 3, 1).as_np_dt64, Datetime(2023, 3, 1, 2).as_np_dt64
                ),
            ),
        )

    def test_has_field(self):
        weather_compo = SynthesisCompositeFactory(
            geos=GeoCompositeFactory(all_sub_areas_factory=lambda _: ["Sub Areas"]),
            interface=SynthesisCompositeInterfaceFactory(
                has_field=lambda x, y, z: (x, y, z)
            ),
        )
        reducer = SynthesisReducerFactory(composite=weather_compo)

        assert_identically_close(
            reducer.has_field("Risk name", "Field"),
            ("Risk name", "Field", ["Sub Areas"]),
        )
