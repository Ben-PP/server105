from fastapi import FastAPI, Depends, HTTPException, status, Body
from model import LoginSchema,LogoutSchema
from auth.jwt_handler import signJWT
from passlib.context import CryptContext
from auth.jwt_bearer import jwtBearer
from utils.init import init
import psycopg2
from psql.blacklist_jwt import blacklist_jwt

init()

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

dummy_content = [
    {
        "id": 1,
        "title": "Penguins",
        "text": "Jeeeeeeeee",
    },
]

@app.get("/ping", tags=["utils"])
def ping():
    return {"data": "Ping ok!"}

@app.get("/test", dependencies=[Depends(jwtBearer())], tags=["test"])
def get_test_post():
    return {"data": dummy_content}

@app.post("/user/login", tags=["user"])
def user_login(user: LoginSchema = Body(default=None)):
    shadow = open("/etc/server105/shadow", "r")
    pwd = pwd_context.hash(user.password)
    for line in shadow:
        if line.startswith(user.username):
            correct_hash = line.split(":")[1].strip()
            if pwd_context.verify(user.password, correct_hash, "bcrypt"):
                # TODO Log
                return signJWT(user.username)
                
            else:
                # TODO Log
                return {
                    "error": "Invalid login details!"
                }

@app.post("/user/logout", tags=["user"])
def user_logout(jwt: LogoutSchema = Body(default=None)):
    token = jwt.jwt
    blacklist_jwt(token)
