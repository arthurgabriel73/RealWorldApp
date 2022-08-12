from httpx import AsyncClient
from src.modules.auth.controllers.auth_controller import AUTH_URL
from tests.acceptance.drivers.client import client_factory


class AuthDriver:
    __ADMIN = {"username": "user", "password": "User123$"}
    __TOKEN_URL = AUTH_URL + "/login"

    def __init__(self):
        self.__test_client: AsyncClient = await client_factory()

    @staticmethod
    def _generate_auth_header(token: str) -> dict:
        return {"Authorization": f"Bearer {token}"}

    def get_admin_token(self) -> str:
        token = await self.__test_client.post(self.__TOKEN_URL, data=self.__ADMIN)
        token = token.json().get("access_token")

        return token

