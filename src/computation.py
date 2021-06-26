from typing import List
from src.cache import Cache
from .big_number import big_pow
import logging

logging.basicConfig(level=logging.INFO)


class FibonacciSolver:
    _cache: Cache

    def __init__(self, cache: Cache) -> None:
        self._cache = cache

    def solve(self, n: int) -> int:
        positive_fibonacci = self._solve_positive(abs(n))
        return positive_fibonacci if n >= 0 else positive_fibonacci * (1 if n % 2 == 1 else -1)

    def _solve_positive(self, n: int) -> int:
        if n == 0:
            return 0

        cached_value = self._cache.get_value(str(n))
        if cached_value is not None:
            return cached_value

        matrix = self._create_initial_fibonacci_matrix()
        self._pow_fibonacci_matrix(matrix, n - 1)

        return matrix[0][0]

    def _pow_fibonacci_matrix(self, matrix: List[List[int]], n: int):
        """Compute the power of a fibonacci matrix (2x2) in place"""
        decompositions = []
        while True:
            if n <= 1:
                break
            decompositions.append(n)
            n = n // 2

        initial_matrix = self._create_initial_fibonacci_matrix()

        # iterated in reversed order so we can cache the fibonacci number
        # of each decomposition.
        for exp in reversed(decompositions):
            self._multiply_fibonacci_matrix(matrix, matrix)
            if exp % 2 != 0:
                self._multiply_fibonacci_matrix(matrix, initial_matrix)

            self._cache.set_value(str(exp + 1), matrix[0][0])
            self._cache.set_value(str(exp), matrix[0][1])
            self._cache.set_value(str(exp - 1), matrix[1][1])

    def _multiply_fibonacci_matrix(self, F, M):
        """Compute the product of two fibonacci matrix (2x2) in place by storing result in first matrix param"""
        x = (F[0][0] * M[0][0]
             + F[0][1] * M[1][0])
        y = (F[0][0] * M[0][1]
             + F[0][1] * M[1][1])
        z = (F[1][0] * M[0][0]
             + F[1][1] * M[1][0])
        w = (F[1][0] * M[0][1]
             + F[1][1] * M[1][1])

        F[0][0] = x
        F[0][1] = y
        F[1][0] = z
        F[1][1] = w

    def _create_initial_fibonacci_matrix(self):
        return [[1, 1], [1, 0]]


def ackermann(m: int, n: int) -> int:
    return ConwayChainedArrowNumber(2, n + 3, m - 2).evaluate() - 3


class ConwayChainedArrowNumber:
    """ Represents numbers using 3-length Conway chained arrow notation p -> q -> r """

    def __init__(self, p, q, r) -> None:
        self.p = p
        self.q = q
        self.r = r
        self._iterations = 0

    def evaluate(self) -> int:
        self._iterations = 0
        result = self._evaluate(self.p, self.q, self.r)
        print('iterations ' + str(self._iterations))
        return result

    def _evaluate(self, p: int, q: int = 1, r: int = 1) -> int:
        if q == 1 or r == 1:
            self._iterations += 1
            return big_pow(p, q, 1000)
        if p == 2 and q == 2:
            return 4
        return self._evaluate(p, self._evaluate(p, q - 1, r), r - 1)


class FactorialSolver:
    MAX_FACTORIAL_KEY = 'max_factorial'
    _cache: Cache

    def __init__(self, cache: Cache) -> None:
        self._cache = cache

    def solve(self, n: int) -> int:
        max_computed_factorial = self._get_max_computed_factorial()
        if n <= max_computed_factorial:
            return self._cache.get_value_or_fail(str(n))

        result = self._cache.get_value_or_fail(str(max_computed_factorial))
        for i in range(max_computed_factorial + 1, n + 1):
            result = result * i
            self._cache.set_value(str(i), result)

        self._cache.set_value(self.MAX_FACTORIAL_KEY, n)
        return result

    def _get_max_computed_factorial(self):
        max_factorial_n = self._cache.get_value(self.MAX_FACTORIAL_KEY)
        if max_factorial_n is None:
            self._cache.set_value(self.MAX_FACTORIAL_KEY, 0)
            self._cache.set_value('0', 1)
            return 0

        return max_factorial_n
