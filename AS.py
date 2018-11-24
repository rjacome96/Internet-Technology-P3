import socket as aSocket
import time
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
    tlds1ServerConnection = (tlds1ServerAddr, tlds1ServerPort)
    tlds1ServerConnection = ('', tlds1ServerPort)
    tlds1SocketServer.connect(tlds1ServerConnection)

    # Connect to tlds2 server
    tlds2ServerPort = 8000
    tlds2ServerAddr = aSocket.gethostbyname(tlds2ServerHostName)
    tlds2ServerConnection = (tlds2ServerAddr, tlds2ServerPort)
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
		
        dataToClient = "Test"
        clientSocket.send(dataToClient.encode('utf-8'))

        tlds1SocketServer.send("AS to TLDS1 here".encode('utf-8'))
        tlds2SocketServer.send("AS to TLDS2 here".encode('utf-8'))
        
        tlds1Message = tlds1SocketServer.recv(1024).decode('utf-8')
        tlds2Message = tlds2SocketServer.recv(1024).decode('utf-8')
        print("[AS]: {}".format(tlds1Message))
        print("[AS]: {}".format(tlds2Message))

		

    clientSocketServer.close()
    tlds1SocketServer.shutdown(aSocket.SHUT_RDWR)
    tlds2SocketServer.shutdown(aSocket.SHUT_RDWR)
    tlds1SocketServer.close()
    tlds2SocketServer.close()

AuthenticationServer()