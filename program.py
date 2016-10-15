#!/usr/bin/env python3
import logging
import argparse

from irc import client

logging.basicConfig(filename='irc_client.log',
                    format='%(asctime)s %(message)s',
                    level=logging.DEBUG)


def get_args():
    parser = argparse.ArgumentParser(description='Connect to an IRC server')
    parser.add_argument('--server', required=True)
    parser.add_argument('--user', required=True)

    return parser.parse_args()


def main():
    args = get_args()

    new_client = client.Client(remote_host=args.server)

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
