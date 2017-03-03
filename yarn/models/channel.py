from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime

from yarn.models.base import Base


class Channel(Base):
    """A channel from a publisher."""
    publisher_id = Column(Integer)
    title = Column(String)
    link = Column(String)
    publication_updated_datetime = Column(DateTime)
    public_channel_id = Column(String)

    @classmethod
    def get_by_public_channel_id(cls, public_channel_id):
        return cls.query.filter(
            cls.public_channel_id == public_channel_id
        ).filter(
            cls.deleted_at.is_(None)
        ).first()

    @classmethod
    def get_or_create_channel(cls, attrs):
        record = cls.get_by_public_channel_id(attrs['public_channel_id'])
        if record is None:
            record = cls(**attrs)
            record.save(record)
        return record
