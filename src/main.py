from fastapi import FastAPI, Depends, Body
from model import LoginSchema,LogoutSchema
from passlib.context import CryptContext
from auth.jwt_bearer import jwtBearer
from utils.init import init
from psql.blacklist_jwt import blacklist_jwt
from psql.authenticate import authenticate_user

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

@app.get("/validate-jwt", dependencies=[Depends(jwtBearer())], tags=["utils"])
def get_test_post():
    return {}

@app.get("/test", dependencies=[Depends(jwtBearer())], tags=["test"])
def get_test_post():
    return {"data": dummy_content}

@app.post("/user/loginv2", tags=["user"])
def user_loginv2(user: LoginSchema = Body(default=None)):
    return authenticate_user(user.username, user.password)

@app.post("/user/logout", tags=["user"])
def user_logout(jwt: LogoutSchema = Body(default=None)):
    token = jwt.jwt
    blacklist_jwt(token)

@app.post("/user/change-password", tags=["user"])
def user_change_password():
    pass # TODO change passwords