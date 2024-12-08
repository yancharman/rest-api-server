import os


class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://yancharman:xoggyw-fyjxed-Nihji9@yan-cluster.kkhp6.mongodb.net/")