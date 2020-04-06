# app/tests/test_config.py


import os


def test_development_config(test_app):
    test_app.config.from_object("app.config.DevelopmentConfig")
    assert test_app.config["SECRET_KEY"] == "change_this_to_some_random_key"
    assert not test_app.config["TESTING"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get("DATABASE_URL")
    assert test_app.config["BCRYPT_LOG_ROUNDS"] == 4
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 900
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 2592000


def test_testing_config(test_app):
    test_app.config.from_object("app.config.TestingConfig")
    assert test_app.config["SECRET_KEY"] == "change_this_to_some_random_key"
    assert test_app.config["TESTING"]
    assert not test_app.config["PRESERVE_CONTEXT_ON_EXCEPTION"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get(
        "DATABASE_TEST_URL"
    )
    assert test_app.config["BCRYPT_LOG_ROUNDS"] == 4
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 3
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 3


def test_production_config(test_app):
    test_app.config.from_object("app.config.ProductionConfig")
    assert test_app.config["SECRET_KEY"] == "change_this_to_some_random_key"
    assert not test_app.config["TESTING"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get("DATABASE_URL")
    assert test_app.config["BCRYPT_LOG_ROUNDS"] == 13
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 900
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 2592000