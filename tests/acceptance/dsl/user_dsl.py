from acceptance.drivers.user_driver import UserDriver
from acceptance.dsl.auth_dsl import AuthDSL
from src.exceptions.not_found import UserNotFound

from faker import Faker

fake = Faker()


class UserDSL:
    def __init__(self):
        self._driver = UserDriver()
        self._authDSL = AuthDSL()
        self.__user_id = ""
        self._response = None
        self._token = None
        self.__bio = None

    def reset_data_cache(self):
        self._token = ""
        self.__user_id = ""
        self._response = {}

    def get_fake_bio(self):
        bio = fake.pystr()
        self.__bio = bio

    async def get_user_01(self) -> None:
        self.__user_id = "30e30b31-fa93-487f-b000-edaaa69f050f"  # user
        self._response = await self._driver.get_user(self.__user_id, self._token)  # CHANGE TO SERVICE

    async def assert_response_is_user_01_data(self):
        assert self._response == {
            "id": self.__user_id,
            "username": "user",
            "email": None,
            "image": None,
            "bio": None
        }

    async def get_non_existent_user(self) -> None:
        self.__user_id = "NOT_A_USER"
        self._response = await self._driver.get_user(self.__user_id, self._token)  # CHANGE TO SERVICE

    async def assert_response_is_not_found(self) -> None:
        assert self._response == {
            "detail": UserNotFound.generate_message(self.__user_id)
        }

    async def update_valid_user(self) -> None:
        uuid = "01ad956f-cb73-424e-bb33-a38736486488"  # user_update
        user_json = {
            "username": "user_update",
            "bio": fake.pystr(),
        }
        self._response = await self._driver.update_user(uuid, self._token, user_json)  # CHANGE TO SERVICE
        self.__bio = user_json["bio"]

    async def assert_response_is_updated_user(self):
        bio = self.__bio
        assert self._response == {
            'username': 'user_update',
            'id': None,
            'email': None,
            'image': None,
            'bio': bio
        }
