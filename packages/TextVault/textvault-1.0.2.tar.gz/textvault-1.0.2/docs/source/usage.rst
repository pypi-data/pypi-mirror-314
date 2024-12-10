=====
Usage
=====

Installation
============

To use TextVault, first install it using pip:

.. code-block:: console

    $ pip install -i https://test.pypi.org/simple/ TextVault

This library requires Python 3.11+ and ``numpy``.
If ``numpy`` is not already installed, you can install it with:

.. code-block:: console

    $ pip install numpy

----------------------------------------------------

.. _knapsack_usage:

Knapsack Encryption Module
==========================

Overview
--------
This module includes ``KnapsackEncryptor`` and ``KnapsackKey`` class.

``KnapsackEncryptor`` class implements `Merkle-Hellman knapsack cryptosystem <https://en.wikipedia.org/wiki/Merkle%E2%80%93Hellman_knapsack_cryptosystem>`_.

How It Works
------------
- ``newkey()``
    This method generates superincreasing sequence as a private key
    and it chooses random modular(> sum of private key) and multipler.
    Then it makes public key by ``[(i*mult)%mod for i in private_key]``

- ``encrypt()``
    This method converts each byte of the plaintext into its integer form and then obtains the binary representation of each integer.
    For every byte, it calculates the sum of the numbers in the public key that correspond to the set bits in the binary representation.
    Finally, it converts list of sum back into text and returns it.
   
- ``decrypt()``
    This method decrypts ciphertext with private key (including sequence, multipier and modular) 
    and reconstructs original text from decrypted list of bytes.
 
For more information, check `Wikipedia <https://en.wikipedia.org/wiki/Merkle%E2%80%93Hellman_knapsack_cryptosystem>`_ and :ref:`API Reference <kanpsack_api>`.

Example
-------

.. code-block:: python

    # After installing TextVault

    from TextVault import KnapsackEncryptor
    txt = "Hello, World!"
    enc = KnapsackEncryptor()

    pub, priv = enc.newkey()
    encrypted = enc.encrypt(txt, pub)
    decrypted = enc.decrypt(encrypted, priv)

    print("Public key:", pub)
    print("Private key:", priv)

    print("Original:", txt)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)

---------------------------------------------

RSA Encryption Module
=====================

This module implements the RSA encryption and decryption algorithm, providing functionality for key generation, encryption, decryption, and saving/loading keys to/from text files.

Overview
--------

The RSA algorithm is an asymmetric cryptographic system that uses a pair of keys:
- **Public Key**: Used to encrypt messages.
- **Private Key**: Used to decrypt messages.

This implementation includes support for Base36 encoding, which allows encrypted messages to be represented as a mix of letters and numbers.

Features
--------
- Generate RSA public and private keys.
- Encrypt plaintext messages using a public key.
- Decrypt ciphertext messages using a private key.
- Save and load keys to and from text files.
- Supports Base36 encoding for ciphertext representation.

Usage
-----

**Key Generation**

The ``newkey()`` function generates a pair of RSA keys (public and private). The keys consist of the following components:
- **Public Key**: `(e, n)`
- **Private Key**: `(d, n)`

Example:

.. code-block:: python

    from TextVault.rsa import RsaEncryptor
    # need to install TextVault into the repository first
    if __name__ == "__main__":
        # Instantiate the Encryptor
        enc = RsaEncryptor()

        print("Generating RSA keys...")
        public_key, private_key = enc.newkey()

-----------------------------------------------------------

Vigenère Encryption Module
==========================

This module implements the Vigenère cipher algorithm, providing functionality to encrypt and decrypt text using a symmetric key.

Core Concept
-------------
The Vigenère cipher is a symmetric encryption technique, meaning the same key is used for both encryption and decryption. The key is a string of uppercase alphabetic characters, and each character in the text is shifted based on the position of the corresponding character in the key.

How It Works
------------
- The `newkey()` method generates a random encryption key of fixed length (10 characters in this case).
- The `encrypt()` method takes plaintext and encrypts it using the provided key.
- The `decrypt()` method decrypts the encrypted text back to its original form using the same key.

Features
--------
- Randomly generates a symmetric Vigenère encryption key.
- Encrypts and decrypts text with the same key.
- Supports both uppercase and lowercase letters, while non-alphabetic characters remain unchanged.


Working Principle
-----------------
The Vigenère cipher uses a key of repeated characters to shift each character in the text. The shift value for each character is determined by the corresponding character in the key. For example, if the key character is "A", the text character is unchanged, but if the key character is "B", the text character is shifted by one position in the alphabet.

Usage Example
--------------
Here’s an example of how to use the Vigenère encryption module:

.. code-block:: python

    from TextVault.vigenere import VigenereEncryptor

    # Create an instance of the Vigenère encryption object
    encryptor = VigenereEncryptor()

    # Generate a new key
    key = encryptor.newkey()

    # Print the generated key
    print("Generated Key:", key.value)

    # Example of encrypting text
    text = "Hello World!"
    encrypted = encryptor.encrypt(text, key)
    print("Encrypted Text:", encrypted)

    # Example of decrypting the text
    decrypted = encryptor.decrypt(encrypted, key)
    print("Decrypted Text:", decrypted)

-----------------------------------------------------------

JMatrix Encryption Module
==========================

`JMatrixEncryptor` is a Python class for matrix-based encryption and decryption. 
It uses a deterministic matrix generation seeded by a constant (`31504`) to create public and private keys.

The public key (a matrix) is used for encryption, while the private key (the matrix's inverse) is used for decryption.

Features
--------

- **newkey()**
    Generates a pair of public and private keys.

- **encrypt(text, key)**
    Encrypts a plaintext string using the public key.

- **decrypt(text, key)**
    Decrypts an encrypted string using the private key.

Usage Examples
--------------

1. **Instantiate the Encryptor**

   .. code-block:: python

       from TextVault.JMatrix import JMatrixEncryptor

       # Create an instance with a matrix size of 3x3
       encryptor = JMatrixEncryptor(matrix_size=3)

2. **Generate Keys**

   .. code-block:: python

       public_key, private_key = encryptor.newkey()
       print(f"Public Key: {public_key}")
       print(f"Private Key: {private_key}")

3. **Encrypt a Message**

   .. code-block:: python

       message = "hello"
       encrypted_message = encryptor.encrypt(message, public_key)
       print(f"Original Message: {message}")
       print(f"Encrypted Message: {encrypted_message}")

4. **Decrypt a Message**

   .. code-block:: python

       decrypted_message = encryptor.decrypt(encrypted_message, private_key)
       print(f"Decrypted Message: {decrypted_message}")

---------------------------------------------

HillCipherWithNumbers Module
============================

The `HillCipherWithNumbers` class implements a modified Hill Cipher algorithm for encrypting and decrypting strings containing both alphabets and numbers. It uses ASCII values for processing and also includes a feature to generate random passwords.

Usage
-----

1. **Initializing the Class**
   - By default, a random key matrix of size 2 is generated.
   - You can also provide your own key matrix.

.. code-block:: python

    from TextVault.HillCipherWithNumbers import Hillcipherwithnumbers

    # Default initialization
    cipher = Hillcipherwithnumbers()

    # Custom key matrix initialization
    key_matrix = [[1, 2], [3, 4]]
    cipher = Hillcipherwithnumbers(key_matrix=key_matrix)

2. **Encrypting Text**

   Encrypt a string containing alphabets and numbers.

.. code-block:: python

    plaintext = "Hello123"
    encrypted = cipher.encrypt(plaintext)
    print("Encrypted:", encrypted)

3. **Decrypting Text**

   Decrypt the encrypted list of numbers back into the original string.

.. code-block:: python

    decrypted = cipher.decrypt(encrypted)
    print("Decrypted:", decrypted)

4. **Generating a Random Password**

   Generate a random password consisting of alphabets and numbers, with a length between 8 and 16 characters.

.. code-block:: python

    password = cipher.generate_random_password()
    print("Random Password:", password)

Advanced Features
-----------------

1. **Generating a New Key**
   - Use the `newkey(size)` method to generate a new random key matrix of the specified size.

.. code-block:: python

    new_key = cipher.newkey(3)  # Generate a 3x3 key matrix
    print("New Key Matrix:", new_key)

2. **ASCII-based Processing**
   - The class processes text by converting each character to its ASCII value for encryption and decryption.

Limitations
-----------

- This class supports only characters within the ASCII range (0–127).
- The key matrix must be invertible under modulo 128 for encryption and decryption to work correctly.

FAQ
---

1. **What can this library be used for?**
   - It can be used for simple encryption and decryption of text-based data.

2. **How is padding handled?**
   - If the length of the text does not match the size of the key matrix, padding with `0` is applied during encryption.

3. **How are numbers treated?**
   - Numbers are treated as their ASCII values and are converted back to their original form during decryption.
