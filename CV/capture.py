import socket

s = socket.socket()
port = 3335
s.connect(('127.0.0.1',port))

s.send ('hello'.encode())
s.close()

