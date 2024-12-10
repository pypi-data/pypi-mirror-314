from abc import ABC, abstractmethod
from typing import Any

class Key:
    def __init__(self, value):
        self.value: Any = value
    
    def __repr__(self):
        '''return ``f"Key({self.value})"``'''
        return f"Key({self.value})"
    
    def __str__(self):
        return self.__repr__()

class Encryptor(ABC):
    @abstractmethod
    def newkey(self):
        pass
    
    @abstractmethod
    def encrypt(self, text: str) -> str:
        pass
    
    @abstractmethod
    def decrypt(self, text) -> str:
        pass

# class LengthLimitExceed(Exception):
#     # 암호화 가능한 문자열의 길이를 초과한 경우
#     pass

# class KeyTypeNotMatch(Exception):
#     pass