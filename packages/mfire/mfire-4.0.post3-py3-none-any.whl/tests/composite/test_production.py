from pathlib import Path
from unittest.mock import patch

import pytest

import mfire.utils.mfxarray as xr
from mfire.composite.production import ProductionComposite
from mfire.settings import SETTINGS_DIR
from mfire.utils import recursive_format
from mfire.utils.date import Datetime
from mfire.utils.json import JsonFile
from tests.composite.factories import (
    ProductionCompositeFactory,
    RiskComponentCompositeFactory,
    SynthesisComponentCompositeFactory,
)


class TestProductionComposite:
    inputs_dir: Path = Path(__file__).parent / "inputs"

    def test_sorted_components(self):
        production = ProductionCompositeFactory(
            components=[
                SynthesisComponentCompositeFactory(id="id_1"),
                RiskComponentCompositeFactory(id="id_2"),
                SynthesisComponentCompositeFactory(id="id_3"),
                RiskComponentCompositeFactory(id="id_4"),
            ]
        )
        assert [component.id for component in production.sorted_components] == [
            "id_2",
            "id_4",
            "id_1",
            "id_3",
        ]

    @pytest.mark.parametrize(
        "components,expected",
        [
            # No fog
            ([SynthesisComponentCompositeFactory()], None),
            ([RiskComponentCompositeFactory(hazard_name="Pluies")], None),
            (
                [
                    SynthesisComponentCompositeFactory(),
                    RiskComponentCompositeFactory(hazard_name="Pluies"),
                ],
                None,
            ),
            # No information about fog
            (
                [
                    RiskComponentCompositeFactory(
                        hazard_name="Brouillard",
                        final_risk_da_factory=xr.DataArray(
                            [[1]],
                            coords={
                                "valid_time": [Datetime(2023, 3, 1)],
                                "id": ["id3"],
                            },
                        ),
                    )
                ],
                None,
            ),
            (
                [
                    RiskComponentCompositeFactory(
                        hazard_name="Brouillard",
                        final_risk_da_factory=xr.DataArray(
                            [[1]],
                            coords={
                                "valid_time": [Datetime(2023, 2, 1)],
                                "id": ["id1"],
                            },
                        ),
                    )
                ],
                None,
            ),
            # Mist without occurrence
            (
                [
                    RiskComponentCompositeFactory(
                        hazard_name="Brouillard",
                        final_risk_da_factory=xr.DataArray(
                            [[0]],
                            coords={
                                "valid_time": [Datetime(2023, 3, 1)],
                                "id": ["id1"],
                            },
                        ),
                    )
                ],
                False,
            ),
            # Mist with occurrence
            (
                [
                    SynthesisComponentCompositeFactory(),
                    RiskComponentCompositeFactory(hazard_name="Pluies"),
                    RiskComponentCompositeFactory(
                        hazard_name="Brouillard",
                        final_risk_da_factory=xr.DataArray(
                            [[1, 0]],
                            coords={
                                "valid_time": [Datetime(2023, 3, 1)],
                                "id": ["id1", "id2"],
                            },
                        ),
                    ),
                ],
                True,
            ),
            (
                [
                    SynthesisComponentCompositeFactory(),
                    RiskComponentCompositeFactory(hazard_name="Pluies"),
                    RiskComponentCompositeFactory(
                        hazard_name="Brouillard",
                        final_risk_da_factory=xr.DataArray(
                            [[0, 1]],
                            coords={
                                "valid_time": [Datetime(2023, 3, 1)],
                                "id": ["id1", "id2"],
                            },
                        ),
                    ),
                ],
                True,
            ),
        ],
    )
    def test_has_risk(self, components, expected):
        valid_time_slice = slice(Datetime(2023, 3, 1), Datetime(2023, 3, 1, 2))
        assert (
            ProductionCompositeFactory(components=components).has_risk(
                "Brouillard", valid_time_slice=valid_time_slice, ids=["id1", "id2"]
            )
            == expected
        )

    def test_compute(self):
        production = ProductionCompositeFactory(
            components=[
                RiskComponentCompositeFactory(geos=["geo1"]),
                RiskComponentCompositeFactory(
                    geos=["geo2"],
                    compute_factory=lambda: xr.Dataset(
                        {"A": ("B", [1])},
                        coords={"B": [1]},  # we force to have non-empty risk
                    ),
                ),
                SynthesisComponentCompositeFactory(
                    geos=["geo3"], compute_factory=lambda: "not_null"
                ),
            ]
        )
        with patch(
            "mfire.text.manager.Manager.compute",
            lambda text_manager, geo_id: f"Texte type={text_manager.component.type} "
            f"pour geo {geo_id}",
        ):
            assert production.compute() == [
                None,
                {"geo2": "Texte type=risk pour geo geo2"},
                {"geo3": "Texte type=text pour geo geo3"},
            ]

    @patch("os.environ", {"MFIRE_DISABLE_PRECACHING": True})
    @pytest.mark.parametrize("config", ["small_conf_text.json", "small_conf_risk.json"])
    def test_integration(self, root_path_cwd, config, assert_equals_result):
        # We need to CWD in root since we load an altitude field
        data = JsonFile(self.inputs_dir / config).load()
        data_prod = next(iter(data.values()))
        prod = ProductionComposite(
            **recursive_format(data_prod, values={"settings_dir": SETTINGS_DIR})
        )

        assert_equals_result(prod)
