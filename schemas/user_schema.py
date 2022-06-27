from pydantic import BaseModel as SCBaseModel, EmailStr


class UserSchemaBase(SCBaseModel):
    id: int | None
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserSchemaSignUp(UserSchemaBase):
    password: str


class UserSchemaUpdate(UserSchemaBase):
    username: str | None
    email: EmailStr | None
    password: str | None
