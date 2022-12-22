import psycopg2
from fastapi import HTTPException
from ..connect_db import connect_db

def is_user_admin(uid: str) -> bool:
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor()
    cursor.execute("""
        SELECT is_admin FROM users
        WHERE uid=%s;
    """,(uid,))
    is_admin = cursor.fetchone()
    if (is_admin != None):
        return {"is_admin":is_admin[0],}
    raise HTTPException(status_code=409, detail=f"User {uid} not found")