from datetime import datetime
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import hashlib
import bleach
from flask import  request, current_app
from flask_login import login_user
# from ..models import user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown



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
    talks = db.relationship('Talk', backref='author', lazy='dynamic')  #lazy makes talks query not list
    comments = db.relationship('Comment', lazy='dynamic', backref='author')

    def get_api_token(self, expiration=300):            #produces a token for user,5min exp,
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'user': self.id}).decode('utf-8')

    @staticmethod
    def validate_api_token(token):                      #decodes token(inside token is a user id),finds and loads user
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('user')
        if id:
            return User.query.get(id)
        return None

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or \
               hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    @property                                   #made it pprty so that i can say user.password=? so that it looks like a member var
    def password(self):
        raise AttributeError('password is not a readable attribute')    #getter of pperty returns attribute error

    @password.setter
    def password(self, password):                                       #runs hashing fnt storing it in paa hash attr(column in db)
        self.password_hash = generate_password_hash(password)           #trans by werkzeug

    def verify_password(self, password):                                #called when user logs in
        return check_password_hash(self.password_hash, password)        #takes plain text,calls werks function,applies trans fnt to plain txt,compares the hashes

    @staticmethod
    def for_moderation(self, admin=False):
        if admin and self.is_admin:
            return Comment.for_moderation()
        return Comment.query.join(Talk, Comment.talk_id==Talk.id).filter(Talk.author==self).filter(Comment.approved == False)
        # all comments in any talks,for talks authred by 1 user

@login_manager.user_loader                  #flogin doesnt know anything about our objects,,we give it a user loader callback,so that when it needs to load the user
def user_loader(user_id):                   #we provide function that does that work,flask knows how to load users
    return User.query.get(int(user_id))     #comes as unicode




from markdown import markdown
import bleach


class Talk(db.Model):
    __tablename__ = 'talks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    slides = db.Column(db.Text())
    video = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    venue = db.Column(db.String(128))
    venue_url = db.Column(db.String(128))
    date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', lazy='dynamic', backref='talk')

    def approved_comments(self):
        return self.comments.filter_by(approved=True)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)           #markdown source
    body_html = db.Column(db.Text)      #html gen source
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author_name = db.Column(db.String(64))
    author_email = db.Column(db.String(64))
    notify = db.Column(db.Boolean, default=True)
    approved = db.Column(db.Boolean, default=False)
    talk_id = db.Column(db.Integer, db.ForeignKey('talks.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):                #funtion takes value,html
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',  #uses bleach to filter out tags not specified
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(                     #stores it here
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Comment.body, 'set', Comment.on_changed_body)   #sqlalchemy calls

    @staticmethod
    def for_moderation():
        return Comment.query.filter_by(Comment.approved==False)
