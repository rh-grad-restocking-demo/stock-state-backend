from dataclasses import dataclass

from stock.core.product import Product


class RestockThreshold(int):
    """ The minimum amount of product allowed on the shelve.
    The shelve should be restocked if this amount is reached."""


class ProductAmount(int):
    """ An amount of products."""


@dataclass(frozen=True)
class Shelve:
    product: Product
    restock_threshold: RestockThreshold
    stock_amount: ProductAmount

    def is_restock_threshold_reached(self) -> bool:
        return bool(self.stock_amount <= self.restock_threshold)
