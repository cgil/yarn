import datetime

from flask import abort
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.orm import class_mapper

from yarn.lib.database import db


class Base(db.Model):

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime,
        server_default=db.func.now(),
        default=db.func.now()
    )
    deleted_at = Column(DateTime)
    updated_at = Column(
        DateTime,
        server_onupdate=db.func.now(),
        onupdate=db.func.now(),
        default=db.func.now()
    )

    def __init__(self, **kwargs):
        # Remove invalid keys.
        for k in kwargs.keys():
            if k not in self.columns():
                del kwargs[k]
        super(Base, self).__init__(**kwargs)

    def update_relationship(self, relationship, rel_id):
        """Update a relationship on the model."""
        formatted_rel_name = relationship[:-1]
        if relationship in self.relationships():
            rel_id_name = '{}_id'.format(formatted_rel_name)
            setattr(self, rel_id_name, rel_id)

    @classmethod
    def private_fields(cls):
        """Fields that should be private and never exposed."""
        return ('created_at', 'updated_at', 'deleted_at')

    @classmethod
    def relationships(cls):
        """Get all model relationships."""
        return [rel for rel in cls.__mapper__.relationships.keys()
                if rel not in cls.private_fields()]

    @classmethod
    def columns(cls):
        """Get all model columns."""
        return [prop.key for prop in class_mapper(cls).iterate_properties
                if isinstance(prop, ColumnProperty)]

    def to_dict(self):
        """Returns a dict from a record."""
        return {
            col: getattr(self, col) for col in self.columns()
            if col not in self.private_fields()
        }

    def save(self, resource):
        """Save to the database."""
        db.session.add(resource)
        return self.update()

    def update(self):
        """Updates the database records."""
        return db.session.commit()

    def delete(self, resource, soft_delete=True):
        """Delete a resource."""
        # Soft delete the resource by updating the deleted_at field.
        if soft_delete:
            resource.deleted_at = datetime.datetime.utcnow()
            return self.update()
        # Otherwise, permanently delete a resource.
        db.session.delete(resource)
        return db.session.commit()

    @classmethod
    def get_all(cls):
        """Get all records."""
        return cls.query.filter(
            cls.deleted_at.is_(None)
        ).all()

    @classmethod
    def get(cls, record_id):
        """Get a record."""
        return cls.query.filter(
            cls.id == record_id
        ).filter(
            cls.deleted_at.is_(None)
        ).first()

    @classmethod
    def get_or_404(cls, record_id):
        """Get a record or 404."""
        record = cls.query.filter(
            cls.id == record_id
        ).filter(
            cls.deleted_at.is_(None)
        ).first()
        return record or abort(404)
