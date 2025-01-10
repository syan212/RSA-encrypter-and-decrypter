import random
import sympy
import math
def generate_prime(bits):
    while True:
        prime_candidate = random.getrandbits(bits)
        if sympy.isprime(prime_candidate):
            return prime_candidate
def generate_keys():
    p = generate_prime(1024)
    q = generate_prime(1024)
    while abs(p - q) < 6e156:
        q = generate_prime(1024)
    n = p*q
    totient_n = (p-1)*(q-1)
    if 65537 < totient_n and math.gcd(65537, totient_n) == 1:
        e = 65537
    else:
        return generate_keys()
    d = pow(e,-1,totient_n)
    return [n,e],[n,d]
key_true = input("Generate keys? (y/n):")
encrypt_true = input("Encrypt or decrypt? (e/d):")
if key_true.lower() == "y":
    if encrypt_true.lower() == "e":
        message = input("Enter a message:")
        public,private = generate_keys()
        e = int(public[1])
        n = int(public[0])
        message = int.from_bytes(message.encode(), 'big')
        c = bin(pow(message,e,mod=n))[2:]
        print(f'Ciphertext:{c}')
        print(f'Public key:{public},Private key:{private}')
    else:
        print('Seriously?')
else:
    if encrypt_true.lower() == "e":
        message = input("Enter a message:")
        public = input("Enter n and e:").split(",")
        n = int(public[0])
        e = int(public[1])
        message = int.from_bytes(message.encode(), 'big')
        c = bin(pow(message,e,mod=n))[2:]
        print(f'Ciphertext:{c}')
    else:
        message = input("Enter the ciphertext:")
        private = input("Enter n and d:").split(",")
        d = int(private[1])
        n = int(private[0])
        message = int(message,2)
        c = pow(message,d,mod=n)
        c = c.to_bytes((c.bit_length() + 7) // 8, 'big').decode()
        print(f'Unencrypted message:{c}')