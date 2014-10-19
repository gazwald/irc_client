__author__ = 'user'

import socket

# TODO: Add logging


def send_data(message):
    message = bytes(message + '\r\n', 'ascii', errors='skip')
    sent_total = 0
    while sent_total < len(message):
        sent = s.send(message[sent_total:])
        sent_total += sent

    return True


def main():
    # remote_host = 'irc.freenode.org'
    remote_host = 'localhost'
    remote_port = 6667
    details = {'login': 'john', 'name': 'John Smith', 'nickname': 'Johnny'}

    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remote_host, remote_port))

    data = s.recv(1024)
    print("Recieved: ", repr(data))

    msg = 'NICK %s' % (details.get('nickname'))
    send_data(msg)

    data = s.recv(1024)
    print("Recieved: ", repr(data))

    msg = 'USER %s * *  : %s' % (details.get('login'), details.get('name'))
    send_data(msg)

    data = s.recv(1024)
    print("Recieved: ", repr(data))

    msg = 'JOIN #coveredinlard'
    send_data(msg)

    data = s.recv(1024)
    print("Recieved: ", repr(data))

    msg = 'PRIVMSG #coveredinlard :Hello world!'
    send_data(msg)

    data = s.recv(1024)
    print("Recieved: ", repr(data))

    s.close()


if __name__ == "__main__":
    main()