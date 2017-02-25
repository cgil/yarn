from flask import Blueprint
from flask import request
from flask_restful import Api
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from yarn.lib import loggers
from yarn.lib.database import db
from yarn.models.book import Book
from yarn.schemas.books_schema import BooksSchema
from yarn.views.base import BaseAPI
from yarn.views.base import BaseListAPI

logger = loggers.get_logger(__name__)


books_blueprint = Blueprint('books', __name__, url_prefix='/books')
api = Api(books_blueprint)


class BooksListAPI(BaseListAPI):

    model = Book
    schema_model = BooksSchema

    def post(self):
        """Create a new record."""
        logger.info({
            'msg': 'Creating a new record.',
            'view': self.__class__.__name__,
            'method': 'post',
            'schema_model': self.schema_model.__name__,
            'model': self.model.__name__,
        })
        raw_dict = request.get_json(force=True)

        try:
            self.schema.validate(raw_dict)
            attrs = raw_dict['data'].get('attributes') or {}

            record = self.model(**attrs)
            db.session.add(record)
            record.save(record)
            query = self.model.get(record.id)
            result = self.schema.dump(query).data
            return result, 201

        except ValidationError as e:
                logger.error({
                    'msg': 'Error validating new record.',
                    'view': self.__class__.__name__,
                    'method': 'post',
                    'schema_model': self.schema_model.__name__,
                    'model': self.model.__name__,
                    'raw_dict': raw_dict,
                    'error': str(e)
                })
                return {'error': e.messages}, 403

        except SQLAlchemyError as e:
                logger.error({
                    'msg': 'Error creating new record.',
                    'view': self.__class__.__name__,
                    'method': 'post',
                    'schema_model': self.schema_model.__name__,
                    'model': self.model.__name__,
                    'raw_dict': raw_dict,
                    'error': str(e)
                })
                db.session.rollback()
                return {'error': str(e)}, 403


class BooksAPI(BaseAPI):

    model = Book
    schema_model = BooksSchema

api.add_resource(BooksListAPI, '/')
api.add_resource(BooksAPI, '/<id>')
