from dataclasses import dataclass

from stock.core.product import SKU, Category


@dataclass(frozen=True)
class RestockThresholdReached:
    product_sku: SKU
    product_category: Category
