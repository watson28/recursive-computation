from unittest import TestCase
from src.big_number import big_multiply, big_pow, _get_number_chunk


def test_big_multiply_with_same_length_numbers():
    a = 2345
    b = 7891
    expected_result = str(a * b)
    assert big_multiply(str(a), str(b)) == expected_result
    assert big_multiply(str(a), str(b), 2) == expected_result
    assert big_multiply(str(a), str(b), 3) == expected_result


def test_big_multiplify_with_with_different_length_numbers():
    a = 2345
    b = 789
    expected_result = str(a * b)

    assert big_multiply(str(a), str(b)) == expected_result
    assert big_multiply(str(a), str(b)) == expected_result


def test_big_multiply_commutative_property():
    a = 2345
    b = 789

    assert big_multiply(str(a), str(b)) == big_multiply(str(b), str(a))


def test_big_multiply_produce_same_result_regardless_chunk_size():
    a = 5345834976
    b = 3458439
    expected_result = str(a * b)

    for chunk_size in range(1, len(str(a)) + 1):
        assert big_multiply(str(a), str(b), chunk_size) == expected_result


def test_get_number_chunk_returns_single_digits():
    assert _get_number_chunk('54321', 1, 0) == 5


def test_get_number_chunk_returns_two_digits():
    assert _get_number_chunk('54321', 2, 0) == 5


def test_get_subnum_returns_right_number_from_chunks():
    assert _get_number_chunk('5432109876', 2, 3) == 98


class TestBigPow(TestCase):
    def test_power_of_number(self):
        base = 2345
        power = 7891
        assert big_pow(base, power, 10) == base**power
