import logging

from flask import jsonify, make_response, Response
from flask_restful import Resource

from database.database import db_session
from model.book import Book

logger = logging.Logger(__name__)


class BooksIdController(Resource):
    """
    Handles requests for specific book resources.
    """
    def get(self, book_id: int) -> Response:
        """
        Return book with ID of book_id, if exists.

        :param book_id: ID of book to retrieve.
        :return: Book matching ID and 200 on success, 404 if not present
        """
        book = Book.query.filter(Book.id == book_id).first()
        if book is None:
            return make_response("Book does not exist in the system", 404)

        return make_response(jsonify(book), 200)

    def delete(self, book_id: int) -> Response:
        """
        Delete the book with book_id if exists.

        :param book_id: ID of book to delete.
        :return: ID of the deleted book and 200 if successful, else 404.
        """
        book = Book.query.filter(Book.id == book_id).first()

        if book is None:
            return make_response("Book does not exist in the system", 404)

        if len(book.loans):
            return make_response("Book is on loan. This loan must be resolved before removing the book", 400)

        db_session.delete(book)
        db_session.commit()

        return make_response(str(book.id), 200)
