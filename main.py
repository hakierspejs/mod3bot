#!/usr/bin/env python3.8

import multiprocessing
import time

import requests
import irc.client


def notify_thread(msg):
    client = irc.client.Reactor()
    server = client.server()
    server.connect('irc.freenode.net', 6667, 'hsldzat')

    def on_connect(connection, event):
        connection.join('#hakierspejs')

    def on_join(connection, event):
        connection.privmsg('#hakierspejs', msg)
        connection.quit()

    client.add_global_handler("welcome", on_connect)
    client.add_global_handler("join", on_join)
    client.process_forever()


def notify(msg):
    t = multiprocessing.Process(target=notify_thread, args=(msg, ))
    t.start()
    time.sleep(60)
    t.terminate()


def isitopen():
    return bool(
        len(
            requests.get(
                'https://at.hs-ldz.pl/api/v1/users?online=true').json()
        )
    )


def main():
    isopen = isitopen()
    while True:
        nowisopen = isitopen()
        if nowisopen and not isopen:
            notify('Spejs jest otwarty!')
        elif isopen and not nowisopen:
            notify('Spejs jest zamknięty')
        isopen = nowisopen
        time.sleep(600)


if __name__ == '__main__':
    main()
