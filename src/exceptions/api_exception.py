from abc import ABC
from fastapi import HTTPException


class APIException(HTTPException, ABC):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message
        super().__init__(status_code=status, detail=message)
