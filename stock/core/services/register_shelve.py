import logging
from stock.core.product import SKU, Category, Product
from stock.core.shelve import RestockThreshold, ProductAmount, Shelve


class RegisterShelve:

    def __call__(
            self,
            product_sku: SKU,
            product_category: Category,
            shelve_restock_threshold: RestockThreshold,
            shelve_stock_amount: ProductAmount
    ) -> Shelve:
        product = Product(product_sku, product_category)
        shelve = Shelve(product, shelve_restock_threshold, shelve_stock_amount)
        logging.debug("RegisterShelve.__call__:Completed")
        return shelve
