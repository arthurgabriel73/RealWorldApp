from pydantic import BaseModel


class Token(BaseModel):
    """The standard way of returning tokens"""

    access_token: str
    token_type: str = "bearer"
