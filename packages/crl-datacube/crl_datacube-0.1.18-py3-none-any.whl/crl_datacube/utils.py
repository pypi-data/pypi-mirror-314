import asyncio
import concurrent
from typing import Callable, List


async def async_runner(tasks: List[Callable], workers=4):

    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        buff = []
        for task in tasks:
            buff.append(loop.run_in_executor(executor, task))
        responses = await asyncio.gather(*buff)
    return responses

    