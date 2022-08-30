from functools import lru_cache

import sqlalchemy.exc
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.future import select

from src.config.database_conn import get_session, db_engine_factory
from src.exceptions.database_exception import IntegrityError
from src.modules.articles.article_repository import ArticleRepository
from src.modules.articles.dto.article_dto import ArticleDTO, ArticleComplete
from src.modules.articles.entities.article_entity import Article
from src.modules.users.entities.user_entity import User


class ArticleRepositoryImpl(ArticleRepository):
    def __init__(self, engine: AsyncEngine = Depends(get_session)):
        self.__engine = engine

    async def find_by_slug(self, slug: str) -> ArticleDTO:
        async with AsyncSession(self.__engine) as session:
            query = select(Article).filter(Article.slug == slug)
            result = await session.execute(query)
            article: ArticleDTO = result.scalars().unique().one_or_none()

        return article

    async def add_article(self, article: ArticleDTO, slug: str, logged_user: User) -> ArticleComplete:
        try:
            async with AsyncSession(self.__engine) as session:

                author_id = logged_user.id

                article: Article = Article(
                    slug=slug,
                    title=article.title,
                    description=article.description,
                    body=article.body,
                    author_id=author_id,
                                           )
                session.add(article)
                await session.commit()
                await session.refresh(article)

            return article

        except sqlalchemy.exc.IntegrityError:
            raise IntegrityError()


@lru_cache
def article_repository_impl_factory(
        db_engine: AsyncEngine = Depends(db_engine_factory),
) -> ArticleRepositoryImpl:
    return ArticleRepositoryImpl(db_engine)
