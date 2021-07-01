import logging
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from stock.core.shelve import Shelve
from stock.core.errors.shelve_not_found import ShelveNotFound
from stock.core.interfaces.shelves_repository import ShelvesRepositoryInterface


@dataclass(frozen=True)
class RetrieveShelveDTO:
    product_sku: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class RetrievedShelveDTO:
    product_sku: str
    product_category: str
    shelve_restock_threshold: int
    shelve_stock_amount: int

    @classmethod
    def from_shelve(Cls, shelve: Shelve):
        return Cls(
            shelve.product.sku, shelve.product.category,
            shelve.restock_threshold, shelve.stock_amount)


class RetrieveShelveUseCase:

    def __init__(
            self,
            shelves_repo: ShelvesRepositoryInterface):
        self._shelves_repo: ShelvesRepositoryInterface = shelves_repo

    def __call__(self, dto: RetrieveShelveDTO) -> RetrievedShelveDTO:
        shelve: Shelve = self._shelves_repo.retrieve_shelve_by_product_sku(
            dto.product_sku)
        if not shelve:
            raise ShelveNotFound()
        logging.info("RetrieveShelveUseCase.__call__:Completed")
        return RetrievedShelveDTO.from_shelve(shelve)
