import asyncio

import uvicorn

from fastapi import FastAPI

from db import User, database
from src.create_tables import create_tables
from src.modules.articles.controllers import article_controller
from src.modules.auth.controllers import auth_controller
from src.modules.profiles.controllers import profile_controller
from src.modules.users.controllers import user_controller

app = FastAPI(
    title='Real World App - API',
    description='This project is made to learn how to create a complete API using FastAPI and SQLAlchemy ORM'
)


@app.get("/")
async def read_root():
    return await User.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await User.objects.get_or_create(email="test@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


app.include_router(auth_controller.auth_router)
app.include_router(user_controller.user_router)
app.include_router(profile_controller.profile_router)
app.include_router(article_controller.article_router)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(create_tables())
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)
