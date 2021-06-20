from src.big_number import big_multiply


from ..big_number import big_multiply, _get_subnum

def test_big_multiply():
    a = 2345
    b = 7891
    rev_a = str(a)[::-1]
    rev_b = str(b)[::-1]
    expected_result = str(a*b)[::-1]
    assert ''.join(big_multiply(rev_a, rev_b)) == expected_result
    assert ''.join(big_multiply(rev_a, rev_b, 2)) == expected_result
    # assert ''.join(big_multiply(rev_a, rev_b, 3)) == expected_result

def test_get_subnum_returns_single_digits():
    assert _get_subnum('54321', 1, 0) == 5


def test_get_subnum_returns_two_digits():
    assert _get_subnum('54321', 2, 0) == 45

def test_get_subnum_returns_right_number_from_chunks():
    assert _get_subnum('5432109876', 2, 3) == 89
