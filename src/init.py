import psycopg2
from passlib.context import CryptContext
from actions.connect_db import connect_db

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
    SELECT 'admin','{admin_pwd}',false,true
    WHERE NOT EXISTS (SELECT * FROM users);

    CREATE TABLE IF NOT EXISTS private_budgets (
        uid text PRIMARY KEY,
        income NUMERIC(6, 2),
        expenses NUMERIC(6, 2),
        CONSTRAINT fk_uid
            FOREIGN KEY(uid)
                REFERENCES users(uid)
                ON DELETE CASCADE
                ON UPDATE CASCADE
    );
    CREATE TABLE IF NOT EXISTS public_budgets (
        uid text PRIMARY KEY,
        income NUMERIC(6, 2),
        expenses NUMERIC(6, 2),
        CONSTRAINT fk_uid
            FOREIGN KEY(uid)
                REFERENCES users(uid)
                ON DELETE CASCADE
                ON UPDATE CASCADE
    );
    CREATE TABLE IF NOT EXISTS private_transactions (
        id text PRIMARY KEY,
        uid text NOT NULL,
        amount NUMERIC(6, 2) NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        CONSTRAINT fk_uid
            FOREIGN KEY(uid)
                REFERENCES private_budgets(uid)
                ON DELETE CASCADE
                ON UPDATE CASCADE
    );
    CREATE TABLE IF NOT EXISTS public_transactions (
        id text PRIMARY KEY,
        uid text NOT NULL,
        amount NUMERIC(6, 2) NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        CONSTRAINT fk_uid
            FOREIGN KEY(uid)
                REFERENCES public_budgets(uid)
                ON DELETE CASCADE
                ON UPDATE CASCADE
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