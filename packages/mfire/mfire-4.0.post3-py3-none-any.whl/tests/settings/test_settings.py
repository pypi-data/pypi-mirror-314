import os
from unittest.mock import patch

import numpy as np
import pytest

from mfire.settings import Settings


class TestSettings:
    def test_random_choice(self):
        np.random.seed(0)
        settings = Settings()
        settings.disable_random = True
        assert settings.random_choice(["a", "b"]) == "a"
        assert settings.random_choice(["a", "b"]) == "a"
        settings.disable_random = False
        assert settings.random_choice(["a", "b"]) == "a"
        assert settings.random_choice(["a", "b"]) == "b"

    @patch("os.environ", {"mfire_test": "test"})
    def test_clean(self):
        assert os.environ["mfire_test"] == "test"
        Settings().clean()
        assert "mfire_test" not in os.environ

    @patch("os.environ", {})
    def test_set(self):
        Settings().set(config_filename="test1", mask_config_filename="test_2")
        assert os.environ == {
            "mfire_config_filename": "test1",
            "mfire_mask_config_filename": "test_2",
        }

    def test_set_language_fails(self):
        with pytest.raises(ValueError, match="Language ch not supported"):
            Settings.set_language("ch")

    def test_translate(self):
        assert Settings.translate("en dessous de") == "en dessous de"
        Settings.set_language("en")
        assert Settings.translate("en dessous de") == "under"
        Settings.set_language("es")
        assert Settings.translate("en dessous de") == "por debajo"

    def test_grid_names(self):
        assert (
            Settings().grid_names().sort()
            == [
                "eurw1s100",
                "eurw1s40",
                "franxl1s100",
                "glob01",
                "glob025",
                "globd01",
                "globd025",
            ].sort()
        )

    def test_default_settings(self):
        assert Settings().disable_random is False
        assert Settings().disable_parallel is False
