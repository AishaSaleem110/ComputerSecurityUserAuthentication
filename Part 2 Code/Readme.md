# Fixing Needham-Schroeder Protocol

CO876 CW2: Advanced Question Week 19  

### The Code

This code was written in Python 3.10. There is only one python file named as OptionalQuestion.py:

# Following are two classes found in OptionalQuestion.py
* My_server: Server class represents the Server which is responsible for generating and distribution of the keys and will act as our Key Distribution Center (KDC). The server uses Fernet library to generate keys.
* User: User class represents any party which needs to communicate with other party on the network using secure session key from the Server

### Running The Code
*To run the code, import  OptionalQuestion.py into any existing python project and right click on file
and select Run OptionalQuestion.py

*Or use any online compiler such as:
1. Open link https://www.onlinegdb.com/online_python_compiler 
2. Copy and paste the code in OptionalQuestion.py 
3. and Run.

*The file is self-contained and all necessary libraries are imported.


### What is in the code
When OptionalCode.py file is run, the main function provides following two demonstrations:

*First demonstrate running Needham Schroeder Protocol successfully without any intruder or replay attack
*Then it demonstrates how protocol fails the authentication when an intruder tries a replay attack

### How Needham Schroeder is Used

The naive Needham-Schroeder can be split up into 5 main steps:
1.	 A → S : A,B, Na
Alice sends a message to server sending her identity, Bob’s identity B and a random number Nonce Na.

2.	 S → A : {Na,B,Kab, {Kab,A}Kbs } Kas
Server generates a session key Kab and sends it back to Alice. It also sends a package with session key Kab and Alice’s nonce Na to be sent to B encrypted in Kbs for Alice to forward it to Bob.
 
3.	A → B : {Kab,A}Kbs 
Alice then forwards that whole package received from Server S to Bob. Bob is able to decrypt it as it is encrypted Kbs is the shared key between Bob and Server.

4. B → A : {Nb}Kab 
Bob now decrypts the package and has gotten Kab. Bob now generates a random number Nonce Nb and encrypt is using Kab (session key Bob has just received) to show to Alice that he has successfully gotten the session key.

5. A → B : {Nb − 1}Kab 
Now Alice performs a simple operation on the Nonce Nb and send it back to Bob showing Alice is still available to start communication.

Here Na and Nb are nonces.

### Security from Replay Attacks
It is possible for an intruder to interrupt messages from an earlier session. An intruder can intercept KAB from an older session and use the key to get successful authentication as Bob. There is no mechanism at Bob to ensure that Kab which is sent to Bob at step 3 is fresh or an old session being sent.
It is called a Replay Attack where intruder can reuse the old session key and pass it as a new one. 

#Fixes in Needham Protocol
To combat the above issues, I have used the following two fixes:
1. Adding authentication of Alice/User 1 by including a new Nonce
2. Adding timestamp is a common fix in security protocols which is useful to identify replaying of old session key. I have introduced timestamps at the step 4 and 5 of the protocol. 

### References
*I have used instruction given in PC class week 20 advanced question to add authentication of user1/Alice

*I have used the following paper as reference to add timestamp fix:

Denning, Dorothy & Sacco, Giovanni. (1981). Timestamps in Key Distribution Protocols. Commun. ACM. 24. 533-536. 10.1145/358722.358740. 