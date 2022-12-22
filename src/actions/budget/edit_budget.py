import psycopg2
from ..connect_db import connect_db

def edit_budget(
    uid: str,
    private_income: float,
    private_expense: float,
    public_income: float,
    public_expense: float,
    ):
        conn = connect_db()
        cursor: psycopg2.cursor = conn.cursor()
        if (private_income != None):
            cursor.execute("""
                UPDATE private_budgets
                SET income=%s
                WHERE uid=%s
            """,(private_income,uid,))
        if (private_expense != None):
            cursor.execute("""
                UPDATE private_budgets
                SET expense=%s
                WHERE uid=%s
            """,(private_expense,uid,))
        if (public_income != None):
            cursor.execute("""
                UPDATE public_budgets
                SET income=%s
                WHERE uid=%s
            """,(public_income,uid,))
        if (public_expense != None):
            cursor.execute("""
                UPDATE public_budgets
                SET expense=%s
                WHERE uid=%s
            """,(public_expense,uid,))
        cursor.close()
        conn.commit()
        conn.close()