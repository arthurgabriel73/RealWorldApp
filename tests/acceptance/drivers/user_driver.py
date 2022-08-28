from acceptance.drivers.client import client_factory
from acceptance.drivers.auth_driver import AuthDriver
from modules.users.dto.user_dto import IncomingUserDTO, UserComplete


from src.modules.users.controllers.user_controller import USERS_URL
from src.modules.auth.controllers.auth_controller import AUTH_URL


from src.modules.users.user_repository import UserRepository
from src.modules.users.password_repository import PasswordRepository


from faker import Faker

fake = Faker()


class UserDriver:

    def __init__(self):
        self.__test_client = None
        self._authDriver = AuthDriver()

    async def create_test_client(self):
        self.__test_client = client_factory()

    async def get_user(self, user_id: str, token: str) -> dict:
        await self.create_test_client()

        header = AuthDriver.generate_auth_header(token)
        url = USERS_URL + "/" + user_id
        user = await self.__test_client.get(url, headers=header)

        return user.json()

    async def update_user(self, user_id: str, token: str, user_json: dict) -> dict:
        await self.create_test_client()

        header = AuthDriver.generate_auth_header(token)
        url = USERS_URL + "/" + user_id
        user = await self.__test_client.put(url, headers=header, json=user_json)

        return user.json()

    async def create_random_user(self) -> dict:
        await self.create_test_client()

        username = fake.pystr()
        password = fake.password()

        random_user = {
            "username": username,
            "password": password
        }

        url = AUTH_URL + "/signup"
        response = await self.__test_client.post(url, json=random_user)
        random_user = response.json()

        return random_user
