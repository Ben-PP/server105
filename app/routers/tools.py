from fastapi import APIRouter,Depends
from jwt import jwt_bearer

router = APIRouter(
    prefix="/tools",
    tags=["tools"],
)

@router.get("/ping")
def ping():
    return {"data": "Ping ok!"}

@router.get("/validate-jwt", dependencies=[Depends(jwt_bearer.jwtBearer())])
def get_test_post():
    return {}