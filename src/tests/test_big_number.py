import pytest
from src.big_number import big_multiply
from ..big_number import big_multiply, _get_subnum

def test_big_multiply_with_same_length_numbers():
    a = 2345
    b = 7891
    rev_a = str(a)[::-1]
    rev_b = str(b)[::-1]
    expected_result = str(a*b)[::-1]
    assert ''.join(big_multiply(rev_a, rev_b)) == expected_result
    assert ''.join(big_multiply(rev_a, rev_b, 2)) == expected_result
    assert ''.join(big_multiply(rev_a, rev_b, 3)) == expected_result

def test_big_multiplify_with_with_different_length_numbers():
    a = 2345
    b = 789
    rev_a = str(a)[::-1]
    rev_b = str(b)[::-1]
    expected_result = str(a*b)[::-1]

    assert ''.join(big_multiply(rev_a, rev_b)) == expected_result
    assert ''.join(big_multiply(rev_b, rev_a)) == expected_result

def test_big_multiply_commutative_property():
    a = 2345
    b = 789
    rev_a = str(a)[::-1]
    rev_b = str(b)[::-1]

    assert ''.join(big_multiply(rev_a, rev_b)) == ''.join(big_multiply(rev_b, rev_a))

def test_big_multiply_produce_same_result_regardless_chunk_size():
    a = 5345834976
    b = 3458439
    rev_a = str(a)[::-1]
    rev_b = str(b)[::-1]
    expected_result = str(a*b)[::-1]

    for chunk_size in range(1, len(str(a)) + 1):
        assert ''.join(big_multiply(rev_a, rev_b, chunk_size)) == expected_result


def test_get_subnum_returns_single_digits():
    assert _get_subnum('54321', 1, 0) == 5


def test_get_subnum_returns_two_digits():
    assert _get_subnum('54321', 2, 0) == 45

def test_get_subnum_returns_right_number_from_chunks():
    assert _get_subnum('5432109876', 2, 3) == 89
