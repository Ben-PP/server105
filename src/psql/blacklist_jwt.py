import psycopg2

def blacklist_jwt(jwt):
    conn = psycopg2.connect(
        dbname="db105",
        user="admin",
        password="optiplex",
        host="172.16.160.116",
        port="5432",
    )
    cursor: psycopg2.cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO jwt_blacklist
        VALUES ('{jwt}');
    """)
    cursor.close()
    conn.commit()
