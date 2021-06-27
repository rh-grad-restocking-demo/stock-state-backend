from dataclasses import dataclass

from stock.core.shelve import ProductAmount, Shelve
from stock.core.services.add_to_shelve import AddToShelve
from stock.core.messages.restocked import Restocked
from stock.core.interfaces.shelves_topics import ShelvesTopicsInterface
from stock.core.interfaces.shelves_repository import ShelvesRepositoryInterface
from stock.app.retrieve_shelve_use_case import RetrieveShelveDTO, RetrieveShelveUseCase


@dataclass(frozen=True)
class RestockShelveDTO:
    product_sku: str
    amount: int


class RestockShelveUseCase:

    def __init__(
            self,
            shelves_repo: ShelvesRepositoryInterface,
            shelves_topics: ShelvesTopicsInterface):
        self._shelves_repo: ShelvesRepositoryInterface = shelves_repo
        self._shelves_topics: ShelvesTopicsInterface = shelves_topics

    def __call__(self, dto: RestockShelveDTO):
        retrieve_shelve = RetrieveShelveUseCase(self._shelves_repo)
        shelve: Shelve = retrieve_shelve(RetrieveShelveDTO(dto.product_sku))
        add_to_shelve = AddToShelve()
        amount_to_be_added = ProductAmount(dto.amount)
        updated_shelve: Shelve = add_to_shelve(
            shelve, amount_to_be_added)
        self._shelves_repo.save_shelve(updated_shelve)
        self._shelves_topics.send_restocked_message(
            Restocked.from_shelve(shelve, amount_to_be_added))
