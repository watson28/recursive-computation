from fastapi.testclient import TestClient
from unittest import TestCase 
from unittest.mock import MagicMock, patch
from requests import Response
from src.server import app
from src.computation import FibonacciSolver


@patch.object(FibonacciSolver, 'solve')
class TestFibonacciService(TestCase):
    client: TestClient

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_requires_number(self, mock_fibonacci_solve: MagicMock):
        response = self._call_fibonacci_service('')
        assert response.status_code == 404

    def test_requires_positive_number(self, mock_fibonacci_solve: MagicMock):
        response = self._call_fibonacci_service(str(-10))
        assert response.status_code == 422

    def test_accept_zero_number(self, mock_fibonacci_solve: MagicMock):
        response = self._call_fibonacci_service(str(0))
        assert response.status_code == 200

    def test_call_computation_fibonacci_with_parameter(self, mock_fibonacci_solve: MagicMock):
        n = 10
        self._call_fibonacci_service(str(n))
        mock_fibonacci_solve.assert_called_with(n)

    def test_returns_result_computation_fibonacci(self, mock_fibonacci_solve: MagicMock):
        result = 11
        mock_fibonacci_solve.return_value = result
        response = self._call_fibonacci_service('6')
        assert response.json()['result'] == result

    def _call_fibonacci_service(self, n: str) -> Response:
        return self.client.get(f'/fibonacci/{n}')