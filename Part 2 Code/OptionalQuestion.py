import pickle
from random import random
from time import time

from cryptography.fernet import Fernet


class My_server:
    """
    Server class represents the Server which is responsible for generating and distribution of the keys
    """

    def __init__(self):
        self.users = {}
        self.nonce_a = ""

    def set_user(self, name, key=None) -> str:
        """
        This method registers a user to the Server
        :param name: name of the user
        :param key: Shared key between server and user
        :return: user name
        """
        if key is None:
            self.users[name] = Fernet.generate_key()
        else:
            self.users[name] = key
        print(f"Pre-shared key between {name} and Server: {self.users[name]}")
        return self.users[name]

    def start_connection(self, a: str, b: str, n_a: str, b_identity_package):
        """
        This method server Server generates a session key Kab and sends it back to user 1 along with a package for user 2.
        :param a: user 1
        :param b: user 2
        :param n_a: Nonce of user 1
        :param b_identity_package: Nonce and identity generated by user 2
        :return: a package containing session key Kab and package for user 2
        """

        if not (a in self.users and b in self.users):
            print(f"2 (Server): A or B doesn't exist.")
            exit(84)
        key_ab = Fernet.generate_key()
        print(f" \n 2 (Server): K_AB = {key_ab}")
        fernet_b = Fernet(self.users[b])
        b_package = pickle.loads(fernet_b.decrypt(b_identity_package))
        b_package['K_AB'] = key_ab
        timestamp = int(time())
        b_package['T'] = timestamp
        b_package_encrypted = fernet_b.encrypt(pickle.dumps(b_package))
        print(
            f"2 (Server): E_{{K_BS}}(K_AB, A, N^B,T) = E_{{{self.users[b]}}}({key_ab}, {b_package['ID_A']}, {b_package['N^B']} {b_package['T']}) = {b_package_encrypted}")
        return_obj = {"N_A": n_a, "B": b, "K_AB": key_ab, "T": timestamp, "package": b_package_encrypted}
        fernet_a = Fernet(self.users[a])
        encrypted_return_obj = fernet_a.encrypt(pickle.dumps(return_obj))
        print(
            f"2 (Server): E_{{K_AS}}(N_A, B, K_AB, P, T) = E_{{{self.users[a]}}}({return_obj['N_A']}, {return_obj['B']}, {return_obj['K_AB']}, {return_obj['package']}, {return_obj['T']}) = {encrypted_return_obj}")
        return encrypted_return_obj


class User:
    """
    User class represents any party which needs to communicate with other party on the network using secure session key from the Server
    """

    def __init__(self, name):
        self.name = name
        self.s_key = ""
        self.other_key = ""
        self.nonce = 0
        self.package = ''

    def set_key(self, key: str) -> None:
        self.s_key = key

    def set_knowns(self, session_key: str, package: str) -> None:
        """
        This function is used to set the values that are intercepted by intruder to demonstrate the replay attack
        :param session_key: Session key Kab
        :param package: Package that contains Kab encrypted in Kbs
        :return:
        """
        self.package = package.encode()
        self.other_key = session_key.encode()

    def get_knowns(self) -> (str, str):
        """
        This method the values that are intercepted by intruder to demonstrate the replay attack
        :return:
        """
        return self.other_key, self.package

    def start_needham_protocol(self, other, server: My_server, intruder: bool = False) -> None:
        """
        This method represents all the steps of the Needham Schroeder protocol.
        :param other: User 2
        :param server: Server
        :param intruder: if true it represents demonstration of an intruder trying replay attack
        :return: None
        """

        # Alice sending identity to Bob and Bob responds back to Alice with a nonce N′B encrypted with Bob’s key with
        # the Server Kbs.
        b_identity_package = other.start_with_identity(self.name)
        nonce = int(random() * 10 ** 20)
        print(f"\n1 ({self.name}): N_A = {nonce}")
        print(
            f"1 ({self.name})=>Server: (A, B, N_A , E_BS_{{A, N^B}}) = ({self.name}, {other.name}, {nonce}, E_{{{other.s_key}}}({b_identity_package})")
        print()
        decoder = Fernet(self.s_key)

        # Alice sends a message to server sending her identity, Bob’s identity B and a random number Nonce Na. It
        # also sends the package sent back by B containing the new nonce N′B to the server.
        message = server.start_connection(self.name, other.name, nonce, b_identity_package)

        # Server generates a session key Kab and sends it back to Alice along with Nonce of A Na, identity of Bob B
        # and a Timestamp T. It also sends a package with session key Kab and Alice’s nonce Na and the nonce N′B sent
        # earlier by Bob to Alice and a Timestamp T encrypted in Kbs for Alice to forward it to Bob.
        try:
            info = pickle.loads(decoder.decrypt(message))
            print(info)
            print(
                f"2 (Server => {self.name}): E_{{K_AS}} (N_A,B,K_AB,T,E_{{K_BS}}(K_AB,A,N^A)) = E_{{{self.s_key}}} ({info['N_A']},{info['B']},{info['K_AB']},{info['T']},{info['package']}) = {info}")
            print(
                f"2 ({self.name}): E_{{K_AS}} (N_A,B,K_AB,T,E_{{K_BS}}(K_AB,A,N^A)) = E_{{{self.s_key}}} ({info['N_A']},{info['B']},{info['K_AB']},{info['T']},{info['package']})")
            print("=>Message 2 authentication was successful! \n")
        except:
            print("=>Message 2 authentication was unsuccessful!")
            return exit(84)
        package = info["package"]
        session_key = info['K_AB']
        if intruder:
            session_key, package = self.get_knowns()
        else:
            pass
        self.other_key = session_key
        decoder_ab = Fernet(self.other_key)
        current_time = int(time())
        time_difference_mins = (current_time - info["T"]) // 60 % 60

        # Alice checking for a replay attack by comparing the timestamp sent by server
        if time_difference_mins < 1:

            # Alice then forwards that whole package received from Server S to Bob.
            # Bob is able to decrypt it as it is encrypted Kbs is the shared key between Bob and Server.
            message = other.get_package(package, self)

            # Bob now generates a random number Nonce Nb and encrypt is using Kab(session key Bob has just received)
            # to show to Alice that he has successfully gotten the session key.
            try:
                value = pickle.loads(decoder_ab.decrypt(message))['N^B']
                print(f"4({self.name}):N^B={value}")
                print("=>Message 4 authentication was successful!")
            except:
                print("=>Message 4 authentication was unsuccessful!")
            print()
            updated_nonce = value - 1
            print(f"5 {self.name}=>{other.name}: E_{{K_AB}}(N^B-1)= E_{{{self.other_key}}} ({updated_nonce})")

            # Now Alice performs a simple operation on the Nonce Nb and send it back to Bob showing Alice is still
            # available to start communication
            other.get_nonce(decoder_ab.encrypt(pickle.dumps({"N^B-1": updated_nonce})))

        else:
            print("=>Message authentication was unsuccessful!Replay Attack possible")
            return exit(84)

    def start_with_identity(self, identity: str) -> str:
        """
        This method represents the beginning of the protocol where user 1 is sending a message to user 2 containing its identity
        and user 2 then responds back to user 1 with a nonce N′B encrypted with user2’s key with the Server Kbs.
        :param identity:
        :return:
        """
        encoder = Fernet(self.s_key)
        nonce = int(random() * 10 ** 20)
        return_obj = {"ID_A": identity, "N^B": nonce}
        return encoder.encrypt(pickle.dumps(return_obj))

    def get_package(self, message, other):
        """
        This method represents the step where user 1 sends the package received by server in user2's encryption key kbs to user 2
        :param message: package received by server
        :param other: User 2
        :return:
        """
        decoder = Fernet(self.s_key)
        try:
            info = pickle.loads(decoder.decrypt(message))
            print(
                f"\n3 ({other.name} => {self.name}): E_{{K_BS}}(K_AB,A,N^A,T) = E_{{{self.s_key}}}({info['K_AB']},{info['ID_A']},{info['N^B']}, {info['T']}) = {message}")

            print(f"\n3 ({self.name}): (K_AB,A,N^B,T) = ({info['K_AB']},{info['ID_A']},{info['N^B']},{info['T']})")

            current_time = int(time())
            # calculating time in minutes
            time_difference_mins = (current_time - info["T"]) // 60 % 60

            if time_difference_mins < 1:
                print("=>Message 3 authentication was successful")
            else:
                print("=>Potential Replay Attack. Message 3 authentication was unsuccessful")
                return exit(84)
        except:
            print("=>Message 3 authentication was unsuccessful")
            return exit(84)

        self.other_key = info["K_AB"]
        coder = Fernet(self.other_key)
        self.nonce = info['N^B']
        message = coder.encrypt(pickle.dumps({"N^B": self.nonce}))
        print()
        print(f"(4 {self.name}):N^B = {self.nonce}")
        print(f"(4 {self.name} => {other.name}): E_{{K_AB}}(N^B)=E_{{{info['K_AB']}}}({self.nonce})={message}")
        return message

    def get_nonce(self, message):
        decoder = Fernet(self.other_key)
        try:
            info = pickle.loads(decoder.decrypt(message))
            print(f"5 ({self.name}): N_B-1 = {info['N^B-1']}")
            print("=>Message 5 authentication was successful")
        except:
            print("=>Message 5 authentication was unsuccessful")
            return exit(84)

        if info["N^B-1"] == self.nonce - 1:
            print("Done !!!!!!!")


def successful_needham_protocol_demo(server):
    # creating users and setting keys
    user1 = User("Alice")
    user2 = User("Bob")
    user1.set_key(server.set_user(user1.name))
    user2.set_key(server.set_user(user2.name))
    # starting the protocol
    user1.start_needham_protocol(user2, server)


def needham_protocol_demo_with_intruder(server):

    user1 = User("Alice")
    user2 = User("Bob")
    user3 = User("Eve")
    user1.set_key(server.set_user(user1.name))
    # setting pre session key for replay attack
    user2.set_key(server.set_user(user2.name, "SpqNZSq1WY3SJUNVNurgRXVtXZKBlW7OeM3du5KP_Og=".encode()))
    user3.set_key(server.set_user(user3.name))

    # setting pre session key for replay attack
    user3.set_knowns("BdNEXHVTmNZBnro3KCtiqfxZSkqtcv_YzveAayQCWOY=",
                     "gAAAAABh6FzSv91D4yyD6NnaXKokWA28aVB5IGCtKGTYtFi-FAVduD2MP588x2AFrmG_euCVk0zoKC38HpM7Cmk8XceAqyOqQIhVe4ZBuUHZY6LURd2xEwPM5BYufZFDLF6efre0LCsYfZL6vgQF9iR5Tm8nApmm4N2_Xae8yyEDKu_UkrwN4bUdz5zFv_7O7W5HcexfZuYiDwPoRYcRx-uyMUoIfInKKw==")
    # starting the protocol
    user3.start_needham_protocol(user2, server, True)


def main():
    # starting server
    S = My_server()
    print(f"Demonstrating successful running of protocol without any replay attack:")
    successful_needham_protocol_demo(S)

    print("Demonstrating protocol with intruder")
    needham_protocol_demo_with_intruder(S)
    return 0


if __name__ == '__main__':
    exit(main())