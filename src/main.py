from fastapi import FastAPI

from src.core.configs import settings
from src.models.users.controllers.user_controller import user_router

app = FastAPI(
    title='Real World App - API',
    description='This project is made to learn how to create a complete API using FastAPI and SQLAlchemy ORM'
)

app.include_router(user_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)
