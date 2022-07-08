from pydantic import BaseModel, validator
from pydantic.class_validators import Optional

from src.tools.password_tools import check_password_strength, get_hash, get_salt


class IncomingUserDTO(BaseModel):
    username: str
    password: str

    @validator("password")
    def password_must_be_strong(cls, password):
        return check_password_strength(password)

    def get_salted_hash(self, salt: Optional[str] = None):
        if salt is None:
            salt = get_salt()
        hashed_password = get_hash(self.password + salt)
        return f"{salt} {hashed_password}"
