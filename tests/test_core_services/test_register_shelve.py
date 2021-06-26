from stock.core.product import SKU, Category, Product
from stock.core.shelve import RestockThreshold, ProductAmount, Capacity, Shelve
from stock.core.services.register_shelve import RegisterShelve


def test_register_shelve():
    register_shelve = RegisterShelve()
    shelve: Shelve = register_shelve(
        SKU("somesku"), Category.FRESH,
        Capacity(25), RestockThreshold(10), ProductAmount(25))
    assert isinstance(shelve, Shelve)
