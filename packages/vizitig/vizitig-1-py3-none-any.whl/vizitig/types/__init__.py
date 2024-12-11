import re
import math
from dataclasses import dataclass
from enum import Enum
from typing import Iterator, List, Literal, Mapping, SupportsIndex, Tuple, cast

from typing_extensions import Self

from vizitig.env_var import VIZITIG_PYTHON_ONLY

Nucleotide = Literal["A", "C", "G", "T"]
non_CGTA = re.compile("[^ACGT]")


class ESign(Enum):
    pp = "++"
    mp = "-+"
    mm = "--"
    pm = "+-"


class DNAPython(str):
    """A light class to type string with only letters ACGT"""

    def __iter__(self) -> Iterator[Nucleotide]:
        for x in super().__iter__():
            yield cast(Nucleotide, x)

    def enum_kmer(self, k: int) -> Iterator["Kmer"]:
        kmer = KmerPython.from_dna(self[:k])
        yield kmer
        for a in self[k:]:
            kmer = kmer.add_right_nucleotid(a)
            yield kmer

    def enum_canonical_kmer(self, k: int) -> Iterator["Kmer"]:
        kmer = KmerPython.from_dna(self[:k])
        rc = kmer.reverse_complement()
        yield min(kmer, rc)
        for a in self[k:]:
            kmer = kmer.add_right_nucleotid(a)
            rc = rc.add_left(complement_table[char_to_int[a]])
            yield min(kmer, rc)

    @classmethod
    def from_str(cls, seq: str) -> Iterator["DNA"]:
        yield from (cls(subseq) for subseq in non_CGTA.split(seq))

    def __getitem__(self, __key: SupportsIndex | slice) -> Self:
        return type(self)(super().__getitem__(__key))


Quarter = Literal[0b00, 0b01, 0b10, 0b11]

char_to_int: Mapping[Nucleotide, Quarter] = {"A": 0b00, "C": 0b01, "G": 0b10, "T": 0b11}
int_to_char: Mapping[Quarter, Nucleotide] = {0b00: "A", 0b01: "C", 0b10: "G", 0b11: "T"}
complement_table: Mapping[Quarter, Quarter] = {
    k: cast(Quarter, (~k & 0b11)) for k in int_to_char
}


if not VIZITIG_PYTHON_ONLY:
    try:
        from vizibridge import DNA
    except ImportError:
        DNA = DNAPython
else:
    DNA = DNAPython


@dataclass
class KmerPython:
    data: int
    size: int

    @classmethod
    def from_dna(cls, seq: DNA) -> Self:
        return cls.from_iter(map(char_to_int.__getitem__, seq))  # type: ignore
        # mypy claim that it expect a str instead of a Nucleotide ???

    def __reduce__(self):
        return (self.__class__, (self.data, self.size))

    @classmethod
    def from_iter(cls, it: Iterator[Quarter]) -> Self:
        data = 0
        size = 0
        for q in it:
            data += q
            data = data << 2
            size += 1
        return cls(data >> 2, size)

    def __iter__(self):
        data = self.data
        for a in range(self.size)[::-1]:
            yield (data & (0b11 << (a * 2))) >> (a * 2)

    def __repr__(self):
        return "".join(map(int_to_char.__getitem__, self))

    def add_left_nucleotid(self, n: Nucleotide) -> Self:
        return self.add_left(char_to_int[n])

    def add_right_nucleotid(self, n: Nucleotide) -> Self:
        return self.add_right(char_to_int[n])

    def add_left(self, n: Quarter) -> Self:
        data = (self.data >> 2) + (n << ((self.size - 1) * 2))
        return type(self)(data, self.size)

    def add_right(self, n: Quarter) -> Self:
        data = ((self.data << 2) + (n)) & ((1 << (2 * self.size)) - 1)
        return type(self)(data, self.size)

    def reverse_complement(self) -> Self:
        c = map(complement_table.__getitem__, reversed(list(self)))  # type: ignore
        return self.from_iter(c)  # type: ignore
        # mypy claim weird stuff ...

    def canonical(self) -> Self:
        return min(self, self.reverse_complement())

    def is_canonical(self) -> bool:
        return self == self.canonical()

    def __hash__(self):
        return hash((self.data, self.size))

    def __lt__(self, other) -> bool:
        assert self.size == other.size
        return self.data <= other.data

    def __gt__(self, other) -> bool:
        assert self.size == other.size
        return self.data >= other.data


if not VIZITIG_PYTHON_ONLY:
    try:
        from vizibridge import Kmer

        # Here Kmer is a only a type (a union of classes) and can't be instantiated directly.
        AvailableKmerTypes = KmerPython | Kmer
    except ImportError:
        AvailableKmerTypes = KmerPython
        Kmer = KmerPython
else:
    AvailableKmerTypes = KmerPython
    Kmer = KmerPython


@dataclass
class Color:
    id: str
    description: str
    type: str = "Color"
    offset: int | None = None

    def set_offset(self, offset: int):
        self.offset = offset

    def __hash__(self):
        return hash((self.id, self.type, self.offset))


@dataclass
class SubseqData:
    id: str
    type: str
    start: int
    stop: int
    list_attr: List[str]
    offset: int | None = None
    first_kmer: int | None = None
    last_kmer: int | None = None
    gene: str | None = None

    def set_offset(self, offset: int):
        self.offset = offset

    def __hash__(self):
        return hash((self.id, self.type, self.offset))

    def add_first_kmer(self, kmer: Kmer):
        assert isinstance(kmer, Kmer)
        self.first_kmer = kmer.data
        return self

    def get_first_kmer(self, k):
        return Kmer(int.from_bytes(self.first_kmer), k)

    def get_last_kmer(self, k):
        return Kmer(int.from_bytes(self.last_kmer), k)

    def add_last_kmer(self, kmer: Kmer):
        assert isinstance(kmer, Kmer)
        self.last_kmer = kmer.data
        return self

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        if self.id != other.id:
            return False
        if self.type != other.type:
            return False
        if self.start != other.start:
            return False
        if self.stop != other.stop:
            return False
        if self.list_attr != other.list_attr:
            return False
        return True


@dataclass
class ViziStringArray:
    # This structure can take up to 2.5MB in RAM.
    data: str = ""
    maxSize: int = 25000000
    length: int = 0
    read_head: int = 0

    def add(self, data):
        assert isinstance(data, str)
        len_to_add = len(data)
        if self.length + len_to_add > self.maxSize:
            shift_len = self.length + len_to_add - self.maxSize
            self.read_head += shift_len
            self.data = self.data[shift_len::]
            self.data += data
            self.length = self.maxSize
        else:
            self.length += len_to_add
            self.data += data

    def __getitem__(self, key: Tuple[int, int]):
        return self.data[key[0] - self.read_head : key[1] - self.read_head]


class Zero:
    """Abstract symbol to be used to be encoded as the INT 0.
    Should be used for filtering between kmer and non kmer metadata.
    e.g. G.find_all_nodes(lambda e:e.lt(Zero())) will return all nodes
    with some metadata.

    Remark that it works as BLOB type in SQLite are always larger than 0 apparently.

    """


Metadata = Color | SubseqData
ViziKey = Metadata | Literal["sequence"] | Kmer | Zero


def encode_kmer(kmer: Kmer, k: int) -> int | bytes:
    data = kmer.data
    if k < 32:
        return data
    return int.to_bytes(data, length=math.ceil(k / 4))


def decode_kmer(data: bytes | int, k: int) -> Kmer:
    if isinstance(data, bytes):
        return Kmer(int.from_bytes(data), k)
    return Kmer(data, k)
