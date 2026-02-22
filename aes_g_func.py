"""AES g() helper for key expansion."""

from aes_sbox import S_BOX

RCON = [
    0x00,
    0x01,
    0x02,
    0x04,
    0x08,
    0x10,
    0x20,
    0x40,
    0x80,
    0x1B,
    0x36,
]


def g_function(word, round_index):
    """Apply RotWord, SubWord, and Rcon XOR."""
    rotated = word[1:] + word[:1]
    substituted = [S_BOX[value] for value in rotated]
    substituted[0] ^= RCON[round_index]
    return substituted
