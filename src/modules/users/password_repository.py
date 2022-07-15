from abc import ABC, abstractmethod


class PasswordRepository(ABC):
    @abstractmethod
    def add_password(self, username: str, salted_hash: str) -> str:
        ...
