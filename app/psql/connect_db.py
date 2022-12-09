import psycopg2
from decouple import config

def connect_db():
    return psycopg2.connect(
        dbname = "db105",
        user = "admin",
        password = config("db_psswd"),
        host = config("db_host"),
        port = config("db_port"),
    )