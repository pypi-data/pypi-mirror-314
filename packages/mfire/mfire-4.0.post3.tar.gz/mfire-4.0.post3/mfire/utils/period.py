from __future__ import annotations

from datetime import tzinfo
from typing import Generator, Iterable, Optional, Union

import numpy as np
from pytz import timezone

from mfire.composite.base import BaseModel
from mfire.utils.date import Datetime, Timedelta
from mfire.utils.string import _
from mfire.utils.template import TemplateRetriever


class Period:
    """Period : class describing periods objects defined by :
    - a beginning (self.begin_time)
    - an end (self.end_time)
    """

    def __init__(
        self,
        begin_time: Union[Datetime, str],
        end_time: Optional[Union[Datetime, str]] = None,
    ):
        """__init__ : initialization method

        Args:
            begin_time (Datetime): Beginning of the period.
            end_time (Optional[Datetime], optional): End of the period.
                Defaults to None.
        """
        self._begin_time = Datetime(begin_time)
        self._end_time = self._begin_time
        if end_time is not None:
            self._end_time = Datetime(end_time)
        self._template_retriever = None

    def copy(self) -> Period:
        return Period(self._begin_time, self._end_time)

    def __eq__(self, obj: object) -> bool:
        return (
            isinstance(obj, self.__class__)
            and self.begin_time == obj.begin_time
            and self.end_time == obj.end_time
        )

    def __hash__(self):
        return hash((self.begin_time, self.end_time))

    @property
    def to_json(self) -> dict:
        return {"begin_time": self._begin_time, "end_time": self._end_time}

    @property
    def total_hours(self) -> int:
        return (self.end_time - self.begin_time).total_hours

    @property
    def begin_time(self) -> Datetime:
        """begin_time

        Returns:
            Datetime: Beginning of the period
        """
        return self._begin_time

    @begin_time.setter
    def begin_time(self, begin_time: Datetime):
        """begin_time : self.begin_time setter. Checks the given datetime
        compatibility with self._end_time

        Args:
            begin_time (Datetime): datetime object to initialize the
                self.begin_time object
        """
        if self._begin_time == self._end_time:
            self._end_time = Datetime(begin_time)
        self._begin_time = Datetime(begin_time)
        if self._begin_time > self._end_time:
            self._end_time = self._begin_time

    @property
    def end_time(self) -> Datetime:
        """end_time

        Returns:
            Datetime: End of the period
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: Datetime):
        """end_time : self.end_time setter. Checks the given datetime
        compatibility with the self._begin_time

        Args:
            end_time (Dateime): datetime object to initialize the
                self.end_time object
        """
        if end_time is None:
            end_time = self._begin_time
        self._end_time = Datetime(end_time)
        if self._begin_time > self._end_time:
            self._begin_time = self._end_time

    @property
    def duration(self) -> Timedelta:
        return self.end_time - self.begin_time

    def basic_union(self, period: Period) -> Period:
        """union: creates the basic union of self and a given period.
        Example:
        >>> p1 = Period(Datetime(2021, 1, 1), Datetime(2021, 1, 2))
        >>> p2 = Period(Datetime(2021, 1, 3), Datetime(2021, 1, 4))
        >>> p1.basic_union(p2)
        Period(Datetime(2021, 1, 1), Datetime(2021, 1, 4))

        Args:
            period (Period): given period to unite with self.

        Returns:
            Period: "united" period
        """
        begin_time = min(self.begin_time, period.begin_time)
        end_time = max(self.end_time, period.end_time)
        return self.__class__(begin_time, end_time)

    def union(self, period: Period) -> Periods:
        """union: creates the union of self and a given period.
        Example:
        >>> p1 = Period(Datetime(2021, 1, 1, 10), Datetime(2021, 1, 1, 15))
        >>> p2 = Period(Datetime(2021, 1, 1, 16), Datetime(2021, 1, 1, 18))
        >>> p3 = Period(Datetime(2021, 1, 1, 12), Datetime(2021, 1, 1, 17))
        >>> p1.basic_union(p2)
        Periods([p1, p2])
        >>> p1.basic_union(p3)
        Periods([Period(Datetime(2021, 1, 1, 10), Datetime(2021, 1, 1, 17))])

        Args:
            period (Period): given period to unite with self.

        Returns:
            Periods: union of the period (length 1 if intersection 2 otherwise)
        """
        if self.intersects(period):
            return Periods([self.basic_union(period)])
        if self.begin_time < period.begin_time:
            return Periods([self, period])
        return Periods([period, self])

    def intersects(self, period: Period) -> bool:
        """intersects: checks whether a given period intersects with self.
        Example:
        >>> p1 = Period(Datetime(2021, 1, 1), Datetime(2021, 1, 2))
        >>> p2 = Period(Datetime(2021, 1, 3), Datetime(2021, 1, 4))
        >>> p3 = Period(Datetime(2021, 1, 1, 23), Datetime(2021, 1, 2, 23))
        >>> p1.intersects(p2)
        False
        >>> p1.intersects(p3)
        >>> p1.intersects(p3)
        True
        >>> p2.intersects(p3)
        False

        Args:
            period (Period): given period to check whether it intersects self.

        Returns:
            bool: Whether period intersects with self.
        """
        return (
            period.begin_time <= self.begin_time <= period.end_time
            or self.begin_time <= period.begin_time <= self.end_time
        )

    def intersection(self, period: Period) -> Timedelta:
        """intersection: give the TimeDelta of the intersection a given
        period intersects and self
        Example:
        >>> p1 = Period(Datetime(2021, 1, 1, 10), Datetime(2021, 1, 1, 12))
        >>> p2 = Period(Datetime(2021, 1, 1, 11), Datetime(2021, 1, 1, 15))
        >>> p3 = Period(Datetime(2021, 1, 1, 12), Datetime(2021, 1, 1, 16))
        >>> p1.intersects(p2)
        Timedelta(hours=1)
        >>> p1.intersects(p3)
        Timedelta(hours=0)
        >>> p2.intersects(p3)
        Timedelta(hours=3)

        Args:
            period (Period): given period to do the intersection

        Returns:
            Timedelta: The Timedelta of the intersection between self and period
            or None if no intersection
        """
        if not self.intersects(period):
            return Timedelta(0)
        return Timedelta(
            min(self.end_time, period.end_time)
            - max(self.begin_time, period.begin_time)
        )

    def extends(self, period: Period, request_time: Datetime = None) -> bool:
        """extends: checks whether a given period is an extension of self. We consider
        that a period p1 extends another period p2 if the period (p1 +/- 3H) intersects
        the period (p2 +/- 3H) or if the jonctions have the same textual
        descriptions.
        Example:
        >>> p1 = Period(Datetime(2021, 1, 1), Datetime(2021, 1, 2))
        >>> p2 = Period(Datetime(2021, 1, 3), Datetime(2021, 1, 4))
        >>> p3 = Period(Datetime(2021, 1, 1, 23), Datetime(2021, 1, 2, 23))
        >>> p1.extends(p2)
        False
        >>> p1.extends(p3)
        True
        >>> p2.extends(p3)
        True

        Args:
            period (Period): period to check whether it extends self.
            request_time (Datetime, optional): Point of view for textual
                descriptions. Defaults to None.

        Returns:
            bool: Whether the given period and self extend themselves.
        """
        return (
            period.begin_time - Timedelta(hours=3)
            <= self.begin_time
            <= period.end_time + Timedelta(hours=3)
            or self.begin_time - Timedelta(hours=3)
            <= period.begin_time
            <= self.end_time + Timedelta(hours=3)
            or (
                request_time is not None
                and (
                    self.begin_time.describe(request_time)
                    == period.end_time.describe(request_time)
                    or self.end_time.describe(request_time)
                    == period.begin_time.describe(request_time)
                )
            )
        )

    def describe(
        self, request_time: Datetime, tz: tzinfo = timezone("Europe/Paris")
    ) -> str:
        """describe: provides a textual description of the self period
        according to a given request_time (point of view).

        Args:
            request_time (Datetime): Point of view used for describing
                self.

        Returns:
            str: Textual description of self.
        """
        request_time = Datetime(request_time).astimezone(tz)
        begin_time = self.begin_time.astimezone(tz)
        end_time = self.end_time.astimezone(tz)

        if self.total_hours <= 24:
            begin_diff = Timedelta(begin_time - request_time.midnight).total_hours
            if 0 <= begin_diff <= 31:
                tpl, key = TemplateRetriever.get_by_name("period").get(
                    [
                        1,
                        request_time.hour,
                        begin_diff,
                        Timedelta(end_time - request_time.midnight).total_hours,
                    ],
                    return_centroid=True,
                )
                begin_time = request_time.midnight + Timedelta(hours=int(key[2]))

            else:
                tpl, key = TemplateRetriever.get_by_name("period").get(
                    [
                        0,
                        request_time.hour,
                        begin_time.hour,
                        Timedelta(end_time - begin_time.midnight).total_hours,
                    ],
                    return_centroid=True,
                )
                begin_time = begin_time.replace(hour=int(key[2]))

            if "{weekday" in tpl:
                weekday_p1 = Datetime(begin_time + Timedelta(hours=24))
                weekday_p2 = Datetime(begin_time + Timedelta(hours=48))
                weekday_m1 = Datetime(begin_time - Timedelta(hours=24))

                tpl = tpl.format(
                    weekday=begin_time.weekday_name,
                    weekday_p1=weekday_p1.weekday_name,
                    weekday_p2=weekday_p2.weekday_name,
                    weekday_m1=weekday_m1.weekday_name,
                )
            return tpl

        return TemplateRetriever.table_by_name("date")["literal_period"].format(
            date_1=begin_time.describe(request_time),
            date_2=end_time.describe(request_time),
        )

    def __repr__(self):
        return f"Period(begin_time={self.begin_time}, end_time={self.end_time})"

    def __str__(self):
        return self.__repr__()


class Periods(list[Period]):
    def __init__(self, iterable: Optional[Iterable] = None):
        if iterable is None:
            iterable = []
        super().__init__(iterable)

    def reduce(self, n: Optional[int] = None) -> Periods:
        """
        This function reduces a Periods element
        If n is given, at most n elements are kept
        """
        self[:] = sorted(self, key=lambda x: x.begin_time)
        new_periods = Periods()
        i = 0
        while i < len(self):
            j = i + 1
            max_end_time = self[i].end_time
            while j < len(self) and self[j].begin_time < self[i].end_time:
                max_end_time = max(max_end_time, self[j].end_time)
                j += 1

            new_periods.append(
                Period(begin_time=self[i].begin_time, end_time=max_end_time)
            )
            i = j

        if n is not None:
            while len(new_periods) > n:
                basic_unions = [
                    new_periods[i].basic_union(new_periods[i + 1])
                    for i in range(len(new_periods) - 1)
                ]
                idx = np.argmin([union.total_hours for union in basic_unions])
                new_periods = Periods(
                    new_periods[:idx] + [basic_unions[idx]] + new_periods[idx + 2 :]
                )

        return new_periods

    def __iadd__(self, other):
        new_periods = self + other
        self[:] = new_periods
        return self

    def __add__(self, other) -> Periods:
        if len(self) == 0:
            return other
        if len(other) == 0:
            return self

        new_periods = Periods(super().__add__(other))
        return new_periods.reduce()

    @property
    def begin_time(self):
        return self[0].begin_time

    @property
    def end_time(self):
        return self[-1].end_time

    def all_intersections(self, periods: Periods) -> Generator[Timedelta]:
        """all_intersections: method to generate all intersections with other sequence
        of Period

        Args:
            periods (Periods): Sequence of periods to intersect.
        """
        for p1 in self:
            for p2 in periods:
                inter = p1.intersection(p2)
                if inter:
                    yield inter

    @property
    def total_hours(self) -> int:
        return sum(time_delta.total_hours for time_delta in self.all_timedelta)

    @property
    def total_days(self) -> int:
        if len(self) == 0:
            return 0

        min_start_time = min(p.begin_time for p in self)
        max_end_time = min(p.end_time for p in self)
        return 1 + (max_end_time - min_start_time).days

    @property
    def all_timedelta(self) -> Generator[Timedelta]:
        """all_timedelta: method to generate all delta times"""
        for p in self:
            yield Timedelta(p.end_time - p.begin_time)

    def hours_of_intersection(self, periods: Periods) -> int:
        """hours_of_intersection: method to give the number of hours of intersection
        with another Periods

        Args:
            periods (Periods): Another Periods
        """
        summed_time = Timedelta(0)
        for intersection in self.all_intersections(periods):
            summed_time += intersection
        return summed_time.total_hours

    def hours_of_union(self, periods: Periods) -> int:
        """hours_of_intersection: method to give the number of hours of union with
        another Periods

        Args:
            periods (Periods): Another Periods to make the union.
        """
        hours_inter = self.hours_of_intersection(periods)
        return self.total_hours + periods.total_hours - hours_inter

    def are_same_temporalities(self, *args) -> bool:
        """are_same_temporalities: method indicating if any sequences of periods
        represent the same temporality. Two sequence of periods are the same
        temporality if the overlapping lasts at least 3h and the proportion
        of overlap is at least 25%
        """
        for periods in args:
            hours_inter = self.hours_of_intersection(periods)
            min_hours = min(self.total_hours, periods.total_hours)

            # TS are considered to have same temporalities
            if hours_inter < min(min_hours, 3) or hours_inter / min_hours < 0.25:
                return False
        return True


class PeriodDescriber(BaseModel):
    """Class for describing periods or sequences of periods.
    If a single period is given, the class will simply use the period.describe
    method.
    Else, if a sequence of periods is given, the period describer will first
    try to reduce the number of periods by merging those which extends themselves,
    and then will use the period.describe method on all the reduced periods.

    Args:
        request_time (Datetime): Point of view used for describing the
            given periods
    """

    cover_period: Period
    request_time: Datetime

    def reduce(self, periods: Periods, n: Optional[int] = None) -> Periods:
        """Reduces a sequence of periods to another sequence of periods, where those
        new periods are a merging of previous periods that extends themselves.

        Args:
            periods (Periods): Sequence of periods to reduce.
            n (Optional[int]): number of periods that we want to keep

        Returns:
            Periods: Reduced periods.
        """
        new_periods = Periods()
        if len(periods) == 0:
            return new_periods

        current_period = periods[0]
        for period in periods:
            if period.extends(current_period, self.request_time):
                current_period = current_period.basic_union(period)
            else:
                new_periods += [current_period]
                current_period = period
        new_periods += [current_period]
        return new_periods.reduce(n)

    def describe(self, periods: Union[Periods, Period]) -> str:
        """describe: method for describing periods or sequences of periods.
        If a single period is given, the method will simply use the period.describe
        method.
        Else, if a sequence of periods is given, the period describer will first
        try to reduce the number of periods by merging those which extends themselves,
        and then will use the period.describe method on all the reduced periods.

        Args:
            periods (Union[Periods, Period]): Periods to describe.

        Returns:
            str: Textual description of given period(s)
        """
        if isinstance(periods, Period):
            periods = Periods([periods])

        periods = self.reduce(periods)
        if periods.end_time <= self.cover_period.begin_time + Timedelta(hours=3):
            return _("en début de période")
        if periods.begin_time >= self.cover_period.end_time - Timedelta(hours=3):
            return _("en fin de période")
        if (
            len(periods) == 2
            and periods.begin_time <= self.cover_period.begin_time + Timedelta(hours=3)
        ) and periods.end_time >= self.cover_period.end_time - Timedelta(hours=3):
            return _("jusqu'à {temp1} puis à nouveau à partir de {temp2}").format(
                temp1=periods[0].end_time.describe(self.request_time),
                temp2=periods[1].begin_time.describe(self.request_time),
            )

        if len(periods) > 1:
            from mfire.utils.string import concatenate_string

            return concatenate_string((p.describe(self.request_time) for p in periods))

        if (
            periods.begin_time <= self.cover_period.begin_time
            and periods.end_time >= self.cover_period.end_time
        ):
            return _("sur toute la période")

        return periods[0].describe(self.request_time)
