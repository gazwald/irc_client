#!/usr/bin/env python3
import logging
import argparse
import os

from irc import client


log_name = "%s.log" % os.path.basename(__file__)
logging.basicConfig(filename=log_name,
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

    if args.user:
        new_client.set_user(args.user)

    while True:
        value = input('> ')
        if '/' in value:
            if 'quit' in value.lower():
                new_client.quit(value.split(' ')[1])
            elif 'join' in value.lower():
                new_client.set_channel(value.split(' ')[1])
            elif 'switch' in value.lower():
                new_client.switch_channel(value.split(' ')[1])
            else:
                # I don't know what you wanted to do
                # Send it and hope for the best
                new_client.send(value)
        else:
            msg = 'PRIVMSG %s :%s' % (new_client.get_channel(), value)
            new_client.send(msg)


if __name__ == "__main__":
    main()
