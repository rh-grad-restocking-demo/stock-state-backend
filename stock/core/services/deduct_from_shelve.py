import logging
from stock.core.product import SKU, Category, Product
from stock.core.shelve import RestockThreshold, ProductAmount, Shelve


class DeductFromShelve:

    def __call__(
        self,
        shelve: Shelve,
        amount: ProductAmount
    ) -> Shelve:
        if amount > shelve.stock_amount:
            updated_shelve_stock_amount: ProductAmount = 0
        else:
            updated_shelve_stock_amount: ProductAmount = shelve.stock_amount - amount
        updated_shelve = Shelve(
            shelve.product, shelve.restock_threshold,
            updated_shelve_stock_amount
        )
        logging.debug("DeductFromShelve.__call__:Completed")
        return updated_shelve
