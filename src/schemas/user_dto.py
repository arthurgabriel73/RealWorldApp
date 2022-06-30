from pydantic import BaseModel, EmailStr


class UserDto(BaseModel):
    id: int | None
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserSignUp(UserDto):
    password: str


class UserUpdate(UserDto):
    username: str | None
    email: EmailStr | None
    password: str | None
    image: str | None
    bio: str | None


class UserComplete(UserDto):
    username: str | None
    email: EmailStr | None
    image: str | None
    bio: str | None
