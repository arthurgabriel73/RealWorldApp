from src.exceptions.api_exception import APIException


class AssetNotFound(APIException):
    def __init__(self, message: str):
        super().__init__(404, message)

    @staticmethod
    def generate_base_message(asset: str, identifier_name: str, identifier: str) -> str:
        return f"The {asset} identified by {identifier_name}: {identifier} could not be found."


class UserNotFound(AssetNotFound):
    def __int__(self, identifier: str):
        message = self.generate_message(identifier)
        super().__init__(message)

    @staticmethod
    def generate_message(identifier: str) -> str:
        return AssetNotFound.generate_base_message("user", "username", identifier)
