from __future__ import annotations

from collections import defaultdict
from functools import cached_property
from typing import Callable, Dict, List, Optional, Tuple, Union

import numpy as np
from pydantic import field_validator

from mfire.composite.component import RiskComponentComposite
from mfire.composite.operator import ComparisonOperator
from mfire.text.base.builder import BaseBuilder
from mfire.text.base.reducer import BaseReducer
from mfire.utils.lpn import Lpn
from mfire.utils.string import _, concatenate_string, get_synonym, split_var_name
from mfire.utils.wwmf import Wwmf

_start_stop_str = "{start} à {stop}"


class RepValueReducer(BaseReducer):
    feminine: bool = False
    plural: bool = False
    differentiate_plain_and_mountain: bool = False

    composite: Optional[RiskComponentComposite] = None

    @field_validator("data", mode="before")
    def check_data(cls, data: dict) -> dict:
        """Validate if data has a var_name key with an accumulated variable as value."""
        var_name: Optional[str] = data.get("var_name")

        if var_name is None:
            raise KeyError("Key 'var_name' not found.")

        return data

    @property
    def phenomenon(self) -> str:
        return ""

    @property
    def def_article(self) -> str:
        """Returns the definite article based on plural and feminine"""
        if self.plural:
            return _("les")
        return _("la") if self.feminine else _("le")

    @property
    def indef_article(self) -> str:
        """Returns the indefinite article based on plural and feminine"""
        if self.plural:
            return _("des")
        return _("une") if self.feminine else _("un")

    @property
    def around_word(self) -> str:
        return _("aux alentours de")

    @staticmethod
    def compare(a: dict, b: dict) -> bool:
        """Compares representative values.

        If the plain values are equals or don't exist, the comparison is based on the
        mountain value.

        Args:
            a (dict): First value to compare
            b (dict): Second value to compare.

        Returns:
            bool: True if dictionary a is the largest, False otherwise.
        """
        try:
            operator = ComparisonOperator(a["plain"]["operator"].strict)
            if not operator.is_order or operator(
                a["plain"]["value"], b["plain"]["value"]
            ):
                return True
            if a["plain"]["value"] != b["plain"]["value"]:
                return False
        except KeyError:
            if (plain_in_a := "plain" in a) or "plain" in b:
                return plain_in_a

        try:
            operator = ComparisonOperator(a["mountain"]["operator"].strict)
            return operator.is_order and operator(
                a["mountain"]["value"], b["mountain"]["value"]
            )
        except KeyError:
            return "mountain" in a

    @staticmethod
    def units(unit: Optional[str]) -> str:
        """
        Get the unity. If None then it returns an empty string
        """
        return unit or ""

    @staticmethod
    def replace_critical(dict_in: Dict) -> Tuple[Optional[float], Optional[float]]:
        op, value, next_critical, threshold = (
            dict_in.get("operator"),
            dict_in.get("value"),
            dict_in.get("next_critical"),
            dict_in.get("threshold"),
        )
        if value is None or op is None:
            return None, None
        op = ComparisonOperator(op)
        if next_critical is not None and op(value, next_critical):
            rep_value = next_critical + np.sign(next_critical - value)
            local = value
        else:
            rep_value = value
            local = (
                threshold
                if dict_in.get("occurrence") and op(threshold, value)
                else None
            )  # handling of too low/high values compared with the threshold(#38212)
        return rep_value, local

    def round(self, x: Optional[float], **_kwargs) -> Optional[str]:
        """
        Make a rounding of the value

        Args:
            x (Optional[float]): Value to round

        Returns:
            [Optional[str]]: String of the rounded value or None if not possible
        """
        return str(x) if x is not None and abs(x) > 1e-6 else None

    @property
    def around(self) -> str:
        """
        Returns a synonym of the around
        """
        return get_synonym(self.around_word)

    @property
    def definite_var_name(self) -> str:
        """Returns the definite var_name name."""
        return f"{self.def_article} {self.phenomenon}"

    @property
    def indefinite_var_name(self) -> str:
        """Returns the indefinite var_name name."""
        return f"{self.indef_article} {self.phenomenon}"

    def _initialize_frmt_table(self) -> dict[str, str]:
        return {
            "var_name": self.phenomenon,
            "definite_var_name": self.definite_var_name,
            "indefinite_var_name": self.indefinite_var_name,
            "feminine": "e" if self.feminine else "",
            "plural": "s" if self.plural else "",
            "around": self.around,
        }

    def _compute_plain_frmt_table(self, frmt_table: dict) -> Optional[str]:
        if "plain" not in self.data:
            return None

        plain_dict = self.data["plain"]
        operator = ComparisonOperator(plain_dict.get("operator"))
        rep_value, local = self.replace_critical(plain_dict)
        rep_plain = self.round(
            rep_value, operator=operator, around=frmt_table["around"]
        )
        if rep_plain is not None:
            if rep_plain != "":
                frmt_table[
                    "plain_value"
                ] = f"{rep_plain} {self.units(plain_dict['units'])}"

            local_plain = self.round(
                local, operator=operator, around=frmt_table["around"]
            )
            if local_plain is not None and local_plain != rep_plain:
                frmt_table[
                    "local_plain_value"
                ] = f"{local_plain} {self.units(plain_dict['units'])}"
        return rep_plain

    def _compute_mountain_frmt_table(self, frmt_table: dict, rep_plain: Optional[str]):
        if "mountain" not in self.data:
            return
        mountain_dict = self.data["mountain"]
        operator = ComparisonOperator(mountain_dict.get("operator"))
        rep_value, local = self.replace_critical(mountain_dict)
        rep_mountain = self.round(
            rep_value, operator=operator, around=frmt_table["around"]
        )
        if rep_mountain is not None and (
            self.differentiate_plain_and_mountain or rep_plain != rep_mountain
        ):
            if rep_mountain != "":
                frmt_table[
                    "mountain_value"
                ] = f"{rep_mountain} {self.units(mountain_dict['units'])}"

            local_mountain = self.round(
                local, operator=operator, around=frmt_table["around"]
            )
            if local_mountain is not None and local_mountain != rep_mountain:
                frmt_table[
                    "local_mountain_value"
                ] = f"{local_mountain} {self.units(self.data['mountain']['units'])}"

    def _compute(self) -> dict:
        """
        Make computation and returns the reduced data.

        Returns:
            dict: Reduced data
        """
        frmt_table: dict[str, str] = self._initialize_frmt_table()

        if (mountain_altitude := self.data.get("mountain_altitude")) is not None:
            frmt_table["altitude"] = mountain_altitude

        rep_plain = self._compute_plain_frmt_table(frmt_table)
        self._compute_mountain_frmt_table(frmt_table, rep_plain)
        return frmt_table


class FFRepValueReducer(RepValueReducer):
    feminine: bool = False
    plural: bool = False

    @property
    def phenomenon(self) -> str:
        return _("vent moyen")

    def round(self, x: Optional[float], **_kwargs) -> Optional[str]:
        """
        Rounds values to the nearest interval of 5.
        Examples:
            Input --> Output
             7.5   -->  5 à 10
             12.5   -->  10 à 15

        Args:
            x (float): Value to round

        Returns:
            [Optional[str]]: Rounded value or None if not possible
        """
        if super().round(x) is None:
            return None
        start = (int(x / 5)) * 5
        stop = start + 5
        return _(_start_stop_str).format(start=start, stop=stop)


class TemperatureRepValueReducer(RepValueReducer):
    feminine: bool = True
    plural: bool = False

    @property
    def phenomenon(self) -> str:
        return _("température")

    def round(self, x: Optional[float], **kwargs) -> Optional[str]:
        """
        Rounds down or up as appropriate.
        Examples:
            Input --> Output
             7.5 + <=  -->  7
             7.5 + >= -->  8

        Args:
            x (float): Value to round

        Returns:
            [Optional[str]]: Rounded value or None if not possible
        """
        if x is None:
            return None
        if ComparisonOperator(kwargs["operator"]).is_decreasing_order:
            return str(int(np.floor(x)))
        return str(int(np.ceil(x)))


class FFRafRepValueReducer(RepValueReducer):
    feminine: bool = True
    plural: bool = True

    @property
    def phenomenon(self) -> str:
        return _("rafales")

    @property
    def around_word(self) -> str:
        return _("de l'ordre de")

    def round(self, x: Optional[float], **kwargs) -> Optional[str]:
        """
        Rounds values to the nearest interval of 10.
        Examples:
            Input                            --> Output
             7.5, around=None                -->  5 à 10
             7.5, around="comprises entre"   -->  5 et 10

        Args:
            x (float): Value to round

        Returns:
            [Optional[str]]: Rounded value or None if not possible
        """
        if super().round(x) is None:
            return None
        start = (int(x / 10)) * 10
        stop = start + 10

        if (around := kwargs["around"]) is not None and around.endswith(_("entre")):
            return _("{start} et {stop}").format(start=start, stop=stop)
        return _(_start_stop_str).format(start=start, stop=stop)


class AccumulationRepValueReducer(RepValueReducer):
    feminine: bool = False
    bounds: List
    last_bound_size: int
    differentiate_plain_and_mountain: bool = True
    merge_locals: bool = True

    @field_validator("data", mode="before")
    def check_data(cls, data: dict) -> dict:
        """Validate if data has a var_name key with an accumulated variable as value."""
        super().check_data(data)

        var_name: str = data["var_name"]

        accumulation: Optional[int] = split_var_name(var_name)[1]

        if not accumulation:
            raise ValueError(f"No accumulation found for '{var_name}' var_name.")

        return data

    @property
    def var_name(self) -> str:
        """Get var_name."""
        return self.data["var_name"]

    @property
    def accumulated_hours(self) -> str:
        """
        Gets the number of hours over which the var_name is accumulated.

        Returns:
            str: Number of hours over which the var_name is accumulated
        """
        accumulation: Optional[int] = split_var_name(self.var_name)[1]
        return "{accumulation}h".format(accumulation=accumulation)

    @property
    def definite_var_name(self) -> str:
        """Returns the definite var_name name."""
        return self.accumulation_time_suffix(f"{self.def_article} {self.phenomenon}")

    @property
    def indefinite_var_name(self) -> str:
        """Returns the indefinite var_name name."""
        return self.accumulation_time_suffix(f"{self.indef_article} {self.phenomenon}")

    @property
    def accumulated_phenomenon(self) -> str:
        """Returns the accumulated var_name name."""
        return self.accumulation_time_suffix(self.phenomenon)

    def accumulation_time_suffix(self, var: str) -> str:
        return _("{var} sur {accumulated_hours}").format(
            var=var, accumulated_hours=self.accumulated_hours
        )

    def _initialize_frmt_table(self) -> dict[str, str]:
        frmt_table: dict[str, str] = super()._initialize_frmt_table()
        frmt_table["var_name"] = self.accumulated_phenomenon
        return frmt_table

    def _value_as_string(self, x: float) -> str:
        for low_bound, up_bound in self.bounds:
            if x < up_bound:
                start, stop = low_bound, up_bound
                break
        else:
            start = int(x / self.last_bound_size) * self.last_bound_size
            stop = start + self.last_bound_size
        return _(_start_stop_str).format(start=start, stop=stop)

    def round(self, x: Optional[float], **_kwargs) -> Optional[str]:
        if x is not None:
            if abs(x) > 1e-6:
                return self._value_as_string(x)
            return ""
        return None

    def _pop_mountain_keys(self, frmt_table: dict) -> None:
        """Remove 'mountain' keys of self.data and frmt_table dictionaries."""
        self.data.pop("mountain")
        frmt_table.pop("mountain_value", None)
        frmt_table.pop("local_mountain_value", None)

    def _compute(self) -> dict:
        frmt_table: dict = super()._compute()

        if self.merge_locals is False:
            return frmt_table

        # Merge plain and mountain local values if it is possible
        if "plain" in self.data and "mountain" in self.data:
            p_value: str = frmt_table.get("plain_value")
            m_value: str = frmt_table.get("mountain_value")
            lp_value: str = frmt_table.get("local_plain_value")
            lm_value: str = frmt_table.get("local_mountain_value")

            if p_value is not None and p_value == m_value:
                self._pop_mountain_keys(frmt_table)
                if lp_value is None and lm_value is not None:
                    frmt_table["plain_value"] += (
                        _(" (localement {lm_value} sur les hauteurs)")
                    ).format(lm_value=lm_value)

            elif (
                p_value is None
                and m_value is None
                and lp_value is not None
                and lp_value == lm_value
            ):
                self._pop_mountain_keys(frmt_table)

        return frmt_table


class SnowRepValueReducer(AccumulationRepValueReducer):
    # List contents of the tuples with the lower limits and the amplitude of the
    # interval
    bounds: List = [(0, 1), (1, 3), (3, 5), (5, 7), (7, 10), (10, 15), (15, 20)]
    last_bound_size: int = 10

    @property
    def phenomenon(self) -> str:
        return _("potentiel de neige")


class FallingWaterRepValueReducer(AccumulationRepValueReducer):
    # List contents of the tuples with the lower limits and the amplitude of the
    # interval
    bounds: List = [
        (3, 7),
        (7, 10),
        (10, 15),
        (15, 20),
        (20, 25),
        (25, 30),
        (30, 40),
        (40, 50),
        (50, 60),
        (60, 80),
        (80, 100),
    ]
    last_bound_size: int = 50

    def round(self, x: Optional[float], **kwargs) -> Optional[str]:
        """
        Rounds the value to the nearest interval.

        Examples:
            Input --> Output
             42   -->  40 to 45
             39   -->  35 to 40
        """
        rounding_val = super().round(x, **kwargs)
        if rounding_val not in [None, ""] and x < 3:
            return _("au maximum") + " 3"
        return rounding_val


class PrecipitationRepValueReducer(FallingWaterRepValueReducer):
    @property
    def phenomenon(self) -> str:
        return _("cumul de précipitation")


class RainRepValueReducer(FallingWaterRepValueReducer):
    @property
    def phenomenon(self) -> str:
        return _("cumul de pluie")


class LpnRepValueReducer(RepValueReducer):
    def _compute(self) -> dict:
        if (
            "LPN__SOL" not in self.composite.params
            or "WWMF__SOL" not in self.composite.params
        ):
            return {}

        geo_da = self.composite.geo(self.geo_id)
        if (
            snow_geo_da := geo_da.where(
                Wwmf.is_snow(self.composite.params["WWMF__SOL"].compute())
            )
        ).count() > 0:
            geo_da = snow_geo_da
        else:
            geo_da = self.composite.risks_of_level(
                self.composite.final_risk_max_level(self.geo_id)
            )[0].spatial_risk_da.sel(id=self.geo_id)
            geo_da = geo_da.where(geo_da > 0)

        lpn_da = self.composite.params["LPN__SOL"].compute() * geo_da
        lpn = Lpn(da=lpn_da, period_describer=self.composite.period_describer)
        if lpn.extremums_da is None:
            return {}

        return {
            "key": lpn.template_key,
            "lpn": lpn.extremums,
            "temp": lpn.temporalities,
        }


class AltitudeRepValueReducer(RepValueReducer):
    """
    This class will represent the sentences "Surveillance client au-dessus/en-dessous de
    xxx m : ...

    """

    @field_validator("data", mode="before")
    def check_data(cls, data: dict) -> dict:
        """Return simply data.

        This validator override RepValueReducer.check_data which verifies that data
        has a key called var_name.
        """
        return data

    @staticmethod
    def get_reducer(var_name: str) -> Optional[Callable]:
        prefix = split_var_name(var_name, full_var_name=False)[0]
        reducers = {
            "FF": FFRepValueReducer,
            "RAF": FFRafRepValueReducer,
            "T": TemperatureRepValueReducer,
            "PRECIP": PrecipitationRepValueReducer,
            "EAU": RainRepValueReducer,
            "NEIPOT": SnowRepValueReducer,
            "LPN": LpnRepValueReducer,
        }
        try:
            return reducers[prefix]
        except KeyError:
            return None

    @staticmethod
    def _compute_loop_new_val(frmt_table, key):
        new_val = frmt_table.get(key, "")
        if new_val:
            new_val = _("de {new_val}").format(new_val=new_val)
        if local_val := frmt_table.get(f"local_{key}"):
            local_val = _("localement de {local_val}").format(local_val=local_val)
            new_val = f"{new_val} ({local_val})" if new_val != "" else local_val
        return new_val

    def _compute_loop(self, values, var_name, data, reducer_class):
        reducer: RepValueReducer = reducer_class(
            data=data | {"var_name": var_name},
            differentiate_plain_and_mountain=True,
            merge_locals=False,
            composite=self.composite,
            geo_id=self.geo_id,
        )

        is_acc = isinstance(reducer, AccumulationRepValueReducer)
        accum = f"{reducer.accumulation_time_suffix('')} " if is_acc else ""
        frmt_table = reducer.compute()

        for key, values_list in values.items():
            if new_val := self._compute_loop_new_val(frmt_table, key):
                values_list.append(accum + new_val)

        if is_acc:
            for zone in {"plain", "mountain"}.intersection(reducer.data.keys()):
                key: str = f"{zone}_value"

                if all((key not in frmt_table, f"local_{key}" not in frmt_table)):
                    values[key].append(accum + _("non significatif"))

    def _compute(self) -> dict:
        """
        Make computation and returns the reduced data.

        Returns:
            dict: Reduced data
        """

        var_name = next(iter(self.data))
        reducer_class = self.get_reducer(var_name)
        if reducer_class is None:
            return {}

        values: dict[str, list] = {"plain_value": [], "mountain_value": []}
        for var_name, data in self.data.items():
            self._compute_loop(values, var_name, data, reducer_class)

        reducer = reducer_class(
            data={"var_name": var_name} | next(iter(self.data.values()))
        )
        frmt_table = reducer.compute()
        frmt_table = {
            "altitude": frmt_table.get("altitude", "xxx"),
            "var_name": reducer.phenomenon,
            "feminine": frmt_table["feminine"],
            "plural": frmt_table["plural"],
        }
        for key, val in values.items():
            if val:
                frmt_table[key] = concatenate_string(val, last_delimiter=f" {_('et')} ")

        return frmt_table


class RepValueBuilder(BaseBuilder):
    """
    This class enable to speak about representative values
    """

    module_name: str = "risk"
    reducer: Optional[RepValueReducer] = None
    reducer_class: type = RepValueReducer
    composite: Optional[RiskComponentComposite] = None

    @property
    def template_name(self) -> str:
        """
        Get the template name.

        Returns:
            str: The template name.
        """
        return "rep_value_generic"

    @property
    def _template_key_not_accumulated(self) -> str:
        """Get the template key for a not accumulated variable."""
        key_parts = []

        if "plain_value" in self.reduction:
            if "local_plain_value" in self.reduction:
                key_parts.append("local")
            key_parts.append("plain")
        if "mountain_value" in self.reduction:
            if "local_mountain_value" in self.reduction:
                key_parts.append("local")
            key_parts.append("mountain")

        return "_".join(key_parts)

    @property
    def _template_key_accumulated(self) -> str:
        """Get the template key for an accumulated variable."""
        key_parts = []

        for zone in filter(lambda v: v in self.reducer.data, ["plain", "mountain"]):
            if f"{zone}_value" not in self.reduction:
                key_parts.append(f"no_acc_{zone}")

                if f"local_{zone}_value" in self.reduction:
                    key_parts.append(f"local_{zone}")
            else:
                if f"local_{zone}_value" in self.reduction:
                    key_parts.append("local")
                key_parts.append(zone)

        return "_".join(key_parts)

    @property
    def template_key(self) -> Optional[Union[str, np.ndarray]]:
        """
        Get the template key.

        Returns:
            Union[str, np.ndarray]: The template key.
        """
        if isinstance(self.reducer, AccumulationRepValueReducer):
            return self._template_key_accumulated
        return self._template_key_not_accumulated

    @classmethod
    def get_builder(cls, data: dict, builder: BaseBuilder) -> Optional[RepValueBuilder]:
        """
        Returns a RepValueBuilder object for the given data dictionary.

        Args:
            data: A dictionary of data, where the keys are the variable names and the
                values are the variable values.

        Returns:
            A RepValueBuilder object for the given data dictionary, or None if no
                builder is available.
        """
        prefix = split_var_name(data["var_name"], full_var_name=False)[0]
        builders = {
            "FF": FFRepValueBuilder,
            "RAF": FFRafRepValueBuilder,
            "T": TemperatureRepValueBuilder,
            "PRECIP": PrecipitationRepValueBuilder,
            "EAU": RainRepValueBuilder,
            "NEIPOT": SnowRepValueBuilder,
            "LPN": LpnRepValueBuilder,
        }
        try:
            return builders[prefix](
                data=data, composite=builder.composite, geo_id=builder.geo_id
            )
        except KeyError:
            return None

    def pre_process(self):
        """Make a pre-process operation on the text."""
        super().pre_process()
        rep_value = self.reduction.get("mountain_value") or self.reduction.get(
            "plain_value", ""
        )

        if rep_value.startswith("au"):
            self.reduction["around"] = "d'"
            self.text = self.text.replace("{around} ", "{around}")

    @staticmethod
    def _compute_all_altitude(all_data: dict, builder: BaseBuilder) -> str:
        altitude_data = defaultdict(dict)
        for key, data in all_data.items():
            altitude_data[split_var_name(key)[0]][key] = data

        text = ""
        for param, data in altitude_data.items():
            if param != "LPN__SOL":
                builder_class = AltitudeRepValueBuilder
            else:
                builder_class = LpnRepValueBuilder
                data |= {"var_name": param}

            if builder_text := builder_class(
                data=data, composite=builder.composite, geo_id=builder.geo_id
            ).compute():
                text += f"\n{builder_text}"

        return text.rstrip()

    @staticmethod
    def _compute_all_no_altitude(all_data: dict, builder: BaseBuilder) -> str:
        text = ""
        for key, data in all_data.items():
            builder_class = RepValueBuilder.get_builder(
                data=data | {"var_name": key}, builder=builder
            )
            if isinstance(builder_class, LpnRepValueBuilder):
                text += "\n"
            if builder_class is not None:
                text += builder_class.compute() + " "
        return text.rstrip()

    @staticmethod
    def compute_all(all_data: dict, builder: BaseBuilder) -> str:
        """
        Calculates a textual representation of all the variables in the given data
        dictionary.

        Args:
            data: A dictionary of data, where the keys are the variable names and the
                values are the variable values.

        Returns:
            A textual representation of all the variables in the data dictionary.
        """
        if not all_data:
            return ""

        # If monitoring with altitude, generate a specific sentence
        if "mountain_altitude" in next(iter(all_data.values())):
            return RepValueBuilder._compute_all_altitude(all_data, builder)

        # Otherwise, generate a sentence for each variable
        return RepValueBuilder._compute_all_no_altitude(all_data, builder)


class FFRepValueBuilder(RepValueBuilder):
    reducer_class: type = FFRepValueReducer


class TemperatureRepValueBuilder(RepValueBuilder):
    reducer_class: type = TemperatureRepValueReducer


class FFRafRepValueBuilder(RepValueBuilder):
    reducer_class: type = FFRafRepValueReducer

    @property
    def template_name(self) -> str:
        """
        Get the template name.

        Returns:
            str: The template name.
        """
        return "rep_value_raf"


class SnowRepValueBuilder(RepValueBuilder):
    reducer_class: type = SnowRepValueReducer


class PrecipitationRepValueBuilder(RepValueBuilder):
    reducer_class: type = PrecipitationRepValueReducer


class RainRepValueBuilder(RepValueBuilder):
    reducer_class: type = RainRepValueReducer


class LpnRepValueBuilder(RepValueBuilder):
    reducer_class: type = LpnRepValueReducer

    @property
    def template_name(self) -> Union[str, List[str]]:
        """
        Get the template name.

        Returns:
            str: The template name.
        """
        return "rep_value_lpn"

    @cached_property
    def template_key(self) -> Optional[Union[str, List, np.ndarray]]:
        """
        Get the template key.

        Returns:
            Union[str, np.ndarray]: The template key.
        """
        return self.reduction.get("key")


class AltitudeRepValueBuilder(RepValueBuilder):
    reducer_class: type = AltitudeRepValueReducer

    @property
    def template_name(self) -> str:
        """
        Get the template name.

        Returns:
            str: The template name.
        """
        return "rep_value_altitude"

    def compute(self) -> str:
        if not self.reduction:
            return ""
        return super().compute()
