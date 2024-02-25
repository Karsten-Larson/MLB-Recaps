import asyncio

from typing import Any, List, Tuple

def async_generate(obj: callable, args_tuple_list: List[Tuple[Any]] | List[Any]) -> List[Any]:
    async def create(args: Tuple[Any] | Any):
        match args:
            case tuple():
                return obj(*args)
            case _:
                return obj(args)

    async def generate() -> List[Any]:
        tasks = [asyncio.create_task(create(args)) for args in args_tuple_list]

        await asyncio.gather(*tasks)
        return [task.result() for task in tasks]

    return asyncio.run(generate())

def async_run(run: callable, args_tuple_list: List[Tuple[Any]] | List[Any]) -> List[Any]:
    async def create(args: Tuple[Any] | Any):
        match args:
            case tuple():
                return run(*args)
            case _:
                return run(args)

    async def generate() -> List[Any]:
        tasks = [asyncio.create_task(create(args)) for args in args_tuple_list]

        await asyncio.gather(*tasks)
        return [task.result() for task in tasks]

    return asyncio.run(generate())