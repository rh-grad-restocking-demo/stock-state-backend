import os
from stock.core.product import SKU
from stock.core.shelve import Shelve
import sys
import logging

import click

from stock.adapters.repositories.postgres_db import PostgresDB
from stock.adapters.repositories.shelves_repository import ShelvesRepository
from stock.adapters.topics.shelves_topics import ShelvesTopics
from stock.app.register_shelve_use_case import RegisterShelveDTO, ReigsterShelveUseCase
from stock.app.retrieve_shelve_use_case import RetrieveShelveDTO, RetrieveShelveUseCase
from stock.app.deplete_shelve_use_case import DepleteShelveDTO, DepleteShelveUseCase
from stock.app.restock_shelve_use_case import RestockShelveDTO, RestockShelveUseCase


LOGGING_DEBUG_LEVEL = int(os.environ.get("LOGGING_DEBUG_LEVEL", 20))
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USERNAME = os.environ.get("DB_USERNAME", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "toor")
DB_DATABASE = os.environ.get("DB_DATABASE", "stock-state")

logging.basicConfig(
    stream=sys.stdout,
    encoding='utf-8',
    level=LOGGING_DEBUG_LEVEL)

postgres_db = PostgresDB(
    DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
shelves_repository = ShelvesRepository(postgres_db)
shelves_topics = ShelvesTopics()


@click.group()
def commands():
    pass


@click.command()
def setup_db():
    """Create required database tables (WARNING: will delete existing tables)."""
    postgres_db.setup_database_tables()


@click.command()
@click.option('--product_sku', required=True, help='Stock-Keeping Unit acting as the ID of a product.')
@click.option('--product_category', required=True, help='Product category: fresh, frozen, non-perishable, or non-food.')
@click.option('--shelve_capacity', required=True, type=int, help='Amount of products that can be on the shelve.')
@click.option('--shelve_restock_threshold', type=int, required=True, help='Amount of stock on the shelve triggering a restock.')
@click.option('--shelve_stock_amount', required=True, type=int, help='Current amount of stock on the shelve.')
def register_shelve(
    product_sku: str,
    product_category: str,
    shelve_capacity: int,
    shelve_restock_threshold: int,
    shelve_stock_amount: int
):
    """Register a product shelve."""
    register_shelve_use_case = ReigsterShelveUseCase(
        shelves_repository, shelves_topics)
    register_shelve_use_case(
        RegisterShelveDTO(
            product_sku, product_category.upper(), shelve_capacity,
            shelve_restock_threshold, shelve_stock_amount))


@click.command()
@click.option('--product_sku', required=True, help='Stock-Keeping Unit acting as the ID of a product.')
def retrieve_shelve(
    product_sku: str
):
    """Retrieve information on a shelve."""
    retrieve_shelve_use_case = RetrieveShelveUseCase(shelves_repository)
    shelve: Shelve = retrieve_shelve_use_case(
        RetrieveShelveDTO(product_sku))
    print(shelve)


@click.command()
@click.option('--product_sku', required=True, help='Stock-Keeping Unit acting as the ID of a product.')
@click.option('--amount', required=True, type=int, help='Amount to be removed from shelve stock.')
def deplete_shelve(
    product_sku: str,
    amount: int
):
    """Remove a specific amount from the shelve stock."""
    deplete_shelve_use_case = DepleteShelveUseCase(
        shelves_repository, shelves_topics)
    deplete_shelve_use_case(DepleteShelveDTO(product_sku, amount))


@click.command()
@click.option('--product_sku', required=True, help='Stock-Keeping Unit acting as the ID of a product.')
@click.option('--amount', required=True, type=int, help='Amount to be added to shelve stock.')
def restock_shelve(
    product_sku: str,
    amount: int
):
    """Add a specific amount to the shelve stock."""
    restock_shelve_use_case = RestockShelveUseCase(
        shelves_repository, shelves_topics)
    restock_shelve_use_case(RestockShelveDTO(product_sku, amount))


commands.add_command(setup_db)
commands.add_command(register_shelve)
commands.add_command(retrieve_shelve)
commands.add_command(deplete_shelve)
commands.add_command(restock_shelve)


if __name__ == '__main__':
    commands()
