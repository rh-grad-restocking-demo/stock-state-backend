from typing import Optional
from abc import ABC, abstractmethod

from stock.core.product import SKU
from stock.core.shelve import Shelve


class ShelvesRepositoryInterface(ABC):

    @abstractmethod
    def save_shelve(self, shelve: Shelve):
        pass

    @abstractmethod
    def retrieve_shelve_by_product_sku(
            self, product_sku: SKU) -> Optional[Shelve]:
        pass
