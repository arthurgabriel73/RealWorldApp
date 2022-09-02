from tests.acceptance.drivers.auth_driver import AuthDriver
from src.exceptions.auth import CouldNotValidate


class AuthDSL:
    def __init__(self) -> None:
        self.__driver = AuthDriver()
        self._token = ""
        self._response: {any: any} = {}

    def fake_token(self) -> None:
        self._token = "AFakeToken"

    async def login_authorized(self) -> None:
        self._token = await self.__driver.get_token()

    def assert_response_is_unauthorized(self) -> None:  # not used, needs to be invalid password
        assert self._response == {"error": CouldNotValidate.MESSAGE}
