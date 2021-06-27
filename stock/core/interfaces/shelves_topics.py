from abc import ABC, abstractmethod

from stock.core.messages.restocked import Restocked
from stock.core.messages.depleted import Depleted
from stock.core.messages.restock_threshhold_reached import RestockThresholdReached
from stock.core.messages.registered_shelve import RegisteredShelve


class ShelvesTopicsInterface(ABC):

    @abstractmethod
    def send_restocked_message(self, message: Restocked):
        pass

    @abstractmethod
    def send_depleted_message(self, message: Depleted):
        pass

    @abstractmethod
    def send_restock_threshold_reached_message(self, message: RestockThresholdReached):
        pass

    @abstractmethod
    def send_registered_shelve_message(self, message: RegisteredShelve):
        pass
