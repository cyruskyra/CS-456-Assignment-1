"""Client for introductory socket programming."""

import sys
import socket


def client_udp_negotiation(server_address, n_port, req_code):
    """
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(req_code, ("", n_port))
        r_port = int(client_socket.recvfrom(1024))
        if r_port == -1:
            print("REQUEST CODE IS INVALID")
            sys.exit(1)
        print("TRANSACTION PORT NEGOTIATED: " + r_port)
        print("CONFIRMING TRANSACTION PORT WITH SERVER")
        client_socket.sendto(r_port, ("", n_port))
        ack = str(client_socket.recvfrom(1024))
        if ack == "ok":
            print("TRANSACTION PORT CONFIRMATION ACKNOWLEDGED")
            return r_port
        else:
            print("TRANSACTION PORT CONFIRMATION FAILED")
    except socket.error, e:
        print("CONNECTION ERROR: " + e)
        sys.exit(1)


def client_tcp_transaction(r_port, msg):
    """
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("", r_port))
    client_socket.send(msg)
    client_rcv_msg = client_socket.recv(1024)
    return client_rcv_msg


def main():
    """
    Args:
        req_code: the request code determined by the user.
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
    client_rcv_msg = client_tcp_transaction(r_port, msg)
    print("CLIENT_RCV_MSG='{}'".format(client_rcv_msg))


if __name__ == "__main__":
    main()
