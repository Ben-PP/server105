import psycopg2

def write(table: str):
    conn = psycopg2.connect(dbname="db105", user="admin", password="optiplex", host="172.16.160.116", port="5432",)
    cursor: psycopg2.cursor = conn.cursor()
    cursor.execute(f"""CREATE TABLE {table} (
        Id SERIAL PRIMARY KEY,
        Name varchar(254) NOT NULL
    );""")
    cursor.close()
    conn.commit()
    