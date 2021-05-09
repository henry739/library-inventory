import logging

from flask import jsonify, request, make_response, Response
from flask_restful import Resource
from jsonschema import ValidationError

from database.database import db_session
from model.book import Book
from schema.schema_validator import SchemaValidator

logger = logging.Logger(__name__)


class BooksController(Resource):
    """
    Handles requests for book resources.
    """

    def __init__(self):
        self.validator = SchemaValidator("schema/book.schema.json")

    def post(self) -> Response:
        """
        Create a new book in the inventory.
        :return: Book ID and 201 on successful creation, 400 if validation fails.
        """
        # Validate
        try:
            self.validator.validate(request.json)
            if "id" in request.json:
                return make_response("New records should not contain an ID", 400)

        except ValidationError:
            logger.exception(f"Request body failed validation against JsonSchema")
            return make_response("Invalid request format", 400)

        # Persist
        book = Book(**request.json)
        db_session.add(book)
        db_session.commit()

        # Respond
        return make_response(str(book.id), 201)

    def get(self) -> Response:
        """
        Return all books in the inventory exactly matching the title GET parameter.
        :return: List of books and 200 on success
        """
        title = request.args.get("title")
        result = Book.query.filter(Book.title == title).all()

        return make_response(jsonify(result), 200)
