from abc import ABC, abstractmethod
from typing import Optional

from modules.articles.dto.article_dto import ArticleDTO
from modules.articles.entities.article_entity import Article
from modules.users.entities.user_entity import User


class ArticleRepository(ABC):
    @abstractmethod
    def find_by_slug(self, slug: str) -> Optional[Article]:
        ...

    @abstractmethod
    def add_article(self, article: ArticleDTO, slug: str, logged_user: User) -> Optional[Article]:
        ...
