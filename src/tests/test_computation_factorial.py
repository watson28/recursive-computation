from typing import Union
import pytest  # type: ignore
from src.computation import FactorialSolver
from unittest.mock import create_autospec
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


def test_factorial_init_cache_max_factorial():
    cache_instance = _create_mock_cache_instance()

    FactorialSolver(cache_instance).solve(10)

    cache_instance.set_value.assert_any_call(FactorialSolver.MAX_FACTORIAL_KEY, 10)


def test_factorial_doesnt_cache_max_factorial_whe_exist():
    cache_instance = _create_mock_cache_instance(max_factorial=10, max_factorial_result=3628800)

    FactorialSolver(cache_instance).solve(10)

    assert not cache_instance.set_value.called


def test_factorial_return_result_from_cache_when_exist():
    n = 10
    cached_result = 999
    cache_instance = _create_mock_cache_instance(11, 39916800, {str(n): cached_result})

    solver = FactorialSolver(cache_instance)

    assert solver.solve(n) == cached_result


def test_factorial_cache_value_between_n_and_max_computed_factorial():
    n = 10
    max_cached_n = 5
    result_max_cached_n = 120
    cache_instance = _create_mock_cache_instance(max_cached_n, result_max_cached_n)

    solver = FactorialSolver(cache_instance)
    solver.solve(n)

    # +1 because the final cache update for MAX_FACTORIAL_KEY
    assert cache_instance.set_value.call_count == (n - max_cached_n + 1)
    for index, m in enumerate(range(max_cached_n + 1, n + 1)):
        assert cache_instance.set_value.mock_calls[index].args[0] == str(m)


def test_factorial_cache_value_max_factorial():
    n = 10
    max_cached_n = 5
    result_max_cached_n = 120
    cache_instance = _create_mock_cache_instance(max_cached_n, result_max_cached_n)

    solver = FactorialSolver(cache_instance)
    solver.solve(n)

    cache_instance.set_value.assert_called_with(FactorialSolver.MAX_FACTORIAL_KEY, n)


def _create_mock_cache_instance(max_factorial: Union[int, None] = 0, max_factorial_result: Union[int, None] = 1, values: dict = {}):
    MockCache = create_autospec(Cache)

    def mock_get_value(key):
        if key == FactorialSolver.MAX_FACTORIAL_KEY:
            return max_factorial
        if key == str(max_factorial):
            return max_factorial_result
        return values.get(key, None)

    MockCache.return_value.get_value.side_effect = mock_get_value
    MockCache.return_value.get_value_or_fail.side_effect = mock_get_value

    return MockCache()
