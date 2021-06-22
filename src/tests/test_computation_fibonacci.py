import json
import os
from unittest import TestCase 
import pytest # type: ignore
from src.computation import FibonacciSolver

test_cases_file_path =os.path.join(os.path.dirname(__file__), './fibonacci_test_cases.json')
fibonacci_test_cases = json.load(open(test_cases_file_path))

@pytest.mark.parametrize(
    'n,result',
    [(case['n'], case['result']) for case in fibonacci_test_cases]
)
def test_fibonacci_cases(n, result):
    solver = FibonacciSolver()
    assert(solver.solve(n)) == result
