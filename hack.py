import socket
import itertools
import sys
import string

HOST = sys.argv[1]
PORT = int(sys.argv[2])
ADRESS = (HOST, PORT)
letter = list(string.ascii_lowercase)
numbers = string.digits
whole_list = list(itertools.chain(letter, numbers))
flag = False
password = ""
n = 1

with socket.socket() as s:
    s.connect(ADRESS)
    while not flag:
        for item in itertools.product(whole_list, repeat=n):
            password = "".join(item)
            password = password.encode()
            s.send(password)
            result = s.recv(1024)
            result = result.decode()
            if result == "Connection success!":
                password = password.decode()
                print(password)
                flag = True
                break
        n += 1
