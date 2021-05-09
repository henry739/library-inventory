from flask import Flask, make_response
from flask_restful import Api, Resource

from api.books.books_controller import BooksController
from api.books.books_id_controller import BooksIdController
from api.loans.loans_controller import LoansController
from api.loans.loans_id_controller import LoansIdController
from api.users.users_controller import UsersController
from api.users.users_id_controller import UsersIdController
from database.database import init_database

API_BASE = "/api/v1"


class TestResource(Resource):
    def get(self):
        return make_response("Hello World!", 200)


if __name__ == "__main__":
    init_database()
    server = Flask(__name__)
    api = Api(server)

    api.add_resource(TestResource, "/")

    api.add_resource(BooksController, f"{API_BASE}/books")
    api.add_resource(BooksIdController, f"{API_BASE}/books/<int:book_id>")

    api.add_resource(UsersController, f"{API_BASE}/users")
    api.add_resource(UsersIdController, f"{API_BASE}/users/<int:user_id>")

    api.add_resource(LoansController, f"{API_BASE}/loans")
    api.add_resource(LoansIdController, f"{API_BASE}/loans/<int:loan_id>")

    server.run(host="0.0.0.0")
