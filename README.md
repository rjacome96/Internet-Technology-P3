# Internet-Technology-P3
DNS client with Authentication server

Project 3

December 10, 2018

Professor Badri Nath

Roy Jacome & Kishan Patel

Python version used across all programs: Python 3

How to Run our Project: First start TLDS2.py, second TLDS1.py, third AS.py, and finally Client.py. All ports and IP addresses are hard coded as requested in the project announcment. No input is needed for any program, however, the TLDS servers and client assume that text files: "PROJ3-TLDS2.txt", "PROJ3-KEY2.txt", "PROJ3-TLDS1.txt", "PROJ3-KEY1.txt", and "PROJ3-HNS.txt" are within the same directory as the program running respectively.

Client program creates three sockets and immediately connects to Root (Authentication) server and the two TLDS servers. Client then reads in the given HNS file one line at a time. It takes the given key and challange string, creates the digest and sends the challenge and digest to the root server. Client then waits for a response from server to indicate which of the two TLDS servers to connect to. Once an answer is given, Client connects to appropiate TLDS server, feeds it the hostname request and writes the reply into the RESLOVED.txt file

Authentication Server program creates three sockets, one for client and two for the TLDS servers. Server then begins to wait for client and receives the client's challenge and digest. Server then sends the challenge string to both TLDS servers and awaits a reply from both. Once server receives their respective digest from the Client's challenge string, Root server compare their digest with the Client. Server then chooses the matching digests (if any) and sends the name of the matching TLDS server to the Client. Root server also notifies the TLDS servers if they either matched or not.

Both TLDS servers work very similarly to each other. Both create two sockets to listen for Root server and Client. Both servers fill their DNS tables using a dictionary data structure and save their given keys into a variable. They both then wait until Root server send them a challenge string. Servers then create a digest with the given challenge string and their key and send the resulting digest to the Root server. Both servers then wait to be told whether they matched or not. If matched, then the specified server continues on to service the Client. The other goes back to listening for the server again for the next Client request. The server that continues to service the client directly then waits to be given a host name to look up. Once sent a host name, it looks it up in its dictionary and returns to client the appropiate response.