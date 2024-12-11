from __future__ import annotations

from typing import Optional

from mfire.settings import get_logger
from mfire.text.synthesis.wind_reducers.exceptions import WindSynthesisError
from mfire.text.synthesis.wind_reducers.wind.case3.wind_direction import Pcd
from mfire.text.synthesis.wind_reducers.wind.helpers import SummaryKeysMixin, WindPeriod
from mfire.text.synthesis.wind_reducers.wind.wind_intensity import Pci
from mfire.utils.date import Datetime

LOGGER = get_logger(name=__name__, bind="wind_block")


class WindBlock(SummaryKeysMixin, WindPeriod):
    """WindBlock class."""

    def __init__(
        self,
        begin_time: Datetime,
        end_time: Datetime,
        pci: Optional[list[Pci]] = None,
        pcd: Optional[list[Pcd]] = None,
    ):
        """Initialize a WindBlock instance.

        A WindBlock is a suite of type 3 terms.
        """
        self._pci: list[Pci] = []
        self._pcd: list[Pcd] = []
        super().__init__(begin_time, end_time)

        if pci:
            self.pci = pci

        if pcd:
            self.pcd = pcd

    @property
    def pci(self) -> list[Pci]:
        """Get the periods with a common intensity (PCI)."""
        return self._pci

    @pci.setter
    def pci(self, pci: Optional[list[Pci]]) -> None:
        """Set the periods with a common intensity (PCI)."""
        if not pci:
            pci = []
        self._check_input_periods(pci, Pci)
        self._pci = pci

    @property
    def pcd(self) -> list[Pcd]:
        """Get the periods with a common direction (PCD)."""
        return self._pcd

    @pcd.setter
    def pcd(self, pcd: Optional[list[Pcd]]) -> None:
        """Set the wind direction periods."""
        if not pcd:
            pcd = []
        self._check_input_periods(pcd, Pcd)
        self._pcd = pcd

    @property
    def pci_cnt(self) -> int:
        """Get the counter of the wind intensity periods."""
        return len(self._pci)

    @property
    def pcd_cnt(self) -> int:
        """Get the counter of the wind direction periods."""
        return len(self._pcd)

    def _check_input_periods(self, periods: list[Pci] | list[Pcd], item_class) -> None:
        """Check if input periods."""
        periods_len: int = len(periods)

        if periods_len == 0:
            return

        for period in periods:
            if isinstance(period, item_class) is False:
                raise TypeError(
                    f"Bad period type '{type(period)}' found in '{item_class}' list: "
                    f"{period}"
                )

        if periods[0].begin_time < self.begin_time:
            raise WindSynthesisError(
                f"begin_time of the 1st period '{periods[0].begin_time}' is < "
                f"block begin_time '{self.begin_time}' !"
            )

        if periods[-1].end_time > self.end_time:
            raise WindSynthesisError(
                f"end_time of the last period'{periods[-1].end_time}' is > "
                f"block end_time '{self.begin_time}' !"
            )

        if periods_len == 1:
            return

        period_cur: Pci = periods[0]

        for i in range(1, periods_len):
            period_next: Pci = periods[i]

            if period_cur.end_time > period_next.begin_time:
                raise WindSynthesisError(
                    f"Temporally unordered periods found: {period_cur} does not precede"
                    f"{period_next} !"
                )

            period_cur = period_next

    def merge(self, other: WindBlock) -> WindBlock:
        """Merge the wind block with another one.

        The begin_time of the output come from the earliest WindBlock.
        The end_time of the output come from the last WindBlock.
        """
        if (
            other.begin_time < self.end_time < other.end_time
            or self.begin_time < other.end_time < self.end_time
        ):
            raise WindSynthesisError(f"Cannot merge these 2 blocks:\n{self}\n{other} !")

        blocks: list[WindBlock] = [
            min([self, other], key=lambda b: b.begin_time),
            max([self, other], key=lambda b: b.begin_time),
        ]

        wind_block = WindBlock(
            blocks[0].begin_time,
            blocks[1].end_time,
            blocks[0].pci + blocks[1].pci,
            blocks[0].pcd + blocks[1].pcd,
        )

        return wind_block

    def summarize(self, reference_datetime: Datetime) -> dict:
        """Summarise tha WindBlock as a dictionary."""

        return {
            self.PCI_K: [p.summarize(reference_datetime) for p in self.pci],
            self.PCD_K: [p.summarize(reference_datetime) for p in self.pcd],
        }

    def __hash__(self) -> int:
        """Hash the WindBlock instance."""
        return hash((self.begin_time, self.end_time))

    def __eq__(self, other: WindBlock) -> bool:
        """Check WindBlock equality."""
        if isinstance(other, WindBlock) is False:
            return False
        return (
            self.begin_time == other.begin_time
            and self.end_time == other.end_time
            and self.pci == other.pci
            and self.pcd == other.pcd
        )

    def __repr__(self) -> str:
        """Serialize a WindBlock as a string representation."""
        return (
            f"{self.__class__.__name__}(begin_time={self.begin_time}, "
            f"end_time={self.end_time}, duration={self.duration}, "
            f"pcd={self.pcd}, pci={self.pci})"
        )
