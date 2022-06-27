from pydantic import BaseModel as SCBaseModel, EmailStr


class UserSchema(SCBaseModel):

    id: int
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
