from fastapi import APIRouter,Body,Depends
from jwt import jwt_bearer, jwt_handler
from model import BudgetSchema
from actions import budget

router = APIRouter(
    prefix="/budget",
    tags=["budget"],
    dependencies=[Depends(jwt_bearer.jwtBearer())]
)

@router.put("/edit-budget", status_code=204)
def budget_edit_budget(
    budgets: BudgetSchema = Body(default=None),
    jwt_token=Depends(jwt_bearer.jwtBearer()),
):
    uid = jwt_handler.getUid(jwt_token)
    budget.edit_budget(
        uid=uid,
        private_income=budgets.private_income,
        private_expense=budgets.private_expense,
        public_income=budgets.public_income,
        public_expense=budgets.public_expense,
    )

@router.get("/get-private-budget")
def get_private_budget(jwt_token=Depends(jwt_bearer.jwtBearer())):
    uid = jwt_handler.getUid(jwt_token)
    return budget.get_private_budget(uid=uid)

@router.get("/get-public-budget")
def get_public_budget(jwt_token=Depends(jwt_bearer.jwtBearer())):
    uid = jwt_handler.getUid(jwt_token)
    return budget.get_public_budget(uid=uid)

@router.get("/get-house-budget")
def get_house_budgets(jwt_token=Depends(jwt_bearer.jwtBearer())):
    uid = jwt_handler.getUid(jwt_token)
    return budget.get_house_budget(uid=uid)