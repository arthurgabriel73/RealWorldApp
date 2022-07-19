from abc import ABC, abstractmethod


class ProfileRepository(ABC):
    @abstractmethod
    def get_followers(self, username) -> list | bool:
        ...

    