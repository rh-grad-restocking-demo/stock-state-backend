from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from stock.core.product import SKU, Category
from stock.core.shelve import RestockThreshold, ProductAmount, Capacity, Shelve


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class RegisteredShelve:
    product_sku: SKU
    product_category: Category
    shelve_capacity: Capacity
    shelve_restock_threshold: RestockThreshold
    shelve_stock_amount: ProductAmount

    @classmethod
    def from_shelve(Cls, shelve: Shelve):
        return Cls(
            shelve.product.sku, shelve.product.category,
            shelve.capacity, shelve.restock_threshold,
            shelve.stock_amount)
