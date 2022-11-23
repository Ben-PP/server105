import psycopg2

def initDb():
    try:
        conn = psycopg2.connect(dbname="db105", user="admin", password="optiplex", host="172.16.160.116", port="5432",)
    except Exception as e:
        print("Error while connecting to database...")
        print(f"Error was:\n{e}")
        return
    cursor: psycopg2.cursor = conn.cursor()
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS users (
        uid text PRIMARY KEY,
        name text NOT NULL,
        pswd_hash text,
        is_admin boolean NOT NULL
    );
    INSERT INTO users (uid, name, pswd_hash, is_admin)
    SELECT 'admin','admin','',true
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
    )
    """)
    cursor.close()
    conn.commit()

def init():
    print("Initializing...")
    initDb()