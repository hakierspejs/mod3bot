#!/usr/bin/env python3.8

import logging
import time

import requests
import irc.client


def notify(msg):
    client = irc.client.Reactor()
    server = client.server()
    server.connect("irc.freenode.net", 6667, "hsldzat")

    def on_connect(connection, event):
        connection.join("#hakierspejs")

    def on_join(connection, event):
        connection.privmsg("#hakierspejs", msg)
        connection.quit()
        raise RuntimeError()

    client.add_global_handler("welcome", on_connect)
    client.add_global_handler("join", on_join)
    try:
        client.process_forever()
    except RuntimeError:
        pass


def isitopen():
    return bool(
        len(
            requests.get(
                "https://at.hs-ldz.pl/api/v1/users?online=true"
            ).json()
        )
    )


def main():
    isopen = isitopen()
    while True:
        time.sleep(600)
        nowisopen = isitopen()
        if nowisopen and not isopen:
            notify("Spejs jest otwarty! Więcej info: https://at.hs-ldz.pl")
        elif isopen and not nowisopen:
            notify("Spejs jest zamknięty! Więcej info: https://at.hs-ldz.pl")
        isopen = nowisopen


if __name__ == "__main__":
    logging.basicConfig(level='INFO')
    main()
