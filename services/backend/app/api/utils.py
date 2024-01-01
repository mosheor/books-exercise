# app/api/utils.py
import abc
import logging
from urllib.parse import urljoin

import httpx
from flask import current_app
from httpx import HTTPError

from app import db
from app.api.models import Author, Quote, User

logger = logging.getLogger(__name__)


def get_all_users():
    return User.query.all()


def get_user_by_id(user_id):
    t = User.query.filter_by(id=user_id).first()
    return t


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user, username, email):
    user.username = username
    user.email = email
    db.session.commit()
    return user


def delete_user(user):
    db.session.delete(user)
    db.session.commit()
    return user


def add_quote(author_name, content):
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


class APIClient(abc.ABC):
    """
    Base class for API clients.
    """
    def __init__(self, base_url):
        self._base_url = base_url
        self._client = httpx.Client()
        self._max_retries = 3

    def _make_request(self, method, endpoint, params=None):
        """Helper method to make a request with retries and error handling."""
        if params is None:
            params = {}

        url = urljoin(self._base_url, endpoint)
        for attempt in range(self._max_retries):
            try:
                response = self._client.request(method, url, params=params)
                response.raise_for_status()
                return response
            except HTTPError as http_err:
                logger.error("HTTP error occurred: %s", str(http_err))
            except Exception as err:
                logger.error("An error occurred: %s", str(err))
        return None

    @abc.abstractmethod
    def get_books_by_author(self, author_name: str):
        ...


class BooksApiClient(APIClient):
    """
    Client for the New York Times Books API.
    """
    def __init__(self, base_url=None):
        super().__init__(base_url=base_url or current_app.config["BOOKS_API_BASE_URL"])

    def get_books_by_author(self, author_name: str):
        return self._make_request(
            "GET", "reviews.json", params={'author': author_name, 'api-key': current_app.config["BOOKS_API_KEY"]}
        )
