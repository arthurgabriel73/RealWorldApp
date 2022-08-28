from pydantic import BaseModel


class ArticleDTO(BaseModel):
    title: str
    description: str | None
    body: str
    tag_list = []

    class Config:
        orm_mode = True


class ArticleComplete(ArticleDTO):
    id: str | None
    slug: str | None
    author_id: str
