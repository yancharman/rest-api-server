import os
from flask import Flask
from flask_restful import Api

from database import Database
from errors import register_error_handlers
from models import BookModel
from routes import init_routes

app = Flask(__name__)
database = Database(app)

api = Api(app)

book_model = BookModel(database.db)
init_routes(api, book_model)
register_error_handlers(app)

if __name__ == '__main__':
    app.run(debug=True)
