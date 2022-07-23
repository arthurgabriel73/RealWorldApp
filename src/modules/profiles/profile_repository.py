from abc import ABC, abstractmethod
from typing import Optional

from src.modules.profiles.entities.follow_relation_entity import FollowRelation
from src.modules.users.entities.user_entity import User


class ProfileRepository(ABC):
    @abstractmethod
    def get_followers(self, username) -> list | bool:
        ...

    def follow_user(self, username: str, logged_user: User) -> Optional[FollowRelation]:
        ...
    