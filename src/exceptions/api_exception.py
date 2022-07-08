from abc import ABC


class APIException(Exception, ABC):
    def __init__(self, message: str, status: int):
        self.message = message
        self.status = status
        super().__init__()
