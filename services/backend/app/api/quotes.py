# app/api/quotes.py
# APIs for quotes

from flask import request
from flask_restx import Namespace, Resource, fields, inputs
from sqlalchemy import func

from app.api.models import Quote
from app.api.utils import add_quote

quotes_namespace = Namespace("quotes")

# this model does not have to match the database
# doing this add description to Swagger Doc
quote = quotes_namespace.model(
    "Quote",
    {
        "id": fields.Integer(readOnly=True),
        "content": fields.String(required=True),
        "author_name": fields.String(required=True),
    },
)

random_quotes_parser = quotes_namespace.parser()
random_quotes_parser.add_argument(
    'limit', type=inputs.int_range(1, 10), default=3,
    help='Limit of the amount of quotes returned. Should be between 1 and 10.'
)


class Quotes(Resource):
    @quotes_namespace.marshal_with(quote)
    def get(self):
        """Returns all quotes with author info"""
        quotes = Quote.query.all()
        quotes_list = []
        for q in quotes:
            # to_dict() is a helper function in Quote class in models.py
            quotes_list.append(q.to_dict())
        return quotes_list, 200

    @quotes_namespace.expect(quote, validate=True)
    @quotes_namespace.response(201, "quote was added!")
    @quotes_namespace.response(400, "Sorry, this quote already exists.")
    def post(self):
        """add a new quote"""
        post_data = request.get_json()
        content = post_data.get("content")
        author_name = post_data.get("author_name")
        response_object = {}

        quote = Quote.query.filter_by(content=content).first()
        if quote:
            response_object["message"] = "Sorry, this quote already exists."
            return response_object, 400

        add_quote(author_name, content)
        response_object["message"] = f"quote was added!"
        return response_object, 201


# we dont use marshal with - no information
class RandomQuotes(Resource):

    @quotes_namespace.expect(random_quotes_parser, validate=True)
    @quotes_namespace.marshal_list_with(quote)
    def get(self):
        """
        Returns random quotes with author info
        If limit is not provided, it will return 3 quotes
        """
        args = random_quotes_parser.parse_args()
        limit = args['limit']

        # A more efficient way to do it - no need to fetch all data into memory
        quotes = Quote.query.order_by(func.random()).limit(limit)
        return [q.to_dict() for q in quotes], 200


quotes_namespace.add_resource(Quotes, "")
quotes_namespace.add_resource(RandomQuotes, "/random")
