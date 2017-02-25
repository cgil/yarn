import logging

import factory
from sqlalchemy.exc import InvalidRequestError

from yarn.lib.database import db
from yarn.models.book import Book

logging.getLogger('factory').setLevel(logging.ERROR)


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):

    """Base Factory."""

    class Meta:
        abstract = True
        sqlalchemy_session = db.session

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        """Returns a dictionary of a built object."""
        for k in kwargs.keys():
            if k in model_class.relationships():
                rel_key = '{}_id'.format(k)
                try:
                    kwargs[rel_key] = str(kwargs[k].id)
                except AttributeError:
                    pass
        obj = super(BaseFactory, cls)._build(model_class, *args, **kwargs)
        obj_dict = obj.to_dict()
        try:
            db.session.expunge(obj)
        except InvalidRequestError:
            pass
        return obj_dict

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Overrides create strategy, commits on create"""
        for k in kwargs.keys():
            if k in model_class.relationships():
                rel_key = '{}_id'.format(k)
                kwargs[rel_key] = str(kwargs[k].id)
        obj = super(BaseFactory, cls)._create(model_class, *args, **kwargs)
        obj.save(obj)
        return obj


class BookFactory(BaseFactory):

    class Meta:
        model = Book

    title = factory.Sequence(lambda n: 'Book Title {0}'.format(n))
    author = factory.Sequence(lambda n: 'Firstname Lastname {0}'.format(n))
    description = factory.Sequence(lambda n: 'Description {0}'.format(n))
    content = factory.Sequence(lambda n: 'Content {0}'.format(n))
    cover_image_url = factory.Sequence(
        lambda n: 'https://www.desktop.com/test_{0}.jpg'.format(n)
    )
