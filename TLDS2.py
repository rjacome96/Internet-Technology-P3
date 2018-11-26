import socket as aSocket
import sys
import time
import hmac

def TLDS2Server():

    try:
        rootServerSocket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        clientServerSocket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        print("[TLDS2]: Successfully created sockets")
    except aSocket.error as err:
        print("Socket open error {}\n".format(err))
        return

    dnsFile = "PROJ3-TLDS1.txt"
    keys2File = "PROJ3-KEY2.txt"
    serverName = "TLDS2"
    hostNotFoundError = "Error: HOST NOT FOUND"

    tlds2_Dict = {}
    tlds2_Key = None

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
                tlds2_Key = key
        
        if(tlds2_Key == None):
            print("[TLDS2]: No Key found in file. Please provide a key")
            return

    except FileNotFoundError:
        print("File not Found. Please Try again")
        return

    rootPort = 8000
    serverBinding = ('', rootPort)
    rootServerSocket.bind(serverBinding)
    print("[TLDS2]: Root Server Socket is binded to port: {}".format(rootPort))

    clientPort = 8500
    serverBinding = ('', clientPort)
    clientServerSocket.bind(serverBinding)
    print("[TLDS2]: Client Socket is binded to port {}".format(clientPort))

    rootServerSocket.listen(1)
    print("[TLDS2]: Listening for one connection on port {}".format(rootPort))
    clientServerSocket.listen(1)
    print("[TLDS2]: Listening for one connection on port {}".format(clientPort))

    rootConnection = rootServerSocket.accept()
    clientConnection = clientServerSocket.accept()
    
    rootSocket = rootConnection[0]
    clientSocket = clientConnection[0]

    while True:

        serverInfo = rootSocket.recv(1024).decode('utf-8')

        if not serverInfo:
            break

        print("[TLDS2]: Recieved from root server: {}".format(serverInfo))

        tldsKey = tlds2_Key

        tlds2Digest = hmac.new(tldsKey.encode(), serverInfo.encode('utf-8'))

        tlds2DigestHex = tlds2Digest.hexdigest()

        rootSocket.send(tlds2DigestHex.encode('utf-8'))

        serverResponse = rootSocket.recv(1024).decode('utf-8')

        if(serverResponse != "Matched"):
            print("[TLDS2]: Did not match client's key")
            continue
        
        clientRequest = clientSocket.recv(1024).decode('utf-8')

        if(clientRequest in tlds2_Dict):
            print("[TLDS2]: {} found".format(clientRequest))
            
            hostName = clientRequest

            hostInfo = tlds2_Dict[hostName]

            hostIPAddress = hostInfo[0]

            hostFlag = hostInfo[1]

            sendToClient = serverName + " " + hostName + " " + hostIPAddress + " " + hostFlag
        else:
            print("[TLDS2]: {} not found".format(clientRequest))

            sendToClient = hostNotFoundError
        
        clientSocket.send(sendToClient.encode('utf-8'))




    time.sleep(10)
    rootSocket.close()

TLDS2Server()