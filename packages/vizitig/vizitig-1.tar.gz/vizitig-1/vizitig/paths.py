from pathlib import Path
from vizitig.env_var import VIZITIG_DIR

root = Path(VIZITIG_DIR)

if not root.exists():
    root.mkdir()

graphs_path = root / "data"
graphs_log = root / "log"
index_path = root / "index"

if not graphs_path.exists():
    graphs_path.mkdir()


def graph_path_name(name: str) -> Path:
    return Path(graphs_path, f"{name}.db")


def log_path_name(name: str) -> Path:
    if not graphs_log.exists():
        graphs_log.mkdir()
    return Path(graphs_log, f"{name}.db")


def index_path_name(name: str) -> Path:
    path = index_path / name
    if not path.exists():
        path.mkdir(parents=True)
    return path
