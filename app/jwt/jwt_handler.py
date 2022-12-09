import time
from jose import jwt
from decouple import config
from psql.connect_db import connect_db

JWT_SECRET = config("jwt_secret")
JWT_ALGORITHM = config("jwt_algorithm")

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user_id: str):
    payload = {
        "user_id": user_id,
        "expiry": time.time() + 86400
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT token FROM jwt_blacklist
        WHERE token = '{token}';
    """)
    if (cursor.fetchone() != None):
        cursor.close()
        return None
    cursor.close()
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token if decode_token["expiry"] >= time.time() else None
    except:
        return {}