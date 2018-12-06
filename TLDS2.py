import socket as aSocket
import sys
import time
import hmac

def TLDS2Server():

    # Create sockets for Root server and Client
    try:
        rootServerSocket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        clientServerSocket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        print("[TLDS2]: Successfully created sockets")
    except aSocket.error as err:
        print("Socket open error {}\n".format(err))
        return

    # Files and this server's name are hardcoded
    # Might need to be written so that it can be given as input
    dnsFile = "PROJ3-TLDS2.txt"
    keys2File = "PROJ3-KEY2.txt"
    serverName = "TLDS2"
    hostNotFoundError = "Error: HOST NOT FOUND"

    # Create dictionary that maps from Host name to IP and flag
    # Also store the server's key
    tlds2_Dict = {}
    tlds2_Key = None

    # Open the DNS and Key file and record data accordingly
    try:
        with open(dnsFile, "r") as dnsTableFile, open(keys2File, "r") as keysFile:
            for fieldLine in dnsTableFile:
                dictKey = fieldLine.rstrip()
                recordString = dictKey.rsplit()
                hostName = recordString[0]
                ipAddress = recordString[1]
                flag = recordString[2].rstrip()
                
                if flag == "NS":
                    continue

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

    # Bind ports so that Root server and client can connect
    rootPort = 8000
    serverBinding = ('', rootPort)
    rootServerSocket.bind(serverBinding)
    print("[TLDS2]: Root Server Socket is binded to port: {}".format(rootPort))

    clientPort = 8500
    serverBinding = ('', clientPort)
    clientServerSocket.bind(serverBinding)
    print("[TLDS2]: Client Socket is binded to port {}".format(clientPort))

    rootServerSocket.listen(1)
    clientServerSocket.listen(1)
    print("[TLDS2]: Listening for one connection on port {}".format(rootPort))
    print("[TLDS2]: Listening for one connection on port {}".format(clientPort))

    rootConnection = rootServerSocket.accept()
    clientConnection = clientServerSocket.accept()
    
    rootSocket = rootConnection[0]
    clientSocket = clientConnection[0]

    # Service Root and client until Root server disconnects
    while True:

        serverInfo = rootSocket.recv(1024).decode('utf-8')

        if not serverInfo:
            break

        print("[TLDS2]: Recieved from root server: {}".format(serverInfo))

        # Using client's challenge string, create a digest with server's key
        # And then send it back to Root server
        tlds2Digest = hmac.new(tlds2_Key.encode(), serverInfo.encode('utf-8'))
        tlds2DigestHex = tlds2Digest.hexdigest()
        rootSocket.send(tlds2DigestHex.encode('utf-8'))

        # Wait for response from server on whether or not the digest matched with client's
        # From here on, it could probably rewritten without being dependent on the server's response
        # But works for now as is
        serverResponse = rootSocket.recv(1024).decode('utf-8')
        if(serverResponse != "Matched"):
            print("[TLDS2]: Did not match client's key")
            continue
        
        # Using the client's request, search if server has it
        # Return result or error
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