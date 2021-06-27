import pytest  # type: ignore
from src.computation import FactorialSolver
from unittest.mock import MagicMock, create_autospec
from src.cache import Cache

factorial_test_cases = [
    {'n': 0, 'result': 1},
    {'n': 1, 'result': 1},
    {'n': 2, 'result': 2},
    {'n': 3, 'result': 6},
    {'n': 4, 'result': 24},
    {'n': 5, 'result': 120},
    {'n': 6, 'result': 720},
    {'n': 7, 'result': 5040},
    {'n': 8, 'result': 40320},
    {'n': 9, 'result': 362880},
    {'n': 10, 'result': 3628800},
    {'n': 11, 'result': 39916800},
    {'n': 12, 'result': 479001600},
    {'n': 13, 'result': 6227020800},
    {'n': 14, 'result': 87178291200},
    {'n': 15, 'result': 1307674368000},
    {'n': 16, 'result': 20922789888000},
    {'n': 17, 'result': 355687428096000},
    {'n': 18, 'result': 6402373705728000},
    {'n': 19, 'result': 121645100408832000},
    {'n': 20, 'result': 2432902008176640000},
]


@pytest.mark.parametrize(
    'n,result',
    [(case['n'], case['result']) for case in factorial_test_cases]
)
def test_factorial_solver_return_correct_value(n, result):
    cache_instance = _create_mock_cache_instance()

    solver = FactorialSolver(cache_instance)

    assert(solver.solve(n)) == result


def test_factorial_cache_value_of_computed_factorial():
    n = 10
    cache_instance = _create_mock_cache_instance()

    result = FactorialSolver(cache_instance).solve(n)

    cache_instance.add_to_set_value.assert_called_with(FactorialSolver.CACHED_VALUES_KEY, n)
    cache_instance.set_value.assert_called_with(str(n), result)


def test_factorial_use_cached_value_when_exist():
    n = 10
    cached_values = {'10': 999, '9': 888, '8': 777}
    cache_instance = _create_mock_cache_instance(cached_values)

    result = FactorialSolver(cache_instance).solve(n)

    assert result == cached_values[str(n)]


def test_factorial_returns_correct_value_when_exist_cached_value_lower_than_n():
    cached_values = {'10': 999, '9': 888, '8': 777}
    cache_instance = _create_mock_cache_instance(cached_values)

    result = FactorialSolver(cache_instance).solve(11)

    assert result == 11 * cached_values['10']


def _create_mock_cache_instance(values: dict = {}) -> MagicMock:
    MockCache = create_autospec(Cache)

    def mock_get_value(key):
        return values.get(key, None)

    MockCache.return_value.get_value.side_effect = mock_get_value
    MockCache.return_value.get_value_or_fail.side_effect = mock_get_value
    MockCache.return_value.get_set_value.return_value = sorted(map(lambda item: int(item), values.keys()))

    return MockCache()
