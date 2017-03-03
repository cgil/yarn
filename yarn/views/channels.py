from flask import Blueprint
from flask import request
from flask_restful import Api
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from yarn.lib import loggers
from yarn.lib.database import db
from yarn.lib import feed
from yarn.models.channel import Channel
from yarn.schemas.channels_schema import ChannelsSchema
from yarn.views.base import BaseAPI
from yarn.views.base import BaseListAPI

logger = loggers.get_logger(__name__)


channels_blueprint = Blueprint('channels', __name__, url_prefix='/channels')
api = Api(channels_blueprint)


class ChannelsListAPI(BaseListAPI):

    model = Channel
    schema_model = ChannelsSchema

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
            channel_data = feed.fetch_channel(attrs['channel_url'])
            record = feed.get_or_create_channel(channel_data.feed, attrs['channel_url'])  # TODO: Not guaranteed to fetch.

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


class ChannelsAPI(BaseAPI):

    model = Channel
    schema_model = ChannelsSchema

api.add_resource(ChannelsListAPI, '/')
api.add_resource(ChannelsAPI, '/<id>')
