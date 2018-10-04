"""Client for introductory socket programming.

Initiates a negotiation request with the server. If correct request code was
sent, then confirms a TCP transaction socket with the server. Sends a message
to the server, and waits for server to reply with the reverse message.
"""

import sys
import socket


def client_udp_negotiation(server_address, n_port, req_code):
    """Initiates a negotiation request and confirms a transaction port with server.

    Initiates a negotiation request with the server on n_port with the request
    code req_code. If the request code is valid, receives and confirms a TCP
    port with the server to conduct a transaction on. If the confirmation is
    successful, returns this TCP port. If the request code is invalid, exits
    the program.

    Args:
        server_address: address of the server to contact.
        n_port: port to negotiate with the server on.
        req_code: client request code for negotiation.

    Returns:
        r_port: TCP port to conduct a transaction on with the server.
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("INITIATING NEGOTIATION WITH REQUEST CODE: " + str(req_code))
        client_socket.sendto(str(req_code).encode('utf-8'),
                             (server_address, n_port))
        r_port = int(client_socket.recvfrom(1024)[0])
        if r_port == -1:
            print("REQUEST CODE IS INVALID")
            sys.exit(1)
        print("TRANSACTION PORT NEGOTIATED: " + str(r_port))
        print("CONFIRMING TRANSACTION PORT WITH SERVER")
        client_socket.sendto(str(r_port).encode('utf-8'),
                             (server_address, n_port))
        ack = (client_socket.recvfrom(1024)[0]).decode('utf-8')
        if ack == "ok":
            print("TRANSACTION PORT CONFIRMATION ACKNOWLEDGED")
            return r_port
        else:
            print("TRANSACTION PORT CONFIRMATION FAILED")
            sys.exit(1)
    except socket.error as e:
        print("CONNECTION ERROR: " + str(e))
        sys.exit(1)


def client_tcp_transaction(server_address, r_port, msg):
    """Sends a message to the server and receives it back reversed.

    Connects to the server at server_address on r_port. Sends
    string msg to the server, and waits for a reply. Reply should
    be msg but reversed.

    Args:
        server_address: address of the server to contact.
        r_port: port to conduct transaction with the server on.
        msg: message to be sent to the server for reversing.

    Returns:
        client_rcv_msg: the reply recieved from the server.
    """
    print("INITIATING TRANSACTION")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, r_port))
    print("SENDING MESSAGE: " + msg)
    client_socket.sendall(msg.encode('utf-8'))
    client_rcv_msg = (client_socket.recv(1024)).decode('utf-8')
    return client_rcv_msg


def main():
    """Negotiates a random port with server to transact messages.

    Checks if all command line arguments are determined.
    Negotiates a TCP port over UDP with a server to transact messages.
    Sends a message to the server over the TCP port and waits for a
    reply.

    Command Line Args:
        server_address: address of the server to contact.
        n_port: port to negotiate with the server on.
        req_code: client request code for negotiation.
        msg: message to be sent to the server for reversing.

    Raises:
        IndexError: If some parameters are not determined in the
            command line arguments.
        ValueError: If any of the parameter types are wrong.
    """
    try:
        server_address, msg = map(str, [sys.argv[1], sys.argv[4]])
        n_port, req_code = map(int, [sys.argv[2], sys.argv[3]])
    except IndexError:
        print("MISSING PARAMETER(S), "
              "<SERVER_ADDRESS> <N_PORT> <REQ_CODE> <MSG> REQUIRED")
        sys.exit(1)
    except ValueError:
        print("PARAMETER TYPE WRONG, TRY AGAIN")
        sys.exit(1)
    r_port = client_udp_negotiation(server_address, n_port, req_code)
    client_rcv_msg = client_tcp_transaction(server_address, r_port, msg)
    print("CLIENT_RCV_MSG='{}'".format(client_rcv_msg))


if __name__ == "__main__":
    main()
