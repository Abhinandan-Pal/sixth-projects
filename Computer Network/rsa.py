import math
import random
from typing import Tuple


def miller_rabin(n: int, k: int = 40) -> bool:
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def is_prime(n: int) -> bool:
    firstprimes = [  # first 100
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
        127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
        179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
        233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
        283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
        353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
        419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
        467, 479, 487, 491, 499, 503, 509, 521, 523, 541
    ]

    if n < 2:
        return False

    if n in firstprimes:
        return True

    for prime in firstprimes:
        if n % prime == 0:
            return False

    return miller_rabin(n)


def gen_prime(nbits: int) -> int:
    assert(nbits % 8 == 0)
    nbytes = int(nbits / 8)
    while True:
        x = int.from_bytes(random.randbytes(nbytes), 'little')
        if is_prime(x):
            return x


def generate_keypair(p, q) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    assert is_prime(p)
    assert is_prime(q)
    assert p != q

    n = p * q
    phi = (p-1) * (q-1)
    e = random.randrange(1, phi)
    g = math.gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = math.gcd(e, phi)
    d = pow(e, -1, phi)

    publickey = (e, n)
    privatekey = (d, n)
    return (publickey, privatekey)


def encrypt(publickey: Tuple[int, int], plaintext: int) -> int:
    key, n = publickey
    ciphertext = pow(plaintext, key, n)
    return ciphertext


def decrypt(privatekey: Tuple[int, int], ciphertext: int) -> int:
    key, n = privatekey
    plaintext = pow(ciphertext, key, n)
    return plaintext


if __name__ == '__main__':
    p = gen_prime(2048)
    q = gen_prime(2048)
    print(p, q)

    publickey, privatekey = generate_keypair(p, q)
    print(publickey, privatekey)

    message = input("Message (int): ")

    encrypted_msg = encrypt(privatekey, int(message))
    print(f"Encrypted message: {encrypted_msg}")

    decrypted_msg = decrypt(publickey, encrypted_msg)
    print(f"Decrypted message: {decrypted_msg}")
