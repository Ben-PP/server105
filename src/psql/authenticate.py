import psycopg2
from fastapi import HTTPException
from passlib.context import CryptContext
from auth.jwt_handler import signJWT
from psql.connect_db import connect_db

def authenticate_user(uid: str, pwd: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor()
    cursor.execute(f"""
        SELECT psswd_hash FROM users WHERE uid = '{uid}';
    """)
    fetch = cursor.fetchone()
    cursor.close()
    conn.close()
    if (fetch == None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if (pwd_context.verify(pwd, fetch[0], "bcrypt")):
        return signJWT(uid)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
        