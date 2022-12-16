from fastapi import APIRouter,Body,Depends
from model import LoginSchema,LogoutSchema,ChangePwdSchema,AddUserSchema, \
    RemoveUserSchema
from jwt import jwt_bearer,jwt_handler
from psql.authenticate import authenticate_user
from psql.blacklist_jwt import blacklist_jwt
from psql.change_password import change_password
from psql.add_user import add_user
from psql.remove_user import remove_user
from psql.get_all_users import get_all_users

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

# Adds user
@router.post(
    "/add-user",
    dependencies=[Depends(jwt_bearer.jwtBearer())],
)
def user_add_user(
    user: AddUserSchema = Body(default=None),
    jwt_token=Depends(jwt_bearer.jwtBearer())
):
    requester_uid = jwt_handler.getUid(jwt_token)
    add_user(
        requester_uid=requester_uid,
        uid=user.uid,
        pwd=user.pwd,
        can_make_transactions=user.can_make_transactions,
        is_admin=user.is_admin,
    )

@router.post(
    "/remove-user",
    dependencies=[Depends(jwt_bearer.jwtBearer())],
)
def user_remove_user(
    user: RemoveUserSchema = Body(default=None),
    jwt_token=Depends(jwt_bearer.jwtBearer())
):
    requester_uid = jwt_handler.getUid(jwt_token)
    remove_user(
        requester_uid=requester_uid,
        uid=user.uid,
    )

@router.get(
    "/get-all-users",
    dependencies=[Depends(jwt_bearer.jwtBearer())],
)
def user_get_all_users(jwt_token=Depends(jwt_bearer.jwtBearer())):
    requester_uid = jwt_handler.getUid(jwt_token)
    return get_all_users(requester_uid=requester_uid)