import math


def big_multiply(a: str, b: str, chunk_size=1) -> str:
    m = math.ceil(len(a) / chunk_size)
    n = math.ceil(len(b) / chunk_size)
    result = ""
    carry = 0
    a_max = m - 1
    a_min = m
    b_min = n
    for col in range(m + n - 1):
        a_max -= (1 if col >= n else 0)
        a_min = max(a_min - 1, 0)
        b_min = max(b_min - 1, 0)
        col_size = a_max - a_min + 1
        col_total = 0
        for i in range(col_size):
            col_total += (
                + _get_number_chunk(a, chunk_size, a_min + i) * _get_number_chunk(b, chunk_size, b_min + col_size - i - 1)
            )
        col_total_str = str(col_total + carry)
        is_last_col = (col == (m + n - 2))
        if is_last_col:
            result = col_total_str + result
        else:
            result = col_total_str[-chunk_size:] + result
            carry = int(col_total_str[:-chunk_size]) if len(col_total_str) > chunk_size else 0

    return result


def _get_number_chunk(number: str, chunk_size: int, chunk_index: int) -> int:
    total_chunk = math.ceil(len(number) / chunk_size)
    end = len(number) - (total_chunk - 1 - chunk_index) * chunk_size

    return int(
        number[max(end - chunk_size, 0): end]
    )


def big_pow(base: int, power: int, chunk_size=1) -> int:
    decompositions = []
    exp = power
    while True:
        if exp <= 1:
            break
        decompositions.append(exp)
        exp = exp // 2

    base_str = str(base)
    result_str = base_str

    i = 0
    for exp in reversed(decompositions):
        i += 1
        result_str = big_multiply(result_str, result_str, chunk_size)
        if exp % 2 != 0:
            result_str = big_multiply(result_str, base_str, chunk_size)

    return int(result_str)
