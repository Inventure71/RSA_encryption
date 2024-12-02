import json
import random
from traceback import print_tb

from test import encrypted_message

try:
    # Load prime numbers from JSON
    with open('prime_numbers.json', 'r') as f:
        prime_numbers = json.load(f)
except:
    print("no file found")
    prime_numbers = []

def getRandomPrimeNumber():
    return prime_numbers[random.randint(0, len(prime_numbers) - 1)]

def findFactorsOfNumber(N):
    factors = []
    for prime in prime_numbers:
        if prime > N:
            break
        elif (N % prime) == 0 and prime != 1:
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
        provisional_E = random.randint(2, eulers_totient_function - 1)
        is_coprime = True
        for factor in factors:
            if (provisional_E % factor) == 0:
                is_coprime = False
                print(f"{provisional_E} is not a coprime of {eulers_totient_function}")
                break
        if is_coprime:
            print(f"{provisional_E} is a coprime of {eulers_totient_function}")
            return provisional_E

# Updated letters string to include space
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

# You can uncomment these lines to use random primes
# first_prime_number = getRandomPrimeNumber()
# second_prime_number = getRandomPrimeNumber()

# For testing purposes, using small primes
first_prime_number = 43
print("First prime number:", first_prime_number)
second_prime_number = 47
print("Second prime number:", second_prime_number)

n = first_prime_number * second_prime_number
print("Public key (n):", n)

eulers_totient_function = (first_prime_number - 1) * (second_prime_number - 1)
print("Euler's totient function:", eulers_totient_function)

public_exponent = getPublicExponent(eulers_totient_function, True)

# Calculate the modular inverse
private_exponent = modular_inverse(public_exponent, eulers_totient_function)
print(f"The modular inverse (d) is: {private_exponent}")

public_key = [n, public_exponent]
private_key = [n, private_exponent]

print("Public Key:", public_key)
print("Private Key:", private_key)

n = 2021
public_exponent = 5
private_exponent = 773

def convert_to_numbers(message):
    """
    Converts a message to its numerical representation.
    Each character is mapped to a 2-digit number:
    A=00, B=01, ..., Z=25, space=26.
    """
    converted_message = ""
    for letter in str(message):
        if letter not in letters:
            raise ValueError(f"Invalid character in message: '{letter}'")
        else:
            # Pad each character to be 2 numbers, e.g., 01 instead of 1
            converted_message += str(letters.index(letter)).zfill(2)
    return int(converted_message)

def decode_ascii_string(numeric_string):
    """
    Decodes a numeric string back to its alphabetical representation.
    """
    new_message = ""
    index = 0
    # Reverse the numeric string
    numeric_string = numeric_string[::-1]
    while index < len(numeric_string):
        # Extract two digits
        if index + 1 < len(numeric_string):
            first_letter = numeric_string[index + 1]
        else:
            first_letter = '0'
        second_letter = numeric_string[index]
        combined = first_letter + second_letter
        num = int(combined)
        if num >= len(letters):
            raise ValueError(f"Invalid numeric value for decoding: {num}")
        new_message += letters[num]
        index += 2
    # Reverse the message to get the correct order
    return new_message[::-1]

def find_max_letters_per_block(n):
    """
    Determines the maximum number of letters per block such that
    the integer representation of the block is less than n.
    """
    k = 1
    while True:
        max_block_int = int('26' * k)
        if max_block_int >= n:
            return k - 1 if k > 1 else 1
        k += 1

def get_encrypted_block_size(n):
    """
    Determines the number of digits required to represent (n - 1).
    This ensures consistent padding for encrypted blocks.
    """
    return len(str(n - 1))

def encrypt(message, public_exponent, n, max_letters, encrypted_block_size):
    """
    Encrypts the message using the public exponent and modulus.
    """
    encrypted_message = ""
    index = 0

    print("\nStarting encryption")
    while index < len(message):
        # Extract the block based on max_letters
        block = message[index:index + max_letters]
        print(f"\nEncrypting block: '{block}'")

        current_block = convert_to_numbers(block)
        print(f"Block in numerical form: {current_block}")

        # Encrypt the block using n as the modulus
        encrypted_int = pow(current_block, public_exponent, n)
        print(f"Encrypted integer: {encrypted_int}")

        # Pad the encrypted block to the fixed size
        encrypted_block = str(encrypted_int).zfill(encrypted_block_size)
        encrypted_message += encrypted_block
        print(f"Encrypted block (padded): {encrypted_block}")
        print(f"Encrypted message so far: {encrypted_message}")

        index += max_letters

    print("\nFinal encrypted message:", encrypted_message)
    return encrypted_message

def decrypt(encrypted_message, private_exponent, n, encrypted_block_size):
    """
    Decrypts the encrypted message using the private exponent and modulus.
    """
    message = ""
    index = 0
    print("\nStarting decryption")

    while index < len(encrypted_message):
        # Extract the encrypted block based on fixed size
        current_block = encrypted_message[index:index + encrypted_block_size]
        print(f"\nEncrypted block: {current_block}")

        # Decrypt the block
        decrypted_int = pow(int(current_block), private_exponent, n)
        print(f"Decrypted integer: {decrypted_int}")

        # Decode the decrypted integer back to characters
        try:
            decoded_block = decode_ascii_string(str(decrypted_int))
            print(f"Decoded block: '{decoded_block}'")
            message += decoded_block
        except ValueError as ve:
            print(f"Decoding error: {ve}")
            return None

        index += encrypted_block_size

    print("\nFinal decrypted message:", message)
    return message

if __name__ == "__main__":
    message = "THE TRUTH WILL SET YOU FREE BUT FIRST IT WILL MAKE YOU MISERABLE"

    # Determine maximum number of letters per block based on n
    max_letters = find_max_letters_per_block(n)
    print(f"\nMax letters per block: {max_letters}")

    # Determine encrypted block size based on n
    encrypted_block_size = get_encrypted_block_size(n)
    print(f"Encrypted block size (digits): {encrypted_block_size}")

    # Encrypt the message
    encrypted_message = encrypt(message, public_exponent, n, max_letters, encrypted_block_size)

    # Decrypt the message
    decrypted_message = decrypt(encrypted_message, private_exponent, n, encrypted_block_size)

    print("\nDecrypted Message:", decrypted_message)
