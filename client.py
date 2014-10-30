#!/usr/bin/env python3
import socket
import threading
import logging
import argparse


logging.basicConfig(filename='irc_client.log',level=logging.DEBUG)


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
    logging.debug(data)

    if 'PRIVMSG' in data:
        split_data = data.split(' ')
        channel = split_data[2]
        user = split_data[0].split('!')[0]
        user = user.strip(':')
        message = split_data[3]
        message = message.strip(':')
        print('%s - <%s>: %s' % (channel, user, message))
    elif 'PING' in data:
        send_data(data.replace('PING', 'PONG'))
    else:
        print(data)


def poll():
    while True:
        format_data(recv_data(s.recv(1024)))


def get_args():
    parser = argparse.ArgumentParser(description='Connect to an IRC server')
    parser.add_argument('--server', required=True)

    return parser.parse_args()


def main():
    args = get_args()

    creat_socket(remote_host=args.server, remote_port=6667)

    recv = threading.Thread(target=poll)
    recv.daemon = True
    recv.start()

    current_channel = None

    while True:
        value = input('> ')
        if '/' in value:
            if 'quit' in value.lower():
                msg = 'QUIT :Client quit.'
                send_data(msg)
                break
            elif 'join' in value.lower():
                channel = value.split(' ')[1]
                if current_channel is None:
                    current_channel = channel

                msg = 'JOIN %s' % channel
                send_data(msg)
            elif 'nick' in value.lower():
                user = value.split(' ')[1]
                msg = 'NICK %s' % user
                send_data(msg)
                msg = 'USER %s * *  : %s' % (user, user)
                send_data(msg)
            elif 'switch' in value.lower():
                current_channel = value.split()[1]

            else:
                # I don't know what you wanted to do
                # Send it and hope for the best
                send_data(value)
        else:
            msg = 'PRIVMSG %s :%s' % (current_channel, value)
            send_data(msg)


if __name__ == "__main__":
    main()
    s.close()