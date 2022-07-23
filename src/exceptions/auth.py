from src.exceptions.api_exception import APIException


class Unauthorized(APIException):
    def __init__(self, message: str) -> None:
        super().__init__(401, message)


class InvalidPassword(Unauthorized):
    def __init__(self) -> None:
        super().__init__("Password is invalid.")


class TokenHasExpired(Unauthorized):
    def __init__(self) -> None:
        super().__init__("The token has expired.")


class CouldNotValidate(Unauthorized):
    MESSAGE = "It was not possible to validate the token."

    def __init__(self) -> None:
        super().__init__(self.MESSAGE)
