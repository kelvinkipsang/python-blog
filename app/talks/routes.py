from flask import render_template
from . import talks
from ..models import User
#instead of creating a global app,im creating a global blueprint and placing routes in it

@talks.route('/')
def index():
    return render_template('talks/index.html')

@talks.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('talks/user.html', user=user) #sending argument user to tmeplate user.html


