from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserSignUp(UserDTO):
    password: str


class UserUpdate(UserDTO):
    email: EmailStr | None
    bio: str | None
    image: str | None


class UserComplete(UserDTO):
    username: str | None
    email: EmailStr | None
    image: str | None
    bio: str | None
