import psycopg2
from passlib.context import CryptContext
from psql.connect_db import connect_db

def initDb():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    admin_pwd = pwd_context.hash("admin")
    try:
        conn = connect_db()
    except Exception as e:
        print("Error while connecting to database...")
        print(f"Error was:\n{e}")
        return
    cursor: psycopg2.cursor = conn.cursor()
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS users (
        uid text PRIMARY KEY,
        psswd_hash text NOT NULL,
        can_make_transactions bool NOT NULL,
        is_admin boolean NOT NULL
    );
    INSERT INTO users (uid, psswd_hash,can_make_transactions,is_admin)
    SELECT 'admin','{admin_pwd}',true,true
    WHERE NOT EXISTS (SELECT * FROM users);
    CREATE TABLE IF NOT EXISTS budgets (
        uid text PRIMARY KEY,
        income NUMERIC(6, 2),
        expenses NUMERIC(6, 2)
    );
    CREATE TABLE IF NOT EXISTS transactions (
        uid text PRIMARY KEY,
        amount NUMERIC(6, 2),
        timestamp TIMESTAMP WITH TIME ZONE
    );
    CREATE TABLE IF NOT EXISTS jwt_blacklist (
        token text PRIMARY KEY
    );
    """)
    cursor.close()
    conn.commit()
    conn.close()

def init():
    print("Initializing...")
    initDb()