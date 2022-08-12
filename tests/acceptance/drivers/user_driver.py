from src.modules.users.controllers.user_controller import USERS_URL
from tests.acceptance.drivers.auth_driver import AuthDriver
from tests.acceptance.drivers.client import client_factory
from httpx import AsyncClient


class UserDriver(AuthDriver):
    def __init__(self):
        AuthDriver.__init__(self)
        self.__test_client: AsyncClient = await client_factory()

    def get_user(self, user_id: str, token: str) -> dict:
        header = AuthDriver._generate_auth_header(token)
        url = USERS_URL + "/" + user_id
        user = await self.__test_client.get(url, headers=header)

        return user.json()
