# app/config.py


import os


class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "change_this_to_some_random_key"
    BCRYPT_LOG_ROUNDS = 13
    ACCESS_TOKEN_EXPIRATION = 900  # 15 minutes
    REFRESH_TOKEN_EXPIRATION = 2592000  # 30 days
    BOOKS_API_KEY = os.environ.get("BOOKS_API_KEY")
    BOOKS_API_BASE_URL = os.environ.get("BOOKS_API_BASE_URL", "https://api.nytimes.com/svc/books/v3/")



class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    BCRYPT_LOG_ROUNDS = 4
    ACCESS_TOKEN_EXPIRATION = 3
    REFRESH_TOKEN_EXPIRATION = 3
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
