from __future__ import print_function
import logging
from proton.reactor import Container

from stock.core.interfaces.shelves_topics import ShelvesTopicsInterface
from stock.core.messages.restocked import Restocked
from stock.core.messages.depleted import Depleted
from stock.core.messages.restock_threshhold_reached import RestockThresholdReached
from stock.core.messages.registered_shelve import RegisteredShelve
from stock.adapters.topics.message_handler import MessageHandler


class ShelvesTopics(ShelvesTopicsInterface):

    def __init__(self, host: str):
        self._host = host

    def send_restocked_message(self, message: Restocked):
        # Container(MessageHandler(
        #     self._host, "shelveRestocksAddress", message.to_json())
        # ).run()
        logging.warning(
            "ShelvesTopics.send_restocked_message:Not implemented")

    def send_depleted_message(self, message: Depleted):
        # Container(MessageHandler(
        #     self._host, "shelveDepletionsAddress", message.to_json())
        # ).run()
        logging.warning(
            "ShelvesTopics.send_depleted_message:Not implemented")

    def send_restock_threshold_reached_message(self, message: RestockThresholdReached):
        Container(MessageHandler(
            self._host, "shelveRestockThresholdReachedAddress", message.to_json())
        ).run()

    def send_registered_shelve_message(self, message: RegisteredShelve):
        # Container(MessageHandler(
        #     self._host, "shelveRegistrationsAddress", message.to_json())
        # ).run()
        logging.warning(
            "ShelvesTopics.send_registered_shelve_message:Not implemented")


class ShelvesTopicsDisabled(ShelvesTopicsInterface):

    def send_restocked_message(self, message: Restocked):
        logging.info(
            "ShelvesTopics.send_restocked_message:Disabled")

    def send_depleted_message(self, message: Depleted):
        logging.info(
            "ShelvesTopics.send_depleted_message:Disabled")

    def send_restock_threshold_reached_message(self, message: RestockThresholdReached):
        logging.info(
            "ShelvesTopics.send_restock_threshold_reached_message:Disabled")

    def send_registered_shelve_message(self, message: RegisteredShelve):
        logging.info(
            "ShelvesTopics.send_registered_shelve_message:Disabled")
