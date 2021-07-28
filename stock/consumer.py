import os
from stock.core.product import SKU
from stock.core.shelve import Shelve
import sys
import logging

import click

from stock.adapters.repositories.postgres_db import PostgresDB
from stock.adapters.repositories.shelves_repository import ShelvesRepository
from stock.adapters.topics.shelves_topics import ShelvesTopics, ShelvesTopicsDisabled
from stock.adapters.topics.receive_handler import ReceiveHandler
from stock.app.register_shelve_use_case import RegisterShelveDTO, ReigsterShelveUseCase
from stock.app.retrieve_shelve_use_case import RetrieveShelveDTO, RetrieveShelveUseCase
from stock.app.deplete_shelve_use_case import DepleteShelveDTO, DepleteShelveUseCase
from stock.app.restock_shelve_use_case import RestockShelveDTO, RestockShelveUseCase
from stock.core.messages.purchased_product import PurchasedProduct


LOGGING_DEBUG_LEVEL = int(os.environ.get("LOGGING_DEBUG_LEVEL", 20))
DB_HOST = os.environ.get("DB_HOST", "stock-db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USERNAME = os.environ.get("DB_USERNAME", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "toor")
DB_DATABASE = os.environ.get("DB_DATABASE", "stock")
BROKER_HOST = os.environ.get("BROKER_HOST", "supermarket-broker-amqp-0-svc")

logging.basicConfig(
    stream=sys.stdout,
    encoding='utf-8',
    level=LOGGING_DEBUG_LEVEL)

postgres_db = PostgresDB(
    DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
shelves_repository = ShelvesRepository(postgres_db)
shelves_topics = ShelvesTopics(BROKER_HOST)


def deplete_shelve(purchased_product_message: PurchasedProduct):
    """Remove a specific amount from the shelve stock."""
    global shelves_repository
    global shelves_topics
    deplete_shelve_use_case = DepleteShelveUseCase(
        shelves_repository, shelves_topics)
    deplete_shelve_use_case(DepleteShelveDTO(
        purchased_product_message.sku,
        purchased_product_message.amount))


def app():
    global shelves_topics
    shelves_topics.consume_items_purchased_messages(deplete_shelve)


if __name__ == '__main__':
    app()
