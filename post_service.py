from models import db, Post
from sqlalchemy import exc
from user_service import UserService
from datetime import datetime


class PostService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_post(self, post_id):
        return Post.query.get(post_id)

    def get_posts(self, user_id):
        user = self.user_service.get_user(user_id)
        return user.posts

    def create_post(self, user_id, title, content, tags):
        if title != '' and content != '':
            post = Post(
                title=title,
                content=content,
                created_at=datetime.now(),
                user_id=user_id
            )
            post.tags = []
            for tag in tags:
                post.tags.append(tag)
            try:
                db.session.add(post)
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()

    def update_post(self, post_id, title, content, tags):
        if title != '' and content != '':
            post = self.get_post(post_id)
            if post:
                post.title = title
                post.content = content
                post.tags = []
                for tag in tags:
                    post.tags.append(tag)
            try:
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()

    def delete_post(self, post_id):
        Post.query.filter_by(id=post_id).delete()
        db.session.commit()
