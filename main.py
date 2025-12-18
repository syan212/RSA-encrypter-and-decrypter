import random
import math
from sympy import isprime


def generate_prime(bits: int) -> int:
    """Generates a prime of size `bits`"""
    while True:
        prime_candidate = random.getrandbits(bits)
        if isprime(prime_candidate):
            return prime_candidate


def generate_keys() -> tuple[tuple[int, int], tuple[int, int]]:
    """Generates RSA key in form [n, e] (public key), [n, d](private key)"""
    p = generate_prime(1024)
    q = generate_prime(1024)
    while abs(p - q) < 6e156:
        q = generate_prime(1024)
    n = p * q
    totient_n = (p - 1) * (q - 1)
    if 65537 < totient_n and math.gcd(65537, totient_n) == 1:
        e = 65537
    else:
        return generate_keys()
    d = pow(e, -1, totient_n)
    return (n, e), (n, d)


key_true = input('Generate keys? (y/n):').lower()
if key_true != 'y' and key_true != 'n':
    print('Invalid input. Enter y/n.')
    exit(1)

encrypt_true = input('Encrypt or decrypt? (e/d):').lower()
if encrypt_true != 'e' and encrypt_true != 'd':
    print('Invalid input. Enter e/d.')
    exit(1)

if key_true == 'y' and encrypt_true == 'd':
    print('Invalid input. Not allowed.')
    exit(1)

message = input(
    'Enter the ciphertext: ' if encrypt_true == 'd' else 'Enter a message: '
)

if key_true == 'y':
    public, private = generate_keys()
    n, e = public[0], public[1]
    message = int.from_bytes(message.encode(), 'big')
    c = bin(pow(message, e, mod=n))[2:]
    print(f'Ciphertext (as a number): {c}')
    print(f'Public key: {public}')
    print(f'Private key: {private}')
else:
    try:
        n, e_or_d = (
            int(num)
            for num in input(
                'Enter n and e:' if encrypt_true == 'e' else 'Enter n and d:'
            ).split(',')
        )
    except ValueError:
        print('Invalid input. Ensure the input is two integers seperated by commas.')
        exit(1)
    d = pow(int(message, 2), e_or_d, mod=n) if encrypt_true == 'd' else 0
    c = (
        bin(pow(int.from_bytes(message.encode(), 'big'), e_or_d, mod=n))
        if encrypt_true == 'e'
        else d.to_bytes((d.bit_length() + 7) // 8, 'big').decode()
    )
    print(f'Ciphertext (as a number): {c}')
