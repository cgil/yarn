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
    description = Column(String)
    content = Column(Text)
    content_type = Column(String)
    public_entry_id = Column(String)
    published_updated_datetime = Column(DateTime)
    published_datetime = Column(DateTime)

    @classmethod
    def get_by_public_entry_id(cls, public_entry_id):
        return cls.query.filter(
            cls.public_entry_id == public_entry_id
        ).filter(
            cls.deleted_at.is_(None)
        ).first()

    @classmethod
    def get_or_create_entry(cls, attrs):
        record = cls.get_by_public_entry_id(attrs['public_entry_id'])
        if record is None:
            record = cls(**attrs)
            record.save()
        return record

    def update_published_updated_datetime(self, updated_datetime):
        self.published_updated_datetime = updated_datetime
        self.save()
