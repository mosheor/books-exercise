# app/tests/conftest.py
from datetime import datetime

import pytest

from app import create_app, db
from app.api.models import Author, Quote, User


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object("app.config.TestingConfig")
    with app.app_context():
        yield app  # testing happens here


@pytest.fixture(scope="module")
def test_database():
    db.create_all()
    yield db  # testing happens here
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="module")
def add_user():
    def _add_user(username, email, password):
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    return _add_user


def _add_quote(author_name, content):
    author = Author()
    quote = Quote()

    author.name = author_name
    quote.content = content

    # check whether the author exists
    exist_author = db.session.query(Author).filter_by(name=author.name).first()
    if exist_author is not None:  # the current author exists
        quote.author = exist_author
    else:
        quote.author = author

    db.session.add(quote)
    db.session.commit()
    return quote


@pytest.fixture(scope="module")
def add_quote():
    return _add_quote


@pytest.fixture
def add_quotes(test_database):
    for i in range(20):
        _add_quote(f"Or Moshe {i}", f"Quote #{i}")
    yield
    test_database.session.query(Quote).delete()
    test_database.session.query(Author).delete()


@pytest.fixture
def add_authors(test_database):
    db.session.add_all([
        Author(name="Or Moshe", birthday=datetime(1998, 4, 22), bornlocation='Tel Aviv', bio='A nice guyyy'),
        Author(name="Leo Messi", birthday=datetime(1987, 6, 24), bornlocation='Rosario', bio='A nice player'),
        Author(name="Author 3", birthday=datetime(1910, 8, 3), bornlocation='Earth', bio='A spooky one'),
        Author(name="Suzanne Collins", birthday=datetime(1959, 8, 3), bornlocation='Earth', bio='A nice author'),
    ])
    yield
    test_database.session.query(Author).delete()
