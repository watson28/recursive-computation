import pytest  # type: ignore
from unittest.mock import MagicMock, create_autospec
from src.computation import FibonacciSolver
from src.cache import Cache

fibonacci_test_cases = [
    {"n": -8, "result": -21},
    {"n": -7, "result": 13},
    {"n": -6, "result": -8},
    {"n": -5, "result": 5},
    {"n": -4, "result": -3},
    {"n": -3, "result": 2},
    {"n": -2, "result": -1},
    {"n": -1, "result": 1},
    {"n": -1, "result": 1},
    {"n": 0, "result": 0},
    {"n": 1, "result": 1},
    {"n": 2, "result": 1},
    {"n": 3, "result": 2},
    {"n": 4, "result": 3},
    {"n": 5, "result": 5},
    {"n": 6, "result": 8},
    {"n": 7, "result": 13},
    {"n": 8, "result": 21},
    {"n": 9, "result": 34},
    {"n": 10, "result": 55},
    {"n": 11, "result": 89},
    {"n": 12, "result": 144},
    {"n": 13, "result": 233},
    {"n": 14, "result": 377},
    {"n": 15, "result": 610},
    {"n": 16, "result": 987},
    {"n": 17, "result": 1597},
    {"n": 18, "result": 2584},
    {"n": 19, "result": 4181},
    {"n": 20, "result": 6765},
    {"n": 21, "result": 10946},
    {"n": 22, "result": 17711},
]


@pytest.mark.parametrize(
    'n,result',
    [(case['n'], case['result']) for case in fibonacci_test_cases]
)
def test_fibonacci_cases(n, result):
    cache_instance = _create_mocked_cache_instance({})

    solver = FibonacciSolver(cache_instance)
    assert(solver.solve(n)) == result


@pytest.mark.parametrize('n', [case['n'] for case in fibonacci_test_cases])
def test_fibonacci_caches_correct_values_when_computing_result(n):
    cache_instance = _create_mocked_cache_instance({})

    FibonacciSolver(cache_instance).solve(n)

    for call in cache_instance.set_value.mock_calls:
        cached_n, cached_result = call.args
        assert cached_result == _find_expected_result(cached_n)


def test_use_cached_positive_input_when_computing_negative():
    n = -8
    cache_instance = _create_mocked_cache_instance({'8': 21})

    FibonacciSolver(cache_instance).solve(n)

    cache_instance.get_value.assert_called_with('8')


def _find_expected_result(n: int):
    return next(
        case['result'] for case in fibonacci_test_cases if str(case['n']) == n
    )


def _create_mocked_cache_instance(values: dict) -> MagicMock:
    MockCache = create_autospec(Cache)
    MockCache.return_value.get_value.side_effect = lambda key: values.get(key, None)

    return MockCache()
