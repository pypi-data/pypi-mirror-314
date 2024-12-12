import sqlite3
import tempfile
import shutil
from pathlib import Path
from typing import Iterable, Iterator, Tuple
from typing_extensions import Self
from vizitig.env_var import VIZITIG_TMP_DIR

from vizitig.index.classes import Shard, SetShard
from vizitig.types import Kmer, encode_kmer, decode_kmer
from vizitig.utils import SubLog
from vizitig.utils import vizitig_logger as logger


class BaseSQLite:
    priority = 3
    k: int

    @property
    def connector(self):
        return sqlite3.connect(self._path)

    def __len__(self) -> int:
        with self.connector as db:
            c = db.cursor()
            return next(iter(c.execute("SELECT count FROM kmer_size")))[0]

    def __iter__(self) -> Iterator[Tuple[Kmer]]:
        with self.connector as db:
            c = db.cursor()
            yield from (
                decode_kmer(kmer, self.k)
                for (kmer,) in c.execute("SELECT kmer FROM kmer_idx")
            )


class SQLiteSet(BaseSQLite, SetShard):
    @classmethod
    def build_kmer(
        cls,
        path: Path,
        shard_idx: int,
        shard_number: int,
        kmer_iter: Iterator[Kmer],
        k: int,
    ) -> Self:
        if k < 32:
            kmer_type = "INTEGER"
        else:
            kmer_type = "BLOB"
        if path.exists():
            logger.warning("Index already exists, erasing and rebuilding")
            path.unlink()

        tmp_fd, _tmp_path = tempfile.mkstemp(prefix=VIZITIG_TMP_DIR)
        tmp_path = Path(_tmp_path)
        with sqlite3.connect(tmp_path) as db:
            db.execute(
                f"CREATE TABLE kmer_idx(kmer {kmer_type} PRIMARY KEY) WITHOUT ROWID",
            )
            c = db.cursor()
            c.executemany(
                "INSERT OR IGNORE INTO kmer_idx(kmer) VALUES (?) ",
                (
                    (encode_kmer(kmer, k),)
                    for kmer in kmer_iter
                    if (cls.hash(kmer) % shard_number == shard_idx)
                ),
            )

            logger.info("Counting kmers")
            c.execute(
                "CREATE TABLE kmer_size AS SELECT count(1) as count FROM kmer_idx",
            )
            c.close()
        logger.info(f"moving from {tmp_path} to {path}")
        shutil.move(tmp_path, path)
        return cls(path, shard_idx, shard_number, k)

    def __contains__(self, kmer: Kmer) -> bool:
        if self.hash(kmer) % self._shard_number != self._shard_idx:
            return False

        with self.connector as db:
            c = db.cursor()
            try:
                next(
                    iter(
                        c.execute(
                            "SELECT 1 FROM kmer_idx WHERE kmer=?",
                            (encode_kmer(kmer, self.k),),
                        ),
                    ),
                )[0]
                return True
            except StopIteration:
                return False


class SQLiteIndex(BaseSQLite, Shard):
    Set = SQLiteSet

    @classmethod
    def build_kmer(
        cls,
        path: Path,
        shard_idx: int,
        shard_number: int,
        kmer_iter: Iterator[Tuple[Kmer, int]],
        k: int,
    ) -> Self:
        if k < 32:
            kmer_type = "INTEGER"
        else:
            kmer_type = "BLOB"
        if path.exists():
            logger.warning("Index already exists, erasing and rebuilding")
            path.unlink()

        tmp_fd, _tmp_path = tempfile.mkstemp(prefix=VIZITIG_TMP_DIR)
        tmp_path = Path(_tmp_path)
        with sqlite3.connect(tmp_path) as db:
            db.execute(
                f"CREATE TABLE kmer_idx(kmer {kmer_type} PRIMARY KEY, val INTEGER) WITHOUT ROWID",
            )
            c = db.cursor()
            c.executemany(
                "INSERT OR IGNORE INTO kmer_idx(kmer, val) VALUES (?, ?) ",
                (
                    (encode_kmer(kmer, k), val)
                    for kmer, val in kmer_iter
                    if (cls.hash(kmer) % shard_number == shard_idx)
                ),
            )

            logger.info("Counting kmers")
            c.execute(
                "CREATE TABLE kmer_size AS SELECT count(1) as count FROM kmer_idx",
            )
            c.close()
        logger.info(f"moving from {tmp_path} to {path}")
        shutil.move(tmp_path, path)
        return cls(path, shard_idx, shard_number, k)

    def __getitem__(self, kmer: Kmer) -> int:
        if self.hash(kmer) % self._shard_number != self._shard_idx:
            raise KeyError(kmer)

        with self.connector as db:
            c = db.cursor()
            try:
                return next(
                    iter(
                        c.execute(
                            "SELECT val FROM kmer_idx WHERE kmer=?",
                            (encode_kmer(kmer, self.k),),
                        ),
                    ),
                )[0]
            except StopIteration:
                raise KeyError(kmer)
            finally:
                c.close()

    def join(
        self,
        other: Iterable[Tuple[Kmer, int]],
    ) -> Iterable[Tuple[int, int]]:
        """First we compute an offset for each vizikey.
        Then we insert in a temp table kmer, vizikey_offset
        Then we perform in DB the join.

        This function should be safe to be used with multiprocessing.
        """

        def build_iterator() -> Iterable[Tuple[Kmer, int]]:
            for kmer, value in other:
                yield (encode_kmer(kmer, self.k), value)

        with SubLog("SQLite Join"):
            with self.connector as db:
                c = db.cursor()
                c.execute(
                    "CREATE TEMPORARY TABLE metadata_tmp(kmer INTEGER, key INTEGER, PRIMARY KEY (kmer, key)) WITHOUT ROWID",
                )
                c.executemany(
                    "INSERT OR IGNORE INTO metadata_tmp VALUES (?, ?)", build_iterator()
                )
                logger.info("starting the join")
                it = c.execute("""
SELECT DISTINCT val, key
FROM 
    kmer_idx INNER JOIN metadata_tmp ON kmer_idx.kmer = metadata_tmp.kmer 
""")
                yield from it
                c.close()

    def join_index(self, other: Self) -> Iterable[Tuple[int, int]]:
        assert self.k == other.k

        with self.connector as db:
            c = db.cursor()
            c.execute("ATTACH ? as other", (str(other.path),))
            it = c.execute("""
SELECT DISTINCT A.val, B.val from kmer_idx as A INNER JOIN other.kmer_idx as B
    ON A.kmer = B.kmer
""")
            yield from it
            c.close()

    def intersection(self, other: Iterable[Kmer]) -> Iterable[int]:
        with SubLog("SQLite intersection"):
            with self.connector as db:
                c = db.cursor()
                c.execute(
                    "CREATE TEMPORARY TABLE kmer_tmp(kmer INTEGER PRIMARY KEY) WITHOUT ROWID"
                )
                c.executemany(
                    "INSERT OR IGNORE INTO kmer_tmp VALUES (?)",
                    ((encode_kmer(e, self.k),) for e in other),
                )

                logger.info("starting the intersection")
                yield from (
                    t[0]
                    for t in c.execute("""
SELECT DISTINCT val
FROM 
    kmer_idx INNER JOIN kmer_tmp ON kmer_idx.kmer = kmer_tmp.kmer 
""")
                )
                c.close()

    def intersection_index(self, other: SQLiteSet) -> Iterable[int]:
        assert self.k == other.k

        with self.connector as db:
            c = db.cursor()
            c.execute("ATTACH ? as other", (str(other.path),))
            it = c.execute("""
SELECT DISTINCT A.val from kmer_idx as A INNER JOIN other.kmer_idx as B
    ON A.kmer = B.kmer
""")
            yield from (e[0] for e in it)
            c.close()
