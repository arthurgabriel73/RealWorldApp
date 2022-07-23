from abc import ABC, abstractmethod
from typing import Optional

from src.modules.profiles.dto.follow_dto import FollowRelationDTO
from src.modules.users.entities.user_entity import User


class ProfileRepository(ABC):
    @abstractmethod
    def get_followers(self, username) -> list | bool:
        ...

    @abstractmethod
    def follow_username(self, username: str, logged_user: User) -> Optional[FollowRelationDTO]:
        ...

    @abstractmethod
    def unfollow_username(self, username: str, logged_user: User) -> Optional[FollowRelationDTO]:
        ...
    