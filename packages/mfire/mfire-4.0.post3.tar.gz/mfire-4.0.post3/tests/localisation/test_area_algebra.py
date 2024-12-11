import numpy as np
import pytest

import mfire.utils.mfxarray as xr
from mfire.localisation.area_algebra import (
    GenericArea,
    compute_iol,
    compute_iol_left,
    compute_iou,
    generic_merge,
)
from tests.functions_test import assert_identically_close


class TestAreaAlgebraFunctions:
    def test_compute_iou(self):
        left_da = xr.DataArray([[1, 1], [0, 1]], coords={"lon": [1, 2], "lat": [3, 4]})
        right_da = xr.DataArray(
            [[[1, 0], [1, 0]], [[0, 1], [0, 1]]],
            coords={"id": ["a", "b"], "lon": [1, 2], "lat": [3, 4]},
        )
        assert_identically_close(
            compute_iou(left_da, right_da, dims=("lon", "lat")),
            xr.DataArray([0.25, 2 / 3], coords={"id": ["a", "b"]}),
        )

    def test_compute_iol_left(self):
        left_da = xr.DataArray([[1, 1], [0, 1]], coords={"lon": [1, 2], "lat": [3, 4]})
        right_da = xr.DataArray(
            [[[1, 0], [1, 0]], [[0, 1], [0, 1]]],
            coords={"id": ["a", "b"], "lon": [1, 2], "lat": [3, 4]},
        )
        assert_identically_close(
            compute_iol_left(left_da, right_da, dims=("lon", "lat")),
            xr.DataArray([1 / 3, 2 / 3], coords={"id": ["a", "b"]}),
        )

    def test_generic_merge(self):
        left_da = xr.DataArray([0], coords={"lon": [1]}, name="name")
        right_da = xr.DataArray([1], coords={"lon": [2]}, name="name")
        assert_identically_close(generic_merge(left_da, None), left_da)
        assert_identically_close(generic_merge(None, right_da), right_da)
        assert_identically_close(
            generic_merge(left_da, right_da),
            xr.DataArray([0, 1], coords={"lon": [1, 2]}, name="name"),
        )

    @pytest.mark.parametrize(
        "phenomenon_map,expected",
        [
            # a is excluded since IoL < 25%
            ([[0, 0, 0], [1, 0, 0], [0, 0, 0]], None),
            # a is included since IoL(=0.25) >= 25%
            ([[0, 0, 0], [1, 1, 0], [0, 0, 0]], ["a"]),
            # check the exclusion with a and b
            ([[1, 1, 0], [0, 0, 0], [0, 0, 0]], ["b"]),
            ([[1, 1, 0], [1, 1, 0], [0, 0, 0]], ["a"]),
            ([[1, 0, 0], [0, 0, 0], [0, 0, 0]], ["b"]),
            # several locations (locations are stored according to proportion of
            # phenomenon)
            ([[0, 0, 1], [1, 1, 1], [0, 0, 0]], ["c", "a"]),
            ([[1, 0, 1], [0, 0, 1], [0, 0, 1]], ["c", "b"]),
        ],
    )
    def test_compute_iol(self, phenomenon_map, expected):
        lat = [30, 31, 32]
        lon = [40, 41, 42]
        area_ids = ["a", "b", "c"]

        geos_descriptive = xr.DataArray(
            np.array(
                [
                    [[1, 1, 0], [1, 1, 0], [1, 1, 0]],  # area "a"
                    [[1, 1, 0], [0, 0, 0], [0, 0, 0]],  # area "b"
                    [[0, 0, 1], [0, 0, 1], [0, 0, 1]],  # area "c"
                ]
            ),
            coords={"id": area_ids, "lat": lat, "lon": lon},
        )
        phenomenon_map = xr.DataArray(
            [phenomenon_map], coords={"id": ["id_axis"], "lat": lat, "lon": lon}
        )

        result = compute_iol(geos_descriptive, phenomenon_map, dims=("lat", "lon"))
        if result is not None:
            result = list(result.id.data)

        assert result == expected


class TestGenericArea:
    def test_filter_areas(self):
        area = GenericArea()
        lon, lat = [40, 41], [30, 31]
        ids = ["id_1", "id_2", "id_3", "id_4"]
        area_da = xr.DataArray(
            [[1, 0], [1, 0]], coords={"longitude": lon, "latitude": lat}
        )
        areas_list_da = xr.DataArray(
            [[[0, 1], [0, 1]], [[1, 0], [1, 0]], [[0, 0], [1, 0]], [[1, 0], [0, 0]]],
            coords={"id": ids, "longitude": lon, "latitude": lat},
        )
        assert area.filter_areas(area_da, areas_list_da) == ["id_3", "id_4"]

    def test_alt_kwargs(self):
        area = GenericArea(alt_min=10, alt_max=30)
        assert area.alt_kwargs == {"alt_min": 10, "alt_max": 30}

    @pytest.mark.parametrize(
        "domain_name,sub_area_name,expected",
        [
            (
                "en Isère",
                ["à Grenoble", "entre 1000 m et 1500 m", "entre 1000 m et 2000 m"],
                ["à Grenoble", "entre 1000 m et 1500 m", "au-dessus de 1000 m"],
            ),
            (
                "au-dessus de 1500 m",
                "sur le massif de Belledonne",
                "sur le massif de Belledonne au-dessus de 1500 m",
            ),
            (
                "entre 1500 m et 2000 m",
                "sur le massif de Belledonne",
                "sur le massif de Belledonne au-dessus de 1500 m",
            ),
            ("entre 1000 m et 1800 m", "au-dessus de 1500 m", "entre 1500 m et 1800 m"),
            ("entre 1000 m et 2000 m", "au-dessus de 1500 m", "au-dessus de 1500 m"),
        ],
    )
    def test_rename_inter(self, domain_name, sub_area_name, expected):
        area = GenericArea(alt_min=500, alt_max=2000)
        assert area.rename_inter(domain_name, sub_area_name) == expected

    @pytest.mark.parametrize(
        "domain_name,area_names,expected",
        [
            (
                "en Isère",
                ["à Grenoble", "entre 1000 m et 1500 m", "entre 1000 m et 2000 m"],
                [
                    "comp_à Grenoble",
                    "en dessous de 1000 m et au-dessus de 1500 m",
                    "en dessous de 1000 m",
                ],
            ),
            (
                "au-dessus de 1500 m",
                "sur le massif de Belledonne",
                "au-dessus de 1500 m sauf sur le massif de Belledonne",
            ),
            (
                "entre 1500 m et 2000 m",
                "sur le massif de Belledonne",
                "au-dessus de 1500 m sauf sur le massif de Belledonne",
            ),
            ("entre 1000 m et 1800 m", "au-dessus de 1500 m", "entre 1000 m et 1500 m"),
            ("entre 500 m et 1800 m", "au-dessus de 1500 m", "en dessous de 1500 m"),
        ],
    )
    def test_rename_difference(self, domain_name, area_names, expected):
        area = GenericArea(alt_min=500, alt_max=2000)
        assert area.rename_difference(domain_name, area_names) == expected
