import hashlib
import secrets
from datetime import datetime

# using SHA256 for hashing

# A simple demo storage
users = {}


def calculate_hash(password: str, n: int, salt: str = "") -> str:
    salted_password = password + salt

    # Following formula is used to calculate hash
    # h=(H^n)(p || s)

    hashed_value = hashlib.sha256(salted_password.encode("utf-8"))
    n -= n

    while n > 0:
        hashed_value = hashlib.sha256(hashed_value.hexdigest().encode("utf-8"))
        n -= n

    return hashed_value.hexdigest()


def verify_login(users: dict, username_login: str) -> bool:
    print("Verification required")

    date_time_obj = datetime.now()

    hashed_salted_password = str(users[username_login]['key'])

    modified_password = hashed_salted_password + date_time_obj.strftime("%d%m%y%X")

    hashed_result = calculate_hash(modified_password, 1, "")

    print(hashed_result)

    print("The otp is:", str(hashed_result[-12:]))

    otp = input("Please enter otp: ")

    if hashed_result[-12:] == otp:
        return True
    else:
        return False


def user_registration() -> None:
    n = 2
    salt = secrets.token_hex()

    # Add a user
    print("Create account with details:")

    username = input("Enter username: ")
    password = input("Enter Password: ")
    info = input("Enter your pet name: ")

    key = calculate_hash(password, n, salt)

    # storing data
    users[username] = {
        'salt': salt,
        'key': key,
        'info': info
    }

    print(" Your account has been created....")


def login_attempt() -> None:
    print("Login demo")
    username_login = input("Please enter username to login: ")
    result = verify_login(users, username_login)
    if result:
        print("Your pet name is: ", users[username_login]['info'])
    else:
        print("Wrong otp")


def main():
    user_registration()

    play = True

    while play:
        operation = int(input("Please enter 1 if you want to login or 2 to quit:"))

        if operation == 1:

            login_attempt()

        else:
            break

    return 0


if __name__ == '__main__':
    exit(main())
