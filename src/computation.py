from typing import List
from src.cache import Cache
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


class AckermannSolver:
    _cache: Cache

    def __init__(self, cache: Cache) -> None:
        self._cache = cache

    def solve(self, m: int, n: int) -> int:
        if m == 0:
            return n + 1
        if m == 1:
            return n + 2

        result = self._cache.get_value(f'{m},{n}')
        if result is not None:
            return result

        result = self._evaluate_conway_chained_arrow(2, n + 3, m - 2) - 3
        self._cache.set_value(f'{m},{n}', result)

        return result

    def _evaluate_conway_chained_arrow(self, p: int, q: int = 1, r: int = 1) -> int:
        """
        evalues a 3-length Conway chained arrow number p -> q -> r

        Explicit recursive version:
        if r == 0:
            return p * q
        if q == 1 or r == 1:
            return p**q
        if p == 2 and q == 2:
            return 4
        return self._evaluate_conway_chained_arrow(
            p,
            self._evaluate_conway_chained_arrow(p, q - 1, r),
            r - 1
        )
        """
        q_stack = [q]
        r_stack = [r]

        while (len(r_stack) > 0):
            q_item = q_stack.pop()
            r_item = r_stack.pop()

            if r_item == 0:
                q_stack.append(p * q_item)
            elif q_item == 1 or r_item == 1:
                q_stack.append(p**q_item)
            elif p == 2 and q_item == 2:
                q_stack.append(4)
            else:
                r_stack.append(r_item - 1)
                r_stack.append(r_item)
                q_stack.append(q_item - 1)

        return q_stack.pop()


class FactorialSolver:
    CACHED_VALUES_KEY = 'cached_values'
    _cache: Cache

    def __init__(self, cache: Cache) -> None:
        self._cache = cache

    def solve(self, n: int) -> int:
        sorted_cached_values = self._cache.get_set_value(self.CACHED_VALUES_KEY, 0, n)
        n_floor = sorted_cached_values[-1] if len(sorted_cached_values) > 0 else 0
        n_floor_result = self._cache.get_value_or_fail(str(n_floor)) if n_floor > 0 else 1

        result = 1
        for i in range(n_floor + 1, n + 1):
            result = result * i

        result = result * n_floor_result

        self._cache.set_value(str(n), result)
        self._cache.add_to_set_value(self.CACHED_VALUES_KEY, n)
        return result
