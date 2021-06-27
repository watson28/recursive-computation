from src.computation import AckermannSolver
from src.cache import Cache
import pytest  # type: ignore
from unittest.mock import create_autospec

ackermann_test_cases = [
    {'m': 0, 'n': 0, 'result': 1},
    {'m': 0, 'n': 1, 'result': 2},
    {'m': 0, 'n': 2, 'result': 3},
    {'m': 0, 'n': 3, 'result': 4},
    {'m': 0, 'n': 4, 'result': 5},
    {'m': 1, 'n': 0, 'result': 2},
    {'m': 1, 'n': 1, 'result': 3},
    {'m': 1, 'n': 2, 'result': 4},
    {'m': 1, 'n': 3, 'result': 5},
    {'m': 1, 'n': 4, 'result': 6},
    {'m': 2, 'n': 0, 'result': 3},
    {'m': 2, 'n': 1, 'result': 5},
    {'m': 2, 'n': 2, 'result': 7},
    {'m': 2, 'n': 3, 'result': 9},
    {'m': 2, 'n': 4, 'result': 11},
    {'m': 3, 'n': 0, 'result': 5},
    {'m': 3, 'n': 1, 'result': 13},
    {'m': 3, 'n': 2, 'result': 29},
    {'m': 3, 'n': 3, 'result': 61},
    {'m': 3, 'n': 4, 'result': 125},
    {'m': 4, 'n': 0, 'result': 13},
    {'m': 4, 'n': 1, 'result': 65533},
    {'m': 5, 'n': 0, 'result': 65533},
]


@pytest.mark.parametrize(
    'm,n,result',
    [(case['m'], case['n'], case['result']) for case in ackermann_test_cases]
)
def test_solver_return_correct_value(m: int, n: int, result: int):
    solver = AckermannSolver(_create_mock_cache_instance())

    assert(solver.solve(m, n)) == result


def test_solver_cache_result():
    cache = _create_mock_cache_instance()
    solver = AckermannSolver(cache)

    solver.solve(3, 0)

    cache.set_value.assert_called_with('3,0', 5)


def test_solver_return_result_from_cache_when_exist():
    cached_result = 999
    cache = _create_mock_cache_instance({'3,0': cached_result})
    solver = AckermannSolver(cache)

    result = solver.solve(3, 0)

    cache.get_value.assert_called_with('3,0')
    assert result == cached_result


def _create_mock_cache_instance(values: dict = {}):
    MockCache = create_autospec(Cache)
    MockCache.return_value.get_value.side_effect = lambda key: values.get(key, None)

    return MockCache()
