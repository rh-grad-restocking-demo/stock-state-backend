import os
from stock.core.product import SKU
from stock.core.shelve import Shelve
import sys
import logging

import click

from stock.adapters.repositories.postgres_db import PostgresDB
from stock.adapters.repositories.shelves_repository import ShelvesRepository
from stock.adapters.topics.shelves_topics import ShelvesTopics, ShelvesTopicsDisabled
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
BROKER_HOST = os.environ.get("BROKER_HOST", "localhost")

logging.basicConfig(
    stream=sys.stdout,
    encoding='utf-8',
    level=LOGGING_DEBUG_LEVEL)

postgres_db = PostgresDB(
    DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
shelves_repository = ShelvesRepository(postgres_db)
shelves_topics = ShelvesTopics(BROKER_HOST)


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
@click.option('--shelve_restock_threshold', type=int, required=True, help='Amount of stock on the shelve triggering a restock.')
@click.option('--shelve_stock_amount', required=True, type=int, help='Current amount of stock on the shelve.')
@click.option('--disable_messaging', default=False, help='Disable sending messages.')
def register_shelve(
    product_sku: str,
    product_category: str,
    shelve_restock_threshold: int,
    shelve_stock_amount: int,
    disable_messaging: bool
):
    """Register a product shelve."""
    global shelves_repository
    global shelves_topics
    if disable_messaging:
        shelves_topics = ShelvesTopicsDisabled()
    register_shelve_use_case = ReigsterShelveUseCase(
        shelves_repository, shelves_topics)
    register_shelve_use_case(
        RegisterShelveDTO(
            product_sku, product_category.upper(),
            shelve_restock_threshold, shelve_stock_amount))


@click.command()
@click.option('--product_sku', required=True, help='Stock-Keeping Unit acting as the ID of a product.')
def retrieve_shelve(
    product_sku: str
):
    """Retrieve information on a shelve."""
    global shelves_repository
    retrieve_shelve_use_case = RetrieveShelveUseCase(shelves_repository)
    shelve: Shelve = retrieve_shelve_use_case(
        RetrieveShelveDTO(product_sku))
    print(shelve)


@click.command()
@click.option('--product_sku', required=True, help='Stock-Keeping Unit acting as the ID of a product.')
@click.option('--amount', required=True, type=int, help='Amount to be removed from shelve stock.')
@click.option('--disable_messaging', default=False, help='Disable sending messages.')
def deplete_shelve(
    product_sku: str,
    amount: int,
    disable_messaging: bool
):
    """Remove a specific amount from the shelve stock."""
    global shelves_repository
    global shelves_topics
    if disable_messaging:
        shelves_topics = ShelvesTopicsDisabled()
    deplete_shelve_use_case = DepleteShelveUseCase(
        shelves_repository, shelves_topics)
    deplete_shelve_use_case(DepleteShelveDTO(product_sku, amount))


@click.command()
@click.option('--product_sku', required=True, help='Stock-Keeping Unit acting as the ID of a product.')
@click.option('--amount', required=True, type=int, help='Amount to be added to shelve stock.')
@click.option('--disable_messaging', default=False, help='Disable sending messages.')
def restock_shelve(
    product_sku: str,
    amount: int,
    disable_messaging: bool
):
    """Add a specific amount to the shelve stock."""
    global shelves_repository
    global shelves_topics
    if disable_messaging:
        shelves_topics = ShelvesTopicsDisabled()
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
