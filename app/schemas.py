from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    email = fields.Str()
    created_at = fields.DateTime()


class PostSchema(Schema):
    id = fields.Integer()
    title = fields.Str()
    content = fields.Str()
    user = fields.Nested(UserSchema)


class LikeSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    post_id = fields.Integer()
