from fastapi import FastAPI
from init import init
from routers import *

init()

app = FastAPI()
app.include_router(user.router)
app.include_router(tools.router)





