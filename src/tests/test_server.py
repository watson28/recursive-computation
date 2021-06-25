from fastapi.testclient import TestClient
from unittest import TestCase
from unittest.mock import MagicMock, patch
from requests import Response
from src.server import app


@patch('src.server.FactorialSolver', autospec=True)
@patch('src.server.RedisCache', autospec=True)
@patch('src.server.FibonacciSolver', autospec=True)
class TestFibonacciService(TestCase):
    def test_requires_number(self, *args):
        with TestClient(app) as client:
            response = self._call_fibonacci_service(client, '')
            assert response.status_code == 404

    def test_requires_positive_number(self, *args):
        with TestClient(app) as client:
            response = self._call_fibonacci_service(client, str(-10))
            assert response.status_code == 422

    def test_accept_zero_number(self, *args):
        with TestClient(app) as client:
            response = self._call_fibonacci_service(client, str(0))
            assert response.status_code == 200

    def test_call_computation_fibonacci_with_parameter(self, fibonacci_solver: MagicMock, *args):
        n = 10
        with TestClient(app) as client:
            fibonacci_solver.return_value.solve.return_value = 1
            self._call_fibonacci_service(client, str(n))
            fibonacci_solver.return_value.solve.assert_called_with(n)

    def test_returns_result_computation_fibonacci(self, fibonacci_solver: MagicMock, *args):
        result = 11
        with TestClient(app) as client:
            fibonacci_solver.return_value.solve.return_value = result
            response = self._call_fibonacci_service(client, '6')
            assert response.json()['result'] == result

    def _call_fibonacci_service(self, client, n: str) -> Response:
        return client.get(f'/fibonacci/{n}')


@patch('src.server.FibonacciSolver', autospec=True)
@patch('src.server.RedisCache', autospec=True)
@patch('src.server.FactorialSolver', autospec=True)
class TestFactorialService(TestCase):
    def test_requires_number(self, *args):
        with TestClient(app) as client:
            response = self._call_factorial_service(client, '')
            assert response.status_code == 404

    def test_requires_positive_number(self, *args):
        with TestClient(app) as client:
            response = self._call_factorial_service(client, str(-10))
            assert response.status_code == 422

    def test_accept_zero_number(self, *args):
        with TestClient(app) as client:
            response = self._call_factorial_service(client, str(0))
            assert response.status_code == 200

    def test_call_computation_factorial_with_parameter(self, factorial_solver: MagicMock, *args):
        n = 10
        with TestClient(app) as client:
            self._call_factorial_service(client, str(n))
            factorial_solver.return_value.solve.assert_called_with(n)

    def test_returns_result_computation_factorial(self, factorial_solver: MagicMock, *args):
        result = 11
        with TestClient(app) as client:
            factorial_solver.return_value.solve.return_value = result
            response = self._call_factorial_service(client, '6')
            assert response.json()['result'] == result

    def _call_factorial_service(self, client: TestClient, n: str) -> Response:
        return client.get(f'/factorial/{n}')
