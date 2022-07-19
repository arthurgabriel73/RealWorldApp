from pydantic import BaseModel


class ProfileDTO(BaseModel):
    username: str
    bio: str | None
    image: str | None
    followers: bool | list[str]

    class Config:
        orm_mode = True
