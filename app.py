"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from user_service import UserService

user_service = UserService()

### TEST DB ###
DB_URI = 'postgresql:///blogly_test'

### PRODUCTION DB ###
# DB_URI = 'postgresql:///blogly'

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

debug = DebugToolbarExtension(app)

@app.route('/')
def root():
    """ Redirect to list of users. """
    return redirect('/users')

@app.route('/users')
def get_users():
    """ Show all users. """
    users = user_service.get_users()
    return render_template('users.html', users = users)

@app.route('/users/new')
def new_user_form():
    """ Registration form. """
    return render_template('new_user.html')

@app.route('/users/new', methods = ['POST'])
def new_user():
    """ Process registration. """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user = user_service.create_user(first_name, last_name, image_url)
    return redirect(f'/users')

@app.route('/users/<int:user_id>')
def get_user(user_id):
    """ Show a user. """
    user = user_service.get_user(user_id)
    return render_template('user.html', user = user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """ Edit user form. """
    user = user_service.get_user(user_id)
    return render_template('edit_user.html', user = user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def edit_user(user_id):
    """ Process user update. """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user_service.update_user(user_id, first_name, last_name, image_url)
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    """ Delete user. """
    user_service.delete_user(user_id)
    return redirect('/users')