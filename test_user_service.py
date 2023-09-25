from unittest import TestCase
from models import db, User
from sqlalchemy import text, exc
from app import app, user_service

if app.config['SQLALCHEMY_DATABASE_URI'] != 'postgresql:///blogly_test':
    raise Exception("Use test database to run tests!!!")

db.drop_all()
db.create_all()

class UserServiceTestCase(TestCase):
    """ Tests for UserService. """

    def setUp(self):
        """ Delete all users. Reset the id sequence. Add test user. """
        User.query.delete()
        db.session.execute(text('ALTER SEQUENCE users_id_seq RESTART WITH 1;'))
        user1 = User(first_name = 'Jonathan', last_name = 'Joestar')
        user2 = User(first_name = 'Joseph', last_name = 'Joestar')
        user3 = User(first_name = 'Jotaro', last_name = 'Kujo')
        user4 = User(first_name = 'Josuke', last_name = 'Higashikata')
        user5 = User(first_name = 'Giorno', last_name = 'Giovanna')

        db.session.add_all([user1, user2, user3, user4, user5])
        db.session.commit()
        
    def tearDown(self):
        """ Rollback back any failed sessions. """
        db.session.rollback()

    def test_get_users_success(self):
        """ Should return all users. """
        self.assertEqual(len(user_service.get_users()), 5)

    def test_get_users_success_empty(self):
        """ Should return empty list if there are no users. """
        User.query.delete()
        db.session.commit()
        self.assertEqual(user_service.get_users(), [])

    def test_get_user_success(self):
        """ Should return the user with an id of 1. """
        user = user_service.get_user(1)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.first_name, 'Jonathan')
        self.assertEqual(user.last_name, 'Joestar')
        self.assertEqual(user.image_url, None)

    def test_get_user_failure(self):
        """ Should return None when fetching a user that does not exist. """
        user = user_service.get_user(-1)
        self.assertIsNone(user)

    def test_create_user_success(self):
        """ Should create a new user successfully. """
        user_service.create_user('Dio', 'Brando')
        user = user_service.get_user(6)
        self.assertEqual(user.id, 6)
        self.assertEqual(user.first_name, 'Dio')
        self.assertEqual(user.last_name, 'Brando')
        self.assertEqual(user.image_url, '')
        self.assertEqual(len(user_service.get_users()), 6)

    def test_create_user_failure(self):
        """ Should raise integrity exception when failing to create a user. """
        user_service.create_user('', '', '')
        self.assertRaises(exc.IntegrityError)

    def test_update_user_success(self):
        """ Should update a user successfully. """
        user_service.update_user(1, 'Dio', 'Brando', '')
        user = user_service.get_user(1)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.first_name, 'Dio')
        self.assertEqual(user.last_name, 'Brando')
        self.assertEqual(user.image_url, '')

    def test_update_user_failure(self):
        """ Should raise integrity exception when failing to update a user. """
        self.assertIsNone(user_service.update_user(1, '', '', ''))
        self.assertRaises(exc.IntegrityError)

    def test_delete_user_success(self):
        """ Should delete a user successfully. """
        user_service.delete_user(1)
        self.assertEqual(len(user_service.get_users()), 4)