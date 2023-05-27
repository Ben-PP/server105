import psycopg2
from ..connect_db import connect_db

def edit_budget(
        uid: str,
        private_income: float,
        private_expense: float,
        public_income: float,
        public_expense: float,):
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor()
    cursor.execute("""
        UPDATE budgets
        SET private_income=COALESCE(%(private_income)s, private_income),
            private_expenses=COALESCE(%(private_expenses)s, private_expenses),
            public_income=COALESCE(%(public_income)s, public_income),
            public_expenses=COALESCE(%(public_expenses)s, public_expenses)
        WHERE uid=%(uid)s
    """, {
        "uid":uid,
        "private_income":private_income,
        "private_expenses":private_expense,
        "public_income":public_income,
        "public_expenses":public_expense
    })
    cursor.close()
    conn.commit()
    conn.close()