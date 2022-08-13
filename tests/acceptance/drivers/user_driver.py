from acceptance.drivers.client import client_factory
from src.modules.users.controllers.user_controller import USERS_URL
from tests.acceptance.drivers.auth_driver import AuthDriver


class UserDriver(AuthDriver):

    def __init__(self):
        AuthDriver.__init__(self)

    async def create_test_client(self):
        self.__test_client = await client_factory()

    async def get_user(self, user_id: str, token: str) -> dict:
        await self.create_test_client()
        header = AuthDriver._generate_auth_header(token)
        url = USERS_URL + "/" + user_id
        user = await self.__test_client.get(url, headers=header)

        return user.json()
