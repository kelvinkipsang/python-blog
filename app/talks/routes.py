from flask import render_template
from . import talks

#instead of creating a global app,im creating a global blueprint and placing routes in it

@talks.route('/')
def index():
    return render_template('talks/index.html')

@talks.route('/user/<username>')
def user(username):
    return render_template('talks/user.html', username=username) #sending argument username to tmeplate user.html