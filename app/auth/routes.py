from flask import render_template,flash, redirect, url_for
from . import auth
from .forms import LoginForm

@auth.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit:
        pass
    return render_template('auth/login.html', form=form)   #calling login.html and passing the form
                                                           #passing form object(from forms.py) for merging

from flask_login import login_user, logout_user, login_required

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you\'ve logged out')
    return redirect(url_for('talks.index'))
