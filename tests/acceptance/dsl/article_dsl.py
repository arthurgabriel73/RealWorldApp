from tests.acceptance.drivers.article_driver import ArticleDriver
from tests.acceptance.dsl.auth_dsl import AuthDSL
from src.exceptions.not_found import ArticleNotFound

from faker import Faker

from src.tools.generate_slug import generate_slug

fake = Faker()


class ArticleDSL:

    def __init__(self):
        self._driver = ArticleDriver()
        self._authDSL = AuthDSL()
        self._article = None
        self.__slug = ""

    def reset_data_cache(self):
        self.__slug = ""
        self._article = {}

    async def create_article(self):
        title = fake.pystr()
        article = {
            "title": title,
            "description": "string",
            "body": "string",
            "tag_list": []
        }
        self._article = await self._driver.create_test_article(article)
        self.__slug = generate_slug(title)

    async def get_article(self):
        await self.create_article()
        self._article = await self._driver.get_article(self.__slug)

    async def assert_response_is_article_data(self):
        assert self.__slug == self._article["slug"]

    async def get_non_existent_article(self) -> None:
        self.__slug = "NOT A SLUG"
        self._article = await self._driver.get_article(self.__slug)  # CHANGE TO SERVICE

    async def assert_response_is_not_found(self) -> None:
        assert self._article == {
            "detail": ArticleNotFound.generate_message(self.__slug)
        }
