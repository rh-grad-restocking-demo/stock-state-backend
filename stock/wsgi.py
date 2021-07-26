import os
from stock.core.product import SKU
from stock.core.shelve import Shelve
import sys
import logging

from flask import Flask
from flask import request, jsonify
from flask_cors import CORS

from stock.adapters.repositories.postgres_db import PostgresDB
from stock.adapters.repositories.shelves_repository import ShelvesRepository
from stock.adapters.topics.shelves_topics import ShelvesTopics, ShelvesTopicsDisabled
from stock.app.register_shelve_use_case import RegisterShelveDTO, ReigsterShelveUseCase
from stock.app.retrieve_shelve_use_case import RetrieveShelveDTO, RetrieveShelveUseCase
from stock.app.deplete_shelve_use_case import DepleteShelveDTO, DepleteShelveUseCase
from stock.app.restock_shelve_use_case import RestockShelveDTO, RestockShelveUseCase
from stock.core.errors.shelve_not_found import ShelveNotFound
from stock.core.errors.shelve_understocked import ShelveUnderstocked


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


app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "stock-state-backend-web"


@app.route("/api/shelve/<sku>", methods=["GET"])
def get_retrieve_shelve(sku: str):
    """Retrieve information on a shelve."""
    global shelves_repository
    retrieve_shelve_use_case = RetrieveShelveUseCase(shelves_repository)
    shelve: Shelve = retrieve_shelve_use_case(
        RetrieveShelveDTO(sku))
    return shelve.to_json(), 200


@app.route("/api/shelve-restock", methods=["POST"])
def post_shelve_restock():
    """Add a specific amount to the shelve stock."""
    global shelves_repository
    global shelves_topics
    data = request.json
    restock_shelve_use_case = RestockShelveUseCase(
        shelves_repository, shelves_topics)
    restock_shelve_use_case(RestockShelveDTO(data["sku"], data["amount"]))
    return 'Shelve was restocked', 200


@app.route("/api/shelve-deplete", methods=["POST"])
def post_shelve_deplete():
    """Remove a specific amount from the shelve stock."""
    global shelves_repository
    global shelves_topics
    data = request.json
    deplete_shelve_use_case = DepleteShelveUseCase(
        shelves_repository, shelves_topics)
    deplete_shelve_use_case(DepleteShelveDTO(data["sku"], data["amount"]))
    return 'Shelve was depleted', 200


@app.errorhandler(ShelveNotFound)
def handle_shelve_not_found(error):
    return 'Shelve not found', 404


@app.errorhandler(ShelveUnderstocked)
def handle_shelve_understocked(error):
    return 'Shelve is understocked', 409
