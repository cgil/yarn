from marshmallow_jsonapi import fields

from yarn.schemas.base import BaseSchema


class ChannelsSchema(BaseSchema):

    id = fields.UUID(dump_only=True)
    publisher_id = fields.Integer()
    title = fields.Str()
    link = fields.Url()
    publication_updated_datetime = fields.DateTime()
    public_channel_id = fields.Str()

    class Meta:
        type_ = 'channels'
        strict = True
