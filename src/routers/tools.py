from fastapi import APIRouter,Depends
from jwt import jwt_bearer,jwt_handler
from psql.is_user_admin import is_user_admin

router = APIRouter(
    prefix="/tools",
    tags=["tools"],
)

@router.get("/ping")
def ping():
    return {"data": "Ping ok!"}

@router.get("/validate-jwt", dependencies=[Depends(jwt_bearer.jwtBearer())])
def validate_jwt(jwt_token=Depends(jwt_bearer.jwtBearer())):
    requester_uid = jwt_handler.getUid(jwt_token)
    return is_user_admin(requester_uid)