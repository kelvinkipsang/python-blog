from flask import render_template
from . import auth
from .forms import LoginForm

@auth.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit:
        pass
    return render_template('auth/login.html', form=form)   #calling login.html and passing the form
                                                           #passing form object(from forms.py) for merging

