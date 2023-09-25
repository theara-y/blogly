from models import db, User
from sqlalchemy import exc

class UserService:
    def get_users(self):
        return User.query.all()

    def get_user(self, id):
        return User.query.get(id)

    def create_user(self, first_name, last_name, image_url = ''):
        if first_name != '' and last_name != '':
            user = User(
                first_name = first_name, 
                last_name = last_name, 
                image_url = image_url
            )
            try:
                db.session.add(user)
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()

    def update_user(self, user_id, first_name, last_name, image_url = ''):
        if first_name != '' and last_name != '':
            user = self.get_user(user_id)
            if user:
                user.first_name = first_name
                user.last_name = last_name
                user.image_url = image_url
            try:
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()

    def delete_user(self, id):
        User.query.filter_by(id = id).delete()
        db.session.commit()