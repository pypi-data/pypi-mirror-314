from os import getenv, cpu_count
from pathlib import Path

# VIZITIG_TMP_DIR:
#   directory to store temp files, Default None
VIZITIG_TMP_DIR = getenv("VIZITIG_TMP_DIR")

# VIZITIG_SHARD_NB:
#   default number of shard when building index,
#   default  min(cpu_c - 1, 10) where cpu_c is the CPU_COUNT

if getenv("VIZITIG_SHARD_NB"):
    VIZITIG_SHARD_NB = int(str(getenv("VIZITIG_SHARD_NB")))
else:
    cpu_c = cpu_count()
    if cpu_c is not None:
        VIZITIG_SHARD_NB = min(cpu_c - 1, 10)
    else:
        VIZITIG_SHARD_NB = 4

# VIZITIG_DIR:
#   directory where to store vizitig data, default ~/.vizitig

VIZITIG_DIR = Path(getenv("VIZITIG_DIR", "~/.vizitig")).expanduser()


# VIZITIG_PYTHON_ONLY:
#   use only Python types and do not try to use vizibridge, default False

VIZITIG_PYTHON_ONLY = getenv("VIZITIG_PYTHON_ONLY", False)


# VIZITIG_DEFAULT_INDEX:
#   set the default index to use in vizitig. Default False
#   if not set, vizitig will choose one.

VIZITIG_DEFAULT_INDEX = getenv("VIZITIG_DEFAULT_INDEX")

# VIZITIG_NO_TMP_INDEX:
#   if set, will build temporary index

VIZITIG_NO_TMP_INDEX = False
if getenv("VIZITIG_NO_TMP_INDEX"):
    VIZITIG_NO_TMP_INDEX = True
