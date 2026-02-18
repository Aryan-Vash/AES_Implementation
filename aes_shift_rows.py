"""AES ShiftRows utilities."""


def shift_rows(state):
    """Cyclic left shift row i by i positions."""
    shifted = [row[:] for row in state]
    for row_index in range(1, 4):
        shifted[row_index] = state[row_index][row_index:] + state[row_index][:row_index]
    return shifted


def inv_shift_rows(state):
    """Cyclic right shift row i by i positions."""
    shifted = [row[:] for row in state]
    for row_index in range(1, 4):
        shifted[row_index] = state[row_index][-row_index:] + state[row_index][:-row_index]
    return shifted
