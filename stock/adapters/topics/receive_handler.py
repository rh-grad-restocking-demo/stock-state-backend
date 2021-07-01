from __future__ import print_function

from typing import Callable
import logging

from proton.handlers import MessagingHandler
from proton.reactor import Container


class ReceiveHandler(MessagingHandler):
    def __init__(self, host: str, address: str, message_handler: Callable[[str], None]):
        super(ReceiveHandler, self).__init__()
        self.conn_url = host
        self.address = address
        self.message_handler = message_handler
        self.desired = 0
        self.received = 0

    def on_start(self, event):
        conn = event.container.connect(self.conn_url)
        event.container.create_receiver(conn, self.address)

    def on_link_opened(self, event):
        logging.debug("ReceiveHandler.on_link_opened:Created receiver for source address '{0}'".format
                      (self.address))

    def on_message(self, event):
        message = event.message
        logging.debug(
            "ReceiveHandler.on_message:Received message '{0}'".format(message.body))
        self.message_handler(message.body)
        self.received += 1
        if self.received == self.desired:
            event.receiver.close()
            event.connection.close()
