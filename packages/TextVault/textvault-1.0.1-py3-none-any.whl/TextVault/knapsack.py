try: from .base_class import Encryptor, Key
except ImportError: from base_class import Encryptor, Key

import random
import base64
from typing import Self

class KnapsackKey(Key):
    """
    Key class for TextVault.KnapsackEncryptor.
    """
    def __init__(self, value: str): 
        super().__init__(value)
    
    def export_txt(self, file_name: str):
        """
        Export key to text file.
        """
        with open(file_name, "w") as f:
            f.write(self.value)
    
    @classmethod
    def import_txt(cls, file_name: str) -> Self:
        """
        Import key from text file.
        """
        with open(file_name, "r") as f:
            return cls(f.read())

class KnapsackEncryptor(Encryptor):
    """
    Encryptor class which implements Merkle-Hellman knapsack cryptosystem.
    """
    
    @staticmethod
    def _list_encode(li: list[int]) -> str:
        b = b'!'.join(base64.b64encode(i.to_bytes(3)) for i in li)
        return b.decode()

    @staticmethod
    def _list_decode(txt: str) -> list[int]:
        ret = [int.from_bytes(base64.b64decode(i)) for i in txt.split('!')]
        return ret
    
    @staticmethod
    def _split_string(txt: str) -> list[int]:
        bt = txt.encode()
        return [*bt]

    @staticmethod
    def _join_string(li: list[int]) -> str:
        tp = [i.to_bytes() for i in li]
        bt = b''.join(tp)
        s = bt.decode()
        return s
    
    def newkey(self) -> tuple[KnapsackKey, KnapsackKey]:
        """
        Return a new (public key, private key) tuple for knapsack-cryptosystem.

        :return: new (public key, private key) tuple
        :rtype: tuple[KnapsackKey, KnapsackKey]

        """

        length = 10

        def isprime(n):
            if n<=1: return False
            for i in range(2, int(n**.5)+1):
                if n%i == 0: break
            else: return True
            return False

        # 초증가 수열 (이전 수들의 합보다 다음 수의 값이 큼)
        private_key = []
        sm = 0
        for _ in range(length):
            private_key.append(sm + random.randint(1,50))
            sm += private_key[-1]
        
        while 1:
            mod = random.randint(sm+1, 65535)
            if isprime(mod): break
        
        mult = random.randint(10,mod-1)

        # private_key = [2, 4, 6, 13, 27, 55, 111]
        # mod = 211
        # mult = 17

        public_key = [(x * mult) % mod for x in private_key]
        private_key += [mod, mult]

        return KnapsackKey(self._list_encode(public_key)), KnapsackKey(self._list_encode(private_key))

    def encrypt(self, text: str, key: KnapsackKey) -> str:
        """
        Encrypt text with public key and return result.

        :param text: Text to encrypt.
        :type text: str
        :param key: public key
        :type key: TextVault.KnapsackKey
        :return: encrypted text.
        :rtype: str

        """
        key = self._list_decode(key.value)

        # key 길이만큼의 이진수(01010111..)로 각 문자열 block들을 표현
        binary_message = [f'{c:0{len(key)}b}' for c in self._split_string(text)]

        encrypted = [sum(int(x[i])*key[i] for i in range(len(key))) for x in binary_message]
        return self._list_encode(encrypted)
    
    def decrypt(self, text: str, key: KnapsackKey) -> str:
        """
        Decrypt text with private key and return result.

        :param text: Text to decrypt.
        :type text: str
        :param key: private key
        :type key: TextVault.KnapsackKey
        :return: decrypted text.
        :rtype: str

        """
        key = self._list_decode(key.value)
        if len(key) < 3: raise ValueError("Key format doesn't match")

        *arr, mod, mult = key
        inv_mult = pow(mult, -1, mod)
        
        encrypted = self._list_decode(text)
        encrypted = [i*inv_mult%mod for i in encrypted]

        recovered = []
        for sum_val in encrypted:
            cur = []
            for value in reversed(arr):
                if sum_val >= value:
                    cur.append('1')
                    sum_val -= value
                else:
                    cur.append('0')
            recovered.append(int(''.join(cur)[::-1],2))

        return self._join_string(recovered)
    

if __name__ == "__main__":
    enc = KnapsackEncryptor()

    pub, priv = enc.newkey()
    a = enc.encrypt("한글 암호화", pub)

    print(a)
    A = enc.decrypt(a, priv)
    print(A)