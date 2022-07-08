from abc import ABC, abstractmethod
from typing import Optional

from src.modules.users.entities.user import User
from src.schemas.user_dto import UserSignUp, UserComplete, UserUpdate


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        ...

    @abstractmethod
    def create_new_user(self, user: UserSignUp) -> Optional[User]:
        ...

    @abstractmethod
    def update_user(self, user_id: int, user: UserUpdate) -> Optional[User]:
        ...
