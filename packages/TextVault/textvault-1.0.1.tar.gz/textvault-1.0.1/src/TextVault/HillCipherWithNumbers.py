from .base_class import Encryptor, Key
import random
import numpy as np

class Hillcipherwithnumbers(Encryptor):

    def __init__(self, key_matrix=None, size=2):
        self.mod = 128  # Using ASCII range
        if key_matrix:
            self.key_matrix = np.array(key_matrix)
        else:
            self.key_matrix = self.newkey(size)

    def newkey(self, size):
        while True:
            matrix = [[random.randint(0, self.mod - 1) for _ in range(size)] for _ in range(size)]
            try:
                det = int(round(np.linalg.det(matrix)))
                if np.gcd(det, self.mod) == 1:  # Ensure determinant is invertible mod self.mod
                    self.key_matrix = np.array(matrix)
                    return self.key_matrix
            except np.linalg.LinAlgError:
                continue

    def _char_to_num(self, char):
        if char.isalpha():
            return ord(char)  # Use ASCII code for alphabets
        elif char.isdigit():
            return ord(char)  # Treat digits as their ASCII values

    def _num_to_char(self, num):
        if 48 <= num <= 57:  # ASCII range for digits
            return chr(num)  # Convert back to digit characters
        elif 65 <= num <= 90 or 97 <= num <= 122:  # ASCII range for alphabets
            return chr(num)  # Convert back to alphabet characters
        else:
            raise ValueError("Invalid number for conversion to character")

    def _process_text(self, text):
        nums = [self._char_to_num(char) for char in text]
        while len(nums) % self.key_matrix.shape[0] != 0:
            nums.append(0)  # Padding with 0
        return np.array(nums)

    def encrypt(self, plaintext):
        nums = self._process_text(plaintext)
        nums = nums.reshape(-1, self.key_matrix.shape[0])
        encrypted_nums = (np.dot(nums, self.key_matrix) % self.mod).flatten()
        return encrypted_nums.tolist()

    def decrypt(self, encrypted_nums):
        encrypted_nums = np.array(encrypted_nums)
        encrypted_nums = encrypted_nums.reshape(-1, self.key_matrix.shape[0])
        det = int(round(np.linalg.det(self.key_matrix)))
        det_inv = pow(det, -1, self.mod)
        adj = np.round(np.linalg.inv(self.key_matrix) * det).astype(int)  # Adjugate matrix
        inverse_key = (det_inv * adj % self.mod).astype(int)
        decrypted_nums = (np.dot(encrypted_nums, inverse_key) % self.mod).flatten()
        return ''.join(self._num_to_char(int(round(num))) for num in decrypted_nums if num != 0)

    def generate_random_password(self):
        """
        Generates a random password of length between 8 and 16 characters consisting of alphabets and numbers.
        """
        length = random.randint(8, 16)
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.choices(characters, k=length))
