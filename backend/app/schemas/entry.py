from marshmallow import Schema, fields


class EntrySchema(Schema):
    id = fields.Integer(required=True)
    user_id = fields.String(required=True)
    category_id = fields.Integer(required=True)
    kind = fields.String(required=True)
    amount = fields.Decimal(as_string=True, required=True)
    description = fields.String(allow_none=True)
    date = fields.Date(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
