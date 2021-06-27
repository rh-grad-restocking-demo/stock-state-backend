import logging
from dataclasses import dataclass

from stock.core.shelve import ProductAmount, Shelve
from stock.core.services.deduct_from_shelve import DeductFromShelve
from stock.core.messages.depleted import Depleted
from stock.core.interfaces.shelves_topics import ShelvesTopicsInterface
from stock.core.interfaces.shelves_repository import ShelvesRepositoryInterface
from stock.app.retrieve_shelve_use_case import RetrieveShelveDTO, RetrieveShelveUseCase


@dataclass(frozen=True)
class DepleteShelveDTO:
    product_sku: str
    amount: int


class DepleteShelveUseCase:

    def __init__(
            self,
            shelves_repo: ShelvesRepositoryInterface,
            shelves_topics: ShelvesTopicsInterface):
        self._shelves_repo: ShelvesRepositoryInterface = shelves_repo
        self._shelves_topics: ShelvesTopicsInterface = shelves_topics

    def __call__(self, dto: DepleteShelveDTO):
        retrieve_shelve = RetrieveShelveUseCase(self._shelves_repo)
        shelve: Shelve = retrieve_shelve(RetrieveShelveDTO(dto.product_sku))
        deduct_from_shelve = DeductFromShelve()
        amount_to_be_depleted = ProductAmount(dto.amount)
        updated_shelve: Shelve = deduct_from_shelve(
            shelve, amount_to_be_depleted)
        self._shelves_repo.save_shelve(updated_shelve)
        self._shelves_topics.send_depleted_message(
            Depleted.from_shelve(shelve, amount_to_be_depleted))
        logging.info("DepleteShelveUseCase.__call__:Completed")
