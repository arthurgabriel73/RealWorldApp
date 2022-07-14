from abc import ABC, abstractmethod
from typing import Optional

from src.modules.users.entities.user_entity import User
from src.modules.users.dto.user_dto import UserUpdate


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        ...

    @abstractmethod
    def add_user(self, username: str, salted_hash: str) -> Optional[User]:
        ...

    @abstractmethod
    def update_user(self, user_id: int, user: UserUpdate) -> Optional[User]:
        ...

    @abstractmethod
    def find_user_by_username(self, username: str) -> Optional[User]:
        ...