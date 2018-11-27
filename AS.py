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
    
    # The names that the TLDS servers will go by
    # (If they will not be reffered to by their host name)
    tlds1ServerName = "TLDS1"
    tlds2ServerName = "TLDS2"

    # The names of the TLDS servers, will be given as input later
    tlds1ServerHostName = "kill.cs.rutgers.edu"
    tlds2ServerHostName = "grep.cs.rutgers.edu"

    # Easier to send to TLDS whether their digests matched with the client's
    matchedMessage = "Matched".encode('utf-8')
    noMatchMessage = "No Match".encode('utf-8')

    # Pick port and bind it to this machine's IP address for Client
    port = 6000
    serverBinding = ('', port)
    clientSocketServer.bind(serverBinding)
    print("[AS]: Socket is binded to port: ", port)

    # Connect to tlds1 server
    tlds1ServerPort = 7000
    tlds1ServerAddr = aSocket.gethostbyname(tlds1ServerHostName)
    tlds1ServerConnection = (tlds1ServerAddr, tlds1ServerPort)
    #tlds1ServerConnection = ('', tlds1ServerPort)
    tlds1SocketServer.connect(tlds1ServerConnection)

    # Connect to tlds2 server
    tlds2ServerPort = 8000
    tlds2ServerAddr = aSocket.gethostbyname(tlds2ServerHostName)
    tlds2ServerConnection = (tlds2ServerAddr, tlds2ServerPort)
    #tlds2ServerConnection = ('', tlds2ServerPort)
    tlds2SocketServer.connect(tlds2ServerConnection)


    # Have socket listen on the port 6000
    clientSocketServer.listen(1)
    print("[AS]: Listening for one connection on port 6000...")
    clientConnection = clientSocketServer.accept()

    clientSocket = clientConnection[0]

    # Once connected, service the client until the end
    while True:

        # Obtain client's digest and challenge string
        clientInfo = clientSocket.recv(1024).decode('utf-8')
        
        if not clientInfo:
            break

        print("[AS]: Recieved from client: {}".format(clientInfo))

        # Distinguish client's digest and challenge string
        clientInfo = clientInfo.split()
        clientChallengeString = clientInfo[0]
        clientDigestHex = clientInfo[1]
        print("[AS]: Client challenge string: {}".format(clientChallengeString))
        print("[AS]: Client digest: {}".format(clientDigestHex))

        # Send client's challenge string to both TLDS servers
        tlds1SocketServer.send(clientChallengeString.encode('utf-8'))
        tlds2SocketServer.send(clientChallengeString.encode('utf-8'))
        
        # Receive the servers' resluting digests in hex form
        tlds1DigestHex = tlds1SocketServer.recv(1024).decode('utf-8')
        tlds2DigestHex = tlds2SocketServer.recv(1024).decode('utf-8')
        print("[AS]: {}".format(tlds1DigestHex))
        print("[AS]: {}".format(tlds2DigestHex))


        # Compare client's digest with both servers' digests
        # Client is authenticated for TLDS1
        if(hmac.compare_digest(clientDigestHex, tlds1DigestHex)):
            print("[AS]: Client authorized for TLDS1")
            tlds1SocketServer.send(matchedMessage)
            tlds2SocketServer.send(noMatchMessage)
            dataToClient = tlds1ServerName
        # Client is authenticated for TLDS2
        elif(hmac.compare_digest(clientDigestHex, tlds2DigestHex)):
            print("[AS]: Client authorized for TLDS2")
            tlds2SocketServer.send(matchedMessage)
            tlds1SocketServer.send(noMatchMessage)
            dataToClient = tlds2ServerName
        # No server authenticated for Client
        else:
            print("[AS]: No digest matched")
            tlds1SocketServer.send(noMatchMessage)
            tlds2SocketServer.send(noMatchMessage)
            dataToClient = "TLDS servers' digest did not matched client's"

        clientSocket.send(dataToClient.encode('utf-8'))

		

    clientSocketServer.close()
    tlds1SocketServer.shutdown(aSocket.SHUT_RDWR)
    tlds2SocketServer.shutdown(aSocket.SHUT_RDWR)
    tlds1SocketServer.close()
    tlds2SocketServer.close()

AuthenticationServer()