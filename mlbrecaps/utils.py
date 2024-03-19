import asyncio
import requests
import io
import polars as pl

import itertools
import functools

from typing import Any, List, Tuple

def async_run(func: callable, *args: Any | List[Any]) -> List[Any]:
    # Makes all arguments into lists
    try:
        max_length = max(len(x) for x in args if isinstance(x, list))
    except ValueError:
        raise ValueError("At least one argument must be a list")

    repeated_args = [arg if isinstance(arg, list) else list(itertools.repeat(arg, max_length)) for arg in args]

    # Ensure all list arguments are of the same length
    if not all(len(i) == len(repeated_args[0]) for i in repeated_args):
        raise ValueError("Argument arrays must all be of the same length")

    async def create(*args: List[Any]):
        return func(*args)

    async def generate() -> List[Any]:
        tasks = [asyncio.create_task(create(*args)) for args in zip(*repeated_args)]

        await asyncio.gather(*tasks)
        return [task.result() for task in tasks]

    return asyncio.run(generate())

def copy_cache(func):
    func = functools.cache(func)

    def wrapper(*args, **kwargs):
        return func.copy()

    return wrapper

def dataframe_copy(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).copy()

    return wrapper

def dataframe_from_url(func, use_cache: bool=True):
    if use_cache:
        func = functools.cache(func)

    def wrapper(*args, **kwargs):
        url: str = func(*args, **kwargs)
        csv: bytes = requests.get(url).content

        return pl.read_csv(io.StringIO(csv.decode('utf-8')))

    return wrapper