from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int | None
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserSignUp(User):
    password: str


class UserUpdate(User):
    username: str | None
    email: EmailStr | None
    password: str | None
    image: str | None
    bio: str | None


class UserComplete(User):
    username: str | None
    email: EmailStr | None
    image: str | None
    bio: str | None
