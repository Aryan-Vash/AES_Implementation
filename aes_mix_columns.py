"""AES MixColumns utilities."""


def gmul(a, b):
    """Galois field multiplication in GF(2^8)."""
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        hi_bit_set = a & 0x80
        a = (a << 1) & 0xFF
        if hi_bit_set:
            a ^= 0x1B
        b >>= 1
    return result


def _mix_single_column(column):
    c0, c1, c2, c3 = column
    return [
        gmul(c0, 2) ^ gmul(c1, 3) ^ c2 ^ c3,
        c0 ^ gmul(c1, 2) ^ gmul(c2, 3) ^ c3,
        c0 ^ c1 ^ gmul(c2, 2) ^ gmul(c3, 3),
        gmul(c0, 3) ^ c1 ^ c2 ^ gmul(c3, 2),
    ]


def _inv_mix_single_column(column):
    c0, c1, c2, c3 = column
    return [
        gmul(c0, 14) ^ gmul(c1, 11) ^ gmul(c2, 13) ^ gmul(c3, 9),
        gmul(c0, 9) ^ gmul(c1, 14) ^ gmul(c2, 11) ^ gmul(c3, 13),
        gmul(c0, 13) ^ gmul(c1, 9) ^ gmul(c2, 14) ^ gmul(c3, 11),
        gmul(c0, 11) ^ gmul(c1, 13) ^ gmul(c2, 9) ^ gmul(c3, 14),
    ]


def mix_columns(state):
    """Apply AES MixColumns on a 4x4 state matrix."""
    mixed = [[0] * 4 for _ in range(4)]
    for col in range(4):
        column = [state[row][col] for row in range(4)]
        transformed = _mix_single_column(column)
        for row in range(4):
            mixed[row][col] = transformed[row]
    return mixed


def inv_mix_columns(state):
    """Apply AES inverse MixColumns on a 4x4 state matrix."""
    mixed = [[0] * 4 for _ in range(4)]
    for col in range(4):
        column = [state[row][col] for row in range(4)]
        transformed = _inv_mix_single_column(column)
        for row in range(4):
            mixed[row][col] = transformed[row]
    return mixed
