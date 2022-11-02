#!/bin/python

import os
import getpass
from passlib.context import CryptContext

# Adds username and password
def add_user(username: str, password: str, pwd_context: CryptContext):
    pwd = pwd_context.hash(password, "bcrypt")
    if not os.path.exists("/etc/server105"):
        os.mkdir("/etc/server105", 774)

    shadow = open("/etc/server105/shadow", "a")
    shadow.write(f"{username}:{pwd}\n")
    shadow.close()

def main():
    username = input('Username: ')

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    while True:
        passwd = getpass.getpass('Give a password: ')
        passwd_confirm = getpass.getpass('Confirm password: ')
        if passwd == passwd_confirm:
            print(len(passwd))
            add_user(username, passwd, pwd_context)
            print(f"User {username} added.")
            break
        print("Passwords did not match!")

if __name__ == "__main__":
    main()