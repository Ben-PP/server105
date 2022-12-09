import psycopg2
from .connect_db import connect_db

def blacklist_jwt(jwt):
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO jwt_blacklist
        VALUES (%s);
    """, (jwt,))
    cursor.close()
    conn.commit()
    conn.close()
