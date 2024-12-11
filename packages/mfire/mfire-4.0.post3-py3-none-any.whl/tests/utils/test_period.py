import pytest

from mfire.settings import Settings
from mfire.utils.date import Datetime, Timedelta
from mfire.utils.period import Period, PeriodDescriber, Periods


class TestPeriod:
    _p1 = Period(Datetime(2021, 1, 1), Datetime(2021, 1, 2))
    _p2 = Period(Datetime(2021, 1, 3), Datetime(2021, 1, 4))
    _p3 = Period(Datetime(2021, 1, 1, 23), Datetime(2021, 1, 2, 23))
    _p4 = Period(Datetime(2021, 1, 1, 10), Datetime(2021, 1, 1, 12))
    _p5 = Period(Datetime(2021, 1, 1, 11), Datetime(2021, 1, 1, 15))
    _p6 = Period(Datetime(2021, 1, 1, 12), Datetime(2021, 1, 1, 16))

    _d1 = Datetime(2021, 1, 1, 20)
    _d2 = Datetime(2021, 1, 2, 12)
    _d3 = Datetime(2021, 1, 5, 9)
    _d4 = Datetime(2021, 2, 1, 9)
    _d5 = Datetime(2021, 1, 1, 18)

    def test_init(self):
        assert isinstance(self._p1, Period)
        assert isinstance(Period(Datetime(2021, 4, 17)), Period)
        assert isinstance(Period("20210417"), Period)

        assert hash(self._p1) == -7293705823702154491
        assert self._p1.to_json == {
            "begin_time": Datetime(2021, 1, 1),
            "end_time": Datetime(2021, 1, 2),
        }
        assert (
            str(self._p1) == "Period(begin_time=2021-01-01T00:00:00+00:00, "
            "end_time=2021-01-02T00:00:00+00:00)"
        )

    @pytest.mark.parametrize(
        "period,begin_time,expected",
        [
            (_p2, _d1, Period(_d1, Datetime(2021, 1, 4))),
            (_p2, _d3, Period(_d3, _d3)),
            (Period(_d1, _d1), _d3, Period(_d3, _d3)),
        ],
    )
    def test_set_begin_time(self, period, begin_time, expected):
        period = period.copy()
        period.begin_time = begin_time
        assert period == expected

    @pytest.mark.parametrize(
        "period,end_time,expected",
        [
            (_p2, _d1, Period(_d1, _d1)),
            (_p2, _d3, Period(Datetime(2021, 1, 3), _d3)),
            (Period(_d3, _d3), _d1, Period(_d1, _d1)),
            (Period(_d1, _d3), None, Period(_d1, _d1)),
        ],
    )
    def test_set_end_time(self, period, end_time, expected):
        period = period.copy()
        period.end_time = end_time
        assert period == expected

    @pytest.mark.parametrize(
        "p1,p2,expected",
        [
            (_p1, _p2, Period("20210101", "20210104")),
            (_p2, _p1, Period("20210101", "20210104")),
            (_p1, _p3, Period("20210101", "202101022300")),
            (_p2, _p3, Period("202101012300", "20210104")),
        ],
    )
    def test_basic_union(self, p1, p2, expected):
        assert p1.basic_union(p2) == expected

    @pytest.mark.parametrize(
        "p1,p2,expected",
        [
            (_p1, _p2, Periods([_p1, _p2])),
            (_p2, _p1, Periods([_p1, _p2])),
            (
                _p4,
                _p5,
                Periods([Period(Datetime(2021, 1, 1, 10), Datetime(2021, 1, 1, 15))]),
            ),
            (
                _p4,
                _p6,
                Periods([Period(Datetime(2021, 1, 1, 10), Datetime(2021, 1, 1, 16))]),
            ),
        ],
    )
    def test_union(self, p1, p2, expected):
        assert p1.union(p2) == expected

    @pytest.mark.parametrize(
        "p1,p2,expected", [(_p1, _p2, False), (_p1, _p3, True), (_p2, _p3, True)]
    )
    def test_extends(self, p1, p2, expected):
        assert p1.extends(p2) is expected

    @pytest.mark.parametrize(
        "p1,p2,expected", [(_p1, _p2, False), (_p1, _p3, True), (_p2, _p3, False)]
    )
    def test_intersects(self, p1, p2, expected):
        assert p1.intersects(p2) is expected

    @pytest.mark.parametrize(
        "p1,p2,expected",
        [
            (_p4, _p5, Timedelta(hours=1)),
            (_p4, _p2, Timedelta(hours=0)),
            (_p5, _p6, Timedelta(hours=3)),
        ],
    )
    def test_intersection(self, p1, p2, expected):
        assert p1.intersection(p2) == expected

    def test_describe(self, assert_equals_result):
        assert_equals_result(
            {
                language: {
                    str((begin_time, end_time)): Period(begin_time, end_time).describe(
                        Datetime(2021, 1, 1, 12)
                    )
                    for begin_time, end_time in [
                        (self._d5, self._d1),
                        (self._d5, self._d2),
                        (self._d5, self._d3),
                        (self._d5, self._d4),
                    ]
                }
                for language in Settings.iter_languages()
            }
        )

    def test_describe_after_midnight(self):
        # This test ensures that period after midnight are well described
        assert (
            Period(Datetime(2024, 7, 21), Datetime(2024, 7, 21, 22)).describe(
                Datetime(2024, 7, 20, 23)
            )
            == "jusqu'en cours de nuit de dimanche à lundi"
        )


class TestPeriods:
    def test_properties(self):
        periods = Periods(
            [
                Period(Datetime(2021, 1, 1, 5), Datetime(2021, 1, 1, 8)),
                Period(Datetime(2021, 1, 1, 12), Datetime(2021, 1, 1, 15)),
            ]
        )
        assert periods.begin_time == Datetime(2021, 1, 1, 5)
        assert periods.end_time == Datetime(2021, 1, 1, 15)

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (
                [Period(Datetime(2021, 1, 1, 5), Datetime(2021, 1, 1, 8))],
                [],
                [Period(Datetime(2021, 1, 1, 5), Datetime(2021, 1, 1, 8))],
            ),
            (
                [],
                [Period(Datetime(2021, 1, 1, 5), Datetime(2021, 1, 1, 8))],
                [Period(Datetime(2021, 1, 1, 5), Datetime(2021, 1, 1, 8))],
            ),
            (
                [
                    Period(Datetime(2021, 1, 1, 5), Datetime(2021, 1, 1, 8)),
                    Period(Datetime(2021, 1, 1, 12), Datetime(2021, 1, 1, 15)),
                ],
                [
                    Period(Datetime(2021, 1, 1, 6), Datetime(2021, 1, 1, 9)),
                    Period(Datetime(2021, 1, 1, 10), Datetime(2021, 1, 1, 11)),
                    Period(Datetime(2021, 1, 1, 14), Datetime(2021, 1, 1, 19)),
                ],
                [
                    Period(Datetime(2021, 1, 1, 5), Datetime(2021, 1, 1, 9)),
                    Period(Datetime(2021, 1, 1, 10), Datetime(2021, 1, 1, 11)),
                    Period(Datetime(2021, 1, 1, 12), Datetime(2021, 1, 1, 19)),
                ],
            ),
        ],
    )
    def test_add(self, a, b, expected):
        assert Periods(a) + Periods(b) == Periods(expected)

        p = Periods(a)
        p += Periods(b)
        assert p == Periods(expected)

    @pytest.mark.parametrize(
        "dates,expected",
        [
            # Union of two datetimes without covering
            (
                [
                    Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 6)),
                    Period(Datetime(2023, 3, 4, 8), Datetime(2023, 3, 4, 12)),
                ],
                [
                    Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 6)),
                    Period(Datetime(2023, 3, 4, 8), Datetime(2023, 3, 4, 12)),
                ],
            ),
            # Union of two datetimes with covering
            (
                [
                    Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 10)),
                    Period(Datetime(2023, 3, 4, 8), Datetime(2023, 3, 4, 12)),
                ],
                [Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 12))],
            ),
            # Union of two datetimes unsorted
            (
                [
                    Period(Datetime(2023, 3, 4, 8), Datetime(2023, 3, 4, 12)),
                    Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 10)),
                ],
                [Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 12))],
            ),
            # Repetition of two datetimes
            (
                [
                    Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 10)),
                    Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 10)),
                ],
                [Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 10))],
            ),
        ],
    )
    def test_reduce_without_n(self, dates, expected):
        periods = Periods(dates)
        assert periods.reduce() == Periods(expected)

    @pytest.mark.parametrize(
        "dates,expected",
        [
            # Reduce the two first
            (
                [
                    Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 10)),
                    Period(Datetime(2023, 3, 4, 11), Datetime(2023, 3, 4, 13)),
                    Period(Datetime(2023, 3, 4, 19), Datetime(2023, 3, 4, 20)),
                ],
                [
                    Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 13)),
                    Period(Datetime(2023, 3, 4, 19), Datetime(2023, 3, 4, 20)),
                ],
            ),
            # Reduce the two last
            (
                [
                    Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 10)),
                    Period(Datetime(2023, 3, 4, 15), Datetime(2023, 3, 4, 18)),
                    Period(Datetime(2023, 3, 4, 19), Datetime(2023, 3, 4, 20)),
                ],
                [
                    Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 10)),
                    Period(Datetime(2023, 3, 4, 15), Datetime(2023, 3, 4, 20)),
                ],
            ),
            # Reduce the third first
            (
                [
                    Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 8)),
                    Period(Datetime(2023, 3, 4, 11), Datetime(2023, 3, 4, 13)),
                    Period(Datetime(2023, 3, 4, 14), Datetime(2023, 3, 4, 15)),
                    Period(Datetime(2023, 3, 4, 22), Datetime(2023, 3, 4, 23)),
                ],
                [
                    Period(Datetime(2023, 3, 4, 4), Datetime(2023, 3, 4, 15)),
                    Period(Datetime(2023, 3, 4, 22), Datetime(2023, 3, 4, 23)),
                ],
            ),
        ],
    )
    def test_reduce_with_n(self, dates, expected):
        periods = Periods(dates)
        assert periods.reduce(n=2) == Periods(expected)

    @pytest.mark.parametrize(
        "periods,expected",
        [
            (
                [
                    Period(Datetime(2021, 1, 1, 5), Datetime(2021, 1, 1, 8)),
                    Period(Datetime(2021, 1, 1, 11), Datetime(2021, 1, 1, 15)),
                ],
                7,
            ),
            (
                [
                    Period(Datetime(2021, 1, 1, 5), Datetime(2021, 1, 2, 8)),
                    Period(Datetime(2021, 1, 2, 11), Datetime(2021, 1, 2, 15)),
                ],
                31,
            ),
        ],
    )
    def test_total_hours(self, periods, expected):
        assert Periods(periods).total_hours == expected

    @pytest.mark.parametrize(
        "periods,expected",
        [
            ([], 0),
            (
                [
                    Period(Datetime(2021, 1, 1, 5), Datetime(2021, 1, 1, 8)),
                    Period(Datetime(2021, 1, 1, 11), Datetime(2021, 1, 1, 15)),
                ],
                1,
            ),
            (
                [
                    Period(Datetime(2021, 1, 1, 5), Datetime(2021, 1, 2, 8)),
                    Period(Datetime(2021, 1, 2, 11), Datetime(2021, 1, 2, 15)),
                ],
                2,
            ),
        ],
    )
    def test_total_days(self, periods, expected):
        assert Periods(periods).total_days == expected

    def test_all_intersections(self):
        p1 = Periods(
            [
                Period(Datetime(2023, 3, 1, 5), Datetime(2023, 3, 1, 10)),
                Period(Datetime(2023, 3, 1, 16), Datetime(2023, 3, 1, 19)),
            ]
        )
        p2 = Periods(
            [
                Period(Datetime(2023, 3, 1, 8), Datetime(2023, 3, 1, 12)),
                Period(Datetime(2023, 3, 1, 15), Datetime(2023, 3, 1, 20)),
            ]
        )

        assert list(p1.all_intersections(p2)) == [
            Timedelta(hours=2),
            Timedelta(hours=3),
        ]

    def test_hours_of_intersection(self):
        p1 = Periods(
            [
                Period(Datetime(2023, 3, 1, 5), Datetime(2023, 3, 1, 10)),
                Period(Datetime(2023, 3, 1, 16), Datetime(2023, 3, 1, 19)),
            ]
        )
        p2 = Periods(
            [
                Period(Datetime(2023, 3, 1, 8), Datetime(2023, 3, 1, 12)),
                Period(Datetime(2023, 3, 1, 15), Datetime(2023, 3, 1, 20)),
            ]
        )

        assert p1.hours_of_intersection(p2) == 5

    def test_hours_of_union(self):
        p1 = Periods(
            [
                Period(Datetime(2023, 3, 1, 5), Datetime(2023, 3, 1, 10)),
                Period(Datetime(2023, 3, 1, 16), Datetime(2023, 3, 1, 19)),
            ]
        )
        p2 = Periods(
            [
                Period(Datetime(2023, 3, 1, 8), Datetime(2023, 3, 1, 12)),
                Period(Datetime(2023, 3, 1, 15), Datetime(2023, 3, 1, 20)),
            ]
        )

        assert p1.hours_of_union(p2) == 12

    def test_are_same_temporalities(self):
        p1 = Periods([Period(Datetime(2023, 3, 1, 5), Datetime(2023, 3, 1, 10))])
        p2 = Periods([Period(Datetime(2023, 3, 1, 6), Datetime(2023, 3, 1, 12))])
        p3 = Periods([Period(Datetime(2023, 3, 1, 15), Datetime(2023, 3, 1, 20))])
        assert p1.are_same_temporalities(p2) is True
        assert p1.are_same_temporalities(p3) is False
        assert p1.are_same_temporalities(p2, p3) is False

        # the proportion of overlap is less than 25%
        p3 = Periods([Period(Datetime(2023, 1, 1), Datetime(2024, 1, 1))])
        p4 = Periods([Period(Datetime(2022, 1, 1), Datetime(2023, 1, 2))])
        assert p3.are_same_temporalities(p4) is False

        # periods are included in each other
        p5 = Periods([Period(Datetime(2023, 1, 1, 10), Datetime(2023, 1, 1, 11))])
        assert p3.are_same_temporalities(p1) is True
        assert p3.are_same_temporalities(p5) is True


class TestPeriodDescriber:
    pdesc = PeriodDescriber(
        cover_period=Period(Datetime(2021, 1, 1), Datetime(2021, 1, 2)),
        request_time=Datetime(2021, 1, 1, 12),
    )
    p1 = Period(Datetime(2021, 1, 1, 18), Datetime(2021, 1, 2, 7))
    p2 = Period(Datetime(2021, 1, 2, 8), Datetime(2021, 1, 2, 16))
    p3 = Period(Datetime(2021, 1, 2, 17), Datetime(2021, 1, 3, 8))

    def test_describe(self):
        assert isinstance(self.pdesc, PeriodDescriber)
        assert (
            self.pdesc.describe(self.p1)
            == "de ce vendredi soir à samedi début de matinée"
        )
        assert (
            self.pdesc.describe(Periods([self.p1, self.p2]))
            == "de ce vendredi soir à samedi après-midi"
        )
        assert (
            self.pdesc.describe(Periods([self.p1, self.p3]))
            == "de ce vendredi soir à samedi début de matinée et de samedi soir à "
            "dimanche matin"
        )

        assert self.pdesc.describe(self.pdesc.cover_period) == "sur toute la période"
        assert (
            self.pdesc.describe(
                Periods([Period(Datetime(2020, 1, 1), Datetime(2021, 1, 1, 3))])
            )
            == "en début de période"
        )
        assert (
            self.pdesc.describe(
                Periods([Period(Datetime(2021, 1, 1, 21), Datetime(2021, 1, 10))])
            )
            == "en fin de période"
        )

        assert (
            self.pdesc.describe(
                Periods(
                    [
                        Period(Datetime(2020, 1, 1, 3), Datetime(2021, 1, 1, 10)),
                        Period(Datetime(2021, 1, 1, 16), Datetime(2021, 1, 21)),
                    ]
                )
            )
            == "jusqu'à ce matin puis à nouveau à partir de cet après-midi"
        )

    def test_reduce(self):
        assert not self.pdesc.reduce(Periods())
        assert self.pdesc.reduce(Periods([self.p1, self.p2, self.p3])) == Periods(
            [Period(self.p1.begin_time, self.p3.end_time)]
        )
