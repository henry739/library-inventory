from flask import Flask, request, jsonify
from flask_restful import Api

from controller.books import BooksController, BooksIdController
from model.database import init_db, db_session
from model.book import Book
from model.registered_user import RegisteredUser
from model.loan import Loan
from datetime import datetime

API_BASE = "/api/v1"

init_db()
server = Flask(__name__)
api = Api(server)

api.add_resource(BooksController, f"{API_BASE}/books")
api.add_resource(BooksIdController, f"{API_BASE}/books/<int:book_id>")


# TODO: Validate input
# TODO: Validate against extra credit rules
# TODO: Ranked fuzzy matching for book searches
# TODO: Switch to Postgres


@server.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Books API
# @server.route(f"{API_BASE}/books", methods=["POST"])
def books_create():
    title = request.json.get("title")
    author = request.json.get("author")
    book = Book(title=title, author=author)

    db_session.add(book)
    db_session.commit()

    return f"{book.id}", 201


# @server.route(f"{API_BASE}/books", methods=["GET"])
def books_search():
    title = request.args.get("title")
    result = Book.query.filter(Book.title == title).all()
    return jsonify(result), 200


# @server.route(f"{API_BASE}/books/<int:book_id>", methods=["GET", "DELETE"])
def books_by_id(book_id):
    if request.method == "GET":
        result = Book.query.filter(Book.id == book_id).first()
        return jsonify(result), 200
    elif request.method == "DELETE":
        Book.query.filter(Book.id == book_id).delete()
        db_session.commit()
        return f"Deleted {book_id}", 200


# Users API
@server.route(f"{API_BASE}/users", methods=["POST"])
def users_post():
    full_name = request.json.get("full_name")
    registered_user = RegisteredUser(full_name=full_name)

    db_session.add(registered_user)
    db_session.commit()

    return f"{registered_user.id}", 201


# Loans API
@server.route(f"{API_BASE}/loans", methods=["POST"])
def loans_post():
    registered_user_id = request.json.get("registered_user_id")
    book_id = request.json.get("book_id")
    datetime_stamp = datetime.utcnow()

    loan = Loan(started=datetime_stamp, registered_user_id=registered_user_id, book_id=book_id)
    db_session.add(loan)
    db_session.commit()

    return f"{loan.id}", 201


@server.route(f"{API_BASE}/loans/<int:user_id>", methods=["GET"])
def loans_by_user(user_id):
    loans = Loan.query.filter(Loan.registered_user_id == user_id).all()
    return jsonify(loans), 200


@server.route(f"{API_BASE}/loans/<int:loan_id>", methods=["GET", "DELETE"])
def loans_by_id(loan_id):
    if request.method == "GET":
        result = Loan.query.filter(Loan.id == loan_id).first()
        return jsonify(result), 200
    elif request.method == "DELETE":
        Loan.query.filter(Loan.id == loan_id).delete()
        db_session.commit()

        return f"Deleted {loan_id}", 200


if __name__ == "__main__":
    server.run()
