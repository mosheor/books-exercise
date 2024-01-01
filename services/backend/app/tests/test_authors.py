import json

from flask import current_app
from pytest_httpx import HTTPXMock

from app.api.models import Author


def test_authors(test_app, add_authors):
    # Arrange
    client = test_app.test_client()

    # Act
    resp = client.get("/authors")
    data = json.loads(resp.data)

    # Assert
    assert resp.status_code == 200
    assert data == [
        {
            'birthday': '1998-04-22',
            'id': 1,
            'name': 'Or Moshe'
        },
        {
            'birthday': '1987-06-24',
            'id': 2,
            'name': 'Leo Messi'
        },
    ]


def test_books(test_app, add_authors, httpx_mock: HTTPXMock):
    # Arrange
    client = test_app.test_client()

    httpx_mock.add_response(
        method="GET",
        url=f"https://api.nytimes.com/svc/books/v3/reviews.json?author=Suzanne%20Collins&"
            f"api-key={current_app.config['BOOKS_API_KEY']}",
        json={
            "status": "OK",
            "copyright": "Copyright (c) 2024 The New York Times Company.  All Rights Reserved.",
            "num_results": 2,
            "results": [
                {
                    "url": "http://www.nytimes.com/2010/09/12/books/review/Roiphe-t.html",
                    "publication_dt": "2010-09-12",
                    "byline": "KATIE ROIPHE",
                    "book_title": "Mockingjay",
                    "book_author": "Suzanne Collins",
                    "summary": "",
                    "uuid": "00000000-0000-0000-0000-000000000000",
                    "uri": "nyt://book/00000000-0000-0000-0000-000000000000",
                    "isbn13": [
                        "9781407109374"
                    ]
                },
                {
                    "url": "https://www.nytimes.com/2020/05/19/books/review/hunger-games-prequel-ballad-of-"
                           "songbirds-and-snakes.html",
                    "publication_dt": "2020-05-19",
                    "byline": "Sarah Lyall",
                    "book_title": "The Ballad of Songbirds and Snakes",
                    "book_author": "Suzanne Collins",
                    "summary": "A teenage Coriolanus Snow stars in Suzanne Collins’s “The Ballad of Songbirds and "
                               "Snakes,” which is every bit as violent and jarring as the first three books.",
                    "uuid": "00000000-0000-0000-0000-000000000000",
                    "uri": "nyt://book/00000000-0000-0000-0000-000000000000",
                    "isbn13": [
                        "9781338635171"
                    ]
                }
            ]
        }
    )
    author_id = Author.query.filter_by(name='Suzanne Collins').first().id

    # Act
    resp = client.get(f"/authors/{author_id}/books")
    data = json.loads(resp.data)

    # Assert
    assert resp.status_code == 200
    assert data == [
        {
            'title': 'Mockingjay',
            'author': 'Suzanne Collins',
            'summary': '',
            'publication_date': '2010-09-12',
            'isbn13': ['9781407109374']
        },
        {
            'title': 'The Ballad of Songbirds and Snakes',
            'author': 'Suzanne Collins',
            'summary': 'A teenage Coriolanus Snow stars in Suzanne Collins’s “The Ballad of Songbirds and Snakes,'
                       '” which is every bit as violent and jarring as the first three books.',
            'publication_date': '2020-05-19',
            'isbn13': ['9781338635171']
        }
    ]


def test_books_not_found(test_app, add_authors):
    # Arrange
    client = test_app.test_client()
    # Act
    resp = client.get("/authors/999999/books")
    data = json.loads(resp.data)

    # Assert
    assert resp.status_code == 404
    assert data == {'message': 'Author with id 999999 not found. You have requested this URI [/authors/999999/books]'
                               ' but did you mean /authors/<int:author_id>/books ?'}
