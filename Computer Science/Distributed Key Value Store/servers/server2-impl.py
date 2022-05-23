# from socket import *
import socket
from _thread import *
import ConfigFile as cf
import sys
import json
import time
import warnings
warnings.filterwarnings("ignore")

ServerSocket = socket.socket()
host2 = cf.server2_name
port2 = cf.server2_port_num
ServerSocket.bind((host2, port2))

server1_name = cf.server1_name
server1_port = cf.server1_port_num

print('The server 2 is ready to receive')
ServerSocket.listen(5)

def check_key(key:str):
    flag = False
    flag2 = True
    command_operators = {'\n','\t','\r','\b','\f','\'','\"','\\','\v','\a'}
    for ch in key:
        if ch in command_operators:
            flag2 = False
    if sys.getsizeof(key) < 250 and key.isalnum():
        flag = True
    return (flag and flag2)

def set_value(clientSocket, temp):
    if not(check_key(temp[1])):
        return "CLIENT_ERROR KEY NOT AS PER PROTOCOL\r\n"
    else:
        value = clientSocket.recv(9541).decode('utf-8')
        if len(value) <= 2147483647:
            if len(temp) != 4:
                return 'CLIENT_ERROR COMMAND PROTOCOL NOT FOLLOWED\r\n'
            elif int(temp[2]) != sys.getsizeof(value):
                return 'CLIENT_ERROR LENGTH OF VALUE DOES NOT MATCH\r\n'
            else:
                try:
                    with open("Database2/"+temp[1]+".json",'w') as write_file:
                        json.dump(value, write_file)
                    return "STORED\r\n"
                except Exception:
                    return "NOT_STORED\r\n"
        else:
            return "NOT_STORED\r\n"

def get_value(clientSocket, temp):
    for i in range(0,len(temp)):
         try:
            with open("Database2/"+temp[i]+".json",'r') as read_file:
                 value = json.load(read_file)
            clientSocket.sendall(str.encode("VALUE "+str(temp[i])+" "+str(sys.getsizeof(value))+" \r\n"+value+ "\r\n"))
         except FileNotFoundError:
            pass

def eventual_consistency(command, value):
    time.sleep(10)
    command[3] = 'ignore'
    temp = ' '.join([item for item in command])
    print("Getting connection for server 1")
    server1_socket = socket.socket()
    server1_socket.connect((server1_name, server1_port))
    print("Conn received for server 1")
    server1_socket.sendall(str.encode(temp))
    server1_socket.sendall(str.encode(value))
    discard = server1_socket.recv(9542).decode('utf-8')
    print("[Message from server 2] Broadcast feedback from Server 1: "+ discard)
    server1_socket.close()

def handler(clientSocket):
    command1 = clientSocket.recv(9541).decode('utf-8')
    temp = command1.split()
    state = temp[-1]
    if state == 'linear':
        try:
            cf.lock2.acquire(blocking= True)
            seq = cf.sequential + 1
            cf.increment()
        finally:
            cf.lock2.release()
    if temp[0] == "set":
        if state == 'linear':
            while cf.current != seq:
                continue
            temp[-1] = 'sequential'
        # print("Sequence number " + str(seq) + " started")
        if temp[-1] == 'sequential':
            print(temp[-1])
            try:
                print("Lock acquired for write")
                cf.lock.acquire(blocking= True)
            finally:
                pass
        set_result = set_value(clientSocket, temp)
        clientSocket.sendall(str.encode(set_result))
        print("here2")
    elif temp[0] == "get":
        state = None
        if temp[len(temp) - 1] == 'linear':
            while cf.current != seq:
                continue
            temp.pop(-1)
            state = 'linear'
        temp.pop(0)
        print("con in read",temp[-1])
        if state == 'linear':
            print("lock acquired for read")
            cf.lock.acquire(blocking= True)
        get_value(clientSocket, temp)
        if state == 'linear':
            print("lock released for read")
            cf.lock.release()
        clientSocket.sendall(str.encode('END\r\n'))
    else:
        clientSocket.sendall(str.encode('ERROR\r\n'))
    try:
        cf.lock2.acquire(blocking= True)
        cf.current += 1
    finally:
        cf.lock2.release()
    if temp[0] == 'set':
        print("lock released")
        cf.lock.release()
    clientSocket.close()
    if temp[0] == 'set' and temp[3] == 'eventual':
        with open("Database2/"+temp[1]+".json",'r') as read_file:
            value = json.load(read_file)
        eventual_consistency(temp, value)

while True:
    clientSocket, address = ServerSocket.accept()
    start_new_thread(handler, (clientSocket, ))
ServerSocket.close()