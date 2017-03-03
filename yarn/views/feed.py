from flask import Blueprint
from sqlalchemy.exc import IntegrityError

from yarn.lib import loggers
from yarn.lib import feed as feed_library

logger = loggers.get_logger(__name__)

feed = Blueprint('feed', __name__)


@feed.route('/feed')
def index():
    try:
        feed_library.update_channels()
        return {}, 201

    except IntegrityError as e:
            logger.error({
                'msg': 'Error processing a record.',
                'view': 'feed',
                'method': 'get',
                'error': str(e)
            })
            return {'error': e.messages}, 403
