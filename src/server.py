from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from api.auth.login_controller import LoginController
from api.books.books_controller import BooksController
from api.books.books_id_controller import BooksIdController
from api.loans.loans_controller import LoansController
from api.loans.loans_id_controller import LoansIdController
from api.users.users_controller import UsersController
from api.users.users_id_controller import UsersIdController
from model.database import database, setup_database
from model.login import Login

API_BASE = "/api/v1"


def create_flask_app(configs: dict) -> Flask:
    """
    Factory function to create a configured instance of our Flask app.

    :param configs: Dictionary of configurations to update flask configs with.
    :return: Configured flask app
    """
    app = Flask(__name__)
    app.config.update(configs)
    jwt = JWTManager(app)
    database.init_app(app)

    api = Api(app)

    api.add_resource(
        BooksController,
        f"{API_BASE}/books",
        resource_class_args=[app.config.get("SCHEMA_ROOT")],
    )
    api.add_resource(BooksIdController, f"{API_BASE}/books/<int:book_id>")
    api.add_resource(
        UsersController,
        f"{API_BASE}/users",
        resource_class_args=[app.config.get("SCHEMA_ROOT")],
    )
    api.add_resource(UsersIdController, f"{API_BASE}/users/<int:user_id>")
    api.add_resource(
        LoansController,
        f"{API_BASE}/loans",
        resource_class_args=[app.config.get("SCHEMA_ROOT")],
    )
    api.add_resource(LoansIdController, f"{API_BASE}/loans/<int:loan_id>")
    api.add_resource(LoginController, f"{API_BASE}/login")

    return app


if __name__ == "__main__":
    config = {
        "SQLALCHEMY_DATABASE_URI": "postgresql+psycopg2://elder_librarian:books@library-db:5432/library",
        "SCHEMA_ROOT": "schema",
        "JWT_SECRET_KEY": "1D5D22BA998265A2F9283E9B34EC4"
    }

    server = create_flask_app(config)
    setup_database(server)

    # Setup default users.
    with server.app_context():
        database.session.add(Login(username="senior-librarian-agatha", password="books4life", role="senior"))
        database.session.add(Login(username="librarian-barry", password="books5life", role="librarian"))
        database.session.commit()

    server.run(host="0.0.0.0")
