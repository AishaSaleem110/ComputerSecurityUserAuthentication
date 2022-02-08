import pickle
from random import random
from cryptography.fernet import Fernet


class my_server():
    def __init__(self):
        self.key_a = ""
        self.name_a = ""
        self.key_b = ""
        self.name_b = ""
        self.nonce_a = ""

    def set_key_a(self, name, key):
        self.key_a = key
        self.name_a = name
        print(f"Pre-shared key between {name} and Server: {key}")

    def set_key_b(self, name, key):
        self.key_b = key
        self.name_b = name
        print(f"Pre-shared key between {name} and Server: {key}")

    def start_connection(self, a, b, n_a):
        if a != self.name_a or b != self.name_b:
            print(f"2 (Server): A or B doesn't exist.")
            exit(84)
        key_ab = Fernet.generate_key()
        print()
        print(f"2 (Server): K_AB = {key_ab}")
        b_package = {"K_AB": key_ab, "A": a}
        fernet_b = Fernet(self.key_b)
        b_package_encrypted = fernet_b.encrypt(pickle.dumps(b_package))
        print(f"2 (Server): E_{{K_BS}}(K_AB, A) = E_{{{self.key_b}}}({key_ab} , {a}) = {b_package_encrypted}")
        return_obj = {"N_A": n_a, "B": b, "K_AB": key_ab, "package": b_package_encrypted}
        fernet_a = Fernet(self.key_a)
        encrypted_return_obj = fernet_a.encrypt(pickle.dumps(return_obj))
        return encrypted_return_obj

class user():
    def __init__(self, name):
        self.name = name
        self.s_key = Fernet.generate_key()
        self.other_key = ""
        self.nonce = 0

    def create_connection(self, other, server):
        nonce = int(random() * 10 ** 20)
        print()
        print(f"1 ({self.name}): N_A = {nonce}")
        print(f"1 ({self.name})=>Server: (A, B, N_A) = ({self.name}, {other.name}, {nonce})")
        print()
        decoder = Fernet(self.s_key)
        message = server.start_connection(self.name, other.name, nonce)
        try:
            info = pickle.loads(decoder.decrypt(message))
            print(info)
            print(f"2 (Server => {self.name}): E_{{K_AS}} (N_A,B,K_AB,E_{{K_BS}}(K_AB,A)) = E_{{{self.s_key}}} ({info['N_A']},{info['B']},{info['K_AB']},{info['package']}) = {info}")
            print(f"2 ({self.name}): E_{{K_AS}} (N_A,B,K_AB,E_{{K_BS}}(K_AB,A)) = E_{{{self.s_key}}} ({info['N_A']},{info['B']},{info['K_AB']},{info['package']})")
            print("=>Message 2 authentication was successful!")
            print()
        except:
            print("=>Message 2 authentication was unsuccessful!")
            exit(84)

        self.other_key = info["K_AB"]
        decoder_ab = Fernet(self.other_key)

        message = other.get_package(info["package"], self)
        try:
            value = pickle.loads(decoder_ab.decrypt(message))["N"]
            print(f"4({self.name}):N_B={value}")
            print("=>Message 4 authentication was successful!")
        except:
            print("=>Message 4 authentication was unsuccessful!")

        print()
        updated_nonce = value - 1
        print(f"5 {self.name}=>{other.name}: E_{{K_AB}}(N_B-1)= E_{{{self.other_key}}} ({updated_nonce})")
        other.get_nonce(decoder_ab.encrypt(pickle.dumps({"N": updated_nonce})))


    def get_package(self, message, other):

        decoder = Fernet(self.s_key)
        try:
            info = pickle.loads(decoder.decrypt(message))
            print(f"3 ({other.name} => {self.name}): E_{{K_BS}}(K_AB,A) = E_{{{self.s_key}}}({info['K_AB']},{info['A']}) = {message}")

            print()
            print(f"3 ({self.name}): (K_AB,A) = ({info['K_AB']},{info['A']})")
            print("=>Message 3 authentication was successful")
        except:
            print("=>Message 3 authentication was unsuccessful")
            exit(84)

        self.other_key = info["K_AB"]
        coder = Fernet(self.other_key)
        self.nonce = int(random() * 10 ** 20)
        message = coder.encrypt(pickle.dumps({"N": self.nonce}))
        print()
        print(f"(4 {self.name}):N_B = {self.nonce}")
        print(f"(4 {self.name} => {other.name}): E_{{K_AB}}(N_B)=E_{{{info['K_AB']}}}({self.nonce})={message}")
        return message


    def get_nonce(self, message):
        decoder = Fernet(self.other_key)
        try:
            info = pickle.loads(decoder.decrypt(message))
            print(f"5 ({self.name}): N_B-1 = {info['N']}")
            print("=>Message 5 authentication was successful")
        except:
            print("=>Message 5 authentication was unsuccessful")
            exit(84)

        if info["N"] == self.nonce - 1:
            print("Done !!!!!!!")

S = my_server()
user1 = user("Alice")
user2 = user("Bob")
S.set_key_a(user1.name, user1.s_key)
S.set_key_b(user2.name, user2.s_key)
user1.create_connection(user2, S)