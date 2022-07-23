from pydantic import BaseModel


class FollowRelationDTO(BaseModel):
    username: str
    user_to_follow: str

    class Config:
        orm_mode = True
