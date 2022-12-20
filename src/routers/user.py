from fastapi import APIRouter,Body,Depends
from model import EditUserSchema,ChangePwdSchema,AddUserSchema, \
    RemoveUserSchema
from jwt import jwt_bearer,jwt_handler
from psql.change_password import change_password
from psql.add_user import add_user
from psql.remove_user import remove_user
from psql.get_all_users import get_all_users
from psql.edit_user import edit_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(jwt_bearer.jwtBearer())]
)

# Changes password for owner of the jwt
@router.put("/change-password", status_code=204)
def user_change_password(passwords: ChangePwdSchema = Body(default=None),
    jwt_token=Depends(jwt_bearer.jwtBearer())
):
    uid = jwt_handler.getUid(jwt_token)
    change_password(uid, passwords.old_password, passwords.new_password)

# Adds user
@router.post("/add-user", status_code=201)
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

@router.delete("/remove-user", status_code=204)
def user_remove_user(
    user: RemoveUserSchema = Body(default=None),
    jwt_token=Depends(jwt_bearer.jwtBearer())
):
    requester_uid = jwt_handler.getUid(jwt_token)
    remove_user(
        requester_uid=requester_uid,
        uid=user.uid,
    )

@router.put("/edit-user", status_code=204)
def user_edit_user(
    user: EditUserSchema = Body(default=None),
    jwt_token=Depends(jwt_bearer.jwtBearer()),
):
    requester_uid = jwt_handler.getUid(jwt_token)
    edit_user(
        requester_uid=requester_uid,
        uid=user.uid,
        can_make_transactions=user.can_make_transactions,
        is_admin=user.is_admin,
    )

@router.get("/get-all-users",)
def user_get_all_users(jwt_token=Depends(jwt_bearer.jwtBearer())):
    requester_uid = jwt_handler.getUid(jwt_token)
    return get_all_users(requester_uid=requester_uid)