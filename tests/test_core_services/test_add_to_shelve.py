import pytest

from stock.core.product import SKU, Category, Product
from stock.core.shelve import RestockThreshold, ProductAmount, Capacity, Shelve
from stock.core.services.add_to_shelve import AddToShelve
from stock.core.errors.shelve_capacity_exceeded import ShelveCapacityExceeded


EXISTING_SHELVE = Shelve(
    Product(SKU("somesku"), Category.FRESH),
    Capacity(25), RestockThreshold(10), ProductAmount(10))


def test_add_to_shelve():
    add_to_shelve = AddToShelve()
    updated_shelve: Shelve = add_to_shelve(EXISTING_SHELVE, ProductAmount(15))
    assert updated_shelve.stock_amount == ProductAmount(25)


def test_add_to_shelve_exceeding_capacity():
    add_to_shelve = AddToShelve()
    with pytest.raises(ShelveCapacityExceeded):
        add_to_shelve(
            EXISTING_SHELVE, ProductAmount(20))
