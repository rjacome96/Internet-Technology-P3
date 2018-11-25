import socket as aSocket
import sys
import time
import hmac

def TLDS2Server():
    
    try:
        rootServerSocket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        clientSocket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        print("[TLDS2]: Successfully created sockets")
    except aSocket.error as err:
        print("Socket open error {}\n".format(err))
        return

    dnsFile = "PROJ3-TLDS1.txt"
    keys2File = "PROJ3-KEY2.txt"

    tlds2_Dict = {}
    tlds2_keys = []

    try:
        with open(dnsFile, "r") as dnsTableFile, open(keys2File, "r") as keysFile:
            for fieldLine in dnsTableFile:
                dictKey = fieldLine.rstrip()
                recordString = dictKey.rsplit()
                hostName = recordString[0]
                ipAddress = recordString[1]
                flag = recordString[2].rstrip()
                
                tlds2_Dict[hostName] = (ipAddress, flag)

            for key in keysFile:
                key = key.rstrip()
                tlds2_keys.append(key)
    except FileNotFoundError:
        print("File not Found. Please Try again")
        return

    port = 8000
    serverBinding = ('', port)
    rootServerSocket.bind(serverBinding)
    print("[TLDS2]: Socket is binded to port: {}".format(port))

    rootServerSocket.listen(1)
    print("[TLDS2]: Listening for one connection on port 8000...")

    rootConnection = rootServerSocket.accept()
    
    rootSocket = rootConnection[0]

    while True:

        serverInfo = rootSocket.recv(1024).decode('utf-8')

        if not serverInfo:
            break

        print("[TLDS2]: Recieved from root server: {}".format(serverInfo))

        rootSocket.send("TLDS2 Server here".encode('utf-8'))


    time.sleep(10)
    rootSocket.close()

TLDS2Server()