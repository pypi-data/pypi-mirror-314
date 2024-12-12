import shutil
from abc import abstractmethod
from collections.abc import Mapping, Set
from pathlib import Path
from typing import Iterable, Tuple, Type, Iterator, Callable
from typing_extensions import Self

from pydantic import BaseModel
from tempfile import TemporaryDirectory, NamedTemporaryFile

from vizitig.errors import (
    InvalidIndexPath,
    InvalidShardPath,
    MissingShardPath,
    IndexNotReady,
)
from vizitig.info import get_graph, GraphLogger
from vizitig.paths import index_path_name
from vizitig.types import Kmer, DNA
from vizitig.env_var import VIZITIG_TMP_DIR
from vizitig.utils import sizeof_fmt
from vizitig.utils import vizitig_logger as logger, SubLog
from vizitig.utils import progress
from multiprocessing import Process


class IndexInfo(BaseModel):
    gname: str
    type: str
    size: int

    def __repr__(self):
        return f"Index({self.type}, {sizeof_fmt(self.size)})"


class BaseShard:
    def __init__(self, path: Path, shard_idx: int, shard_number: int, k: int):
        self._path = path
        self._shard_idx = shard_idx
        self._shard_number = shard_number
        self._k = k

    @property
    def path(self):
        return self._path

    @property
    def k(self):
        return self._k

    @staticmethod
    def hash(kmer: Kmer) -> int:
        return kmer.data

    def get_temp_file(self) -> Path:
        file = NamedTemporaryFile(prefix=VIZITIG_TMP_DIR)
        file.close()
        return Path(file.name)


class SetShard(BaseShard, Set[Kmer]):
    priority: int = 0
    subclasses: dict[str, Type["SetShard"]] = dict()

    @classmethod
    def __init_subclass__(cls):
        SetShard.subclasses[cls.__name__] = cls

    @classmethod
    @abstractmethod
    def build_kmer(
        cls,
        path: Path,
        shard_idx: int,
        shard_number: int,
        kmer_iter: Iterator[Kmer],
        k: int,
    ) -> Self:
        """Build the index from the Kmer.
        Implementation of this method must filter out kmer_iter them self
        """
        ...

    @classmethod
    def build_dna(
        cls,
        path: Path,
        shard_idx: int,
        shard_number: int,
        dna_iter: Iterator[DNA],
        k: int,
    ) -> Self:
        kmer_iter = (kmer for dna in dna_iter for kmer in dna.enum_canonical_kmer(k))
        return cls.build_kmer(path, shard_idx, shard_number, kmer_iter, k)


class Shard(BaseShard, Mapping[Kmer, int]):
    priority: int = 0
    subclasses: dict[str, Type["Shard"]] = dict()
    Set: Type[SetShard]

    @classmethod
    def __init_subclass__(cls):
        Shard.subclasses[cls.__name__] = cls

    @classmethod
    @abstractmethod
    def build_kmer(
        cls,
        path: Path,
        shard_idx: int,
        shard_number: int,
        kmer_iter: Iterator[Tuple[Kmer, int]],
        k: int,
    ) -> Self:
        """Build the index from the Kmer.
        Implementation of this method must filter out kmer_iter them self
        """
        ...

    @classmethod
    def build_dna(
        cls,
        path: Path,
        shard_idx: int,
        shard_number: int,
        dna_iter: Iterator[Tuple[DNA, int]],
        k: int,
    ) -> Self:
        kmer_iter = (
            (kmer, val) for dna, val in dna_iter for kmer in dna.enum_canonical_kmer(k)
        )
        return cls.build_kmer(path, shard_idx, shard_number, kmer_iter, k)

    def join(self, kmer_iter: Iterator[Tuple[Kmer, int]]) -> Iterable[Tuple[int, int]]:
        for kmer, val in kmer_iter:
            if kmer in self:
                yield (self[kmer], val)

    def join_index(self, other: Self) -> Iterable[Tuple[int, int]]:
        return self.join(iter(other.items()))

    def intersection(self, kmer_iter: Iterator[Kmer]) -> Iterable[int]:
        for kmer in kmer_iter:
            if kmer in self:
                yield self[kmer]

    def intersection_index(self, other) -> Iterable[int]:
        return self.intersection(iter(other))


class BaseKmerIndex:
    def __init__(self, path: Path, index_type: Type[Shard | SetShard], k: int):
        self._index_type = index_type
        self._path = path
        self._k = k
        self.check_path()

    @property
    def index_type(self) -> Type[Shard | SetShard]:
        return self._index_type

    @property
    def k(self):
        return self._k

    def check_path(self):
        if not self.path.is_dir():
            raise InvalidIndexPath(f"{self.path} is not a directory")
        shard_names = set()
        for p in self.path.glob("*"):
            if not p.name.isnumeric():
                raise InvalidShardPath(f"{p} is not a valid shard path")
            shard_names.add(int(p.name))
        if not shard_names:
            raise IndexNotReady()
        expected_shard_name = set(range(max(shard_names) + 1))
        missing_path = expected_shard_name - shard_names
        if missing_path:
            raise MissingShardPath(missing_path)
        self._shard_nb = max(shard_names) + 1

    @property
    def shard_number(self) -> int:
        return self._shard_nb

    @property
    def shards(self) -> Tuple[Shard | SetShard, ...]:
        if not hasattr(self, "_shards"):
            self._shards = tuple(
                self.index_type(self.path / str(i), i, self.shard_number, self.k)
                for i in range(self.shard_number)
            )
        return self._shards

    @property
    def file_size(self) -> int:
        if self.path.is_dir():
            return sum(f.stat().st_size for f in self.path.glob("**/*") if f.is_file())
        return self.path.stat().st_size

    def __iter__(self) -> Iterator[Kmer]:
        for shard in self.shards:
            yield from shard

    def __len__(self) -> int:
        return sum(map(len, self.shards))

    @property
    def path(self) -> Path:
        return self._path

    def drop(self):
        if self.path.is_dir():
            shutil.rmtree(self.path)
        else:
            self.path.unlink()


class KmerSetIndex(BaseKmerIndex, Set[Kmer]):
    @classmethod
    def _build_kmer(
        cls,
        path: Path,
        index_type: Type[SetShard],
        kmer_iter: Callable[[], Iterator[Kmer]],
        shard_number: int,
        k: int,
    ) -> Self:
        if path.exists():
            logger.warning(f"Index {path}, erasing and rebuilding")
            shutil.rmtree(path)
            path.mkdir()

        process = []
        for shard_index in range(shard_number):
            shard_path = path / str(shard_index)
            proc = Process(
                target=index_type.build_kmer,
                args=(shard_path, shard_index, shard_number, kmer_iter(), k),
            )
            proc.start()
            process.append(proc)

        for proc in process:
            proc.join()
        return cls(path, index_type, k)

    @classmethod
    def _build_dna(
        cls,
        path: Path,
        index_type: Type[SetShard],
        dna_iter: Callable[[], Iterable[DNA]],
        shard_number: int,
        k: int,
    ) -> Self:
        if path.exists():
            logger.warning(f"Index {path}, erasing and rebuilding")
            shutil.rmtree(path)
        path.mkdir()

        process = []
        for shard_index in range(shard_number):
            shard_path = path / str(shard_index)
            proc = Process(
                target=index_type.build_dna,
                args=(shard_path, shard_index, shard_number, dna_iter(), k),
            )
            proc.start()
            process.append(proc)

        for proc in process:
            proc.join()

        return cls(path, index_type, k)

    def __contains__(self, kmer: Kmer) -> bool:
        n: int = self.shard_number
        i = self.index_type.hash(kmer) % n
        return kmer in self.shards[i]


class KmerIndex(BaseKmerIndex, Mapping[Kmer, int]):
    @classmethod
    def _build_kmer(
        cls,
        path: Path,
        index_type: Type[Shard],
        kmer_iter: Callable[[], Iterator[Tuple[Kmer, int]]],
        shard_number: int,
        k: int,
    ) -> Self:
        if path.exists():
            logger.warning(f"Index {path}, erasing and rebuilding")
            shutil.rmtree(path)
            path.mkdir()

        process = []
        for shard_index in range(shard_number):
            shard_path = path / str(shard_index)
            proc = Process(
                target=index_type.build_kmer,
                args=(shard_path, shard_index, shard_number, kmer_iter(), k),
            )
            proc.start()
            process.append(proc)

        for proc in process:
            proc.join()
        return cls(path, index_type, k)

    @classmethod
    def _build_dna(
        cls,
        path: Path,
        index_type: Type[Shard],
        dna_iter: Callable[[], Iterable[Tuple[DNA, int]]],
        shard_number: int,
        k: int,
    ) -> Self:
        if path.exists():
            logger.warning(f"Index {path}, erasing and rebuilding")
            shutil.rmtree(path)
        path.mkdir()

        process = []
        for shard_index in range(shard_number):
            shard_path = path / str(shard_index)
            proc = Process(
                target=index_type.build_dna,
                args=(shard_path, shard_index, shard_number, dna_iter(), k),
            )
            proc.start()
            process.append(proc)

        for proc in process:
            proc.join()

        return cls(path, index_type, k)

    def join(self, kmer_iter: Iterator[Tuple[Kmer, int]]) -> Iterable[Tuple[int, int]]:
        for kmer, val in kmer_iter:
            if kmer in self:
                yield (self[kmer], val)

    def join_index(self, other: "KmerIndex") -> Iterable[Tuple[int, int]]:
        assert self.k == other.k
        if (
            self.index_type is other.index_type
            and other.shard_number == self.shard_number
        ):
            for left, right in zip(self.shards, other.shards):
                assert isinstance(left, Shard)
                assert isinstance(right, Shard)
                yield from left.join_index(right)
        else:
            yield from self.join(iter(other.items()))

    def intersection(self, kmer_iter: Iterator[Kmer]) -> Iterable[int]:
        for kmer in kmer_iter:
            if kmer in self:
                yield self[kmer]

    def intersection_index(self, other: KmerSetIndex) -> Iterable[int]:
        with SubLog("intersection_index"):
            assert issubclass(self.index_type, Shard)
            if (
                self.index_type.Set is other.index_type
                and other.shard_number == self.shard_number
            ):
                for i, (left, right) in enumerate(zip(self.shards, other.shards)):
                    logger.info(f"Shard: {i}")
                    assert isinstance(left, Shard)
                    assert isinstance(right, SetShard)
                    yield from left.intersection_index(right)
            else:
                logger.warning(
                    "Shard or IndexType mismatch: fall back to (slow) iterator intersection"
                )
                yield from self.intersection(iter(other))

    def __getitem__(self, kmer: Kmer) -> int:
        n: int = self.shard_number
        i = self.index_type.hash(kmer) % n
        shard = self.shards[i]
        assert isinstance(shard, Shard)
        return shard[kmer]


def graph_index_path(gname: str, index_type: Type[Shard]):
    return index_path_name(gname) / index_type.__name__


class GraphIndex(KmerIndex):
    _gname: str | None = None

    def info(self) -> IndexInfo:
        assert self._gname is not None
        return IndexInfo(
            gname=self._gname, type=self._index_type.__name__, size=self.file_size
        )

    @classmethod
    def from_graph(cls, gname: str, index_type: Type[Shard]) -> Self:
        G = get_graph(gname)
        idx = cls(graph_index_path(gname, index_type), index_type, G.metadata.k)
        idx._gname = gname
        return idx

    @property
    def gname(self):
        return self._gname

    @classmethod
    def build_kmer(cls, gname: str, index_type: Type[Shard], shard_number: int) -> Self:
        G = get_graph(gname)
        k = G.metadata.k

        def kmer_iter():
            it = G.nbunch_iter(data="sequence")
            index_iter = (
                (kmer, nid)
                for nid, seq in progress(it, total=G.metadata.size)
                for kmer in DNA(seq).enum_canonical_kmer(k)
            )
            return index_iter

        path = graph_index_path(gname, index_type)

        with GraphLogger(
            gname, f"Index ({index_type.__name__}) Build ({path}) from kmer"
        ):
            return cls._build_kmer(
                path,
                index_type,
                kmer_iter,
                shard_number,
                k,
            )

    @classmethod
    def build_dna(cls, gname: str, index_type: Type[Shard], shard_number: int):
        G = get_graph(gname)
        k = G.metadata.k

        def dna_iter():
            it = G.nbunch_iter(data="sequence")
            return map(lambda e: (DNA(e[1]), e[0]), it)

        path = graph_index_path(gname, index_type)
        with GraphLogger(
            gname, f"Index ({index_type.__name__}) Build ({path}) from DNA"
        ):
            return cls._build_dna(
                path,
                index_type,
                dna_iter,
                shard_number,
                k,
            )


class TemporaryKmerSet(KmerSetIndex):
    _d: TemporaryDirectory | None = None

    @classmethod
    def build_kmer(
        cls,
        index_type: Type[Shard],
        kmer_iter: Callable[[], Iterator[Kmer]],
        shard_number: int,
        k: int,
    ) -> Self:
        d = TemporaryDirectory(prefix=VIZITIG_TMP_DIR)
        assert index_type.Set is not None
        idx = cls._build_kmer(Path(d.name), index_type.Set, kmer_iter, shard_number, k)
        idx._d = d
        return idx

    @classmethod
    def build_dna(
        cls,
        index_type: Type[Shard],
        dna_iter: Callable[[], Iterator[DNA]],
        shard_number: int,
        k: int,
    ) -> Self:
        d = TemporaryDirectory(prefix=VIZITIG_TMP_DIR)
        assert index_type.Set is not None
        idx = cls._build_dna(Path(d.name), index_type.Set, dna_iter, shard_number, k)
        idx._d = d
        return idx

    def __del__(self):
        self._d.cleanup()


class TemporaryKmerIndex(KmerIndex):
    _d: TemporaryDirectory | None = None

    @classmethod
    def build_kmer(
        cls,
        index_type: Type[Shard],
        kmer_iter: Callable[[], Iterator[Tuple[Kmer, int]]],
        shard_number: int,
        k: int,
    ) -> Self:
        d = TemporaryDirectory(prefix=VIZITIG_TMP_DIR)
        idx = cls._build_kmer(Path(d.name), index_type, kmer_iter, shard_number, k)
        idx._d = d
        return idx

    @classmethod
    def build_dna(
        cls,
        index_type,
        dna_iter: Callable[[], Iterable[Tuple[DNA, int]]],
        shard_number: int,
        k: int,
    ) -> Self:
        d = TemporaryDirectory(prefix=VIZITIG_TMP_DIR)
        idx = cls._build_dna(Path(d.name), index_type, dna_iter, shard_number, k)
        idx._d = d
        return idx

    def __del__(self):
        self._d.cleanup()
