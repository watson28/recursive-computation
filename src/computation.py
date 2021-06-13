class FibonacciSolver:
    def __init__(self) -> None:
        pass

    def solve(self, n: int) -> int:
        if n == 0:
            return 0
        matrix = self._create_initial_fibonacci_matrix()
        self.pow_fibonacci_matrix(matrix, n -1)

        return matrix[0][0]

    def pow_fibonacci_matrix(self, matrix, n):
        """Compute the power of a fibonacci matrix (2x2) in place"""
        decompositions = []
        while True:
            if n <= 1:
                break
            decompositions.append(n)
            n = n // 2

        initial_matrix = self._create_initial_fibonacci_matrix()
        for exp in reversed(decompositions):
            self._multiply_fibonacci_matrix(matrix, matrix)
            if exp % 2 != 0:
                self._multiply_fibonacci_matrix(matrix, initial_matrix)

            # print(exp+1, matrix[0][0])

    def _multiply_fibonacci_matrix(self, F, M):
        """Compute the product of two fibonacci matrix (2x2) in place by storing result in first matrix param"""
        x = (F[0][0] * M[0][0] +
             F[0][1] * M[1][0])
        y = (F[0][0] * M[0][1] +
             F[0][1] * M[1][1])
        z = (F[1][0] * M[0][0] +
             F[1][1] * M[1][0])
        w = (F[1][0] * M[0][1] +
             F[1][1] * M[1][1])
     
        F[0][0] = x
        F[0][1] = y
        F[1][0] = z
        F[1][1] = w

    def _create_initial_fibonacci_matrix(self):
        return [[1,1], [1,0]]

def ackermann(m: int, n: int) -> int:
    return 0

def factorial(n: int) -> int:
    return 0