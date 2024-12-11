import sys

if sys.version_info.major < 3:
    raise ValueError("Incompatible with Python2")


version = "1"
compatible_versions = ("0.4", "0.5", "1")
