from stock.core.product import SKU, Category, Product
from stock.core.shelve import RestockThreshold, ProductAmount, Capacity, Shelve
from stock.core.errors.shelve_understocked import ShelveUnderstocked


class DeductFromShelve:

    def __call__(
        self,
        shelve: Shelve,
        amount: ProductAmount
    ) -> Shelve:
        if amount > shelve.stock_amount:
            raise ShelveUnderstocked()
        updated_shelve_stock_amount: ProductAmount = shelve.stock_amount - amount
        updated_shelve = Shelve(
            shelve.product, shelve.capacity, shelve.restock_threshold,
            updated_shelve_stock_amount
        )
        return updated_shelve
