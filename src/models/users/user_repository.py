from abc import ABC, abstractmethod
from typing import Optional

from src.models.users.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        ...
