import psycopg2
from passlib.context import CryptContext
from fastapi import HTTPException
from psql.connect_db import connect_db

def change_password(uid: str, old_psswd: str, new_psswd: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    try:
        conn = connect_db()
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT psswd_hash FROM users
        WHERE uid='{uid}';
    """)
    current_hash = cursor.fetchone()
    if (current_hash == None):
        cursor.close()
        conn.commit()
        conn.close()
        raise HTTPException(status_code=401, detail="Unauthorized")
    if (pwd_context.verify(old_psswd, current_hash[0], "bcrypt")):
        psswd_hash = pwd_context.hash(new_psswd)
        cursor.execute(f"""
            UPDATE users
            SET psswd_hash = '{psswd_hash}'
            WHERE uid = '{uid}';
        """)
    else:
        cursor.close()
        conn.commit()
        conn.close()
        raise HTTPException(status_code=403, detail="Forbidden")
    
    cursor.close()
    conn.commit()
    conn.close()