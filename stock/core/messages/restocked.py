from dataclasses import dataclass

from stock.core.product import SKU, Category
from stock.core.shelve import ProductAmount, Shelve


@dataclass(frozen=True)
class Restocked:
    product_sku: SKU
    product_category: Category
    amount_added: ProductAmount
    resulting_stock_amount: ProductAmount

    @classmethod
    def from_shelve(Cls, shelve: Shelve, amount_added: ProductAmount):
        return Cls(
            shelve.product.sku, shelve.product.category,
            amount_added, shelve.stock_amount)
