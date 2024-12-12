import asyncio
import concurrent.futures


def run_with_keyword(f, *args):
    return f(*args[:-1], **args[-1])


def async_subproc(fct):
    """In async context, we need to decorate long running
    process (and CPU intensive one) to be able to fork them
    appropriately.

    For some weird reason, run_in_executor takes only *args and not
    kword argument.

    """

    async def _fct(*args, **kwargs):
        loop = asyncio.get_running_loop()
        with concurrent.futures.ProcessPoolExecutor() as pool:
            return await loop.run_in_executor(
                pool, run_with_keyword, fct, *args, kwargs
            )

    return _fct
