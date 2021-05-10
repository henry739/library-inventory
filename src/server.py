from flask import Flask
from flask_restful import Api

from api.books.books_controller import BooksController
from api.books.books_id_controller import BooksIdController
from api.loans.loans_controller import LoansController
from api.loans.loans_id_controller import LoansIdController
from api.users.users_controller import UsersController
from api.users.users_id_controller import UsersIdController
from model.database import database, setup_database

API_BASE = "/api/v1"


def create_flask_app() -> Flask:
    """
    Factory function to create a configured instance of our Flask app.
    :return: Configured flask app
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://elder_librarian:books@library-db:5432/library"
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    database.init_app(app)

    api = Api(app)

    api.add_resource(BooksController, f"{API_BASE}/books")
    api.add_resource(BooksIdController, f"{API_BASE}/books/<int:book_id>")
    api.add_resource(UsersController, f"{API_BASE}/users")
    api.add_resource(UsersIdController, f"{API_BASE}/users/<int:user_id>")
    api.add_resource(LoansController, f"{API_BASE}/loans")
    api.add_resource(LoansIdController, f"{API_BASE}/loans/<int:loan_id>")

    return app


if __name__ == "__main__":
    server = create_flask_app()
    setup_database(server)

    server.run(host="0.0.0.0")
