import re
import psycopg2
from fastapi import HTTPException
import actions
def edit_user(
    requester_uid: str,
    uid: str,
    can_make_transactions: bool,
    is_admin: bool,
):
    if (re.search("[^a-zA-ZöÖäÄåÅ-]",uid)):
        raise HTTPException(status_code=409, detail="Username contains invalid characters.")
    if (uid == ""):
        raise HTTPException(status_code=409, detail="Username must not be empty")
    conn = actions.connect_db()
    cursor: psycopg2.cursor = conn.cursor()
    cursor.execute("""
        SELECT is_admin FROM users WHERE uid=%s
    """,(requester_uid,))
    is_requester_admin = cursor.fetchone()[0]
    if (is_requester_admin != True):
        raise HTTPException(status_code=403, detail="Forbidden")
    
    cursor.execute("""
        UPDATE users
        SET can_make_transactions = %s,is_admin = %s
        WHERE uid=%s;
    """,(can_make_transactions,is_admin,uid,))
    cursor.close()
    conn.commit()
    conn.close()