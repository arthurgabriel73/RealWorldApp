import uvicorn

from fastapi import FastAPI

from modules.articles.controllers import article_controller
from src.modules.auth.controllers import auth_controller
from src.modules.profiles.controllers import profile_controller
from src.modules.users.controllers import user_controller

app = FastAPI(
    title='Real World App - API',
    description='This project is made to learn how to create a complete API using FastAPI and SQLAlchemy ORM'
)


app.include_router(auth_controller.auth_router)
app.include_router(user_controller.user_router)
app.include_router(profile_controller.profile_router)
app.include_router(article_controller.article_router)

if __name__ == '__main__':

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)
