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

@router.get("/get-budgets")
def budget_get_budgets(jwt_token=Depends(jwt_bearer.jwtBearer())):
    uid = jwt_handler.getUid(jwt_token)
    return budget.get_budgets(uid=uid)