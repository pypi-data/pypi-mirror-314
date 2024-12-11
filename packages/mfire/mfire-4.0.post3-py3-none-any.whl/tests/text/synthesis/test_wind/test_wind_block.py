import pytest

from mfire.text.synthesis.wind_reducers.exceptions import WindSynthesisError
from mfire.text.synthesis.wind_reducers.wind.case3.wind_block import WindBlock
from mfire.text.synthesis.wind_reducers.wind.case3.wind_direction import (
    Pcd,
    WindDirection,
)
from mfire.text.synthesis.wind_reducers.wind.wind_intensity import Pci, WindIntensity
from mfire.utils.date import Datetime, Timedelta


class TestWindBlock:
    BEGIN_TIME: Datetime = Datetime(2023, 1, 1, 0, 0, 0)
    END_TIME: Datetime = Datetime(2023, 1, 1, 9, 0, 0)
    WIND_BLOCK: WindBlock = WindBlock(BEGIN_TIME, END_TIME)

    def test_creation(self):
        assert self.WIND_BLOCK.begin_time == self.BEGIN_TIME
        assert self.WIND_BLOCK.end_time == self.END_TIME
        assert self.WIND_BLOCK.duration == Timedelta(self.END_TIME - self.BEGIN_TIME)

    def test_wd_period(self):
        wd_period = Pcd(
            Datetime(2023, 1, 1, 2, 0, 0),
            Datetime(2023, 1, 1, 4, 0, 0),
            WindDirection(10.0, 40.0),
        )
        wd_periods = [wd_period]
        self.WIND_BLOCK.pcd = wd_periods
        assert self.WIND_BLOCK.pcd == wd_periods

        self.WIND_BLOCK.pcd = []
        assert self.WIND_BLOCK.pcd == []

        self.WIND_BLOCK.pcd = None
        assert self.WIND_BLOCK.pcd == []

    @pytest.mark.parametrize(
        "wd_periods, exception",
        [
            (
                # 1 Pci: bad type
                [
                    Pci(
                        Datetime(2023, 1, 1, 7, 0, 0),
                        Datetime(2023, 1, 1, 9, 0, 0),
                        WindIntensity(35.0),
                    )
                ],
                TypeError,
            ),
            (
                # 1 Pcd with a begin_time < block begin_time
                [
                    Pcd(
                        Datetime(2022, 12, 31, 22, 0, 0),
                        Datetime(2023, 1, 1, 8, 0, 0),
                        WindDirection(10.0, 40.0),
                    )
                ],
                WindSynthesisError,
            ),
            (
                # 1 Pcd with an end_time > block begin_time
                [
                    Pcd(
                        Datetime(2023, 1, 1, 0, 0, 0),
                        Datetime(2023, 1, 1, 10, 59, 59),
                        WindDirection(10.0, 40.0),
                    )
                ],
                WindSynthesisError,
            ),
            (
                # 1 Pcd with an end_time > block end_time
                [
                    Pcd(
                        Datetime(2023, 1, 1, 7, 0, 0),
                        Datetime(2023, 1, 1, 23, 0, 0),
                        WindDirection(10.0, 40.0),
                    )
                ],
                WindSynthesisError,
            ),
            (
                # 2 unordered Pcd
                [
                    Pcd(
                        Datetime(2023, 1, 1, 7, 0, 0),
                        Datetime(2023, 1, 1, 9, 0, 0),
                        WindDirection(10.0, 40.0),
                    ),
                    Pcd(
                        Datetime(2023, 1, 1, 2, 0, 0),
                        Datetime(2023, 1, 1, 5, 0, 0),
                        WindDirection(10.0, 40.0),
                    ),
                ],
                WindSynthesisError,
            ),
        ],
    )
    def test_wd_period_exceptions(self, wd_periods, exception):
        with pytest.raises(exception):
            self.WIND_BLOCK.pcd = wd_periods

    def test_wf_period(self):
        wf_period = Pci(
            Datetime(2023, 1, 1, 2, 0, 0),
            Datetime(2023, 1, 1, 4, 0, 0),
            WindIntensity(35.0),
        )
        wf_periods = [wf_period]
        self.WIND_BLOCK.pci = wf_periods
        assert self.WIND_BLOCK.pci == wf_periods

        self.WIND_BLOCK.pci = []
        assert self.WIND_BLOCK.pci == []

        self.WIND_BLOCK.pci = None
        assert self.WIND_BLOCK.pci == []

    @pytest.mark.parametrize(
        "wf_periods, exception",
        [
            (
                # 1 Pcd: bad type
                [
                    Pcd(
                        Datetime(2023, 1, 1, 7, 0, 0),
                        Datetime(2023, 1, 1, 9, 0, 0),
                        WindDirection(10.0, 40.0),
                    )
                ],
                TypeError,
            ),
            (
                # 1 Pci with a begin_time < block begin_time
                [
                    Pci(
                        Datetime(2022, 12, 31, 22, 0, 0),
                        Datetime(2023, 1, 1, 8, 0, 0),
                        WindIntensity(35.0),
                    )
                ],
                WindSynthesisError,
            ),
            (
                # 1 Pci with an end_time > block end_time
                [
                    Pci(
                        Datetime(2023, 1, 1, 7, 0, 0),
                        Datetime(2023, 1, 1, 23, 0, 0),
                        WindIntensity(35.0),
                    )
                ],
                WindSynthesisError,
            ),
            (
                # 1 Pci with an end_time > block begin_time
                [
                    Pci(
                        Datetime(2023, 1, 1, 0, 0, 0),
                        Datetime(2023, 1, 1, 10, 59, 59),
                        WindIntensity(35.0),
                    )
                ],
                WindSynthesisError,
            ),
            (
                # 2 unordered Pci
                [
                    Pci(
                        Datetime(2023, 1, 1, 7, 0, 0),
                        Datetime(2023, 1, 1, 9, 0, 0),
                        WindIntensity(35.0),
                    ),
                    Pci(
                        Datetime(2023, 1, 1, 2, 0, 0),
                        Datetime(2023, 1, 1, 5, 0, 0),
                        WindIntensity(35.0),
                    ),
                ],
                WindSynthesisError,
            ),
        ],
    )
    def test_wf_period_exceptions(self, wf_periods, exception):
        with pytest.raises(exception):
            self.WIND_BLOCK.pci = wf_periods

    @pytest.mark.parametrize(
        "blocks, expected",
        [
            (
                [
                    WindBlock(
                        Datetime(2023, 1, 2, 0, 0, 0),
                        Datetime(2023, 1, 2, 10, 0, 0),
                        pci=[
                            Pci(
                                Datetime(2023, 1, 2, 0, 0, 0),
                                Datetime(2023, 1, 2, 8, 0, 0),
                                WindIntensity(35.0),
                            )
                        ],
                        pcd=[
                            Pcd(
                                Datetime(2023, 1, 2, 1, 0, 0),
                                Datetime(2023, 1, 2, 6, 0, 0),
                                WindDirection(10.0, 40.0),
                            )
                        ],
                    ),
                    WindBlock(
                        Datetime(2023, 1, 2, 12, 0, 0),
                        Datetime(2023, 1, 2, 23, 0, 0),
                        pci=[
                            Pci(
                                Datetime(2023, 1, 2, 13, 0, 0),
                                Datetime(2023, 1, 2, 14, 0, 0),
                                WindIntensity(45.0),
                            )
                        ],
                        pcd=[
                            Pcd(
                                Datetime(2023, 1, 2, 13, 0, 0),
                                Datetime(2023, 1, 2, 18, 0, 0),
                                WindDirection(10.0, 40.0),
                            )
                        ],
                    ),
                ],
                WindBlock(
                    Datetime(2023, 1, 2, 0, 0, 0),
                    Datetime(2023, 1, 2, 23, 0, 0),
                    pci=[
                        Pci(
                            Datetime(2023, 1, 2, 0, 0, 0),
                            Datetime(2023, 1, 2, 8, 0, 0),
                            WindIntensity(35.0),
                        ),
                        Pci(
                            Datetime(2023, 1, 2, 13, 0, 0),
                            Datetime(2023, 1, 2, 14, 0, 0),
                            WindIntensity(45.0),
                        ),
                    ],
                    pcd=[
                        Pcd(
                            Datetime(2023, 1, 2, 1, 0, 0),
                            Datetime(2023, 1, 2, 6, 0, 0),
                            WindDirection(10.0, 40.0),
                        ),
                        Pcd(
                            Datetime(2023, 1, 2, 13, 0, 0),
                            Datetime(2023, 1, 2, 18, 0, 0),
                            WindDirection(10.0, 40.0),
                        ),
                    ],
                ),
            )
        ],
    )
    def test_merge(self, blocks, expected):
        assert blocks[0].merge(blocks[1]) == expected

    @pytest.mark.parametrize(
        "blocks",
        [
            [
                WindBlock(Datetime(2023, 1, 2, 0, 0, 0), Datetime(2023, 1, 2, 5, 0, 0)),
                WindBlock(
                    Datetime(2023, 1, 2, 2, 0, 0), Datetime(2023, 1, 2, 10, 0, 0)
                ),
            ],
            [
                WindBlock(Datetime(2023, 1, 2, 0, 0, 0), Datetime(2023, 1, 2, 5, 0, 0)),
                WindBlock(Datetime(2023, 1, 2, 2, 0, 0), Datetime(2023, 1, 2, 3, 0, 0)),
            ],
        ],
    )
    def test_merge_exception(self, blocks):
        with pytest.raises(WindSynthesisError):
            blocks[0].merge(blocks[1])
