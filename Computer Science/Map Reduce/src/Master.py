import socket
from _thread import *
from MapReduce import mapreduce as mr
import ConfigFile as cf

ServerSocket = socket.socket()
host = cf.server_name
port = cf.server_port_num
ServerSocket.bind((host, port))

print('The server is ready to receive')
ServerSocket.listen(5)

def handler(clientSocket):
    # Implementing Fault Tolerance for Master Server
    retry = True
    while retry:
        try:
            num_mappers = int(clientSocket.recv(2048).decode('utf-8'))
            num_reducers = int(clientSocket.recv(2048).decode('utf-8'))
            input_location = clientSocket.recv(2048).decode('utf-8')
            map_func = clientSocket.recv(2048).decode('utf-8')
            red_func = clientSocket.recv(2048).decode('utf-8')
            output_location = clientSocket.recv(2048).decode('utf-8')
            mr_obj = mr(num_mappers,num_reducers)
            status = mr_obj.runMapReduce(input_location,map_func,red_func,output_location)
            clientSocket.sendall(str.encode(status))
            retry = False
        except:
            clientSocket.sendall(str.encode("restart"))
            retry = True
    clientSocket.close()

while True:
    clientSocket, address = ServerSocket.accept()
    start_new_thread(handler, (clientSocket, ))
ServerSocket.close()