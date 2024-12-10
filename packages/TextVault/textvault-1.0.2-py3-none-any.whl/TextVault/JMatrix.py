import numpy as np

try: from .base_class import Encryptor, Key
except ImportError: from base_class import Encryptor, Key

class JMatrixKey(Key):
    def __init__(self, value, is_private=False):
        super().__init__(value)
        self.is_private = is_private


class JMatrixEncryptor(Encryptor):
    def __init__(self, matrix_size=3):
        self.matrix_size = matrix_size
        self.constant = 31504  # Use n=31504 as the constant seed for matrix generation

    def _generate_matrix(self, constant):
  
        np.random.seed(constant)
        matrix = np.random.randint(1, 10, (self.matrix_size, self.matrix_size))
        while np.linalg.det(matrix) == 0:  # Ensure the matrix is invertible
            matrix = np.random.randint(1, 10, (self.matrix_size, self.matrix_size))
        return matrix

    def newkey(self) -> tuple[JMatrixKey, JMatrixKey]:
        """
        Generates a pair of public and private keys
        """
      
        matrix = self._generate_matrix(self.constant)
        inverse_matrix = np.linalg.inv(matrix)

        public_key = JMatrixKey(value=str(matrix.tolist()), is_private=False)
        private_key = JMatrixKey(value=str(inverse_matrix.tolist()), is_private=True)

        return public_key, private_key

    def encrypt(self, text: str, key: JMatrixKey) -> str:
        """
        Encrypts a plaintext string using the public key
        """

 
        if key.is_private:
            raise ValueError("Private key cannot be used for encryption.")

        matrix = np.array(eval(key.value))  # Deserialize the matrix
        text_vector = [ord(char) for char in text]
        while len(text_vector) % len(matrix) != 0:  # Pad to match matrix size
            text_vector.append(0)
        text_matrix = np.array(text_vector).reshape(-1, len(matrix))
        encrypted_matrix = np.dot(text_matrix, matrix).astype(int)
        return str(encrypted_matrix.tolist())

    def decrypt(self, text: str, key: JMatrixKey) -> str:
        """
        Decrypts an encrypted string using the private key
        """


        if not key.is_private:
            raise ValueError("Public key cannot be used for decryption.")

        inverse_matrix = np.array(eval(key.value))  # Deserialize the inverse matrix
        encrypted_matrix = np.array(eval(text))

        decrypted_matrix = np.dot(encrypted_matrix, inverse_matrix).round().astype(int)

        decrypted_vector = decrypted_matrix.flatten().tolist()
        decrypted_text = ''.join(chr(char) for char in decrypted_vector if char > 0)
        return decrypted_text

