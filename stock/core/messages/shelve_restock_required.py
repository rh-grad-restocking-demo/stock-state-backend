from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from stock.core.product import SKU, Category


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class ShelveRestockRequired:
    product_sku: SKU
    product_category: Category
