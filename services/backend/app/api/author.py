from datetime import datetime

from flask_restx import Namespace, Resource, fields

from app.api.models import Author

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


# Add the resource to the API with the specified endpoint
authors_namespace.add_resource(AuthorsResource, '')
