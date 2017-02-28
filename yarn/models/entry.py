from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Integer

from yarn.models.base import Base


class Entry(Base):
    """An entry from a channel."""

    publisher_id = Column(Integer)
    channel_id = Column(Integer)
    title = Column(String)
    link = Column(String)
    summary = Column(String)
    content = Column(Text)
    content_type = Column(String)
    external_entry_id = Column(String)
    publication_updated_datetime = Column(DateTime)
    publication_datetime = Column(DateTime)
