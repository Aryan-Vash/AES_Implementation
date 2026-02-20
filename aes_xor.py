"""AES AddRoundKey utility."""


def add_round_key(state, round_key):
    """XOR a 4x4 state matrix with a 4x4 round key."""
    return [
        [state[row][col] ^ round_key[row][col] for col in range(4)]
        for row in range(4)
    ]
