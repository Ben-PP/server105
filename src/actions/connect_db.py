import psycopg2
from decouple import config

# TODO Optimize with connection pool
def connect_db():
    return psycopg2.connect(
        dbname = config("db_name"),
        user = config("db_username"),
        password = config("db_psswd"),
        host = config("db_host"),
        port = config("db_port"),
    )