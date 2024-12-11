import shutil
import tempfile

from vizitig.env_var import VIZITIG_TMP_DIR
from vizitig.index.classes import Shard, SetShard
from vizitig.utils import SubLog
from vizitig.types import Kmer, DNA
from vizitig.utils import vizitig_logger as logger
from pathlib import Path
from typing import Iterator, Tuple, Iterable, Type
from typing_extensions import Self


try:
    from vizibridge.kmer_index import KmerIndexEntry, DNAIndexEntry, KmerIndex, KmerSet

    class BaseRust:
        priority = 4
        k: int

        @property
        def base_idx(self):
            if not hasattr(self, "_base_idx"):
                self._base_idx = self.base_cls(Path(self.path), self.k)
            return self._base_idx

        def __len__(self) -> int:
            return len(self.base_idx)

        def __iter__(self) -> Iterator[Kmer]:
            last = None
            for kmer in self.base_idx:
                if kmer == last:
                    continue
                last = kmer
                yield Kmer(kmer, self.k)

    class RustSet(BaseRust, SetShard):
        @property
        def base_cls(self) -> Type:
            return KmerSet

        @classmethod
        def build_kmer(
            cls,
            path: Path,
            shard_idx: int,
            shard_number: int,
            kmer_iter: Iterator[Kmer],
            k: int,
        ) -> Self:
            with SubLog(f"Rust Build KmerSet({path})"):
                tmp_fd, _tmp_path = tempfile.mkstemp(prefix=VIZITIG_TMP_DIR)
                open(tmp_fd).close()
                tmp_path = Path(_tmp_path)
                tmp_path.unlink()  # UGLY: if the file exists, rust code will complains
                index_iter = (
                    kmer
                    for kmer in kmer_iter
                    if (cls.hash(kmer) % shard_number == shard_idx)
                )
                logger.info(f"Building index in {tmp_path}")
                KmerSet.build(index_iter, tmp_path, k)
                logger.info(f"file size: {tmp_path.stat().st_size}")
                logger.info(f"moving from {tmp_path} to {path}")
                shutil.copy(tmp_path, path)
            return cls(path, shard_idx, shard_number, k)

        @classmethod
        def build_dna(
            cls,
            path: Path,
            shard_idx: int,
            shard_number: int,
            dna_iter: Iterator[DNA],
            k: int,
        ) -> Self:
            with SubLog(f"Rust Build KmerSet(DNA)({path})"):
                tmp_fd, _tmp_path = tempfile.mkstemp(prefix=VIZITIG_TMP_DIR)
                open(tmp_fd).close()
                tmp_path = Path(_tmp_path)
                tmp_path.unlink()  # UGLY: if the file exists, rust code will complains
                logger.info(f"Building index in {tmp_path}")
                KmerSet.build_dna(dna_iter, tmp_path, k, shard_idx, shard_number)
                logger.info(f"stat: {tmp_path.stat().st_size}")
                logger.info(f"moving from {tmp_path} to {path}")
                shutil.copy(tmp_path, path)
            return cls(path, shard_idx, shard_number, k)

        def __contains__(self, kmer: Kmer) -> bool:
            return kmer in self.base_idx

    class RustIndex(BaseRust, Shard):
        priority = 4
        Set = RustSet

        @property
        def base_cls(self) -> Type:
            return KmerIndex

        @classmethod
        def build_kmer(
            cls,
            path: Path,
            shard_idx: int,
            shard_number: int,
            kmer_iter: Iterator[Tuple[Kmer, int]],
            k: int,
        ) -> Self:
            with SubLog(f"Rust Build Kmer({path})"):
                tmp_fd, _tmp_path = tempfile.mkstemp(prefix=VIZITIG_TMP_DIR)
                open(tmp_fd).close()
                tmp_path = Path(_tmp_path)
                tmp_path.unlink()  # UGLY: if the file exists, rust code will complains
                index_iter = (
                    KmerIndexEntry(kmer=kmer, val=val)
                    for kmer, val in kmer_iter
                    if (cls.hash(kmer) % shard_number == shard_idx)
                )
                logger.info(f"Building index in {tmp_path}")
                KmerIndex.build(index_iter, tmp_path, k)
                logger.info(f"stat: {tmp_path.stat()}")
                logger.info(f"moving from {tmp_path} to {path}")
                shutil.copy(tmp_path, path)
            return cls(path, shard_idx, shard_number, k)

        @classmethod
        def build_dna(
            cls,
            path: Path,
            shard_idx: int,
            shard_number: int,
            dna_iter: Iterator[Tuple[DNA, int]],
            k: int,
        ) -> Self:
            with SubLog(f"Rust Build DNA ({path})"):
                tmp_fd, _tmp_path = tempfile.mkstemp(prefix=VIZITIG_TMP_DIR)
                open(tmp_fd).close()
                tmp_path = Path(_tmp_path)
                tmp_path.unlink()  # UGLY: if the file exists, rust code will complains
                index_iter = (DNAIndexEntry(DNA=DNA, val=val) for DNA, val in dna_iter)
                logger.info(f"Building index in {tmp_path}")
                KmerIndex.build_dna(index_iter, tmp_path, k, shard_idx, shard_number)
                logger.info(f"stat: {tmp_path.stat().st_size}")
                logger.info(f"moving from {tmp_path} to {path}")
                shutil.copy(tmp_path, path)
            return cls(path, shard_idx, shard_number, k)

        def __getitem__(self, kmer: Kmer) -> int:
            return self.base_idx[kmer]

        def join(
            self, kmer_iter: Iterator[Tuple[Kmer, int]]
        ) -> Iterable[Tuple[int, int]]:
            path = self.get_temp_file()
            with SubLog(f"Rust Join Kmer-Iter({path})"):
                kmer_index_entry_it = (
                    KmerIndexEntry(kmer=kmer.base_type, val=val)
                    for kmer, val in kmer_iter
                )
                yield from self.base_idx.join(kmer_index_entry_it, path)

        def join_index(self, other: "RustIndex") -> Iterable[Tuple[int, int]]:
            path = self.get_temp_file()
            with SubLog(f"Rust Join Index({path})"):
                return self.base_idx.join_index(other.base_idx, path)

        def intersection(self, kmer_iter: Iterator[Kmer]) -> Iterable[int]:
            path = self.get_temp_file()
            with SubLog(f"Rust Intersection Kmer-Iter({path})"):
                kmer_base = (kmer.base_type for kmer in kmer_iter)
                return self.base_idx.intersection(kmer_base, path)

        def intersection_index(self, other: RustSet) -> Iterable[int]:
            path = self.get_temp_file()
            with SubLog(f"Rust Intersecton Index({path})"):
                return self.base_idx.intersection_index(other.base_idx, path)


except ImportError as E:  # This could happen with older version of vizibridge
    logger.warning(
        f"Rust Index is not installed, fallback to less efficient index ({E})"
    )
    ...
