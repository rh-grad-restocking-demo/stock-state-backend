import logging
from stock.core.shelve import ProductAmount, Shelve


class AddToShelve:

    def __call__(
        self,
        shelve: Shelve,
        amount: ProductAmount
    ) -> Shelve:
        updated_shelve_stock_amount: ProductAmount = shelve.stock_amount + amount
        updated_shelve = Shelve(
            shelve.product, shelve.restock_threshold,
            updated_shelve_stock_amount
        )
        logging.debug("AddToShelve.__call__:Completed")
        return updated_shelve
