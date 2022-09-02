from tests.acceptance.drivers.client import client_factory
from src.modules.auth.controllers.auth_controller import AUTH_URL
from faker import Faker

fake = Faker()


class AuthDriver:
    __TOKEN_URL = AUTH_URL + "/login"
    __LOGGED_USER = {any: any}

    def __init__(self):
        self.__test_client = None
        self.__username = ""
        self.__password = ""

    async def get_logged_user(self) -> None:
        await self.create_test_user()
        self.__LOGGED_USER = {"username": self.__username, "password": self.__password}

    async def create_test_client(self):
        self.__test_client = client_factory()

    @staticmethod
    def generate_auth_header(token: str) -> dict:
        return {"Authorization": f"Bearer {token}"}

    async def get_token(self) -> str:
        await self.create_test_client()
        await self.get_logged_user()

        token = await self.__test_client.post(self.__TOKEN_URL, data=self.__LOGGED_USER)
        token = token.json().get("access_token")

        return token

    async def create_test_user(self) -> dict:
        await self.create_test_client()

        username = fake.pystr()
        password = fake.password()
        self.__username = username
        self.__password = password

        test_user = {
            "username": username,
            "password": password
        }

        url = AUTH_URL + "/signup"
        response = await self.__test_client.post(url, json=test_user)
        test_user = response.json()

        return test_user

