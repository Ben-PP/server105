import psycopg2, psycopg2.extras
from ..connect_db import connect_db

def get_budgets(uid: str):
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )
    # Fetch private budget
    cursor.execute("""
        SELECT * FROM private_budgets
        WHERE uid=%s
    """,(uid,))
    private_budget = cursor.fetchone()
    cursor.execute("""
        SELECT * FROM private_transactions
        WHERE uid=%s;
    """,(uid,))
    private_budget.update({'transactions':cursor.fetchall()})
    payload = {
        "private_budget":private_budget
    }

    # Fetch public budget
    cursor.execute("""
        SELECT * FROM public_budgets
        WHERE uid=%s
    """,(uid,))
    public_budget = cursor.fetchone()
    cursor.execute("""
        SELECT * FROM public_transactions
        WHERE uid=%s;
    """,(uid,))
    public_budget.update({'transactions':cursor.fetchall()})
    payload.update({"public_budget":public_budget})
    
    cursor.execute("""
        SELECT * FROM public_budgets;
    """,)
    public_budgets = cursor.fetchall()
    public_income = 0
    public_expenses = 0
    for budget in public_budgets:
        public_income += budget["income"]
        public_expenses += budget["expenses"]
    house_budget ={
        "uid":"",
        "income":public_income,
        "expenses":public_expenses,
    }
    cursor.execute("""
        SELECT * FROM public_transactions;
    """)
    public_transactions = cursor.fetchall()
    house_budget.update({"transactions":public_transactions})
    payload.update({"house_budget":house_budget})
    return payload
    
