import asyncio
import webbrowser

import uvicorn

from vizitig.cli import subparsers
from vizitig.info import clean_log


async def delayed_webrowser_launch(delay: int, args):
    await asyncio.sleep(delay)
    webbrowser.open(f"{args.hostname}:{args.port}", new=2)


async def main(args):
    config = uvicorn.Config(
        "vizitig.api:main_api",
        port=args.port,
        host=args.hostname,
        log_level="info",
    )
    server = uvicorn.Server(config)
    tasks = []
    if not args.no_launch_browser:
        tasks.append(asyncio.create_task(delayed_webrowser_launch(2, args)))
    tasks.append(server.serve())
    await asyncio.gather(*tasks)


def run(args):
    clean_log()
    asyncio.run(main(args))


parser = subparsers.add_parser(
    "run",
    help="run Vizitig locally",
)

parser.add_argument("--port", "-p", help="port", type=int, default=4242)

parser.add_argument("--hostname", "-H", help="host", type=str, default="localhost")
parser.add_argument(
    "--no-launch-browser",
    "-l",
    help="flag to avoid to launch the webbrower",
    action="store_true",
)
parser.set_defaults(func=run)
