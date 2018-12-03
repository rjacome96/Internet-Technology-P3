import socket as aSocket
import sys
import hmac

def connectClient():

    # Attempt to create three sockets for the three servers
    try:
        rsClientSocket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        tlds1SocketServer = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        tlds2SocketServer = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        print("[C]: Successfully created sockets")
    except aSocket.error as err:
        print("Socket open error: {0} \n".format(err))
        return

    # The names that the TLDS servers will go by
    # (If they will not be reffered to by their host name)
    tlds1ServerName = "TLDS1"
    tlds2ServerName = "TLDS2"

    # The host names of AS and TLDS servers, hard coded as requested
    tlds1ServerHostName = "cpps.cs.rutgers.edu"
    tlds2ServerHostName = "java.cs.rutgers.edu"
    rsHostName = ''

    # Create the connections for the servers
    rsPort = 6000
    rsAddr = aSocket.gethostbyname(rsHostName)
    rsSocketConnection = (rsAddr, rsPort)
    #rsSocketConnection = ('', rsPort)
    rsClientSocket.connect(rsSocketConnection)

    tlds1ServerPort = 7500
    tlds1ServerAddr = aSocket.gethostbyname(tlds1ServerHostName)
    tlds1ServerConnection = (tlds1ServerAddr, tlds1ServerPort)
    #tlds1ServerConnection = ('', tlds1ServerPort)
    tlds1SocketServer.connect(tlds1ServerConnection)

    tlds2ServerPort = 8500
    tlds2ServerAddr = aSocket.gethostbyname(tlds2ServerHostName)
    tlds2ServerConnection = (tlds2ServerAddr, tlds2ServerPort)
    #tlds2ServerConnection = ('', tlds2ServerPort)
    tlds2SocketServer.connect(tlds2ServerConnection)

    #hnsFile = sys.argv[2]
    hnsFile = "PROJ3-HNS.txt"

    # Begin connecting to servers to satisfy requests
    try:
        with open(hnsFile, "r") as readFile:
            with open("RESOLVED.txt", "w") as writeFile:
                for line in readFile:

                    infoLine = line.split()

                    # Stripping the new line at the end
                    clientKey = infoLine[0].rstrip()
                    clientChallenge = infoLine[1].rstrip()
                    hostName = infoLine[2].rstrip()

                    # Create the digest and digest hexadecimal by using the given key and challenge string
                    clientDigest = hmac.new(clientKey.encode(), clientChallenge.encode('utf-8'))
                    clientDigestHex = clientDigest.hexdigest()

                    # Send challenge and digest to Authentication Server
                    sendToRootServer = clientChallenge + " " + clientDigestHex
                    print("[C]: {}".format(sendToRootServer))
                    
                    # First contact to RS server
                    rsClientSocket.send(sendToRootServer.encode('utf-8'))

                    # Get resulting tlds server from RS server
                    serverResult = rsClientSocket.recv(1024).decode('utf-8')

                    # Determine which TLDS server to connect given by RS server
                    if(serverResult == tlds1ServerName):
                        print("[C]: Connect to TLDS1")
                        tlds1SocketServer.send(hostName.encode('utf-8'))
                        serverResult = tlds1SocketServer.recv(1024).decode('utf-8')
                    elif(serverResult == tlds2ServerName):
                        print("[C]: Connect to TLDS2")
                        tlds2SocketServer.send(hostName.encode('utf-8'))
                        serverResult = tlds2SocketServer.recv(1024).decode('utf-8')
                    else:
                        print("[C]: Client does not connect to anyone")

                    # Write result to file
                    writeFile.write(serverResult + "\n")
    except FileNotFoundError as err:
        print("File not found. Please try again")


    rsClientSocket.shutdown(aSocket.SHUT_RDWR)
    rsClientSocket.close()

connectClient()