from os import getenv
from typing import Callable

import redis

cache: redis.Redis = redis.Redis(host=getenv("CACHE_HOST"), socket_connect_timeout=2)


def get_or_load(key: str, cache_time_in_seconds, if_not_found_callback: Callable[[], object]) -> object:
    if not is_redis_available():
        return if_not_found_callback()
    if cache.exists(key):
        return cache.get(key)
    data = if_not_found_callback()
    cache.set(key, data, ex=cache_time_in_seconds)
    return data


def is_redis_available():
    try:
        cache.ping()
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        print("Redis connection error!")
        return False
    return True
