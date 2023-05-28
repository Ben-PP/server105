import psycopg2, psycopg2.extras, psycopg2.errors
from datetime import datetime
from fastapi import HTTPException
from ..connect_db import connect_db

def add_transaction(uid: str, timestamp: datetime, amount: float, is_public: bool):
    if amount == None or is_public == None:
        print(amount,is_public)
        raise HTTPException(status_code=400, detail="Amount or publicity was not given")
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor()
    cursor.execute("""
        SELECT can_make_transactions FROM users WHERE uid=%s;
    """,(uid,))
    can_make_transactions = cursor.fetchone()[0]
    if not can_make_transactions:
        raise HTTPException(status_code=403, detail="User not allowed to make transactions")
    try:
        cursor.execute("""
            INSERT INTO transactions (uid,timestamp,amount,is_public)
            VALUES (%(uid)s,%(timestamp)s,%(amount)s,%(is_public)s);
        """,{"uid":uid,"timestamp":timestamp,"amount":amount,"is_public":is_public})
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="Transaction is not unique by uid and timestamp")
    
    cursor.close()
    conn.commit()
    conn.close()
