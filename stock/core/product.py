from dataclasses import dataclass
from enum import Enum


class SKU(str):
    """ Stock-Keeping Unit acting as a unique product identifier."""


class Category(Enum):
    FRESH = "fresh"
    FROZEN = "frozen"
    NON_PERISHABLE = "non-perishable"
    NON_FOOD = "non-food"


@dataclass(frozen=True)
class Product:
    sku: SKU
    category: Category
