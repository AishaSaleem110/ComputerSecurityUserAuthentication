from hashlib import sha256
from os.path import isfile
from sys import stderr
import secrets

users = {}


def get_file_hash(address: str, salt: str = "") -> str:
    hasher = sha256()
    if not isfile(address):
        print("File not found, please enter valid path", file=stderr)
        exit(84)

    with open(address, 'rb') as afile:
        buf = afile.readlines()
        for k in buf:
            hasher.update(k)
        hasher.update(salt.encode("utf-8"))
        print(hasher.hexdigest())
    return hasher.hexdigest()


def register():
    print("Create account with details:")

    username = input("Enter username: ")
    password_file_path = input("Enter Password file path: ")
    salt = secrets.token_hex()
    while not isfile(password_file_path):
        password_file_path = input("Enter valid Password file path: ")

    info = input("Enter your pet name: ")

    key = get_file_hash(password_file_path, salt)

    # storing data
    users[username] = {
        'salt': salt,
        'key': key,
        'info': info
    }

    print(" Your account has been created....")


def login():
    print("Login demo")

    username_login = input("Please enter username to login: ")
    password_path_login = input("Please enter password to login: ")

    salt = users[username_login]['salt']

    recalculated_hash = get_file_hash(password_path_login, salt)

    key = users[username_login]['key']

    if recalculated_hash == key:

        print("Your pet name is: ", users[username_login]['info'])
    else:
        print("Wrong credentials")


def main():
    register()

    play = True

    while play:
        operation = int(input("Please enter 1 if you want to login or 2 to quit:"))

        if operation == 1:

            login()
        else:
            break

    return 0


if __name__ == "__main__":
    exit(main())
