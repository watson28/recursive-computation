from abc import ABC, abstractclassmethod
from typing import Union
import redis

class NotFoundCachedValueException(Exception):
    pass

class Cache(ABC):
    @abstractclassmethod
    def get_value(self, key: str) -> Union[int, None]:
        pass

    def get_value_or_fail(self, key: str) -> int:
        value = self.get_value(key)
        if not value:
            raise NotFoundCachedValueException(f'Key "{key} not found in cache.')

        return value

    @abstractclassmethod
    def set_value(self, key: str, value: int) -> None:
        pass


class RedisCache(Cache):
    _cache: redis.Redis

    def __init__(self) -> None:
        super().__init__()
        self._cache = redis.Redis()

    def get_value(self, key: str) -> Union[int, None]:
        return self._cache.get(key)

    def set_value(self, key: str, value: int) -> None:
        self._cache.set(key, value)
        return super().set_value(key, value)