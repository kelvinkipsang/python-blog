from flask import render_template,flash, redirect, url_for,request
from .forms import LoginForm



from . import auth
from ..models import User
# from flask_login import login_user

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit:

        user = User.query.fiter_by(email=form.email.data).first()           #load user by email thro query,thro query object,filter,give first
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('.login'))
        login_user(user, form.remember_me.data)            #call fnt, takes user obj & boolean rem me,writes user session
        return redirect(request.args.get('next') or url_for('talks.index'))     #redirects to main bprint index or the original page the user was visiting

    return render_template('auth/login.html', form=form)            #calling login.html and passing the form
                                                           #passing form object(from forms.py) for merging


from flask_login import login_user, logout_user, login_required

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you\'ve logged out')
    return redirect(url_for('talks.index'))
