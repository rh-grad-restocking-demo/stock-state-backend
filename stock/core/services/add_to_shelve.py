from stock.core.shelve import ProductAmount, Shelve

from stock.core.errors.shelve_capacity_exceeded import ShelveCapacityExceeded


class AddToShelve:

    def __call__(
        self,
        shelve: Shelve,
        amount: ProductAmount
    ) -> Shelve:
        updated_shelve_stock_amount: ProductAmount = shelve.stock_amount + amount
        if updated_shelve_stock_amount > shelve.capacity:
            raise ShelveCapacityExceeded()
        updated_shelve = Shelve(
            shelve.product, shelve.capacity, shelve.restock_threshold,
            updated_shelve_stock_amount
        )
        return updated_shelve
