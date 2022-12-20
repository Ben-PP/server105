from fastapi import APIRouter


router = APIRouter(
    prefix="/tools",
    tags=["tools"],
)

@router.get("/ping")
def ping():
    return {"data": "Ping ok!"}

