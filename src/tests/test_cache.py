from src.cache import RedisCache
from unittest.mock import patch, MagicMock


@patch('src.cache.redis', autospec=True)
def test_redis_cache_returns_str_value(mock_redis: MagicMock):
    mock_redis.Redis.return_value.get.return_value = b'45'
    cache = RedisCache(db_index=99)

    assert cache.get_value('any_key') == 45


@patch('src.cache.redis', autospec=True)
def test_redis_return_none_when_key_does_not_exist(mock_redis: MagicMock):
    mock_redis.Redis.return_value.get.return_value = None
    cache = RedisCache(db_index=99)

    assert cache.get_value('no_exist_key') is None
