from tests.acceptance.drivers.user_driver import UserDriver
from tests.acceptance.dsl.auth_dsl import AuthDSL
from src.exceptions.not_found import UserNotFound

from faker import Faker

fake = Faker()


class UserDSL:
    def __init__(self):
        self._driver = UserDriver()
        self._authDSL = AuthDSL()
        self.__user = None
        self.__user_id = ""
        self._response = None
        self.__bio = None

    def reset_data_cache(self):
        self.__user_id = ""
        self._response = {}

    def generate_user(self):
        test_user = {
            "username": fake.pystr(),
            "password": fake.password()
        }
        self.__user = test_user

    def get_fake_bio(self):
        bio = fake.pystr()
        self.__bio = bio

    async def get_user(self) -> None:
        self.generate_user()
        self.__user = await self._driver.create_test_user(self.__user)

        self.__user_id = self.__user['id']
        self._response = await self._driver.get_user(self.__user_id)  # CHANGE TO SERVICE

    async def assert_response_is_user_data(self):
        assert self._response["id"] == self.__user_id

    async def get_non_existent_user(self) -> None:
        self.__user_id = "NOT_A_USER"
        self._response = await self._driver.get_user(self.__user_id)  # CHANGE TO SERVICE

    async def assert_response_is_not_found(self) -> None:
        assert self._response == {
            "detail": UserNotFound.generate_message(self.__user_id)
        }

    async def update_valid_user(self) -> None:
        self.generate_user()
        self.__user = await self._driver.create_test_user(self.__user)

        self.__user_id = self.__user["id"]

        user_updated = {
            "username": self.__user["username"],
            "bio": "test bio",
        }

        self._response = await self._driver.update_user(self.__user_id, user_updated)  # CHANGE TO SERVICE
        self.__bio = user_updated["bio"]

    async def assert_response_is_updated_user(self):
        bio = self.__bio
        assert self._response["bio"] == bio
