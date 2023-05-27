import psycopg2, psycopg2.extras
from ..connect_db import connect_db

def get_private_budget(uid: str):
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )
    # Fetch private budget
    cursor.execute("""
        SELECT private_income,private_expenses FROM budgets
        WHERE uid=%s
    """,(uid,))
    private_budget = cursor.fetchone()
    cursor.execute("""
        SELECT uid,timestamp,amount FROM transactions
        WHERE uid=%s AND is_public=false;
    """,(uid,))
    private_budget.update({'transactions':cursor.fetchall()})
    payload = {
        "private_budget":private_budget
    }
    conn.commit()
    conn.close()
    return payload

def get_public_budget(uid: str):
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    # Fetch public budget of the user
    cursor.execute("""
        SELECT public_income,public_expenses FROM budgets
        WHERE uid=%s
    """,(uid,))
    public_budget = cursor.fetchone()
    cursor.execute("""
        SELECT uid,timestamp,amount FROM transactions
        WHERE uid=%s AND is_public=true;
    """,(uid,))
    public_budget.update({'transactions':cursor.fetchall()})
    payload = {"public_budget":public_budget}

    conn.commit()
    conn.close()
    return payload

def get_house_budget(uid: str):
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    # Fetch house budget
    cursor.execute("""
        SELECT public_income,public_expenses FROM budgets;
    """,)
    public_budgets = cursor.fetchall()
    public_income = 0
    public_expenses = 0
    for budget in public_budgets:
        public_income += budget["public_income"]
        public_expenses += budget["public_expenses"]
    cursor.execute("""
        SELECT uid,timestamp,amount FROM transactions WHERE is_public=true;
    """)
    public_transactions = cursor.fetchall()
    payload = {
        "house_budget":{
            "uid":"",
            "income":public_income,
            "expenses":public_expenses,
            "transactions":public_transactions
            }
       }

    conn.commit()
    conn.close()
    return payload
    
