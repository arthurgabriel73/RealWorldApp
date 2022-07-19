from abc import ABC

from fastapi import HTTPException


class APIException(HTTPException, ABC):
    def __init__(self, message: str, status: int):
        self.message = message
        self.status = status
        super().__init__(status_code=status, detail=message)
