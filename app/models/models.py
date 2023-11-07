# Create table "CATEGORY"
# I M P O R T S  -  N A T I V E  -  P Y T H O N.
from datetime import datetime

# I M P O R T S  -  F L A S K.
from sqlalchemy import ForeignKey

# O W N  -  I M P O R T S.
from app import app, database as db


# Create table "User"
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.name


# Create table "Category"
class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return self.name


# Create table "Post"
class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), nullable=False
    )

    comment_obj = db.relationship("Comment")

    def __str__(self):
        return self.title


# Create table "Comment"
class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text, nullable=False)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    def __str__(self):
        return self.content
