import logging
from proton.handlers import MessagingHandler
from proton import Message


class SendHandler(MessagingHandler):
    def __init__(self, host: str, address: str, message_body: str):
        super(SendHandler, self).__init__()
        self.conn_url: str = host
        self.address: str = address
        self.message_body: str = message_body

    def on_start(self, event):
        conn = event.container.connect(self.conn_url)
        event.container.create_sender(conn, self.address)

    def on_link_opened(self, event):
        logging.debug("SendHandler.on_link_opened:Opened sender for target address '{0}'".format
                      (event.sender.target.address))

    def on_sendable(self, event):
        message = Message(self.message_body)
        event.sender.send(message)
        logging.debug(
            "SendHandler.on_sendable:Sent message '{0}'".format(message.body))
        event.sender.close()
        logging.debug(
            "SendHandler.on_sendable:Closed sender")
        event.connection.close()
        logging.debug(
            "SendHandler.on_sendable:Closed connection")
