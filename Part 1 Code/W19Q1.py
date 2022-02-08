from hashlib import sha256
import hmac

secret_key = "abc"


def calculate_hmac(message: str, key: str) -> str:
    hmac_generated = hmac.new(key=secret_key.encode(), msg=message.encode(), digestmod=sha256)
    return hmac_generated.hexdigest()[-4:]


def check_transaction_validity(hmac1: str, message: str) -> None:

    hmac2 = calculate_hmac(message, secret_key)

    if hmac1 == hmac2:
        print("Transaction successfull")
    else:
        print("transaction failed.")


message = "Alice, Justin, £1000"

alice_hmac = calculate_hmac(message, secret_key)

print(f"sending to bank: msg='{message}' hmac={alice_hmac}")

print("Bank checking validity of a transaction:")

check_transaction_validity(alice_hmac, message)

eve_message = "Alice, Eve, £1000"

print("Printing Eve's message:")

print(eve_message)

print("hmac",calculate_hmac(eve_message, secret_key))

check_transaction_validity(alice_hmac, eve_message)


