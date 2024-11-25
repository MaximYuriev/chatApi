import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers.auth import auth_router
from routers.chat import chat_router
from routers.page import page_router
from routers.user import user_router

app = FastAPI(title="MessangerAPI")
# app.mount('/static', StaticFiles(directory="./static"), name="static")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(page_router)
app.include_router(chat_router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
