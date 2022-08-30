from acceptance.drivers.client import client_factory
from acceptance.drivers.auth_driver import AuthDriver
from modules.auth.controllers.auth_controller import AUTH_URL

from src.modules.users.controllers.user_controller import USERS_URL

from faker import Faker

fake = Faker()


class UserDriver:

    def __init__(self):
        self.__test_client = None
        self._authDriver = AuthDriver()

    async def create_test_client(self):
        self.__test_client = client_factory()

    async def get_user(self, user_id: str) -> dict:
        await self.create_test_client()

        token = await self._authDriver.get_token()
        header = self._authDriver.generate_auth_header(token)
        url = USERS_URL + "/" + user_id

        user = await self.__test_client.get(url, headers=header)

        return user.json()

    async def update_user(self, user_id: str, user_json: dict) -> dict:
        await self.create_test_client()

        token = await self._authDriver.get_token()
        header = self._authDriver.generate_auth_header(token)
        url = USERS_URL + "/" + user_id

        user = await self.__test_client.put(url, headers=header, json=user_json)

        return user.json()

    async def create_test_user(self, user_json: dict) -> dict:
        await self.create_test_client()

        url = AUTH_URL + "/signup"
        user = await self.__test_client.post(url, json=user_json)

        return user.json()
