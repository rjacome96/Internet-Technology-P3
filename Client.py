import socket as aSocket
import sys
import hmac

def connectClient():

    try:
        rsClientSocket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        tlds1Socket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        tlds2Socket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        print("[C]: Successfully created sockets")
    except aSocket.error as err:
        print("Socket open error: {0} \n".format(err))
        return


    rsPort = 6000
    #rsHostName = rootServerName
    rsHostName = ""
    rsAddr = aSocket.gethostbyname(rsHostName)
    rsSocketConnection = (rsAddr, rsPort)

    rsClientSocket.connect(rsSocketConnection)

    #hnsFile = sys.argv[2]
    hnsFile = "PROJ3-HNS.txt"

    try:
        with open(hnsFile, "r") as readFile:
            with open("RESOLVED.txt", "w") as writeFile:
                for line in readFile:

                    infoLine = line.split()

                    # Stripping the new line at the end
                    clientKey = infoLine[0].rstrip()
                    clientChallenge = infoLine[1].rstrip()
                    hostName = infoLine[2].rstrip()

                    clientDigest = hmac.new(clientKey.encode(), clientChallenge.encode('utf-8'))

                    clientDigestHex = clientDigest.hexdigest()

                    sendToRootServer = clientChallenge + " " + clientDigestHex

                    print("[C]: {}".format(sendToRootServer))
                    

                    # First contact to RS server
                    rsClientSocket.send(sendToRootServer.encode('utf-8'))

                    # Get resulting tlds server from RS server
                    serverResult = rsClientSocket.recv(1024).decode('utf-8')

                    # Write result to file
                    writeFile.write(serverResult + "\n")
    except FileNotFoundError as err:
        print("File not found. Please try again")


    rsClientSocket.shutdown(aSocket.SHUT_RDWR)
    rsClientSocket.close()

connectClient()