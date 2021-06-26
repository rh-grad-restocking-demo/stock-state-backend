import pytest

from stock.core.product import SKU, Category, Product
from stock.core.shelve import RestockThreshold, ProductAmount, Capacity, Shelve
from stock.core.services.deduct_from_shelve import DeductFromShelve
from stock.core.errors.shelve_understocked import ShelveUnderstocked


EXISTING_SHELVE = Shelve(
    Product(SKU("somesku"), Category.FRESH),
    Capacity(25), RestockThreshold(10), ProductAmount(10))


def test_add_to_shelve():
    deduct_from_shelve = DeductFromShelve()
    updated_shelve: Shelve = deduct_from_shelve(
        EXISTING_SHELVE, ProductAmount(5))
    assert updated_shelve.stock_amount == ProductAmount(5)


def test_add_to_shelve_exceeding_capacity():
    deduct_from_shelve = DeductFromShelve()
    with pytest.raises(ShelveUnderstocked):
        deduct_from_shelve(
            EXISTING_SHELVE, ProductAmount(15))
