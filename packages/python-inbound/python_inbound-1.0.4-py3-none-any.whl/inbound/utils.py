import asyncio
from contextlib import suppress
from typing import Any, Awaitable, Callable, Coroutine, ParamSpec, TypeGuard, TypeVar


P = ParamSpec("P")
R = TypeVar("R")


def lazy_load(path: str) -> Any:
    def _import():
        from importlib import import_module, reload

        try:
            module_path, class_name = path.strip(" ").rsplit(".", 1)
        except ValueError as e:
            raise ImportError(f"{path} isn't a valid module path.") from e

        module = import_module(module_path)
        module = reload(module)

        try:
            return getattr(module, class_name)
        except AttributeError as e:
            raise ImportError(f"Module {path} does not have a `{class_name}` attribute") from e

    return _import


def lazy_load_map(map: dict, key: str) -> Any:
    if key not in map:
        raise ValueError(f"Invalid key: {key}, the options are: {list(map.keys())}")

    return lazy_load(map[key])()


def is_async_callable(f: Callable[..., R | Awaitable[R]]) -> TypeGuard[Callable[..., Awaitable[R]]]:
    """
    Test if the callable is an async callable

    :param f: The callable to test
    """
    from inspect import iscoroutinefunction

    if hasattr(f, "__wrapped__"):
        f = f.__wrapped__

    return iscoroutinefunction(f)


def is_sync_callable(f: Callable[..., R | Awaitable[R]]) -> TypeGuard[Callable[..., R]]:
    """
    Test if the callable is a sync callable

    :param f: The callable to test
    """
    return not is_async_callable(f)


async def gather_with_concurrency(limit: int, *coros: Coroutine) -> list:
    """
    Gather coroutines with a limit on concurrency

    :param limit: The limit of coroutines to run concurrently
    :param coros: The coroutines to run
    """
    semaphore = asyncio.Semaphore(limit)

    async def limited_coro(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(limited_coro(c) for c in coros))


async def cancel_task(task: asyncio.Task) -> None:
    """
    Cancel a task

    :param task: The task to cancel
    """
    task.cancel()

    with suppress(asyncio.CancelledError):
        await task
