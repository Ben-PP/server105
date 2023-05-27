import psycopg2
from fastapi import HTTPException
from passlib.context import CryptContext
from jwt import jwt_handler
from ..connect_db import connect_db

def authenticate_user(uid: str, pwd: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor()
    cursor.execute("""
        SELECT psswd_hash,is_admin FROM users WHERE uid = %s;
    """,(uid,))
    fetch = cursor.fetchone()
    cursor.close()
    conn.close()
    if (fetch == None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if (pwd_context.verify(pwd, fetch[0], "bcrypt")):
        response_body = jwt_handler.signJWT(uid)
        response_body.update({"is_admin":fetch[1]})
        return response_body
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
        