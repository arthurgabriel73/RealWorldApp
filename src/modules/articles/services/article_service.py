from functools import lru_cache

from fastapi import Depends

from exceptions.already_exists import ArticleAlreadyExists
from exceptions.database_exception import IntegrityError
from exceptions.not_found import ArticleNotFound
from src.modules.articles.article_repository import ArticleRepository
from src.modules.articles.dto.article_dto import ArticleDTO
from src.modules.articles.repositories.article_repository_impl import article_repository_impl_factory
from src.modules.users.entities.user_entity import User
from tools.generate_slug import generate_slug


class ArticleService:
    def __init__(self, article_repository: ArticleRepository):
        self.__article_repo = article_repository

    async def save_article_in_repository(self, article: ArticleDTO, logged_user: User):
        slug = generate_slug(article.title)
        try:
            article = await self.__article_repo.add_article(article, slug, logged_user)
            return article

        except IntegrityError:
            raise ArticleAlreadyExists(article.title)

    async def get_article_by_slug(self, slug: str) -> ArticleDTO:
        article = await self.__article_repo.find_by_slug(slug)
        if article is None:
            raise ArticleNotFound(slug)
        return article


@lru_cache()
def article_service_factory(
        article_repository: ArticleRepository = Depends(article_repository_impl_factory)
) -> ArticleService:
    return ArticleService(article_repository)
