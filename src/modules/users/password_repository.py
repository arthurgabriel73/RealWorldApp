from abc import ABC, abstractmethod
from typing import Optional

from modules.auth.entities.password_entity import Password


class PasswordRepository(ABC):
    @abstractmethod
    def add_password(self, username: str, salted_hash: str) -> str:
        ...

    @abstractmethod
    def get_password(self, password_id: int) -> Optional[Password]:
        ...
