import pytest  # type: ignore
from src.computation import FibonacciSolver

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
    {"n": 17, "result": 1597}
]


@pytest.mark.parametrize(
    'n,result',
    [(case['n'], case['result']) for case in fibonacci_test_cases]
)
def test_fibonacci_cases(n, result):
    solver = FibonacciSolver()
    assert(solver.solve(n)) == result
