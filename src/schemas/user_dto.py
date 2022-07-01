from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    id: int | None
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserSignUp(UserDTO):
    password: str


class UserUpdate(UserDTO):
    username: str | None
    email: EmailStr | None
    password: str | None
    image: str | None
    bio: str | None


class UserComplete(UserDTO):
    username: str | None
    email: EmailStr | None
    image: str | None
    bio: str | None
