from acceptance.drivers.auth_driver import AuthDriver
from acceptance.drivers.client import client_factory
from src.modules.articles.controllers.article_controller import ARTICLES_URL

from faker import Faker


fake = Faker()


class ArticleDriver:

    def __init__(self):
        self.__test_client = None
        self._authDriver = AuthDriver()

    async def create_test_client(self):
        self.__test_client = client_factory()

    async def get_article(self, slug: str) -> dict:
        await self.create_test_client()

        token = await self._authDriver.get_token()
        header = self._authDriver.generate_auth_header(token)
        url = ARTICLES_URL + "/" + slug
        article = await self.__test_client.get(url, headers=header)

        return article.json()

    async def create_test_article(self, article_json: dict) -> dict:
        await self.create_test_client()

        token = await self._authDriver.get_token()
        header = self._authDriver.generate_auth_header(token)
        url = ARTICLES_URL + "/"
        article = await self.__test_client.post(url, headers=header, json=article_json)

        return article.json()
