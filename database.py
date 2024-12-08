from config import Config
from flask_pymongo import MongoClient


class Database:
    def __init__(self, app=None):
        self.mongo = None
        self.db = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.from_object(Config)
        self.mongo = MongoClient(Config.MONGO_URI)
        self.db = self.mongo['api_server_db']