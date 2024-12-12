import logging
from contextlib import contextmanager
from datetime import datetime
from itertools import groupby
from math import sqrt
from pathlib import Path
from typing import Tuple
from uuid import uuid4

src_root = Path(__file__).parent

last_call = None


def chunk(g, n):
    """Return an iterable over chunk of g of size n; last chunck is of size possibly less than n."""
    for _, x in groupby(enumerate(g), lambda e: e[0] // n):
        yield map(lambda e: e[1], x)


def sizeof_fmt(num: float | int, suffix: str = "B") -> str:
    """Taken from https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size"""
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def number_fmt(num: int) -> str:
    if num > 10**9:
        return f"{num/10**9:0.1f}G"
    if num > 10**6:
        return f"{num/10**6:0.1f}M"
    if num > 10**3:
        return f"{num/10**6:0.1f}K"
    return str(num)


def new_gid():
    return str(uuid4()).replace("-", "")


def compute_sign(seq1: str, seq2: str):
    raise NotImplementedError


def cantor_pairing(k1: int, k2: int) -> int:
    """Cantor pairing function to map two non-negative integers to a single non-negative integer."""
    return (k1 + k2) * (k1 + k2 + 1) // 2 + k2


def inverse_cantor_pairing(z: int) -> Tuple[int, int]:
    """Inverse of the Cantor pairing function to map a single non-negative integer to a pair of non-negative integers."""
    w = (sqrt(8 * z + 1) - 1) // 2
    t = w * (w + 1) // 2
    k2 = z - t
    k1 = w - k2
    return (int(k1), int(k2))


class IteratableFromGenerator:
    def __init__(self, generator):
        self.generator = generator

    def __iter__(self):
        return self.generator()


# Logging utility

log_time: dict[str, datetime] = dict()
old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.trace = ""
    record.depth = ""
    base_time = log_time.setdefault(record.trace, datetime.now())
    record.uptime = record.total_uptime = str(datetime.now() - base_time).split(".")[0]
    return record


base_fmt = "{levelname}::{asctime}::{depth}\t::{uptime}/{total_uptime}\t:: {message}\t:: {trace}"


def reset_logfmt():
    logging.basicConfig(format=base_fmt, style="{", force=True)


logging.setLogRecordFactory(record_factory)
vizitig_logger = logging.getLogger("vizitig")
vizitig_logger.setLevel("DEBUG")
reset_logfmt()


def progress(iterator, total: int | None = None):
    last = 0.0
    step = 1.0
    total = total or getattr(iterator, "__len__", lambda: None)()
    with SubLog("progress"):
        if total:
            if total < 100:
                step = 20.0
            elif total < 200:
                step = 10.0
            elif total < 400:
                step = 5.0
            else:
                step = 1.0

            for i, x in enumerate(iterator):
                yield x
                if last + step < (100 * i / total):
                    last = 100 * i / total
                    vizitig_logger.info(f"{last:0.1f}%")

        else:
            for i, x in enumerate(iterator):
                yield x
                if i % 10000 == 0:
                    vizitig_logger.info(f"{i//1000}k")


@contextmanager
def SubLog(key: str, file: Path | None = None, delete_file=False):
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.trace = f"{record.trace}{key}."
        base_time = log_time.setdefault(record.trace, datetime.now())
        if key.startswith("main"):
            log_time["vizitig"] = log_time[record.trace]
        if record.msg == "done":
            del log_time[record.trace]
        now = datetime.now()
        record.uptime = str(now - base_time).split(".")[0]
        record.depth += "-"
        return record

    logging.setLogRecordFactory(record_factory)
    if file:
        handler = logging.FileHandler(file)
        handler.setFormatter(logging.Formatter(base_fmt, style="{"))
        vizitig_logger.addHandler(handler)
    vizitig_logger.info("start")
    try:
        yield file
    finally:
        vizitig_logger.info("done ", extra=dict(end=True))
        logging.setLogRecordFactory(old_factory)
        if file:
            vizitig_logger.removeHandler(handler)
