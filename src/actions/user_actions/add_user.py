import re
import psycopg2
from fastapi import HTTPException
from passlib.context import CryptContext
from ..connect_db import connect_db

def add_user(
    requester_uid: str,
    uid: str,
    pwd: str,
    can_make_transactions: bool,
    is_admin: bool,
):
    if (re.search("[^a-zA-ZöÖäÄåÅ-]",uid)):
        raise HTTPException(status_code=409, detail="Username contains invalid characters.")
    if (uid == ""):
        raise HTTPException(status_code=409, detail="Username must not be empty")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor()
    cursor.execute("""
        SELECT is_admin FROM users WHERE uid=%s
    """,(requester_uid,))
    is_requester_admin = cursor.fetchone()[0]
    if (is_requester_admin != True):
        raise HTTPException(status_code=403, detail="Forbidden")

    cursor.execute("""
        SELECT uid FROM users WHERE uid=%s;
    """,(uid,))
    user = cursor.fetchone()
    if (user != None):
        raise HTTPException(status_code=409, detail="User allready exists")

    cursor.execute("""
        INSERT INTO users (uid, psswd_hash,can_make_transactions,is_admin)
        VALUES (%s,%s,%s,%s);
    """,(uid,pwd_context.hash(pwd),can_make_transactions,is_admin,))
    cursor.execute("""
        INSERT INTO budgets (uid,public_income,public_expenses,private_income,private_expenses)
        VALUES (%s,0,0,0,0);
    """,(uid,))
    cursor.close()
    conn.commit()
    conn.close()