from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
import json

from stock.core.product import SKU, Category


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class ShelveRestockRequired:
    product_sku: SKU
    product_category: Category

    def to_pam_json_str(self):
        pam_object = {
            "shelve": {
                "com.myspace.retail_demo.Shelve": {
                    "category": self.product_category,
                    "sku": self.product_sku,
                    "restocked": False,
                    "amount": 0
                }
            }
        }
        return json.dumps(pam_object)