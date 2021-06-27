import logging

from stock.core.interfaces.shelves_topics import ShelvesTopicsInterface
from stock.core.messages.restocked import Restocked
from stock.core.messages.depleted import Depleted
from stock.core.messages.restock_threshhold_reached import RestockThresholdReached
from stock.core.messages.registered_shelve import RegisteredShelve


class ShelvesTopics(ShelvesTopicsInterface):

    def send_restocked_message(self, message: Restocked):
        logging.warning(
            "ShelvesTopics.send_restocked_message:Not implemented")

    def send_depleted_message(self, message: Depleted):
        logging.warning(
            "ShelvesTopics.send_depleted_message:Not implemented")

    def send_restock_threshold_reached_message(self, message: RestockThresholdReached):
        logging.warning(
            "ShelvesTopics.send_restock_threshold_reached_message:Not implemented")

    def send_registered_shelve_message(self, message: RegisteredShelve):
        logging.warning(
            "ShelvesTopics.send_registered_shelve_message:Not implemented")
