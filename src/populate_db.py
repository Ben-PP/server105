import psycopg2
from datetime import datetime,timedelta
from passlib.context import CryptContext
from init import init
from actions.connect_db import connect_db


conn = connect_db()
cursor = conn.cursor()
cursor.execute("""
    DROP TABLE IF EXISTS transactions;
    DROP TABLE IF EXISTS budgets;
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS jwt_blacklist;
""")
cursor.close()
conn.commit()
conn.close()
init()
conn = connect_db()
cursor = conn.cursor()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ben = "ben"
ben_pwd = pwd_context.hash(ben)
sara = "sara"
sara_pwd = pwd_context.hash(sara)
william = "william"
william_pwd = pwd_context.hash(william)
jolene = "jolene"
jolene_pwd = pwd_context.hash(jolene)
date_time = datetime.now()
cursor.execute(f"""
    INSERT INTO users (uid, psswd_hash,can_make_transactions,is_admin)
    VALUES
        ('{ben}','{ben_pwd}',true,true),
        ('{sara}','{sara_pwd}',true,true),
        ('{william}','{william_pwd}',true,false),
        ('{jolene}','{jolene_pwd}',false,false);
    INSERT INTO budgets (uid,public_income,public_expenses,private_income,private_expenses)
    VALUES
        ('{ben}',20,10,100,50),
        ('{sara}',30,10,30,10),
        ('{william}',0,10,10,10),
        ('{jolene}',0,0,0,0);
    INSERT INTO transactions (uid,amount, timestamp,is_public)
    VALUES
        ('{ben}',10,'{date_time-timedelta(days=1)}',false),
        ('{ben}',10,'{date_time-timedelta(minutes=45)}',false),
        ('{ben}',-10,'{date_time-timedelta(minutes=30)}',false),
        ('{ben}',-20,'{date_time-timedelta(days=7)}',false),
        ('{ben}',-10,'{date_time-timedelta(days=6)}',false),
        ('{ben}',20,'{date_time-timedelta(days=2)}',false),
        ('{ben}',10,'{date_time-timedelta(days=5)}',false),
        ('{ben}',10,'{date_time-timedelta(days=1,hours=1)}',true),
        ('{sara}',10,'{date_time-timedelta(minutes=45)}',true),
        ('{sara}',-10,'{date_time-timedelta(minutes=30)}',true),
        ('{william}',-20,'{date_time-timedelta(days=7)}',true),
        ('{ben}',-10,'{date_time-timedelta(days=6,hours=5)}',true),
        ('{william}',20,'{date_time-timedelta(days=2)}',true),
        ('{ben}',10,'{date_time-timedelta(days=5,hours=6)}',true);
""")

cursor.close()
conn.commit()
conn.close()