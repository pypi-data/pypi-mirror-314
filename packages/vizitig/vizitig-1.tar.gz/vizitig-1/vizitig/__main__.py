import sys

from vizitig import annotate, generate_graph, genes, index, info, run, update
from vizitig.cli import parser

__all__ = ["info", "generate_graph", "run", "update", "genes", "annotate", "index"]


def main():
    args = parser.parse_args(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
