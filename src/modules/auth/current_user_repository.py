"""from abc import ABC, abstractmethod
from typing import Optional

from src.modules.users.entities.user_entity import User


class GetCurrentUserRepository(ABC):
    @staticmethod
    @abstractmethod
    def get_current_user() -> Optional[User]:
        ...
"""