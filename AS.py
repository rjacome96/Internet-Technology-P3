import socket as aSocket
import time
import hmac
import sys

def AuthenticationServer():

    # Attempt to create three sockets for server
    try:
        tlds1SocketServer = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        tlds2SocketServer = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        clientSocketServer = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        print("[AS]: Successfully created socket")
    except aSocket.error as err:
        print("Socket open error: {0} \n".format(err))
        return

    tlds1ServerName = "TLDS1"
    tlds2ServerName = "TLDS2"
    tlds1ServerHostName = ''
    tlds2ServerHostName = ''

    # Pick port and bind it to this machine's IP address for Client
    port = 6000
    serverBinding = ('', port)
    clientSocketServer.bind(serverBinding)
    print("[AS]: Socket is binded to port: ", port)

    # Connect to tlds1 server
    tlds1ServerPort = 7000
    tlds1ServerAddr = aSocket.gethostbyname(tlds1ServerHostName)
    #tlds1ServerConnection = (tlds1ServerAddr, tlds1ServerPort)
    tlds1ServerConnection = ('', tlds1ServerPort)
    tlds1SocketServer.connect(tlds1ServerConnection)

    # Connect to tlds2 server
    tlds2ServerPort = 8000
    tlds2ServerAddr = aSocket.gethostbyname(tlds2ServerHostName)
    #tlds2ServerConnection = (tlds2ServerAddr, tlds2ServerPort)
    tlds2ServerConnection = ('', tlds2ServerPort)
    tlds2SocketServer.connect(tlds2ServerConnection)

    
    # Have socket listen on the port 6000
    clientSocketServer.listen(1)
    print("[AS]: Listening for one connection on port 6000...")
    clientConnection = clientSocketServer.accept()

    clientSocket = clientConnection[0]

    # Once connected, service the client until the end
    while True:

        clientInfo = clientSocket.recv(1024).decode('utf-8')
        
        if not clientInfo:
            break

        print("[AS]: Recieved from client: {}".format(clientInfo))

        clientInfo = clientInfo.split()
        
        clientChallengeString = clientInfo[0]
        clientDigestHex = clientInfo[1]

        print("[AS]: Client challenge string: {}".format(clientChallengeString))
        print("[AS]: Client digest: {}".format(clientDigestHex))

        tlds1SocketServer.send(clientChallengeString.encode('utf-8'))
        tlds2SocketServer.send(clientChallengeString.encode('utf-8'))
        
        tlds1DigestHex = tlds1SocketServer.recv(1024).decode('utf-8')
        tlds2DigestHex = tlds2SocketServer.recv(1024).decode('utf-8')
        print("[AS]: {}".format(tlds1DigestHex))
        print("[AS]: {}".format(tlds2DigestHex))


        # Client is authenticated for TLDS1
        if(hmac.compare_digest(clientDigestHex, tlds1DigestHex)):
            print("[AS]: Client authorized for TLDS1")
            tlds1SocketServer.send("Matched".encode('utf-8'))
            tlds2SocketServer.send("No Match".encode('utf-8'))
            dataToClient = tlds1ServerName
        # Client is authenticated for TLDS2
        elif(hmac.compare_digest(clientDigestHex, tlds2DigestHex)):
            print("[AS]: Client authorized for TLDS2")
            tlds2SocketServer.send("Matched".encode('utf-8'))
            tlds1SocketServer.send("No Match".encode('utf-8'))
            dataToClient = tlds2ServerName
        # No server authenticated for Client
        else:
            print("[AS]: No digest matched")
            dataToClient = "No Digest Match"

        clientSocket.send(dataToClient.encode('utf-8'))

		

    clientSocketServer.close()
    tlds1SocketServer.shutdown(aSocket.SHUT_RDWR)
    tlds2SocketServer.shutdown(aSocket.SHUT_RDWR)
    tlds1SocketServer.close()
    tlds2SocketServer.close()

AuthenticationServer()