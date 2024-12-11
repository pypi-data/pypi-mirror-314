import shutil
from abc import abstractmethod
from collections.abc import Mapping
from pathlib import Path
from typing import Iterable, Tuple, Type, Iterator, Any, Callable

import networkdisk as nd
from pydantic import BaseModel

from vizitig.errors import NoIndex
from vizitig.info import get_graph
from vizitig.paths import index_path_name
from vizitig.types import Kmer, Metadata, DNA
from vizitig.utils import sizeof_fmt
from vizitig.utils import vizitig_logger as logger
from vizitig.utils import progress
from os import cpu_count
from multiprocessing import Process, Queue

cpu_c = cpu_count()
if cpu_c is not None:
    default_shard_nb = min(cpu_c - 1, 10)
else:
    default_shard_nb = 4


class IndexInfo(BaseModel):
    gname: str
    type: str
    size: int

    def __repr__(self):
        return f"Index({self.type}, {sizeof_fmt(self.size)})"


class AbstractShard(Mapping[Kmer, int]):
    subclasses: dict[str, Type["AbstractShard"]] = dict()
    index_type: Type
    priority: int = 0

    def __init__(self, gname: str, path: Path):
        self._path = path
        self.queue: Queue[Tuple[Kmer, Any] | None] = Queue()
        self._gname = gname

    @classmethod
    def __init_subclass__(cls):
        AbstractShard.subclasses[cls.__name__] = cls

    @property
    def gname(self):
        return self._gname

    @property
    def graph(self) -> nd.sqlite.Graph | nd.sqlite.DiGraph:
        return get_graph(self._gname)

    @property
    def path(self):
        return self._path

    @classmethod
    @abstractmethod
    def build(
        cls,
        gname: str,
        build_path: Path,
        index_iter: Iterator[Tuple[Kmer, int]],
    ): ...

    def iter_data(self) -> Iterator[Tuple[Kmer, Any]]:
        while True:
            item = self.queue.get()
            if item is None:
                break
            yield item
        self.queue = Queue()

    def join_shard(self, return_queue: Queue):
        self.process = Process(target=self._join, args=(return_queue,))
        self.process.start()

    def intersection_shard(self, return_queue: Queue):
        self.process = Process(target=self._intersection, args=(return_queue,))
        self.process.start()

    def send(self, data: Tuple[Kmer, Any] | None):
        self.queue.put(data)

    def _join(self, return_queue: "Queue[Tuple[int, Any] | None]"):
        for t in self.join(self.iter_data()):
            return_queue.put(t)
        return_queue.put(None)

    def _intersection(self, return_queue: "Queue[Tuple[int, Any] | None]"):
        for t in self.intersection(self.iter_data()):
            return_queue.put((t, None))
        return_queue.put(None)

    def join(
        self, kmer_metadata_iter: Iterator[Tuple[Kmer, Metadata]]
    ) -> Iterable[Tuple[int, Metadata]]:
        for kmer, metadata in kmer_metadata_iter:
            if kmer in self:
                yield (self[kmer], metadata)

    def intersection(self, kmer_iter: Iterator[Tuple[Kmer, None]]) -> Iterable[int]:
        for kmer, _ in kmer_iter:
            if kmer in self:
                yield self[kmer]


def dispatch_iterator_to_shards(
    shards: list[AbstractShard], iterator: Iterator, key: Callable[[Any], int]
):
    shard_number = len(shards)
    for row in iterator:
        shards[key(row) % shard_number].send(row)
    for s in shards:
        s.send(None)


class KmerIndex(Mapping[Kmer, int]):
    hash_key_a = 104729
    hash_key_b = 179426549
    hash_key_p = (1 << 128) + 51

    def __init__(self, gname: str, index_type: Type[AbstractShard]):
        self._gname = gname
        self._index_type = index_type
        self._path = index_path_name(gname) / str(self._index_type.__name__)

    @property
    def shard_number(self):
        if not self.path.is_dir():
            raise NoIndex
        return len(tuple(self.path.glob("*")))

    @property
    def shards(self):
        if not hasattr(self, "_shards"):
            self._shards = self.get_new_shards(self.shard_number)
        return self._shards

    @property
    def gname(self):
        return self._gname

    def get_new_shards(self, shard_number):
        shards = []
        for key in range(shard_number):
            shards.append(
                AbstractShard.subclasses[self._index_type.__name__](
                    self._gname, self._path / str(key)
                )
            )
        return shards

    def exists(self) -> bool:
        try:
            shards = self.shards
        except NoIndex:
            return False
        for shard in shards:
            if not shard.path.exists():
                return False
        return True

    @property
    def file_size(self) -> int:
        if self.path.is_dir():
            return sum(f.stat().st_size for f in self.path.glob("**/*") if f.is_file())
        return self.path.stat().st_size

    def info(self) -> IndexInfo:
        if self.exists():
            return IndexInfo(
                gname=self._gname, type=self._index_type.__name__, size=self.file_size
            )
        raise NoIndex(self._index_type.__name__)

    def __getitem__(self, kmer: Kmer):
        n: int = self.shard_number
        i = ((self.hash_key_a * kmer.data + self.hash_key_b) % self.hash_key_p) % n
        return self.shards[i].__getitem__(kmer)

    def __iter__(self):
        for shard in self.shards:
            yield from shard

    def __len__(self):
        return sum(map(len, self.shards))

    @property
    def graph(self) -> nd.sqlite.Graph | nd.sqlite.DiGraph:
        return get_graph(self._gname)

    @property
    def path(self):
        return self._path

    def drop(self):
        if self.path.is_dir():
            shutil.rmtree(self.path)
        else:
            self.path.unlink()

    @classmethod
    def path_from_name(cls, gname: str, suffix: str = "") -> Path:
        return index_path_name(gname) / (cls.__name__ + suffix)

    def build_shards(self, shards):
        for key, shard in enumerate(shards):
            shard.process = Process(
                target=self._index_type.build,
                args=(self._gname, self.path / str(key), shard.iter_data()),
            )

    def start_shards(self):
        for shard in self.shards:
            shard.process.start()

    def stop_shards(self):
        for shard in self.shards:
            shard.process.join()

    def empty_return_queue(self, result_queue: "Queue[Tuple[int, Any] | None]"):
        active_workers: int = self.shard_number
        while active_workers > 0:
            elem = result_queue.get()
            if elem is None:
                active_workers -= 1
            else:
                yield elem

    def build(self, shard_number=default_shard_nb):
        """
        Builds the index - abstract version.
        Keep in mind that this function calls the build function of the child class, but
        the parallelism is implemented here. It leverages sharding : a process made to split
        the data into different pools to accelerate the process and use one CPU thread by shard.
        We limit the number of shards to 10 because more shards get bottlenecked by the I/O
        capacities of classic laptops.
        """

        if self.path.exists():
            logger.warning(
                "Index {} already exists for the graph {}, erasing and rebuilding".format(
                    self.__class__.__name__, self.gname
                )
            )
            shutil.rmtree(self.path)
        Path(self.path).mkdir()

        build_shard_process = [
            Process(target=self.build_shard, args=(i, shard_number))
            for i in range(shard_number)
        ]
        for shard in build_shard_process:
            shard.start()
        for shard in build_shard_process:
            shard.join()

    def join(
        self, other: Iterable[Tuple[Kmer, Metadata]]
    ) -> Iterable[Tuple[int, Metadata]]:
        return_queue: Queue[Tuple[int, Metadata] | None] = Queue()
        dispatcher_process: Process = Process(
            target=dispatch_iterator_to_shards,
            args=(self.shards, other, self.kmer_hash),
        )
        dispatcher_process.start()

        for shard in self.shards:
            shard.join_shard(return_queue)

        yield from self.empty_return_queue(return_queue)
        dispatcher_process.join()
        self.stop_shards()

    def intersection(self, other: Iterable[Kmer]) -> Iterable[int]:
        return_queue: Queue[Tuple[int, None] | None] = Queue()
        dec_other = ((kmer, None) for kmer in other)
        dispatcher_process: Process = Process(
            target=dispatch_iterator_to_shards,
            args=(self.shards, dec_other, self.kmer_hash),
        )
        dispatcher_process.start()

        for shard in self.shards:
            shard.intersection_shard(return_queue)

        yield from (e for e, _ in self.empty_return_queue(return_queue))

        dispatcher_process.join()

        self.stop_shards()

    def build_shard(self, shard_index: int, shard_number: int):
        G = self.graph
        k = G.metadata.k
        it = G.nbunch_iter(data="sequence")
        if hasattr(self._index_type, "build_dna"):
            self._index_type.build_dna(
                it, self.path / str(shard_index), k, shard_index, shard_number
            )
            return
        index_iter = (
            (kmer, nid)
            for nid, seq in progress(it, total=G.metadata.size)
            for kmer in DNA(seq).enum_canonical_kmer(k)
            if self.kmer_hash((kmer, None)) % shard_number == shard_index
        )
        self._index_type.build(self.gname, self.path / str(shard_index), index_iter)

    def kmer_hash(self, row: Tuple[Kmer, Any]) -> int:
        """
        This function is a hash functions, that splits the Tuple[Kmer, Nid] between shards of the index.
        Note that this pushes the data into a queue and returns nothing.
        """
        kmer = row[0]
        return (self.hash_key_a * hash(kmer) + self.hash_key_b) % self.hash_key_p
