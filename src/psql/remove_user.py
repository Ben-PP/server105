import re
import psycopg2
from fastapi import HTTPException
from .connect_db import connect_db

def remove_user(
    requester_uid: str,
    uid: str,
):
    
    if (re.search("[^a-zA-ZöÖäÄåÅ-]",uid)):
        raise HTTPException(
            status_code=409,
            detail="Username contains invalid characters.",
        )
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor()

    cursor.execute("""
        SELECT is_admin FROM users WHERE uid=%s
    """,(requester_uid,))
    is_admin = cursor.fetchone()[0]
    if (is_admin != True):
        raise HTTPException(status_code=403, detail="Forbidden")
    cursor.execute("""
        DELETE FROM users WHERE uid=%s;
    """,(uid,))
    cursor.close()
    conn.commit()
    conn.close()