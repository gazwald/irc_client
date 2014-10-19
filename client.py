__author__ = 'user'

import socket


def main():
    remote_host = 'irc.freenode.org'
    remote_port = 6667
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remote_host, remote_port))
    data = s.recv(1024)
    s.close()
    print('Received: ', repr(data))


if __name__ == "__main__":
    main()