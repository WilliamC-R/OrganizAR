from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.Integer(required=True)
    user_id = fields.String(required=True)
    name = fields.String(required=True)
    kind = fields.String(required=True)
    created_at = fields.DateTime(required=True)
