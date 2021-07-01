from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from stock.core.product import SKU
from stock.core.shelve import ProductAmount


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class PurchasedProduct:
    sku: SKU
    amount: ProductAmount
