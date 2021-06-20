from typing import Generator

def big_multiply(rev_a: str, rev_b: str, chunk_size = 1) -> Generator[str, None, None]:
    """
    Computes the product of two large numbers.
    It expects the numbers to be in reverses order.
    The result is partially retuned in a generator in reverse order,
    starting with the less significant digits till the most significant ones.
    """
    m = (len(rev_a) // chunk_size)
    n = (len(rev_b) // chunk_size)
    carry = 0
    for col in range(m + n -1):
        a_max = min(col, m-1)
        a_min = max(col - n +1, 0)
        b_min = max(col - m + 1, 0)
        col_size = a_max - a_min + 1
        col_total = 0
        for i in range(col_size):
            col_total += (
                + _get_subnum(rev_a, chunk_size, a_min + i)*_get_subnum(rev_b, chunk_size, b_min + col_size - i - 1)
            )
        col_total_str = str(col_total + carry)
        is_last_col = (col == (m + n - 2))
        if is_last_col:
            yield col_total_str[::-1]
        else:
            yield col_total_str[-chunk_size:][::-1]
            carry = int(col_total_str[:-chunk_size]) if len(col_total_str) > chunk_size else 0


def _get_subnum(rev_number: str, chunk_size: int, chunk_index: int) -> int:
    return int(
        rev_number[chunk_size*chunk_index: chunk_size*(chunk_index + 1)][::-1]
    )