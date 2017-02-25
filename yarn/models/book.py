from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text

from yarn.models.base import Base


class Book(Base):
    """A Book."""
    title = Column(String, nullable=False)
    author = Column(String)
    description = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    cover_image_url = Column(String)
