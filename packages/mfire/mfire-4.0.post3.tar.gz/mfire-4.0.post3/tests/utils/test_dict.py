from pathlib import Path

import numpy as np
import pytest

from mfire.utils import recursive_are_equals
from mfire.utils.dict import (
    FormatDict,
    KeyBasedDefaultDict,
    recursive_format,
    recursive_remove_key,
    recursive_replace,
)


class TestDictUtilsFunctions:
    @pytest.mark.parametrize(
        "left,right,kwargs,expected",
        [
            (set(), [], {}, False),  # not same type
            (np.nan, np.nan, {}, True),  # not same type
            (np.nan, 1.0, {}, False),  # not same type
            ({"a": ...}, {}, {}, False),
            ({}, {"a": ...}, {}, False),
            (["a"], [], {}, False),
            (["a"], ["a"], {}, True),
            ([{"id": 1}, {"id": 2}], [{"id": 2}, {"id": 1}], {}, False),
            (
                [
                    {"id": 123, "period": {"id": 123}, "hazard_id": 1},
                    {"id": 123, "period": {"id": 123}, "hazard_id": 2},
                ],
                [
                    {"id": 123, "period": {"id": 123}, "hazard_id": 2},
                    {"id": 123, "period": {"id": 123}, "hazard_id": 1},
                ],
                {},
                True,
            ),
            (
                [
                    {"id": 123, "period": {"id": 123}, "hazard_id": 1, "level": 1},
                    {"id": 123, "period": {"id": 123}, "hazard_id": 1, "level": 2},
                ],
                [
                    {"id": 123, "period": {"id": 123}, "hazard_id": 1, "level": 2},
                    {"id": 123, "period": {"id": 123}, "hazard_id": 1, "level": 1},
                ],
                {},
                True,
            ),
            (set("a"), set("b"), {}, False),
            (set("a"), set("a"), {}, True),
            ("abc", "abc", {}, True),
            ("abc", "def", {}, False),
            ("string {param1}", "string {param2}", {}, False),
            (
                "string {param1}",
                "string {param2}",
                {"param1": "string1", "param2": "string2"},
                False,
            ),
            (
                "string {param1}",
                "string {param2}",
                {"param1": "string1", "param2": "string1"},
                True,
            ),
        ],
    )
    def test_recursive_are_equals(self, left, right, kwargs, expected):
        assert recursive_are_equals(left, right, **kwargs) == expected

    def test_recursive_replace(self):
        dico = {
            "id": "toto",
            "nom": "tata",
            "prenoms": ["tata", "titi"],
            "intro": "Bonjour, je suis tata toto, j'ai 18 ans.",
            "path": Path("folder/tata/file"),
        }
        assert recursive_replace(dico, "tata", "tutu") == {
            "id": "toto",
            "nom": "tutu",
            "prenoms": ["tutu", "titi"],
            "intro": "Bonjour, je suis tutu toto, j'ai 18 ans.",
            "path": Path("folder/tutu/file"),
        }

    def test_recursive_remove_key(self):
        dico = {
            "id": "toto",
            "nom": "tata",
            "prenoms": ["tata", "titi"],
            "recur": {"nom": "tata"},
        }
        assert recursive_remove_key(dico, "nom") == {
            "id": "toto",
            "prenoms": ["tata", "titi"],
            "recur": {},
        }

    @pytest.mark.parametrize(
        "obj,expected",
        [
            (
                "Bonjour, je suis {prenom} {nom}, j'ai {age} ans.",
                "Bonjour, je suis John Doe, j'ai 70 ans.",
            ),
            (
                {
                    "id": "{nom}_{prenom}",
                    "nom": "{nom}",
                    "prenoms": ["{prenom}"],
                    "intro": "Bonjour, je suis {prenom} {nom}, j'ai {age} ans.",
                },
                {
                    "id": "Doe_John",
                    "nom": "Doe",
                    "prenoms": ["John"],
                    "intro": "Bonjour, je suis John Doe, j'ai 70 ans.",
                },
            ),
            (
                ["Votre nom est : {nom}", {"id": "{nom}_{prenom}"}],
                ["Votre nom est : Doe", {"id": "Doe_John"}],
            ),
            (123, 123),
        ],
    )
    def test_recursive_format(self, obj, expected):
        values = {"prenom": "John", "nom": "Doe", "age": 70}
        assert recursive_format(obj, values) == expected


class TestFormatDict:
    def test_missing_key(self):
        dico = {"key1": "value1"}
        with pytest.raises(KeyError, match="key2"):
            "la valeur 1 = {key1}, la valeur 2 = {key2}".format_map(dico)

        dico = FormatDict(dico)
        assert (
            "la valeur 1 = {key1}, la valeur 2 = {key2}".format_map(dico)
            == "la valeur 1 = value1, la valeur 2 = {key2}"
        )


class TestKeyBasedDefaultDict:
    def test_init(self):
        key_based_default_dict = KeyBasedDefaultDict(lambda x: {"key": x})
        assert key_based_default_dict["test"]["key"] == "test"

    def test_no_default_factory(self):
        key_based_default_dict = KeyBasedDefaultDict()
        with pytest.raises(KeyError, match="key"):
            _ = key_based_default_dict["key"]
