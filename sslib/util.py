def required_bytes_given_bitlength(bits):
    if not isinstance(bits, int):
        raise TypeError("bitlength must be an int")
    if bits < 0:
        raise ValueError("bitlength must be nonnegative")
    return (bits+7) // 8

def required_bytes_given_value(value):
    if not isinstance(value, int):
        raise TypeError("value must be an int")
    if value < 0:
        raise ValueError("value must be nonnegative")
    return required_bytes_given_bitlength(int.bit_length(value))

def int_from_bytes(b):
    if not isinstance(b, bytes):
        raise TypeError("expected a sequence of bytes")
    return int.from_bytes(b, byteorder='big', signed=False)

def int_to_bytes(value):
    if not isinstance(value, int):
        raise TypeError("value must be an int")
    if value < 0:
        raise ValueError("value must be nonnegative")
    return value.to_bytes(length=required_bytes_given_value(value), byteorder='big', signed=False)

def select_prime_larger_than(value):
    if not isinstance(value, int):
        raise TypeError("value must be an int")
    mersenne_primes = list(map(lambda x: 2**x-1, [
        17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423,
        9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091,
        # 756839, 859433, 1257787, 1398269, 2976221, 3021377, 6972593,
    ]))
    extra_primes = [
        # smallest (n+1)-bit primes, where n is a power of two
        2**128 + 51,
        2**192 + 133,
        2**256 + 297,
        2**320 + 27,
        2**384 + 231,
        2**448 + 211,
        2**512 + 75,
        2**768 + 183,
        2**1024 + 643,
        2**1536 + 75,
        2**2048 + 981,
        2**3072 + 813,
        2**4096 + 1761,
    ]
    for prime in sorted(mersenne_primes+extra_primes):
        if prime > value:
            return prime
    raise ValueError("value is too large")

def modular_inverse(a, mod):
    if not isinstance(a, int) or not isinstance(mod, int):
        raise TypeError("values must be ints")
    if mod <= 1:
        raise ValueError("invalid mod")
    if a < 0 or a >= mod:
        raise ValueError("out-of-range value")
    b0 = b = mod
    x0, x1 = 0, 1
    while a > 1:
        if b == 0:
            raise ValueError("value and mod must be coprime")
        q = a // b
        a, b = b, a%b
        x0, x1 = x1-q*x0, x0
    if x1 < 0:
        x1 += b0
    return x1
