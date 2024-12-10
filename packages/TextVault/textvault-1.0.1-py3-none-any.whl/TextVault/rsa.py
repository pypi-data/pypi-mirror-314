try: from .base_class import Encryptor, Key
except ImportError: from base_class import Encryptor, Key

import random
from math import gcd

class RsaEncryptor(Encryptor):
    """
    Encryptor class which implements RSA algorithm.
    """
    def generate_prime(self):
        while True:
            num = random.randint(100, 999)  
            if self.is_prime(num):
                return num

    def is_prime(self,n):
        """Function to check if a number is prime."""
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def modular_inverse(self,e, phi):
        """
        Function to find modular inverse--> formula: (e x d) mod phi(n) = 1
        """
        for d in range(1, phi):
            if (e * d) % phi == 1: 
                return d
        return None

    def base36_encode(self,num):
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if num == 0:
            return "0"
        result = []
        while num:
            num, rem = divmod(num, 36)
            result.append(chars[rem])
        return ''.join(reversed(result))

    def base36_decode(self,encoded_str):
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num = 0
        for char in encoded_str:
            num = num * 36 + chars.index(char)
        return num

    
    def newkey(self) ->  tuple[tuple[int,int],tuple[int,int]]:
        """
        RSA key generation
        """
        p = self.generate_prime()
        q = self.generate_prime()
        while q == p:  # Ensure p and q are different
            q = self.generate_prime()

        n = p * q  # for public and private key
        phi = (p - 1) * (q - 1) #Euler's Totient Function: phi(n)=(p−1)×(q−1)

        # Choose public exponent e
        e = random.choice([i for i in range(2, phi) if gcd(i, phi) == 1]) # for public key

        # Compute private key d
        d = self.modular_inverse(e, phi) # for private key

        return (e, n), (d, n)  # Public key, Private key

    def encrypt(self,plaintext: str, public_key: tuple[int,int]) -> str: 
        """
        Encrypt plaintext with public key and return result.

        :param plaintext: Text to encrypt.
        :type plaintext: str
        :param public_key: public key
        :type public_key: TextVault.KnapsackKey
        :return: encrypted text.
        :rtype: str

        """
        e, n = public_key
        block_size = len(self.base36_encode(n))  
        cipher = [
            self.base36_encode((ord(char) ** e) % n).zfill(block_size)  
            for char in plaintext
        ]
        return ''.join(cipher)  # Combine blocks into a single string

    def decrypt(self,ciphertext: str, private_key: tuple[int,int]) -> str:
        """
        Decrypt ciphertext with private key and return result.

        :param ciphertext: Text to decrypt.
        :type ciphertext: str
        :param private_key: private key
        :type private_key: TextVault.KnapsackKey
        :return: decrypted text.
        :rtype: str

        """
        d, n = private_key
        block_size = len(self.base36_encode(n))  # Use the same block size as encryption
        # Split the ciphertext into fixed-size blocks
        blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]
        plain = ''.join([chr((self.base36_decode(block) ** d) % n) for block in blocks])
        return plain

    def save_keys(self,public_key, private_key):
        """Function to save keys to text files"""
        with open("public_key.txt", "w") as pub_file:
            pub_file.write(f"{public_key[0]}\n{public_key[1]}")
        with open("private_key.txt", "w") as priv_file:
            priv_file.write(f"{private_key[0]}\n{private_key[1]}")

    def load_key(self,file_path):
        """Function to load keys from text files"""
        with open(file_path, "r") as file:
            lines = file.readlines()
            return int(lines[0].strip()), int(lines[1].strip())
        
"""
enc = RsaEncryptor()

pub, priv = enc.newkey()
a = enc.encrypt("Hello, World!", pub)

print(a)
A= enc.decrypt(a, priv)
print(A)

"""
