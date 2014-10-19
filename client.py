__author__ = 'user'

import socket
import threading


# TODO: Add logging
# TODO: Add threading


def creat_socket():
    global s

    remote_host = 'localhost'
    remote_port = 6667

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remote_host, remote_port))


def send_data(message):
    message = bytes(message + '\r\n', 'ascii', errors='skip')
    sent_total = 0
    while sent_total < len(message):
        sent = s.send(message[sent_total:])
        sent_total += sent

    return True


def recv_data(data_raw):
    print('Recieved: ')
    data_ascii = data_raw.decode('ascii')
    print(data_ascii)


def main():
    creat_socket()
    details = {'login': 'john', 'name': 'John Smith', 'nickname': 'Johnny'}

    recv_data(s.recv(1024))

    msg = 'NICK %s' % (details.get('nickname'))
    send_data(msg)

    recv_data(s.recv(1024))

    msg = 'USER %s * *  : %s' % (details.get('login'), details.get('name'))
    send_data(msg)

    recv_data(s.recv(1024))

    msg = 'JOIN #coveredinlard'
    send_data(msg)

    recv_data(s.recv(1024))

    msg = 'PRIVMSG #coveredinlard :Hello world!'
    send_data(msg)

    recv_data(s.recv(1024))

    s.close()


if __name__ == "__main__":
    main()