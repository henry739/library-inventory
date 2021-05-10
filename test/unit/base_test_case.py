import json
from typing import List, Union
from unittest import TestCase

from flask.testing import FlaskClient

from model.database import database, setup_database
from model.login import Login
from server import create_flask_app


class BaseTestCase(TestCase):
    API_BASE = "/api/v1"
    client: FlaskClient

    def setUp(self):
        """ Sets up the flask application for testing, using an in-memory sqlite database. """

        self.test_config = {
            "SQLALCHEMY_DATABASE_URI": "sqlite://",  # Use an in-memory database for easy testing.
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,  # Use an in-memory database for easy testing.
            "TESTING": True,
            "JWT_SECRET_KEY": "TEST",
            "SCHEMA_ROOT": "../../src/schema"
        }

        self.server = create_flask_app(self.test_config)
        setup_database(self.server)
        self.database = database

        with self.server.app_context():
            self.database.session.add(Login(username="senior-librarian-agatha", password="books4life"))
            self.database.session.add(Login(username="librarian-barry", password="books5life"))
            self.database.session.commit()

        self.client = self.server.test_client()
        self.headers = {}

    def tearDown(self):
        """ Drops everything in the database, to ensure clean state. """
        with self.server.app_context():
            database.drop_all()

    def login(self, username, password):
        response, status = self.post_json("/login", {"username": username, "password": password})
        if status == 200:
            token = json.loads(response)
            self.headers["Authorization"] = f"Bearer {token.get('access_token')}"

    def post_json(self, endpoint: str, data: dict) -> (str, int):
        response = self.client.post(
            f"{self.API_BASE}{endpoint}",
            data=json.dumps(data),
            content_type="application/json",
            headers=self.headers
        )

        return response.get_data(as_text=True), response.status_code

    def get_by_id(self, endpoint: str, resource_id: int) -> (dict, int):
        response = self.client.get(
            f"{self.API_BASE}{endpoint}/{resource_id}",
            headers=self.headers
        )

        if response.status_code == 200:
            return json.loads(response.get_data(as_text=True)), response.status_code

        return response.get_data(as_text=True), response.status_code

    def delete_by_id(self, endpoint: str, resource_id: Union[int, str]) -> (str, int):
        response = self.client.delete(
            f"{self.API_BASE}{endpoint}/{resource_id}",
            headers=self.headers
        )

        return response.get_data(as_text=True), response.status_code

    def get_with_params(self, endpoint: str, params: dict) -> (List[dict], int):
        response = self.client.get(
            f"{self.API_BASE}{endpoint}",
            query_string=params,
            headers=self.headers
        )

        return json.loads(response.get_data(as_text=True)), response.status_code

