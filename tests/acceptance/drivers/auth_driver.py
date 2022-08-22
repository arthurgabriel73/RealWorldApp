from acceptance.drivers.client import client_factory
from src.modules.auth.controllers.auth_controller import AUTH_URL


class AuthDriver:
    __LOGGED_USER = {"username": "user", "password": "User123$"}
    __TOKEN_URL = AUTH_URL + "/login"

    def __init__(self):
        self.__test_client = None

    async def create_test_client(self):
        self.__test_client = client_factory()

    @staticmethod
    def _generate_auth_header(token: str) -> dict:
        return {"Authorization": f"Bearer {token}"}

    async def get_token(self) -> str:
        await self.create_test_client()
        token = await self.__test_client.post(self.__TOKEN_URL, data=self.__LOGGED_USER)
        token = token.json().get("access_token")

        return token

