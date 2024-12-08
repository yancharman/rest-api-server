from flask import request, Response
from flask_restful import Resource
from bson.json_util import dumps
from errors import NotFoundError, ValidationError
from marshmallow import ValidationError as MarshmallowValidationError
from schemas import BookSchema

class BookListResource(Resource):
    def __init__(self, book_model):
        self.book_model = book_model
        self.book_schema = BookSchema()

    def get(self):
        author_name = request.args.get("author_name")
        if author_name:
            all_books = self.book_model.collection.find({"author_name": author_name})
        else:
            all_books = self.book_model.get_all_books()
        return Response(dumps(all_books), mimetype='application/json', status=200)

    def post(self):
        data = request.get_json()
        try:
            proper_data = self.book_schema.load(data)
        except MarshmallowValidationError as err:
            raise ValidationError("Validation error occurred", details=err.messages)
        added_response = self.book_model.create_book(proper_data)
        return Response(dumps(added_response), mimetype='application/json', status=201)

class BookResource(Resource):
    def __init__(self, book_model):
        self.book_model = book_model
        self.book_schema = BookSchema()

    def get(self, book_id):
        book = self.book_model.get_book_by_isbn(book_id)
        if not book:
            raise NotFoundError(f"Book with id {book_id} not found")
        return Response(dumps(book), mimetype='application/json', status=200)

    def put(self, book_id):
        data = request.get_json()
        try:
            proper_data = self.book_schema.load(data)
        except MarshmallowValidationError as err:
            raise ValidationError("Validation error occurred", details=err.messages)
        updated_response = self.book_model.update_book(book_id, proper_data)
        if not updated_response:
            raise NotFoundError(f"Book with id {book_id} not found")
        return Response(dumps(updated_response), mimetype='application/json', status=200)

    def delete(self, book_id):
        deleted_response = self.book_model.delete_book(book_id)
        if not deleted_response:
            raise NotFoundError(f"Book with id {book_id} not found")
        return {"message": "Book deleted", "_id": book_id}, 200