#!/usr/bin/python           # This is client.py file
import socket
import sys
from _thread import *


def recvall(sock):
    data = ""
    part = "asd"
    while str(part) != "":
        part = str(sock.recv(1024))
        data += part
        print(part)
    sock.close()
    

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('10.3.39.158', 8888)
print (sys.stderr, 'connecting to %s port %s' % server_address)
sock.connect(server_address)

while True:
    try:
        # Send data
        #start_new_thread(recvall ,(sock,))
        message = input("\n buyur abi: ")
        if(message =="exit") :
            print (sys.stderr, 'closing socket')
            sock.close()
        print ('sending "%s\n' % message)
        data = sock.recv(64)
        if not data: 
            break
        print(data)
        sock.sendall(str.encode(message))
        
        
    finally:
        a=0
sock.close()
