from app import ma
from marshmallow import fields


class ShowUsersBasicSchema(ma.Schema):
    username = fields.String()


class UserSchema(ShowUsersBasicSchema):
    id = fields.Integer(dump_only=True)
    password_hash = fields.String()
    is_admin = fields.Boolean()


class CategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class CommentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    content = fields.String()
    date = fields.String()
    author_id = fields.Integer()
    post_id = fields.Integer()


class PostSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    content = fields.String()
    date = fields.String()
    author_id = fields.Integer()
    category_id = fields.Integer()
    comment_obj = fields.Nested(CommentSchema, exclude=("id",), many=True)