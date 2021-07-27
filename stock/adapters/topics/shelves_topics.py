from __future__ import print_function

import logging
from typing import Callable
import json

from proton.reactor import Container

from stock.core.interfaces.shelves_topics import ShelvesTopicsInterface
from stock.core.messages.restocked import Restocked
from stock.core.messages.depleted import Depleted
from stock.core.messages.shelve_restock_required import ShelveRestockRequired
from stock.core.messages.registered_shelve import RegisteredShelve
from stock.core.messages.purchased_product import PurchasedProduct
from stock.adapters.topics.send_handler import SendHandler
from stock.adapters.topics.receive_handler import ReceiveHandler


class ShelvesTopics(ShelvesTopicsInterface):

    def __init__(self, host: str):
        self._host = host

    def send_restocked_message(self, message: Restocked):
        # Container(SendHandler(
        #     self._host, "shelveRestocksAddress", message.to_json())
        # ).run()
        logging.warning(
            "ShelvesTopics.send_restocked_message:Not implemented")

    def send_depleted_message(self, message: Depleted):
        # Container(SendHandler(
        #     self._host, "shelveDepletionsAddress", message.to_json())
        # ).run()
        logging.warning(
            "ShelvesTopics.send_depleted_message:Not implemented")

    def send_shelve_restock_required_message(self, message: ShelveRestockRequired):
        Container(SendHandler(
            self._host, "shelveRestockRequiredAddress", message.to_json())
        ).run()

    def send_registered_shelve_message(self, message: RegisteredShelve):
        # Container(SendHandler(
        #     self._host, "shelveRegistrationsAddress", message.to_json())
        # ).run()
        logging.warning(
            "ShelvesTopics.send_registered_shelve_message:Not implemented")

    def consume_items_purchased_messages(self, message_handler: Callable[[PurchasedProduct], None]):
        logging.info(
            "ShelvesTopics.consume_items_purchased_messages:Will start listening for items purchased messages")

        def callable(message_json: str):
            message = json.loads(message_json)
            purchase_product = PurchasedProduct(
                message["sku"], message["amount"])
            message_handler(purchase_product)

        Container(ReceiveHandler(
            self._host, "itemsPurchasedAddress", callable)
        ).run()


class ShelvesTopicsDisabled(ShelvesTopicsInterface):

    def send_restocked_message(self, message: Restocked):
        logging.info(
            "ShelvesTopics.send_restocked_message:Disabled")

    def send_depleted_message(self, message: Depleted):
        logging.info(
            "ShelvesTopics.send_depleted_message:Disabled")

    def send_shelve_restock_required_message(self, message: ShelveRestockRequired):
        logging.info(
            "ShelvesTopics.send_shelve_restock_required_message:Disabled")

    def send_registered_shelve_message(self, message: RegisteredShelve):
        logging.info(
            "ShelvesTopics.send_registered_shelve_message:Disabled")
