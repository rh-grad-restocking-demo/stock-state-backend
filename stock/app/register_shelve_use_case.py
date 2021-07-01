import logging
from dataclasses import dataclass

from stock.core.product import SKU, Category
from stock.core.shelve import RestockThreshold, ProductAmount, Shelve
from stock.core.services.register_shelve import RegisterShelve
from stock.core.messages.registered_shelve import RegisteredShelve
from stock.core.interfaces.shelves_topics import ShelvesTopicsInterface
from stock.core.interfaces.shelves_repository import ShelvesRepositoryInterface


@dataclass(frozen=True)
class RegisterShelveDTO:
    product_sku: str
    product_category: str
    shelve_restock_threshold: int
    shelve_stock_amount: int


class ReigsterShelveUseCase:

    def __init__(
            self,
            shelves_repo: ShelvesRepositoryInterface,
            shelves_topics: ShelvesTopicsInterface):
        self._shelves_repo: ShelvesRepositoryInterface = shelves_repo
        self._shelves_topics: ShelvesTopicsInterface = shelves_topics

    def __call__(self, dto: RegisterShelveDTO):
        register_shelve = RegisterShelve()
        shelve: Shelve = register_shelve(
            SKU(dto.product_sku),
            Category(dto.product_category),
            RestockThreshold(dto.shelve_restock_threshold),
            ProductAmount(dto.shelve_stock_amount))
        self._shelves_repo.save_shelve(shelve)
        self._shelves_topics.send_registered_shelve_message(
            RegisteredShelve.from_shelve(shelve))
        logging.info("ReigsterShelveUseCase.__call__:Completed")
