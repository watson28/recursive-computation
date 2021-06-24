import pytest # type: ignore
from src.computation import FactorialSolver
from unittest.mock import Mock, create_autospec
from src.cache import Cache

factorial_test_cases = [
    { 'n': 0, 'result': 1 },
    { 'n': 1, 'result': 1 },
    { 'n': 2, 'result': 2 },
    { 'n': 3, 'result': 6 },
    { 'n': 4, 'result': 24 },
    { 'n': 5, 'result': 120 },
    { 'n': 6, 'result': 720 },
    { 'n': 7, 'result': 5040 },
    { 'n': 8, 'result': 40320 },
    { 'n': 9, 'result': 362880 },
    { 'n': 10, 'result': 3628800 },
    { 'n': 11, 'result': 39916800 },
    { 'n': 12, 'result': 479001600 },
    { 'n': 13, 'result': 6227020800 },
    { 'n': 14, 'result': 87178291200 },
    { 'n': 15, 'result': 1307674368000 },
    { 'n': 16, 'result': 20922789888000 },
    { 'n': 17, 'result': 355687428096000 },
    { 'n': 18, 'result': 6402373705728000 },
    { 'n': 19, 'result': 121645100408832000 },
    { 'n': 20, 'result': 2432902008176640000 },
]


@pytest.mark.parametrize(
    'n,result',
    [(case['n'], case['result']) for case in factorial_test_cases]
)
def test_factorial_solver_return_correct_value(n, result):
    cache = create_autospec(Cache)
    cache.return_value.get_value.return_value = 1
    cache.return_value.get_value_or_fail.return_value = 1

    solver = FactorialSolver(cache())

    assert(solver.solve(n)) == result

def test_factorial_init_cache_max_factorial():
    MockCache = create_autospec(Cache)
    MockCache.return_value.get_value.return_value = None
    MockCache.return_value.get_value_or_fail.return_value = None
    cache_instance = MockCache()

    FactorialSolver(cache_instance) 

    cache_instance.set_value.assert_any_call(FactorialSolver.MAX_FACTORIAL_KEY, 0)
    cache_instance.set_value.assert_any_call('0', 1)

def test_factorial_doesnt_cache_max_factorial_whe_exist():
    MockCache = create_autospec(Cache)
    MockCache.return_value.get_value.return_value = 1
    MockCache.return_value.get_value_or_fail.return_value = 1
    cache_instance = MockCache()

    FactorialSolver(cache_instance)

    assert not cache_instance.set_value.called

def test_factorial_return_result_from_cache_when_exist():
    n = 10
    cached_result = 999
    MockCache = create_autospec(Cache)
    mock_get_value = lambda key: cached_result if key == str(n) else n
    MockCache.return_value.get_value.side_effect = mock_get_value
    MockCache.return_value.get_value_or_fail.side_effect = mock_get_value
    cache_instance = MockCache()

    solver = FactorialSolver(cache_instance)

    assert solver.solve(n) == cached_result

def test_factorial_cache_value_between_n_and_max_computed_factorial():
    n = 10
    max_cached_n = 5
    result_max_cached_n = 120
    MockCache = create_autospec(Cache)
    mock_get_value = lambda key: max_cached_n if key == FactorialSolver.MAX_FACTORIAL_KEY else result_max_cached_n
    MockCache.return_value.get_value.side_effect = mock_get_value
    MockCache.return_value.get_value_or_fail.side_effect = mock_get_value
    cache_instance = MockCache()

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
    MockCache = create_autospec(Cache)
    mock_get_value = lambda key: max_cached_n if key == FactorialSolver.MAX_FACTORIAL_KEY else result_max_cached_n
    MockCache.return_value.get_value.side_effect = mock_get_value
    MockCache.return_value.get_value_or_fail.side_effect = mock_get_value
    cache_instance = MockCache()

    solver = FactorialSolver(cache_instance)
    solver.solve(n) 

    cache_instance.set_value.assert_called_with(FactorialSolver.MAX_FACTORIAL_KEY, n)