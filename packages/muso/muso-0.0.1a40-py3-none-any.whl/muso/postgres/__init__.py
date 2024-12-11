# -*- coding: UTF-8 -*-

import functools

import orjson
from psycopg.types.json import set_json_dumps, set_json_loads
from psycopg_pool import AsyncConnectionPool

set_json_loads(orjson.loads)
set_json_dumps(orjson.dumps)

_NAMED_POOL_DICT: dict[str, AsyncConnectionPool] = dict()


async def init(
        *, name: str, dsn: str, pool_size: int = 16,
) -> None:
    if name in _NAMED_POOL_DICT:
        raise ValueError(f'Pool "{name}" already exists')
    if pool_size < 1:
        raise ValueError('Pool size should be greater than 0')
    minsize, maxsize = pool_size, pool_size
    if minsize > 4:
        minsize = 4
    kwargs = dict(autocommit=False)
    pool = AsyncConnectionPool(
        conninfo=dsn, min_size=minsize, max_size=maxsize, open=False,
        name=name, kwargs=kwargs)
    await pool.open(wait=True)
    _NAMED_POOL_DICT[name] = pool


async def close_all():
    for _, pool in _NAMED_POOL_DICT.items():
        await pool.close()
    _NAMED_POOL_DICT.clear()


def with_postgres(*, name: str, transaction: bool = False):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            if name not in _NAMED_POOL_DICT:
                raise SyntaxError(f'Pool "{name}" not found')
            async with _NAMED_POOL_DICT[name].connection() as conn:
                async with conn.cursor() as cursor:
                    kwargs['cursor'] = cursor
                    if transaction:
                        async with conn.transaction():
                            result = await func(*args, **kwargs)
                    else:
                        result = await func(*args, **kwargs)
            return result
        return wrapped

    return wrapper
