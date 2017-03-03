from marshmallow_jsonapi import fields

from yarn.schemas.base import BaseSchema


class EntriesSchema(BaseSchema):

    id = fields.UUID(dump_only=True)
    publisher_id = fields.Integer()
    channel_id = fields.Integer()
    title = fields.Str()
    link = fields.Url()
    description = fields.Str()
    content = fields.Str()
    content_type = fields.Str()
    public_entry_id = fields.Str()
    published_updated_datetime = fields.DateTime()
    published_datetime = fields.DateTime()


    class Meta:
        type_ = 'entries'
        strict = True
