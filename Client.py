import socket as aSocket
import sys
import hmac

def connectClient():

    try:
        rsClientSocket = aSocket.socket(aSocket.AF_INET, aSocket.SOCK_STREAM)
        print("[C]: Successfully created sockets")
    except aSocket.error as err:
        print("Socket open error: {0} \n".format(err))

    """
    Block of code to uncomment if we need to receive
    input from command line
    try:
        rootServerName = sys.argv[1]
    except IndexError:
        print("Not enough arguments given")
        return
    """

    asPort = 6000
    #rsHostName = rootServerName
    rsHostName = ""
    rsAddr = aSocket.gethostbyname(rsHostName)
    rsSocketConnection = (rsAddr, asPort)

    rsClientSocket.connect(rsSocketConnection)

    #hnsFile = sys.argv[2]
    hnsFile = "PROJ3-HNS.txt"

    with open(hnsFile, "r") as readFile:
        with open("RESOLVED.txt", "w") as writeFile:
            for hostName in readFile:
                # Stripping the new line at the end
                hostName = hostName.rstrip()
                # First contact to RS server
                rsClientSocket.send(hostName.encode('utf-8'))

                # Get resulting String from server
                serverResult = rsClientSocket.recv(1024).decode('utf-8')

                # Write result to file
                writeFile.write(serverResult + "\n")


    rsClientSocket.shutdown(aSocket.SHUT_RDWR)
    rsClientSocket.close()

connectClient()