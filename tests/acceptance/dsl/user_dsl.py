from src.exceptions.not_found import UserNotFound
from tests.acceptance.drivers.user_driver import UserDriver
from tests.acceptance.dsl.auth_dsl import AuthDSL


class UserDSL(AuthDSL):
    def __init__(self) -> None:
        AuthDSL.__init__(self)
        self._driver = UserDriver()
        self.__user_id = ""

    def reset_data_cache(self):
        self._token = ""
        self.__user_id = ""
        self._response = {}

    async def get_user_01(self) -> None:
        self.__user_id = "30e30b31-fa93-487f-b000-edaaa69f050f"
        self._response = await self._driver.get_user(self.__user_id, self._token)

    async def assert_response_is_user_01_data(self):
        assert self._response == {
            "id": self.__user_id,
            "username": "user",
            "email": None,
            "image": None,
            "bio": None
        }

    def get_non_existent_user(self) -> None:
        self.__user_id = "NOT_A_USER"
        self._response = self._driver.get_user(self.__user_id, self._token)

    def assert_response_is_not_found(self) -> None:  # verification is necessary
        assert self._response == {
            "error": UserNotFound.generate_message(self.__user_id)
        }
