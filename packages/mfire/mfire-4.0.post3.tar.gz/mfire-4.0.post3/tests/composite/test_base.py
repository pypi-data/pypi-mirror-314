from unittest.mock import patch

import pytest

import mfire.utils.mfxarray as xr
from mfire.composite.base import BaseModel
from tests.composite.factories import BaseCompositeFactory
from tests.functions_test import assert_identically_close


class TestBaseModel:
    class BaseModelFactory(BaseModel):
        a: list = [1, 2]

    def test_model_copy(self):
        # Test of deep=True argument in model_copy
        model1 = self.BaseModelFactory()
        model2 = model1.model_copy()
        model1.a.append(3)
        assert model2.a == [1, 2]


class TestBaseComposite:
    basic_data = xr.DataArray([1, 2, 3])

    def test_data(self):
        composite = BaseCompositeFactory()
        assert composite.data is None
        composite._data = self.basic_data
        assert_identically_close(composite.data, self.basic_data)

    def test_hash(self, assert_equals_result):
        assert_equals_result(BaseCompositeFactory().hash)

    def test_reset(self):
        # Test deletion of self._data
        composite = BaseCompositeFactory()
        composite._data = self.basic_data
        composite.reset()

        assert composite.compute() is None

        # Test of deletion of cache
        path = composite.cached_filename("data")
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w") as file:
            file.close()

        assert path.exists()
        composite.reset()
        assert not path.exists()

    def test_is_cached(self):
        composite = BaseCompositeFactory()
        assert composite.is_cached is False

        path = composite.cached_filename("data")
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w") as file:
            file.close()
        assert composite.is_cached is True

        composite.factories["cached_attrs"] = {}
        assert composite.is_cached is False

    def test_load_cache(self, tmp_path_cwd):
        composite = BaseCompositeFactory()
        with pytest.raises(
            FileNotFoundError,
            match="BaseCompositeFactory not cached, you must compute it before.",
        ):
            composite.load_cache()

        path = composite.cached_filename("data")
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w") as f:
            f.close()

        assert composite.load_cache() is False
        assert composite._data is None

        self.basic_data.to_netcdf(path)
        assert composite.load_cache() is True
        assert_identically_close(composite._data, self.basic_data)

    def test_dump_cache(self, tmp_path_cwd):
        output_folder = tmp_path_cwd / "cache" / "BaseCompositeFactory"

        # Fail to dump
        composite = BaseCompositeFactory()
        composite.dump_cache()
        assert len(list(output_folder.iterdir())) == 0

        # Dump basic data
        composite._data = self.basic_data
        composite.dump_cache()

        assert output_folder.exists()
        output_file = list(output_folder.iterdir())
        assert len(output_file) == 1
        assert_identically_close(xr.open_dataarray(output_file[0]), self.basic_data)

    def test_compute(self, tmp_path_cwd):
        # Behavior by default: data are not kept
        compo = BaseCompositeFactory()
        compo._data = self.basic_data
        assert_identically_close(compo.compute(), self.basic_data)
        assert compo.compute() is None

        # When data are kept
        compo._data = self.basic_data
        compo._keep_data = True
        assert_identically_close(compo.compute(), self.basic_data)
        assert_identically_close(compo.compute(), self.basic_data)

        # Test the kwargs _keep_data
        compo = BaseCompositeFactory()
        compo._data = self.basic_data
        assert_identically_close(compo.compute(keep_data=True), self.basic_data)
        assert_identically_close(compo.compute(), self.basic_data)
        assert compo.compute() is None

        # Test the dumping kwargs possibility
        assert not (tmp_path_cwd / "cache").exists()
        compo = BaseCompositeFactory()

        with patch(
            "mfire.composite.base.BaseComposite._compute",
            lambda *args, **kwargs: self.basic_data,
        ):
            compo.compute(save_cache=True)
            output_file = list(
                (tmp_path_cwd / "cache" / "BaseCompositeFactory").iterdir()
            )
            assert len(output_file) == 1
            assert_identically_close(xr.open_dataarray(output_file[0]), self.basic_data)
