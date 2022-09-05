import asyncio

import uvicorn

from fastapi import FastAPI

from create_tables import create_tables
from modules.articles.controllers import article_controller
from modules.auth.controllers import auth_controller
from modules.profiles.controllers import profile_controller
from modules.users.controllers import user_controller
import starlette.responses as _responses

description: str = "Welcome to Real World App API! Here you can register yourself, get logged, create your own " \
                   "articles and follow other user's profiles. Please create an username and a valid password and " \
                   "then use 'Authorize' (this one with the padlock) to access the functionalities that requires " \
                   "authorization. Also you can access my github: https://github.com/arthurgabriel73 to see more of " \
                   "my work."

app = FastAPI(
    title='Real World App - API',
    description=description
)


@app.get("/")
async def read_root():
    return _responses.RedirectResponse("/docs")

app.include_router(auth_controller.auth_router)
app.include_router(user_controller.user_router)
app.include_router(profile_controller.profile_router)
app.include_router(article_controller.article_router)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(create_tables())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)
