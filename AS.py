import socket as aSocket
import time
import sys

def AuthenticationServer():

    # Attempt to create three sockets for server
    try:
        tlds1SocketServer = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        tlds2SocketServer = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        clientSocketServer = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        print("[RS]: Successfully created socket")
    except aSocket.error as err:
        print("Socket open error: {0} \n".format(err))

    # Pick port and bind it to this machine's IP address for Client
    port = 6000
    serverBinding = ('', port)
    clientSocketServer.bind(serverBinding)
    print("[RS]: Socket is binded to port: ", port)

    # Connect to .edu server
    tlds1ServerPort = 6500
    #eduServerAddr = aSocket.gethostbyname(eduServerHostName)
    #eduServerConnection = (eduServerAddr, eduServerPort)
    tlds1ServerConnection = ('', tlds1ServerPort)
    #eduSocketServer.connect(eduServerConnection)

    # Connect to .com server
    tlds2ServerPort = 7000
    #comServerAddr = aSocket.gethostbyname(comServerHostName)
    #comServerConnection = (comServerAddr, comServerPort)
    tlds2ServerConnection = ('', tlds2ServerPort)
    #comSocketServer.connect(comServerConnection)

    
    # Have socket listen on the port 6000
    clientSocketServer.listen(1)
    print("[RS]: Listening for one connection on port 6000...")
    clientConnection = clientSocketServer.accept()

    clientSocket = clientConnection[0]

    # Once connected, service the client until the end
    while True:

        clientInfo = clientSocket.recv(1024).decode('utf-8')

        print("[RS]: Recieved from client: {}".format(clientInfo))
        
        if not clientInfo:
            break
		
        dataToClient = "Test"
        clientSocket.send(dataToClient.encode('utf-8'))
		

    clientSocketServer.close()

AuthenticationServer()