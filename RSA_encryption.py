import json
import random
from traceback import print_tb

try:
  with open('prime_numbers.json', 'r') as f:
      prime_numbers = json.load(f)
except:
  print("prime_numbers.json not found")
  prime_numbers = [7,13,17]


def getRandomPrimeNumber():
    return prime_numbers[random.randint(0, len(prime_numbers) - 1)]


def findFactorsOfNumber(N):
    factors = []

    for prime in prime_numbers:
        if (N % prime) == 0 and prime != 1:
            factors.append(prime)

    return factors


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def modular_inverse(e, phi_n):
    gcd, x, _ = extended_gcd(e, phi_n)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist (e and phi_n are not coprime)")
    return x % phi_n


def getPublicExponent(eulers_totient_function, coprime=True):
    if not coprime:
        return random.randint(2, eulers_totient_function - 1)

    factors = findFactorsOfNumber(eulers_totient_function)

    while True:
        coprime = True
        provisional_E = random.randint(2, eulers_totient_function - 1)

        for factor in factors:
            if factor == 1:
                None
            elif (provisional_E % factor) == 0:
                coprime = False
                print(f"{provisional_E} is not a coprime of {eulers_totient_function}")
                continue

        if coprime:
            print(f"{provisional_E} is a coprime of {eulers_totient_function}")
            return provisional_E


first_prime_number = 19006727
#first_prime_number = getRandomPrimeNumber()
print("First prime number: ", first_prime_number)
second_prime_number = 190035613
# second_prime_number = getRandomPrimeNumber()
print("Second prime number: ", second_prime_number)

n = first_prime_number * second_prime_number
print("public key: " + str(n))

eulers_totient_function = (first_prime_number - 1) * (second_prime_number - 1)
print("eulers totient function: " + str(eulers_totient_function))

public_exponent = getPublicExponent(eulers_totient_function, True)

#GCD_list = findGCD(eulers_totient_function, public_exponent)
#print(GCD_list)

# Calculate the modular inverse
private_exponent = modular_inverse(public_exponent, eulers_totient_function)
print(f"The modular inverse (d) is: {private_exponent}")

#private_exponent = find_D(GCD_list)
#print(private_exponent)

public_key = [n, public_exponent]
private_key = [n, private_exponent]

print(public_key)
print(private_key)


def convert_to_ashii(message):
    return int(''.join(f"{ord(c):03}" for c in message))


def decode_ascii_string(numeric_string):
    return ''.join(chr(int(numeric_string[i:i + 3])) for i in range(0, len(numeric_string), 3))


def encrypt(message, public_exponent, public_key):
    print("Starting encryption")
    message_int = convert_to_ashii(message)
    print("ASCII message as integer:", message_int)

    if message_int >= public_key:
        raise ValueError("Message is too large for the key size. Please use a larger key or split the message.")

    encrypted_message = pow(message_int, public_exponent, public_key)
    print("Encrypted message:", encrypted_message)
    return encrypted_message


def decrypt(encrypted_message, private_exponent, n):
    print("Starting decryption")
    decrypted_int = pow(encrypted_message, private_exponent, n)
    print("Decrypted integer:", decrypted_int)

    decoded_text = decode_ascii_string(str(decrypted_int).zfill(3))
    print("Decrypted message:", decoded_text)
    return decoded_text


message = encrypt("hello", public_exponent, n)
decrypt(message, private_exponent, n)
