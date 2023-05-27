import psycopg2
from datetime import datetime,timedelta
from passlib.context import CryptContext
from init import init
from actions.connect_db import connect_db


conn = connect_db()
cursor = conn.cursor()
cursor.execute("""
    DROP TABLE IF EXISTS private_transactions;
    DROP TABLE IF EXISTS public_transactions;
    DROP TABLE IF EXISTS private_budgets;
    DROP TABLE IF EXISTS public_budgets;
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
    INSERT INTO private_budgets (uid,income,expenses)
    VALUES
        ('{ben}',100,50),
        ('{sara}',30,10),
        ('{william}',10,10),
        ('{jolene}',0,0);
    INSERT INTO public_budgets (uid,income,expenses)
    VALUES
        ('{ben}',20,10),
        ('{sara}',30,10),
        ('{william}',0,10),
        ('{jolene}',0,0);
    INSERT INTO private_transactions (id,uid,amount,timestamp)
    VALUES
        (1,'{ben}',10,'{date_time+timedelta(days=1)}'),
        (2,'{ben}',10,'{date_time+timedelta(minutes=45)}'),
        (3,'{ben}',-10,'{date_time+timedelta(minutes=30)}'),
        (4,'{ben}',-20,'{date_time+timedelta(days=7)}'),
        (5,'{ben}',-10,'{date_time+timedelta(days=6)}'),
        (6,'{ben}',20,'{date_time+timedelta(days=2)}'),
        (7,'{ben}',10,'{date_time+timedelta(days=5)}');
    INSERT INTO public_transactions (id,uid,amount,timestamp)
    VALUES
        (1,'{ben}',10,'{date_time+timedelta(days=1)}'),
        (2,'{sara}',10,'{date_time+timedelta(minutes=45)}'),
        (3,'{sara}',-10,'{date_time+timedelta(minutes=30)}'),
        (4,'{william}',-20,'{date_time+timedelta(days=7)}'),
        (5,'{ben}',-10,'{date_time+timedelta(days=6)}'),
        (6,'{william}',20,'{date_time+timedelta(days=2)}'),
        (7,'{ben}',10,'{date_time+timedelta(days=5)}');
""")

cursor.close()
conn.commit()
conn.close()