"""AES state conversion helpers."""


def bytes_to_state(block):
    """Convert 16 bytes into AES state matrix (row-major for internal ops)."""
    if len(block) != 16:
        raise ValueError("Block must be exactly 16 bytes")

    state = [[0] * 4 for _ in range(4)]
    for index, value in enumerate(block):
        row = index % 4
        col = index // 4
        state[row][col] = value
    return state


def state_to_bytes(state):
    """Convert AES state matrix back to 16 bytes."""
    output = bytearray(16)
    for col in range(4):
        for row in range(4):
            output[col * 4 + row] = state[row][col]
    return bytes(output)
