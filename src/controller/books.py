from flask import jsonify, request, make_response
from flask_restful import Resource

from model.book import Book
from model.database import db_session


class BooksController(Resource):
    def post(self):
        title = request.json.get("title")
        author = request.json.get("author")
        book = Book(title=title, author=author)

        db_session.add(book)
        db_session.commit()

        return make_response(str(book.id), 201)

    def get(self):
        title = request.args.get("title")
        result = Book.query.filter(Book.title == title).all()

        return make_response(jsonify(result), 200)


class BooksIdController(Resource):
    def get(self, book_id):
        result = Book.query.filter(Book.id == book_id).first()
        if not result:
            return make_response(f"No book found with id {book_id}", 404)
        return make_response(jsonify(result), 200)

    def delete(self, book_id):
        Book.query.filter(Book.id == book_id).delete()
        db_session.commit()
        return make_response(f"Deleted {book_id}", 200)
