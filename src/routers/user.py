from fastapi import APIRouter,Body,Depends
from model import LoginSchema,LogoutSchema,ChangePwdSchema
from jwt import jwt_bearer,jwt_handler
from psql.authenticate import authenticate_user
from psql.blacklist_jwt import blacklist_jwt
from psql.change_password import change_password

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/loginv2",)
def user_loginv2(user: LoginSchema = Body(default=None)):
    return authenticate_user(user.username, user.password)

@router.post("/logout",
    status_code=204,
    dependencies=[Depends(jwt_bearer.jwtBearer())],
)
def user_logout(jwt: LogoutSchema = Body(default=None)):
    token = jwt.jwt
    blacklist_jwt(token)

# Changes password for owner of the jwt
@router.post(
    "/change-password",
    status_code=204,
    dependencies=[Depends(jwt_bearer.jwtBearer())],
)
def user_change_password(passwords: ChangePwdSchema = Body(default=None),
    jwt_token=Depends(jwt_bearer.jwtBearer())
):
    uid = jwt_handler.getUid(jwt_token)
    change_password(uid, passwords.old_password, passwords.new_password)