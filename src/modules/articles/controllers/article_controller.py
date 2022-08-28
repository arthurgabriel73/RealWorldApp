from fastapi import APIRouter, Depends, Body

from src.modules.auth.controllers.auth_controller import get_user_from_token
from src.modules.users.entities.user_entity import User
from src.config.database_conn import get_session

from src.modules.articles.services.article_service import ArticleService, article_service_factory
from src.modules.articles.dto.article_dto import ArticleDTO, ArticleComplete

ARTICLES_URL = '/articles'

article_router = APIRouter(
    prefix=ARTICLES_URL,
    tags=['Articles'],
    dependencies=[Depends(get_session)]
)


@article_router.post("/", response_model=ArticleComplete)
async def create_article(
        article: ArticleDTO = Body(),
        logged_user: User = Depends(get_user_from_token),
        article_service: ArticleService = Depends(article_service_factory)
) -> ArticleDTO:
    return await article_service.save_article_in_repository(article, logged_user)


@article_router.get("/{slug}", response_model=ArticleComplete)
async def get_article(
        slug: str,
        article_service: ArticleService = Depends(article_service_factory)
) -> ArticleDTO:
    return await article_service.get_article_by_slug(slug)
