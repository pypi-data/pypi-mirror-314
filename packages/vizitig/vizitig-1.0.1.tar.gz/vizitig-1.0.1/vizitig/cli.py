import argparse

parser = argparse.ArgumentParser(
    prog="vizitig",
    description="A CLI interface to vizitig",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.set_defaults(func=lambda e: e)

subparsers = parser.add_subparsers(required=True)
