from typing import Literal
from typing_extensions import Self

from minineedle import core
from minineedle.needle import NeedlemanWunsch
from minineedle.smith import SmithWaterman
from pydantic import BaseModel

AlignStrategy = Literal["NW", "SW"]


class Alignment(BaseModel):
    score: int | float
    align_seq1: list[str | None]
    align_seq2: list[str | None]

    @classmethod
    def from_seq(cls, seq1: str, seq2: str, strategy: AlignStrategy = "SW") -> Self:
        if strategy == "NW":
            align = NeedlemanWunsch(seq1, seq2)
        elif strategy == "SW":
            align = SmithWaterman(seq1, seq2)
        else:
            raise NotImplementedError
        align.align()
        Gap = core.Gap()
        _out1, _out2 = align.get_aligned_sequences()
        out1 = [None if x == Gap else x for x in _out1]
        out2 = [None if x == Gap else x for x in _out2]
        return cls(score=align.get_score(), align_seq1=out1, align_seq2=out2)
