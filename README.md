# CS 456 Assignment 1: Introductory Socket Programming

The goal of this assignment is to gain experience with both UDP and TCP socket programming in a client-server environment. A client program (client.py) and a server program (server.py) are implemented here and communicate between each other. The client will send requests to the server to reverse strings (taken as a command line input) over the network using sockets. A  two-stage communication process is used.  In the negotiation stage, the client and the server negotiate on a random TCP port for later use through a negotiation UDP port of the server. Later in the transaction stage, the client connects to the server through the elected random TCP port for actual data transfer.

## How to run the program

Start the server first. First, in your server machine, navigate to the "source" folder of this project:
'''
cd ./source
'''
Then, in your terminal, enter:
'''
chmod +x ./server.sh
./server.sh <REQ_CODE>
'''
where 
* <REQ_CODE> is the request code that client requests will be checked against.
Take note of the stdout in the terminal: the SERVER_PORT is the <N_PORT> to enter in the client command line arguments in the next step.

Once the server has started, start the client. In your client machine, navigate to the "source" folder of this project. Then, in your terminal, enter:
'''
chmod +x ./client.sh
./client.sh <SERVER_ADDRESS> <N_PORT> <REQ_CODE> <MSG>
'''
where 
* <SERVER_ADDRESS> is the address of the server to contact;
* <N_PORT> is the port to negotiate with the server on;
* <REQ_CODE> is the client request code for negotiation; and
* <MSG> is the message to be sent to the server for reversing.

If the client and server request codes are the same, the client will send <MSG> to the server and recieve it back reversed.

## Machine program was tested on

CPU15 on the UWaterloo Undergraduate Linux Servers.

## Author

Kyra Wang Nian Yu, WATID 20809112