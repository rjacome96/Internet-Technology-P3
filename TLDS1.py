import socket as aSocket
import sys
import time
import hmac

def TLDS1Server():

    try:
        rootServerSocket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        clientServerSocket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        print("[TLDS1]: Successfully created sockets")
    except aSocket.error as err:
        print("Socket open error {}\n".format(err))
        return

    dnsFile = "PROJ3-TLDS1.txt"
    keys1File = "PROJ3-KEY1.txt"

    tlds1_Dict = {}
    tlds1_keys = []

    try:
        with open(dnsFile, "r") as dnsTableFile, open(keys1File, "r") as keysFile:
            for fieldLine in dnsTableFile:
                dictKey = fieldLine.rstrip()
                recordString = dictKey.rsplit()
                hostName = recordString[0]
                ipAddress = recordString[1]
                flag = recordString[2].rstrip()
                
                tlds1_Dict[hostName] = (ipAddress, flag)
            
            for key in keysFile:
                key = key.rstrip()
                tlds1_keys.append(key)
    except FileNotFoundError:
        print("File not Found. Please Try again")
        return

    rootPort = 7000
    serverBinding = ('', rootPort)
    rootServerSocket.bind(serverBinding)
    print("[TLDS1]: Root Server socket is binded to port: {}".format(rootPort))

    clientPort = 7500
    serverBinding = ('', clientPort)
    clientServerSocket.bind(serverBinding)
    print("[TLDS1]: Client Socket is binded to port: {}".format(clientPort))


    rootServerSocket.listen(1)
    print("[TLDS1]: Listening for one connection on port {}".format(rootPort))
    clientServerSocket.listen(1)

    rootConnection = rootServerSocket.accept()
    clientConnection = clientServerSocket.accept()
    
    rootSocket = rootConnection[0]
    clientSocket = clientConnection[0]

    while True:

        serverInfo = rootSocket.recv(1024).decode('utf-8')

        if not serverInfo:
            break

        print("[TLDS1]: Recieved from root server: {}".format(serverInfo))

        # Might need to delete the array for TLDS server only uses 1 key
        tldsKey = tlds1_keys[0]

        tlds1Digest = hmac.new(tldsKey.encode(), serverInfo.encode('utf-8'))

        tlds1DigestHex = tlds1Digest.hexdigest()

        rootSocket.send(tlds1DigestHex.encode('utf-8'))


    time.sleep(10)
    rootSocket.close()

TLDS1Server()