from unittest import TestCase

from flask.testing import FlaskClient

from model.database import database, setup_database
from server import create_flask_app


class BaseTestCase(TestCase):
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
