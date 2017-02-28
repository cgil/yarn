from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime

from yarn.models.base import Base


class Channel(Base):
    """A channel from a publisher."""
    publisher_id = Column(Integer)  # Internal publisher id.
    title = Column(String)
    description = Column(String)
    link = Column(String)
    publication_datetime = Column(DateTime)
    external_publication_id = Column(String)
