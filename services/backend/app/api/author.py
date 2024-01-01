from datetime import datetime

from flask_restx import Namespace, Resource, fields

from app.api.models import Author
from app.api.utils import BooksApiClient

authors_namespace = Namespace("authors")

author_model = authors_namespace.model(
    "Author",
    {
        "id": fields.Integer(readOnly=True),
        "name": fields.String(required=True),
        "birthday": fields.Date(),
    },
)


class AuthorsResource(Resource):
    @authors_namespace.marshal_list_with(author_model)
    def get(self):
        """List all authors that were born after 1960"""
        # I assumed that 1960 is not included
        authors = Author.query.filter(Author.birthday >= datetime(1961, 1, 1)).all()
        return authors


# Define the model for the books response
# I assumed these fields are more interesting than the others
book_model = authors_namespace.model('Book', {
    'title': fields.String(attribute='book_title'),
    'author': fields.String(attribute='book_author'),
    'summary': fields.String(),
    'publication_date': fields.Date(attribute='publication_dt'),
    'isbn13': fields.List(fields.String),
})


class BooksResource(Resource):
    @authors_namespace.marshal_list_with(book_model)
    def get(self, author_id):
        # Retrieve the author from the database
        author = Author.query.get(author_id)
        if not author:
            authors_namespace.abort(404, message=f"Author with id {author_id} not found")

        # Make a request to the New York Times Books API
        client = BooksApiClient()
        response = client.get_books_by_author(author_name=author.name)

        # Extract relevant values from the API response
        books_data = response.json().get('results', [])
        return books_data


# Add the resource to the API with the specified endpoint
authors_namespace.add_resource(AuthorsResource, '')
authors_namespace.add_resource(BooksResource, '/<int:author_id>/books')
