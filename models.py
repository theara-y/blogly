"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


def connect_db(app):
    db.init_app(app)
    db.create_all()


class User(db.Model):
    """ User has many posts. """
    __tablename__ = 'users'

    def __repr__(self):
        return f'<User id={self.id} name={self.first_name} {self.last_name}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, default=None)


class Post(db.Model):
    """ Post has one user. """
    __tablename__ = 'posts'

    def __repr__(self):
        return f'<Post id={self.id} user_id={self.id} title={self.title}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref=backref(
        "posts", cascade="all,delete,delete-orphan"))
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')


class Tag(db.Model):
    __tablename__ = 'tags'

    def __repr__(self):
        return f'<Tag id={self.id} name={self.name}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)


class PostTag(db.Model):
    __tablename__ = 'post_tags'
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
