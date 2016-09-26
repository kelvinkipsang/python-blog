from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
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
    talks = db.relationship('Talk', lazy='dynamic', backref='author')
    comments = db.relationship('Comment', lazy='dynamic', backref='author')

    @property                                   #made it pprty so that i can say user.password=? so that it looks like a member var
    def password(self):
        raise AttributeError('password is not a readable attribute')    #getter of pperty returns attribute error

    @password.setter
    def password(self, password):                                       #runs hashing fnt storing it in paa hash attr(column in db)
        self.password_hash = generate_password_hash(password)           #trans by werkzeug

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)