from dataclasses import dataclass

from stock.core.product import Product


class Capacity(int):
    """ The capacity of the shelve.
    This is the maximum amount of product the shelve can hold."""


class RestockThreshold(int):
    """ The minimum amount of product allowed on the shelve.
    The shelve should be restocked if this amount is reached."""


class ProductAmount(int):
    """ An amount of products."""


@dataclass(frozen=True)
class Shelve:
    product: Product
    capacity: Capacity
    restock_threshold: RestockThreshold
    stock_amount: ProductAmount
