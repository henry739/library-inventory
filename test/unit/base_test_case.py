import json
from typing import List
from unittest import TestCase

from flask.testing import FlaskClient

from model.database import database, setup_database
from server import create_flask_app


class BaseTestCase(TestCase):
    API_BASE = "/api/v1"
    client: FlaskClient

    def setUp(self):
        """ Sets up the flask application for testing, using an in-memory sqlite database. """

        self.test_config = {
            "SQLALCHEMY_DATABASE_URI": "sqlite://",  # Use an in-memory database for easy testing.
            "TESTING": True,
            "SCHEMA_ROOT": "../../src/schema"
        }

        self.server = create_flask_app(self.test_config)
        setup_database(self.server)

        self.client = self.server.test_client()

    def tearDown(self):
        """ Drops everything in the database, to ensure clean state. """
        with self.server.app_context():
            database.drop_all()

    def post_json(self, endpoint: str, data: dict) -> (str, int):
        response = self.client.post(
            f"{self.API_BASE}{endpoint}",
            data=json.dumps(data),
            content_type="application/json"
        )

        return response.get_data(as_text=True), response.status_code

    def get_by_id(self, endpoint: str, resource_id: int) -> (dict, int):
        response = self.client.get(
            f"{self.API_BASE}{endpoint}/{resource_id}"
        )

        return json.loads(response.get_data(as_text=True)), response.status_code

    def get_with_params(self, endpoint: str, params: dict) -> (List[dict], int):
        response = self.client.get(
            f"{self.API_BASE}{endpoint}",
            query_string=params
        )

        return json.loads(response.get_data(as_text=True)), response.status_code
