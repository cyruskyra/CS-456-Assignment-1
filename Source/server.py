"""Server for introductory socket programming."""

import sys
import socket


def main(req_code):
    """Negotiates a random port with clients to transact messages.

    Creates an UDP negotiation socket and waits for clients to initiate
    a negotiation. Checks if client sent the correct request code, and
    then creates a TCP transaction socket if so. Receives a message from
    the client, reverses it, sends it back, then continues listening for
    new negotiation initiations.
    
    Args:
        req_code: the request code determined by the user.
    """
    n_socket = create_socket(SOCK_DGRAM, "SERVER_PORT")
    while True:
        r_socket = udp_negotiation(n_socket, req_code)
        tcp_transaction(r_socket)


if __name__ == "__main__":
    try:
        req_code = sys.argv[1]
    except IndexError:
        print "MISSING REQUEST CODE PARAMETER, TRY AGAIN"
        sys.exit(1)
    if not isinstance(req_code, int):
        print "REQUEST CODE MUST BE INTEGER, TRY AGAIN"
        sys.exit(1)
    main(req_code)


def create_socket(socket_type, name_of_port):
    """Returns a socket on a random unoccupied port.

    Args:
        socket_type: socket type to return.
        name_of_port: port identifier to show in the printout.

    Returns:
        new_socket: a new socket of type socket_type.
    """
    new_socket = socket.socket(AF_INET, socket_type)
    new_socket.bind(("", 0))
    print ("{}={}".format(name_of_port, new_socket.getsockname()[1]))
    return new_socket


def udp_negotiation(n_socket, req_code):
    """Processes client request, and creates transaction socket if verified.

    Waits for client on n_socket to initiate negotiation with a request code.
    If the client's request code is the same as the server's request code,
    creates a TCP socket with a random port number. Otherwise, does nothing.
    Then replies client with the TCP socket port number, then acknowledges
    the received TCP socket port number is correct.

    Args:
        n_socket: UDP negotiation socket to wait on for client.
        req_code: the request code that the server verifies against.

    Returns:
        r_socket: random TCP socket to conduct transaction with client on.
    """
    while True:
        print("WAITING FOR CLIENT REQUEST CODE")
        client_req_code, client_address = n_socket.recvfrom(1024)
        if client_req_code == req_code:
            print("CLIENT REQUEST CODE VERIFIED")
            r_socket = create_socket(SOCK_STREAM, "SERVER_TCP_PORT")
            n_socket.sendto(str(r_socket.getsockname()[1]), client_address)
            client_r_port, clientAddress = n_socket.recvfrom(1024)
            if client_r_port == str(r_socket.getsockname()[1]):
                print("CLIENT CONFIRMED TCP PORT")
                n_socket.sendto("ok", client_address)
                return r_socket
            else:
                print("CLIENT FAILED TO CONFIRMED TCP PORT")
                n_socket.sendto("no", client_address)
        else:
            print("CLIENT REQUEST CODE INVALID")


def tcp_transaction(r_socket):
    """Reverses a message from the client and sends it back.

    Waits for client on r_socket to send a message containing a string.
    Reverses the recieved string and sends it back to the client. Then
    closes r_socket.

    Args:
        r_socket: TCP transaction socket to wait on for client.
    """
    r_socket.listen(1)
    connection_socket, client_address = r_socket.accept()
    server_rcv_msg = connection_socket.recv(1024)
    print("SERVER_RCV_MSG='{}'".format(server_rcv_msg))
    reversed_msg = server_rcv_msg[::-1]
    print("REVERSED MESSAGE='{}'".format(reversed_msg))
    connection_socket.send(reversed_msg)
    connection_socket.close()
    r_socket.close()
