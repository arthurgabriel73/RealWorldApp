from pydantic.class_validators import Optional
from pydantic import BaseModel, EmailStr, validator

from src.tools.password_tools import check_password_strength, get_hash, get_salt


class UserDTO(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserUpdate(UserDTO):
    email: EmailStr | None
    bio: str | None
    image: str | None


class UserComplete(UserDTO):
    id: str
    username: str | None
    email: EmailStr | None
    image: str | None
    bio: str | None


class UserLogin(UserDTO):
    password: str


class IncomingUserDTO(UserDTO):
    password: str

    @validator("password")
    def password_must_be_strong(cls, password):
        return check_password_strength(password)

    def get_salted_hash(self, salt: Optional[str] = None):
        if salt is None:
            salt = get_salt()
        hashed_password = get_hash(self.password + salt)
        return f"{salt} {hashed_password}"
