import socket as aSocket
import sys
import time
import hmac

def TLDS1Server():
    try:
        rootServerSocket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        print("[TLDS1]: Successfully created sockets")
    except aSocket.error as err:
        print("Socket open error {}\n".format(err))

    dnsFile = "PROJ3-TLDS1.txt"

    tlds1_Dict = {}

    try:
        with open(dnsFile, "r") as dnsTableFile:
            for fieldLine in dnsTableFile:
                dictKey = fieldLine.rstrip()
                recordString = dictKey.rsplit()
                hostName = recordString[0]
                ipAddress = recordString[1]
                flag = recordString[2].rstrip()
                
                tlds1_Dict[hostName] = (ipAddress, flag)
    except FileNotFoundError:
        print("File not Found. Please Try again")
        return

    port = 7000
    serverBinding = ('', port)
    rootServerSocket.bind(serverBinding)
    print("[TLDS1]: Socket is binded to port: {}".format(port))

    rootServerSocket.listen(1)
    print("[TLDS1]: Listening for one connection on port 7000...")

    rootConnection = rootServerSocket.accept()
    
    rootSocket = rootConnection[0]

    while True:

        serverInfo = rootSocket.recv(1024).decode('utf-8')

        if not serverInfo:
            break

        print("[TLDS1]: Recieved from root server: {}".format(serverInfo))

        rootSocket.send("TLDS1 Server here".encode('utf-8'))


    time.sleep(10)
    rootSocket.close()

TLDS1Server()