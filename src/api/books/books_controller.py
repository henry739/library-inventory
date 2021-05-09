import json
import logging

from flask import jsonify, request, make_response, Response
from flask_restful import Resource
from jsonschema import validate, ValidationError

from database.database import db_session
from model.book import Book

logger = logging.Logger(__name__)


class BooksController(Resource):
    """
    Handles requests for book resources.
    """

    def __init__(self):
        self._schema_filename = "schema/book.schema.json"
        self._schema = None

    def _get_schema(self):
        if self._schema is not None:
            return self._schema

        try:
            with open(self._schema_filename, "r") as schema_file:
                self._schema = json.load(schema_file)
                return self._schema

        except FileNotFoundError:
            logger.exception(f"Unable to load schema file at: {self._schema_filename}")
            raise

        except json.JSONDecodeError:
            logger.exception(f"Invalid JSON schema file at: {self._schema_filename}")
            raise

    def post(self) -> Response:
        """
        Create a new book in the inventory.

        :return: Book ID and 201 on successful creation, 400 if validation fails.
        """

        # Validate
        try:
            validate(instance=request.json, schema=self._get_schema())
            if "id" in request.json:
                return make_response("New Book records should not contain an ID", 400)

        except ValidationError:
            logger.exception(f"Request body failed validation against JsonSchema")
            return make_response("Invalid request format", 400)

        # Persist
        book = Book(**request.json)  # Unexpected fields are disallowed during validation.
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
