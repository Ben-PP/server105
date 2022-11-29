import psycopg2
from psql.connect_db import connect_db

def blacklist_jwt(jwt):
    conn = connect_db()
    cursor: psycopg2.cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO jwt_blacklist
        VALUES ('{jwt}');
    """)
    cursor.close()
    conn.commit()
    conn.close()
