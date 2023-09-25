from unittest import TestCase
from models import db, User
from app import app, user_service
from sqlalchemy import text, exc

if app.config['SQLALCHEMY_DATABASE_URI'] != 'postgresql:///blogly_test':
    raise Exception("Use test database to run tests!!!")

db.drop_all()
db.create_all()

class AppTestCase(TestCase):
    def setUp(self):
        """ Delete all users. Reset the id sequence. Add test user. """
        User.query.delete()
        db.session.execute(text('ALTER SEQUENCE users_id_seq RESTART WITH 1;'))
        user_service.create_user('Jonathan', 'Joestar')
        user_service.create_user('Joseph', 'Joestar')
        user_service.create_user('Jotaro', 'Kujo')
        user_service.create_user('Josuke', 'Higashikata')
        user_service.create_user('Giorno', 'Giovanna')

    def tearDown(self):
        """ Rollback back any failed sessions. """
        db.session.rollback()
    
    def test_root_redirect_to_users(self):
        """ Should redirect root to users page. """
        with app.test_client() as client:
            resp = client.get('/')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/users')

    def test_get_users(self):
        """ Should render users page. """
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jonathan Joestar', html)
            self.assertIn('Joseph Joestar', html)
            self.assertIn('Jotaro Kujo', html)
            self.assertIn('Josuke Higashikata', html)
            self.assertIn('Giorno Giovanna', html)
    
    def test_new_user_form(self):
        """ Should render new user form. """
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a user</h1>', html)
            self.assertIn('First Name</label>', html)
            self.assertIn('Last Name</label>', html)
            self.assertIn('Image URL</label>', html)
            self.assertIn('Add</button>', html)
    
    def test_new_user_redirect_to_users(self):
        """ Should redirect new user to users page. """
        with app.test_client() as client:
            data = {
                'first_name': 'Dio',
                'last_name': 'Brando',
                'image_url': ''
            }
            resp = client.post('/users/new', data = data)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/users')
    
    def test_get_user(self):
        """ Should render user page. """
        with app.test_client() as client:
            resp = client.get('/users/1')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jonathan', html)
            self.assertIn('Joestar', html)
            self.assertIn('Edit</button>', html)
            self.assertIn('Delete</button>', html)
    
    def test_edit_user_form(self):
        """ Should render edit user form. """
        with app.test_client() as client:
            resp = client.get('/users/1/edit')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit a user</h1>', html)
            self.assertIn('Jonathan', html)
            self.assertIn('Joestar', html)
            self.assertIn('Cancel</button>', html)
            self.assertIn('Save</button>', html)
    
    def test_edit_user(self):
        """ Should redirect edited user to users page. """
        with app.test_client() as client:
            data = {
                'first_name': 'Dio',
                'last_name': 'Brando',
                'image_url': ''
            }
            resp = client.post('/users/1/edit', data = data)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/users')
    
    def test_delete_user(self):
        """ Should redirect deleted user to users page. """
        with app.test_client() as client:
            resp = client.post('/users/1/delete')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/users')