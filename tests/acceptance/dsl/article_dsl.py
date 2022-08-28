from acceptance.drivers.article_driver import ArticleDriver
from acceptance.dsl.auth_dsl import AuthDSL
from src.exceptions.not_found import ArticleNotFound

from faker import Faker

from tools.generate_slug import generate_slug

fake = Faker()


class ArticleDSL:

    def __init__(self):
        self._driver = ArticleDriver()
        self._authDSL = AuthDSL()
        self._response = None
        self._token = None
        self.__slug = ""

    def reset_data_cache(self):
        self._token = ""
        self.__slug = ""
        self._response = {}

    async def create_article(self):

        title = fake.pystr()
        article = {
            "title": title,
            "description": fake.pystr(),
            "body": fake.pystr(),
            "tag_list": [fake.pystr(), fake.pystr(), fake.pystr(), fake.pystr()]
        }
        self.__slug = generate_slug(title)
        self._response = await self._driver.create_test_article(article, self._token)

    async def get_article(self):
        await self.create_article()
        self._response = await self._driver.get_article(self.__slug, self._token)

    async def assert_response_is_article_data(self):
        assert self.__slug == self._response["slug"]

    async def get_non_existent_article(self) -> None:
        self.__slug = "NOT A SLUG"
        self._response = await self._driver.get_article(self.__slug, self._token)  # CHANGE TO SERVICE

    async def assert_response_is_not_found(self) -> None:
        assert self._response == {
            "detail": ArticleNotFound.generate_message(self.__slug)
        }
