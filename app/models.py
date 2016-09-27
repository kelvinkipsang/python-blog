from datetime import datetime
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from flask import render_template,redirect, request, url_for, flash
from flask_login import login_user
from ..models import user

class User(UserMixin, db.Model):            #f-login uses usermixn class,which provides default implementations for get id,is anonymous,is active,is auth
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),
                      nullable=False, unique=True, index=True)
    username = db.Column(db.String(64),
                         nullable=False, unique=True, index=True)
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    bio = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))


    @property                                   #made it pprty so that i can say user.password=? so that it looks like a member var
    def password(self):
        raise AttributeError('password is not a readable attribute')    #getter of pperty returns attribute error

    @password.setter
    def password(self, password):                                       #runs hashing fnt storing it in paa hash attr(column in db)
        self.password_hash = generate_password_hash(password)           #trans by werkzeug

    def verify_password(self, password):                                #called when user logs in
        return check_password_hash(self.password_hash, password)        #takes plain text,calls werks function,applies trans fnt to plain txt,compares the hashes

@login_manager.user_loader                  #flogin doesnt know anything about our objects,,we give it a user loader callback,so that when it needs to load the user
def user_loader(user_id):                   #we provide function that does that work,flask knows how to load users
    return User.query.get(int(user_id))     #comes as unicode

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

    return render_template('auth/login.html', form=form)