from sqlalchemy import Column
from sqlalchemy import String

from yarn.models.base import Base


class Publisher(Base):
    """A publisher of content."""
    name = Column(String, nullable=False)
