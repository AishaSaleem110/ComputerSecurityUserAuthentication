import hashlib
import secrets


# using SHA256 for hashing

def calculate_hash(password: str, n: int, salt: str) -> str:
    salted_password = password + salt

    # Following formula is used to calculate hash
    # h=(H^n)(p || s)

    hashed_value = hashlib.sha256(salted_password.encode("utf-8"))
    n -= 1

    while n > 0:
        hashed_value = hashlib.sha256(hashed_value.hexdigest().encode("utf-8"))
        n -= 1

    return hashed_value.hexdigest()


def verify_login(users: dict, password: str, n: int) -> bool:
    # Get the salt
    stored_salt = users[username_login]['salt']
    # Get the correct key
    stored_key = users[username_login]['key']
    # Recompute
    recomputed_key = calculate_hash(password, n, stored_salt)

    if recomputed_key == stored_key:
        return True
    else:
        return False


# A simple demo storage
users = {}
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

play = True

while play:
    operation = int(input("Please enter 1 if you want to login or 2 to quit:"))

    if operation == 1:

        print("Login demo")

        username_login = input("Please enter username to login: ")
        password_login = input("Please enter password to login: ")

        result = verify_login(users, password_login, n)

        if result:
            print("Your pet name is: ", users[username_login]['info'])
        else:
            print("Wrong credentials")

    else:
        break
