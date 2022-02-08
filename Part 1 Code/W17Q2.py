import hashlib
import requests


def calculate_sha_1(password: str) -> str:
    return hashlib.sha1(password.encode("utf-8")).hexdigest()


def calculate_sha_256(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def print_result(password: str, algorithm: str, iteration: int) -> None:
    print("pwd found : %s, with algorithm: %s with %s rounds of hash function." % (pwd, algorithm, iteration))


leaked_pwd_link = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Leaked-Databases/phpbb.txt"
hashed = '3ddcd95d2bff8e97d3ad817f718ae207b98c7f2c84c5519f89cd15d7f8ee1c3b'

data = requests.get(leaked_pwd_link)

for pwd in data.text.splitlines():
    n = 1

    hashed_1 = calculate_sha_1(pwd)
    if hashed_1 == hashed:
        print_result(pwd, 'SHA1', n)
        break

    hashed_256 = calculate_sha_256(pwd)
    if hashed_256 == hashed:
        print_result(pwd, 'SHA256', n)
        break

    n += n
    while n <= 5:
        hashed_1 = calculate_sha_1(hashed_1)
        if hashed_1 == hashed:
            print_result(pwd, 'SHA1', n)
            break

        hashed_256 = calculate_sha_256(hashed_256)
        if hashed_256 == hashed:
            print_result(pwd, 'SHA256', n)
            break
        n += n
