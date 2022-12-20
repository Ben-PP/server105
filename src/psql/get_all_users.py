import psycopg2,psycopg2.extras
from fastapi import HTTPException
from .connect_db import connect_db

def get_all_users(requester_uid):
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )
    cursor.execute("""
        SELECT uid,can_make_transactions,is_admin FROM users
        WHERE uid NOT LIKE 'admin' AND uid NOT LIKE %s;
    """,(requester_uid,))
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return users