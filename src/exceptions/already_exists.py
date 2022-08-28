from src.exceptions.api_exception import APIException


class AssetAlreadyExists(APIException):
    def __init__(self, asset: str, identifier_name: str, identifier: str):
        message = (
            f"The {asset} identified by {identifier_name}: {identifier} already exists."
        )
        super().__init__(406, message)


class UserAlreadyExists(AssetAlreadyExists):
    def __init__(self, identifier: str):
        super().__init__("user", "username", identifier)


class ArticleAlreadyExists(AssetAlreadyExists):
    def __init__(self, identifier: str):
        super().__init__("article", "title", identifier)
