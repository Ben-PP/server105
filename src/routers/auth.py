from fastapi import APIRouter,Body,Depends
from model import LoginSchema
from jwt import jwt_bearer,jwt_handler
from actions.authentication import *

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/loginv2",)
def user_loginv2(user: LoginSchema = Body(default=None)):
    return authenticate_user(user.username, user.password)

@router.post("/logout",
    status_code=204,
    dependencies=[Depends(jwt_bearer.jwtBearer())],
)
def user_logout(jwt_token=Depends(jwt_bearer.jwtBearer())):
    blacklist_jwt(jwt_token)

@router.get("/validate-jwt", dependencies=[Depends(jwt_bearer.jwtBearer())])
def validate_jwt(jwt_token=Depends(jwt_bearer.jwtBearer())):
    requester_uid = jwt_handler.getUid(jwt_token)
    return is_user_admin(requester_uid)