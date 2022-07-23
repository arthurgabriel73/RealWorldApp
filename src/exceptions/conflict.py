from src.exceptions.api_exception import APIException


class ConflictOnUpdate(APIException):
    def __init__(self, identifier: str):
        message = (
            f"Conflict on updating the user identified by: {identifier}."
        )
        super().__init__(406, message)
