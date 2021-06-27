from typing import Optional
import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

from stock.adapters.repositories.postgres_db import PostgresDB
from stock.core.interfaces.shelves_repository import ShelvesRepositoryInterface
from stock.core.product import SKU, Category, Product
from stock.core.shelve import Shelve


class ShelveEntry(PostgresDB.Base):
    __tablename__ = 'shelves'
    sku = Column(String, primary_key=True, autoincrement=False)
    category = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    restock_threshold = Column(Integer, nullable=False)
    stock_amount = Column(Integer, nullable=False)

    def to_shelve(self) -> Shelve:
        return Shelve(
            Product(self.sku, self.category),
            self.capacity, self.restock_threshold,
            self.stock_amount)


class ShelvesRepository(ShelvesRepositoryInterface):

    def __init__(self, postgres_db: PostgresDB):
        self._postgres_db = postgres_db

    def save_shelve(self, shelve: Shelve):
        with self._postgres_db.session_scope() as session:
            existing_shelve_entry: ShelveEntry = session.query(
                ShelveEntry).get(shelve.product.sku)
            if existing_shelve_entry:
                existing_shelve_entry.category = str(shelve.product.category)
                existing_shelve_entry.capacity = int(shelve.capacity)
                existing_shelve_entry.restock_threshold = int(
                    shelve.restock_threshold)
                existing_shelve_entry.stock_amount = int(shelve.stock_amount)
                logging.debug(
                    "ShelvesRepository.save_shelve:Updated existing shelve")
            else:
                new_shelve_entry = ShelveEntry(
                    sku=str(shelve.product.sku),
                    category=str(shelve.product.category),
                    capacity=int(shelve.capacity),
                    restock_threshold=int(shelve.restock_threshold),
                    stock_amount=int(shelve.stock_amount)
                )
                session.add(new_shelve_entry)
                logging.debug(
                    "ShelvesRepository.save_shelve:Created new shelve")

    def retrieve_shelve_by_product_sku(
            self, product_sku: SKU) -> Optional[Shelve]:
        with self._postgres_db.session_scope() as session:
            shelve_entries = session.query(
                ShelveEntry).filter_by(sku=product_sku).all()
            if shelve_entries:
                shelve_entry: ShelveEntry = shelve_entries[0]
                logging.debug(
                    "ShelvesRepository.retrieve_shelve_by_product_sku:Found shelve")
                return shelve_entry.to_shelve()
        logging.debug(
            "ShelvesRepository.retrieve_shelve_by_product_sku:Did not find shelve")
