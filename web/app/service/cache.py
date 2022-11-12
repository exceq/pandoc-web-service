from os import getenv
from typing import Callable

import redis

cache: redis.Redis = redis.Redis(host=getenv("CACHE_HOST"))


def get_or_load(key: str, cache_time_in_seconds, if_not_found_callback: Callable[[], object]) -> object:
    if cache.exists(key):
        return cache.get(key)
    data = if_not_found_callback()
    cache.set(key, data, ex=cache_time_in_seconds)
    return data
