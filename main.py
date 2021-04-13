#!/usr/bin/env python3.8

import datetime
import logging
import time

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


def czy_truc_dupe():
    now = datetime.datetime.now()
    if now.day % 3 != 0:
        return False
    if now.hour != 19:
        return False
    if now.minute not in (0, 1):
        return False
    return True


def main():
    while True:
        time.sleep(60)
        if czy_truc_dupe():
            notify(
                "elo, mamy dzien mod % 3 == 0, "
                "godzina 19:00. wbijamy na Mumble?"
            )


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
