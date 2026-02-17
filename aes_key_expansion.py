"""AES-128 key schedule expansion."""

from aes_g_func import g_function


def _xor_words(word_a, word_b):
    return [a ^ b for a, b in zip(word_a, word_b)]


def _words_to_round_key(words):
    """Convert 4 words into a 4x4 state matrix (row-major representation)."""
    matrix = [[0] * 4 for _ in range(4)]
    for col in range(4):
        for row in range(4):
            matrix[row][col] = words[col][row]
    return matrix


def expand_key(key_bytes):
    """Expand a 16-byte AES-128 key into 11 round keys (4x4 each)."""
    if len(key_bytes) != 16:
        raise ValueError("AES-128 key must be exactly 16 bytes")

    words = [list(key_bytes[index:index + 4]) for index in range(0, 16, 4)]

    for index in range(4, 44):
        temp = words[index - 1][:]
        if index % 4 == 0:
            temp = g_function(temp, index // 4)
        words.append(_xor_words(words[index - 4], temp))

    round_keys = []
    for round_index in range(11):
        start = round_index * 4
        round_keys.append(_words_to_round_key(words[start:start + 4]))

    return round_keys
