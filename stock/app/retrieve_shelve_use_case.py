import logging
from dataclasses import dataclass

from stock.core.shelve import Shelve
from stock.core.errors.shelve_not_found import ShelveNotFound
from stock.core.interfaces.shelves_repository import ShelvesRepositoryInterface


@dataclass(frozen=True)
class RetrieveShelveDTO:
    product_sku: str


class RetrieveShelveUseCase:

    def __init__(
            self,
            shelves_repo: ShelvesRepositoryInterface):
        self._shelves_repo: ShelvesRepositoryInterface = shelves_repo

    def __call__(self, dto: RetrieveShelveDTO) -> Shelve:
        shelve: Shelve = self._shelves_repo.retrieve_shelve_by_product_sku(
            dto.product_sku)
        if not shelve:
            raise ShelveNotFound()
        logging.info("RetrieveShelveUseCase.__call__:Completed")
        return shelve
