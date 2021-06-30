from dataclasses import dataclass
from enum import Enum


class SKU(str):
    """ Stock-Keeping Unit acting as a unique product identifier."""


class Category(Enum):
    FRESH = "FRESH"
    FROZEN = "FROZEN"
    NON_PERISHABLE = "NON-PERISHABLE"
    NON_FOOD = "NON-FOOD"

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class Product:
    sku: SKU
    category: Category
