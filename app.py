"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag
from sqlalchemy import text
from user_service import UserService
from post_service import PostService
from tag_service import TagService

user_service = UserService()
post_service = PostService(user_service)
tag_service = TagService()

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
    return render_template('users.html', users=users)


@app.route('/users/new')
def new_user_form():
    """ Registration form. """
    return render_template('new_user.html')


@app.route('/users/new', methods=['POST'])
def new_user():
    """ Process registration. """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user_service.create_user(first_name, last_name, image_url)
    return redirect(f'/users')


@app.route('/users/<int:user_id>')
def get_user(user_id):
    """ Show a user. """
    user = user_service.get_user(user_id)
    posts = user.posts
    return render_template('user.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """ Edit user form. """
    user = user_service.get_user(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """ Process user update. """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user_service.update_user(user_id, first_name, last_name, image_url)
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """ Delete user. """
    user_service.delete_user(user_id)
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """ New Post Form. """
    user = user_service.get_user(user_id)
    tags = tag_service.get_tags()
    return render_template('new_post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_new_post(user_id):
    """ Handle new post submission. """
    title = request.form['input_title']
    content = request.form['input_content']
    tags = []
    for key in list(request.form.keys()):
        key_parts = key.split('_')
        if key_parts[0] == 'tid':
            tag = tag_service.get_tag(int(key_parts[1]))
            tags.append(tag)
    post_service.create_post(user_id, title, content, tags)
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def get_post(post_id):
    """ Show a post. """
    post = post_service.get_post(post_id)
    return render_template('post.html', post=post, tags=post.tags)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """ Edit post form. """
    post = post_service.get_post(post_id)
    checked_tags = [tag.name for tag in post.tags]
    tags = [tag for tag in tag_service.get_tags() if tag.name not in checked_tags]
    return render_template('edit_post.html', post=post, checked_tags=post.tags, unchecked_tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_edit_post(post_id):
    """ Handle edit post request. """
    title = request.form['input_title']
    content = request.form['input_content']
    tags = []
    for key in list(request.form.keys()):
        key_parts = key.split('_')
        if key_parts[0] == 'tid':
            tag = tag_service.get_tag(int(key_parts[1]))
            tags.append(tag)
    post_service.update_post(post_id, title, content, tags)
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def handle_delete_post(post_id):
    """ Handle delete post request. """
    post_service.delete_post(post_id)
    return redirect(f'/')


@app.route('/tags')
def get_tags():
    """ Show all tags. """
    tags = tag_service.get_tags()
    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def get_tag(tag_id):
    """ Show a tag. """
    tag = tag_service.get_tag(tag_id)
    return render_template('tag.html', tag=tag, posts=tag.posts)


@app.route('/tags/new')
def create_tag_form():
    """ Show create tag form. """
    return render_template('new_tag.html')


@app.route('/tags/new', methods=['POST'])
def handle_create_tag():
    """ Handle create tag request. """
    name = request.form['input_name']
    tag_service.create_tag(name)
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """ Show edit tag form. """
    tag = tag_service.get_tag(tag_id)
    return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def handle_edit_tag(tag_id):
    """ Handle edit tag request. """
    name = request.form['input_name']
    tag_service.update_tag(tag_id, name)
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def handle_delete_tag(tag_id):
    """ Handle delete tag request. """
    tag_service.delete_tag(tag_id)
    return redirect('/tags')
