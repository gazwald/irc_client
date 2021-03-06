#!/usr/bin/env python3
import socket
import threading
import logging
import sys


class Client:
    channels = []
    current_channel = None

    def __init__(self, remote_host, remote_port=6667):
        """
        Create a socket and connect to the server.
        If connection is successful start polling thread.
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
        """
        Creates a thread to continually recieve data from socket.
        """

        self.poller = threading.Thread(target=self.poll)
        self.poller.daemon = True
        self.poller.start()

    def send(self, message):
        """
        Formats messages/commands to send to the server.
        """

        message = bytes(message + '\r\n', 'ascii', errors='skip')

        sent_total = 0
        while sent_total < len(message):
            try:
                sent = self.s.send(message[sent_total:])
                sent_total += sent
            except socket.BrokenPipeError:
                logging.debug("Socket timeout?")
                print("Disconnected")
                break

    def format_data(self, data):
        """
        Attempts to format the data into something readable.
        Otherwise it'll just dump whatever it gets.
        """
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
            logging.debug("Sending PONG...")
            self.send(data.replace('PING', 'PONG'))
        else:
            print(data)

    def recv(self, data):
        """
        Can't remember why I'm doing this.
        """

        return data.decode('utf8')

    def poll(self):
        """
        While the socket is alive attempt to recieve data
        """

        while True:
            if self.poller.is_alive():
                self.format_data(self.recv(self.s.recv(1024)))
            else:
                break

    def set_user(self, user):
        self.send('NICK %s' % user)
        self.send('USER %s * *  : %s' % (user, user))

    def set_channel(self, channel):
        if channel not in self.channels:
            msg = 'JOIN %s' % channel
            self.send(msg)
            self.channels.append(channel)

        self.current_channel = channel

    def get_channel(self):
        return self.current_channel

    def switch_channel(self, channel):
        if channel not in self.channels:
            self.set_channel(channel)
            self.channels.append(channel)
        else:
            channel = self.current_channel

        logging.debug("Current channels: %s" % self.channels)

    def quit(self, message):
        """
        Close the socket and perform any other cleanup tasks
        """

        msg = 'QUIT :Client quit (%s).' % message
        self.send(msg)
        self.s.close()
        sys.exit(message)
