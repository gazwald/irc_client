#!/usr/bin/env python3
import socket
import threading
import time

# TODO: Add logging


def creat_socket(remote_host, remote_port):
    global s

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
    data_ascii = data_raw.decode('ascii')
    return data_ascii


def format_data(data):
    if 'PING' in data:
        send_data(data.replace('PING', 'PONG'))
    elif 'PRIVMSG' in data:
        split_data = data.split(' ').remove(':')
        channel = split_data[2]
        user = split_data[0].split('!')[0]
        message = split_data[3]
        print('%s - <%s>: %s' % (channel, user, message))
    else:
        print(data)


def poll():
    while True:
        format_data(recv_data(s.recv(1024)))


def main():
    creat_socket(remote_host='localhost', remote_port=6667)
    details = {'login': 'john', 'name': 'John Smith', 'nickname': 'Johnny'}


    recv = threading.Thread(target=poll)
    recv.daemon = True
    recv.start()

    msg = 'NICK %s' % (details.get('nickname'))
    send_data(msg)

    recv_data(s.recv(1024))

    msg = 'USER %s * *  : %s' % (details.get('login'), details.get('name'))
    send_data(msg)

    while True:
        value = input("Type command: ")
        if 'quit' in value:
            break
        elif 'join' in value:
            msg = 'JOIN %s' % value.split(' ')[1]
            send_data(msg)
        else:
            msg = 'PRIVMSG #coveredinlard :%s' % value
            send_data(msg)

    # msg = 'NICK %s' % (details.get('nickname'))
    # msg = 'USER %s * *  : %s' % (details.get('login'), details.get('name'))
    # msg = 'JOIN #coveredinlard'
    # msg = 'PRIVMSG #coveredinlard :Hello world!'

if __name__ == "__main__":
    main()
    s.close()