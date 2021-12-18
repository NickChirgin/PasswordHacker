import socket
import sys


HOST = sys.argv[1]
PORT = int(sys.argv[2])
ADRESS = (HOST, PORT)
password = sys.argv[3]
password = password.encode()
with socket.socket() as s:
    s.connect(ADRESS)
    s.send(password)
    result = s.recv(1024)
    result = result.decode()
    print(result)
