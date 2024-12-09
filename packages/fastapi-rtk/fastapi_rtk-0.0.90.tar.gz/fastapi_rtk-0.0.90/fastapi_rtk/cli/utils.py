import asyncio
import time
from typing import Any, Coroutine

from annotated_types import T


def run_in_current_event_loop(coro: Coroutine[Any, Any, T], max_retry=100):
    """
    Runs the given coroutine in the current event loop.

    Args:
        coro (Coroutine[Any, Any, T]): The coroutine to be run.
        max_retry (int, optional): The maximum number of retries to get the event loop. 1 equals to 0.1 second. Defaults to 100.

    Returns:
        T: The result of the coroutine.

    Raises:
        Exception: If failed to get the event loop after the maximum number of retries.
    """
    loop: asyncio.AbstractEventLoop | None = None
    while not loop:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            time.sleep(0.1)
            max_retry -= 1
            if max_retry == 0:
                raise Exception("Failed to get event loop")

    return loop.run_until_complete(coro)
