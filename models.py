from datetime import datetime

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from errors import InvalidDateFormatError, DuplicationError


class BookModel:
    def __init__(self, db):
        self.db = db
        self.collection = self.db['Books']
        self.collection.create_index("isbn", unique=True)

    def get_all_books(self):
        return list(self.collection.find({}))

    def get_book_by_id(self, book_id: str):
        return self.collection.find_one({"_id": ObjectId(book_id)})

    def get_book_by_isbn(self, isbn: str):
        return self.collection.find_one({"isbn": isbn})

    def create_book(self, data:dict):
        if self.get_book_by_isbn(data["isbn"]):
            raise DuplicationError()
        try:
            data["publication_date"] = datetime.strptime(data["publication_date"], "%Y-%m-%d")
        except ValueError:
            raise InvalidDateFormatError()

        book = {
            "isbn": data["isbn"],
            "title": data["title"],
            "author_name": data["author_name"],
            "publisher_name": data["publisher_name"],
            "publication_date": data["publication_date"]
        }
        try:
            res = self.collection.insert_one(book)
            book["_id"] = res.inserted_id
            return book
        except DuplicateKeyError:
            raise ValueError("ISBN must be unique")

    def update_book(self, book_id:str, data:dict):
        try:
            data["publication_date"] = datetime.strptime(data["publication_date"], "%Y-%m-%d")
        except ValueError:
            raise InvalidDateFormatError()

        res = self.collection.update_one({"isbn": book_id}, {"$set": data})
        if res.matched_count > 0:
            return BookModel.get_book_by_isbn(self, data["isbn"])
        return None

    def delete_book(self, book_id:str):
        res = self.collection.delete_one({"isbn": book_id})
        return res.deleted_count > 0