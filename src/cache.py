import os
from abc import ABC, abstractclassmethod
from typing import Union, List
import redis


class NotFoundCachedValueException(Exception):
    pass


class Cache(ABC):
    @abstractclassmethod
    def get_value(self, key: str) -> Union[int, None]:
        pass

    def get_value_or_fail(self, key: str) -> int:
        value = self.get_value(key)
        if value is None:
            raise NotFoundCachedValueException(f'Key "{key} not found in cache.')

        return value

    @abstractclassmethod
    def set_value(self, key: str, value: int) -> None:
        pass

    @abstractclassmethod
    def add_to_set_value(self, key: str, value: int) -> None:
        pass

    @abstractclassmethod
    def get_set_value(self, key: str, start: int, end: int) -> List[int]:
        pass


class RedisCache(Cache):
    _cache: redis.Redis

    def __init__(self, db_index: int) -> None:
        super().__init__()
        self._cache = redis.Redis(
            host=os.environ.get('REDIS_HOST', 'localhost'),
            db=db_index
        )

    def get_value(self, key: str) -> Union[int, None]:
        value = self._cache.get(key)
        return int(value.decode()) if value is not None else None

    def set_value(self, key: str, value: int) -> None:
        self._cache.set(key, value)

    def add_to_set_value(self, key: str, value: int) -> None:
        self._cache.zadd(key, {str(value): value})

    def get_set_value(self, key: str, start: int, end: int) -> List[int]:
        return [
            int(item.decode())
            for item
            in self._cache.zrangebyscore(key, min=start, max=end, withscores=False)
        ]
