from __future__ import annotations

import csv
from ast import literal_eval
from enum import Enum
from typing import Dict, Iterable, List, Optional, Set, Tuple, Union

import mfire.utils.mfxarray as xr
from mfire.utils.string import concatenate_string, decapitalize
from mfire.utils.template import TemplateRetriever


class Wwmf:
    @staticmethod
    def is_severe(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
        """Check if the given WWMF code represents a severe weather phenomenon"""
        return (wwmf == 49) | (wwmf == 59) | (wwmf == 85) | (wwmf == 98) | (wwmf == 99)

    @staticmethod
    def is_visibility(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
        """Check if the given WWMF code represents visibility"""
        return (30 <= wwmf) & (wwmf <= 39)

    @staticmethod
    def is_precipitation(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
        """Check if the given WWMF codes represents precipitation"""
        return (40 <= wwmf) & (wwmf <= 99)

    @staticmethod
    def is_snow(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
        """Check if the given WWMF code belongs to the snow family"""
        return (wwmf == 58) | (60 <= wwmf) & (wwmf <= 63) | (77 <= wwmf) & (wwmf <= 83)

    @staticmethod
    def is_rain(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
        """Check if the given WWMF code belongs to the rain family"""
        return (40 <= wwmf) & (wwmf <= 59) | (70 <= wwmf) & (wwmf <= 78) | (wwmf == 93)

    @staticmethod
    def is_shower(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
        """Check if the given WWMF code belongs to the shower family"""
        return (70 <= wwmf) & (wwmf <= 85) | (wwmf == 92)

    @staticmethod
    def is_thunderstorm(wwmf: Union[int, xr.DataArray]) -> Union[bool, xr.DataArray]:
        """Check if the given WWMF code belongs to the thunderstorm family"""
        return (wwmf == 84) | (wwmf == 85) | (90 <= wwmf) & (wwmf <= 99)

    class Family(Enum):
        """Enumeration of all families and subfamilies of weather phenomena."""

        VISIBILITY = 0
        RAIN = 1
        SNOW = 2
        SHOWER = 3
        THUNDERSTORM = 4

    class Subgrp(Enum):
        """Enumeration of some grouping of labels for weather phenomena."""

        A1 = (40, 50, 51, 52, 53)
        A2 = (58, 60, 61, 62, 63)
        A3 = (70, 71, 72, 73)
        A4 = (77, 78, 80, 81, 82, 83)
        A5 = (90, 91, 92, 93, 97)
        B1 = (49, 59)
        B2 = (84,)
        B3 = (85,)
        B4 = (98,)
        B5 = (99,)

        @classmethod
        @property
        def B_group(cls) -> List[int]:
            return sum(
                (list(b.value) for b in [cls.B1, cls.B2, cls.B3, cls.B4, cls.B5]),
                start=[],
            )

        @classmethod
        def split_groups(cls, *wwmfs: int) -> Tuple[list, list]:
            group_a, group_b = [], []
            for wwmf in wwmfs:
                if wwmf in cls.B_group:
                    group_b.append(wwmf)
                else:
                    group_a.append(wwmf)
            return group_a, group_b

    @staticmethod
    def families(*wwmfs: Union[int, Wwmf.Subgrp]) -> Set[Wwmf.Family]:
        """Identify the families of weather phenomena represented by the given WWMF
        codes.

        Args:
            *wwmfs: Variable number of WWMF codes to check.

        Returns:
            Tuple[Wwmf.Family, ...]: Tuple of WWMF families represented by the given
            codes.
        """
        families = set()
        funcs = {
            Wwmf.is_visibility: Wwmf.Family.VISIBILITY,
            Wwmf.is_rain: Wwmf.Family.RAIN,
            Wwmf.is_snow: Wwmf.Family.SNOW,
            Wwmf.is_shower: Wwmf.Family.SHOWER,
            Wwmf.is_thunderstorm: Wwmf.Family.THUNDERSTORM,
        }
        for func, family in funcs.items():
            for wwmf in wwmfs:
                if isinstance(wwmf, Wwmf.Subgrp):
                    families |= Wwmf.families(*wwmf.value)
                elif func(wwmf):
                    families.add(family)
                    break
        return families

    @staticmethod
    def subfamilies(*wwmfs: int) -> Tuple[Wwmf.Subgrp, ...]:
        """Identify the subfamilies of weather phenomena represented by the given WWMF
        codes.

        Args:
            *wwmfs: Variable number of WWMF codes to check.

        Returns:
            Tuple[Wwmf.Subgrp, ...]: Tuple of WWMF subfamilies represented by the given
            codes.
        """
        return tuple(
            subgroup for subgroup in Wwmf.Subgrp if set(subgroup.value) & set(wwmfs)
        )

    @staticmethod
    def labels() -> Dict[Tuple, str]:
        return Wwmf._load_labels("wwmf_labels")

    @staticmethod
    def labels_no_risk() -> Dict[Tuple, str]:
        return Wwmf._load_labels("wwmf_labels_no_risk")

    @staticmethod
    def grouped_label(*wwmfs: int, labels: Dict) -> Optional[str]:
        wwmfs = sorted(wwmfs)
        if len(wwmfs) >= 3 and all(Wwmf.is_precipitation(ts) for ts in wwmfs):
            try:
                return labels[Wwmf.subfamilies(*wwmfs)]
            except KeyError:
                return None

        for key, value in labels.items():
            if len(key) != len(wwmfs):
                continue
            if all(
                arg in key[i] if isinstance(key[i], Iterable) else arg == key[i]
                for i, arg in enumerate(wwmfs)
            ):
                return value
        return None

    @staticmethod
    def label(
        *wwmfs: int, labels: Optional[Dict] = None, concatenate: bool = True
    ) -> Optional[str]:
        """Find the label for the given WWMF codes.

        Args:
            *wwmfs (int): Variable number of WWMF codes to generate a label for.
            labels (Dict): Dictionary mapping a label according code(s) or group(s).
            concatenate (bool): Indicates if the final result should be concatenated
                labels if not found

        Returns:
            Optional[str]: Generated label for the given WWMF codes, or None if no match
            is found.
        """
        if labels is None:
            labels = Wwmf.labels()

        if len(wwmfs) == 1:
            return labels.get((wwmfs[0],), None)

        if grouped_label := Wwmf.grouped_label(*wwmfs, labels=labels):
            return grouped_label

        if not concatenate:
            return None

        result = concatenate_string(
            [labels[(wwmfs[0],)]] + [decapitalize(labels[(arg,)]) for arg in wwmfs[1:]]
        )
        result = (
            result.replace(" {loc}", "")
            .replace(" {locOrages}", "")
            .replace(" {locNeige}", "")
            + " {loc}"
        )
        return result

    @staticmethod
    def _load_labels(template: str) -> Dict[Tuple, str]:
        result = {}

        def _cast(elt):
            try:
                return literal_eval(elt)
            except ValueError:
                return Wwmf.Subgrp[elt]

        with open(TemplateRetriever.path_by_name(template)) as fp:
            reader = csv.reader(fp)
            for row in reader:
                result[tuple(_cast(elt) for elt in row[:-1] if elt != "")] = row[-1]
        return result
