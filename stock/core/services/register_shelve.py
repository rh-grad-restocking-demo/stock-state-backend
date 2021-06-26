from stock.core.product import SKU, Category, Product
from stock.core.shelve import RestockThreshold, ProductAmount, Capacity, Shelve


class RegisterShelve:

    def __call__(
            self,
            product_sku: SKU,
            product_category: Category,
            shelve_capacity: Capacity,
            shelve_restock_threshold: RestockThreshold,
            shelve_stock_amount: ProductAmount
    ) -> Shelve:
        product = Product(product_sku, product_category)
        shelve = Shelve(product, shelve_capacity,
                        shelve_restock_threshold, shelve_stock_amount)
        return shelve
