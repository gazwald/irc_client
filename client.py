#!/usr/bin/env python3
import socket
import threading
import logging
import argparse
import sys


logging.basicConfig(filename='irc_client.log',
                    format='%(asctime)s %(message)s',
                    level=logging.DEBUG)


class Client:
    def __init__(self, remote_host, remote_port=6667):
        """
        Create a socket and connect to the server.
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((remote_host, remote_port))
        except socket.error:
            self.quit("Socket error, bailing...")
        else:
            self.previous_message = ""
            self.start_polling()

    def start_polling(self):
        self.poller = threading.Thread(target=self.poll)
        self.poller.daemon = True
        self.poller.start()

    def send(self, message):
        message = bytes(message + '\r\n', 'ascii', errors='skip')

        sent_total = 0
        while sent_total < len(message):
            sent = self.s.send(message[sent_total:])
            sent_total += sent

    def format_data(self, data):
        if data != self.previous_message:
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
            self.send(data.replace('PING', 'PONG'))
        else:
            if data != self.previous_message:
                print(data)

        self.previous_message = data

    def recv(self, data):
        data_ascii = data.decode('ascii')
        return data_ascii

    def poll(self):
        while True:
            if self.poller.is_alive():
                self.format_data(self.recv(self.s.recv(1024)))
            else:
                break

    def quit(self, message):
        self.s.close()
        sys.exit(message)


def get_args():
    parser = argparse.ArgumentParser(description='Connect to an IRC server')
    parser.add_argument('--server', required=True)
    parser.add_argument('--user', required=True)

    return parser.parse_args()


def main():
    args = get_args()

    new_client = Client(remote_host=args.server)

    current_channel = None

    while True:
        value = input('> ')
        if '/' in value:
            if 'quit' in value.lower():
                msg = 'QUIT :Client quit.'
                new_client.send(msg)
                new_client.quit()
                break
            elif 'join' in value.lower():
                channel = value.split(' ')[1]
                if current_channel is None:
                    current_channel = channel

                msg = 'JOIN %s' % channel
                new_client.send(msg)
            elif 'nick' in value.lower():
                msg = 'NICK %s' % args.user
                new_client.send(msg)
                msg = 'USER %s * *  : %s' % (args.user, args.user)
                new_client.send(msg)
            elif 'switch' in value.lower():
                current_channel = value.split()[1]

            else:
                # I don't know what you wanted to do
                # Send it and hope for the best
                new_client.send(value)
        else:
            msg = 'PRIVMSG %s :%s' % (current_channel, value)
            new_client.send(msg)


if __name__ == "__main__":
    main()
