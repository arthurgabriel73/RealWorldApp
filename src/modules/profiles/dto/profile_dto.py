from pydantic import BaseModel, EmailStr, validator


class ProfileDTO(BaseModel):
    username: str
    bio: str
    image: str
    following: bool | list[str]

    class Config:
        orm_mode = True
