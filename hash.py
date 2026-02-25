"""Hash utilities for AES workflow."""


def polynomial_rolling_hash(data, base=257, mod=(2**61 - 1), width=6):
    """Return a fixed-length base62 polynomial rolling hash."""
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    payload = data.encode("utf-8") if isinstance(data, str) else bytes(data)

    value = 0
    for byte in payload:
        value = (value * base + byte + 1) % mod

    if value == 0:
        encoded = "0"
    else:
        chars = []
        while value > 0:
            value, remainder = divmod(value, 62)
            chars.append(alphabet[remainder])
        chars.reverse()
        encoded = "".join(chars)

    if len(encoded) < width:
        encoded = encoded.rjust(width, "0")
    return encoded[-width:]
