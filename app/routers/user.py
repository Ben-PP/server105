from fastapi import APIRouter,Body,Depends
from model import LoginSchema,LogoutSchema,ChangePwdSchema
from jwt import jwt_bearer
from psql.authenticate import authenticate_user
from psql.blacklist_jwt import blacklist_jwt
from psql.change_password import change_password

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/loginv2")
def user_loginv2(user: LoginSchema = Body(default=None)):
    return authenticate_user(user.username, user.password)

@router.post("/logout")
def user_logout(jwt: LogoutSchema = Body(default=None)):
    token = jwt.jwt
    blacklist_jwt(token)

@router.post("/change-password", dependencies=[Depends(jwt_bearer.jwtBearer())])
def user_change_password(password: ChangePwdSchema = Body(default=None)):
    change_password(password.uid, password.old_password, password.new_password)