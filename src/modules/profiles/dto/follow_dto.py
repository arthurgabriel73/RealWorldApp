from pydantic import BaseModel


class FollowRelationDTO(BaseModel):
    username: str
    follower: str

    class Config:
        orm_mode = True
