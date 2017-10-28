from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,

    # HTTP session NOT DB session, for passing user state
    session
)

import datetime

# ORM Heavy Technology
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
# session needs secret_key for parsing
app.secret_key = 'rocky'
db = SQLAlchemy(app)


# DB classes
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)

    posts = db.relationship('Post', backref='author', lazy='dynamic')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(600))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# create DB
db.create_all()
db.session.commit()

"""
index page
    - for new users: go to signup page
    - for return users: go to login page
    - if already login, find all the blog posts
    - if already login, go to create blog page
    
signup page
    - create new user account
    - after creation, redirect  to index page
    
login page
    - a form to login
    - after login, redirect to index page
    
logout (no html page)
    - user logout
    
create blog page
    - a form to create blog
    - after creation, redirect to index page
"""


# decorator for routing rule (for visiting contents)
@app.route('/')
def index():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if not user:
            session.pop('username', None)
            return render_template('index.html.jinja')
        else:
            blogs = user.posts.all()
            return render_template('index.html.jinja', user=user, blogs=blogs)
    return render_template('index.html.jinja')


# GET page content / POST signup results
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # add user
        username = request.form['username']
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('signup.html.jinja')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        # password validation process
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('login.html.jinja')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        content = request.form['content']
        user = User.query.filter_by(username=session['username']).first()
        post = Post(content=content, timestamp=datetime.datetime.utcnow(), author=user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html.jinja')


# decorator for error handler, like status code 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html.jinja'), 404


# start local server
# Flask debug mode will reload the server automatically, awesome!
app.run(debug=True)
