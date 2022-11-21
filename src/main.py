from fastapi import FastAPI, Depends, HTTPException, status, Body
from model import LoginSchema
from auth.jwt_handler import sign_JWT
from passlib.context import CryptContext
from auth.jwt_bearer import jwtBearer
import psql.psql as postgres

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

dummy_content = [
    {
        "id": 1,
        "title": "Penguins",
        "text": "Jeeeeeeeee",
    },
]

@app.get("/psql", tags=["test"])
def psql(table: str):
    postgres.write(table=table)
    return {"data": "It works"}

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
                return sign_JWT(user.username)
                
            else:
                # TODO Log
                return {
                    "error": "Invalid login details!"
                }
