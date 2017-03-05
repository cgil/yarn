from flask import Blueprint
from flask import request
from flask_restful import Api
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from yarn.lib import loggers
from yarn.lib.database import db
from yarn.models.channel import Channel
from yarn.models.entry import Entry
from yarn.schemas.entries_schema import EntriesSchema
from yarn.views.base import BaseAPI
from yarn.views.base import BaseListAPI

logger = loggers.get_logger(__name__)


entries_blueprint = Blueprint('entries', __name__, url_prefix='/entries')
api = Api(entries_blueprint)


class EntriesListAPI(BaseListAPI):

    model = Entry
    schema_model = EntriesSchema

    def get(self):
        """Get all records."""
        logger.info({
            'msg': 'Getting all records.',
            'view': self.__class__.__name__,
            'method': 'get',
            'schema_model': self.schema_model.__name__,
            'model': self.model.__name__,
        })
        records = db.session.query(self.model, Channel).join(
            Channel,
            self.model.channel_id == Channel.id
        ).filter(
            self.model.deleted_at.is_(None)
        ).all()
        record_entries = []
        for record in records:
            record.Entry.channel_title = record.Channel.title
            record_entries.append(record.Entry)
        results = self.schema.dump(record_entries, many=True).data
        return results

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


class EntriesAPI(BaseAPI):

    model = Entry
    schema_model = EntriesSchema

    def get(self, id):
        """Get a single record."""
        logger.info({
            'msg': 'Getting a record.',
            'view': self.__class__.__name__,
            'method': 'get',
            'schema_model': self.schema_model.__name__,
            'model': self.model.__name__,
            'record_id': id,
        })
        record = self.model.get_or_404_with_channel(id)
        record.Entry.channel_title = record.Channel.title
        result = self.schema.dump(record.Entry).data
        return result

api.add_resource(EntriesListAPI, '/')
api.add_resource(EntriesAPI, '/<id>')
