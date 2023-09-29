from models import db, Tag
from sqlalchemy import exc


class TagService:
    def get_tags(self):
        return db.session.query(Tag).all()

    def get_tag(self, tag_id):
        return db.session.query(Tag).filter(Tag.id == tag_id).one()

    def create_tag(self, name):
        if name != '':
            tag = Tag(name=name)
        try:
            db.session.add(tag)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()

    def update_tag(self, tag_id, name):
        if name != '':
            tag = self.get_tag(tag_id)
            tag.name = name
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()

    def delete_tag(self, tag_id):
        tag = self.get_tag(tag_id)
        db.session.delete(tag)
        db.session.commit()
