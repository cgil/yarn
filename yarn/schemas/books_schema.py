from marshmallow_jsonapi import fields

from yarn.schemas.base import BaseSchema


class BooksSchema(BaseSchema):

    id = fields.UUID(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str()
    description = fields.Str()
    content = fields.Str()
    cover_image_url = fields.Url()

    class Meta:
        type_ = 'books'
        strict = True
