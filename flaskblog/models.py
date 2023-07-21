from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

# login manager
@login_manager.user_loader # decorator - tells flask-login how to get user
def load_user(user_id):
    return User.query.get(int(user_id))

# models
class User(db.Model, UserMixin):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False) # 20 char max, unique, not null
    email = db.Column(db.String(120), unique=True, nullable=False) # 120 char max, unique, not null
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # 20 char max, not null, default
    password = db.Column(db.String(60), nullable=False) # 60 char max, not null
    posts = db.relationship('Post', backref='author', lazy=True) # one to many relationship, backref allows us to get user who created post

    # methods
    def get_reset_token(self, expires_sec=1800):
        # create serializer object
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        # return token
        return s.dumps({'user_id': self.id}).decode('utf-8') # dumps = serialize, decode = convert to string

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    @staticmethod # static method - does not take self as argument
    def verify_reset_token(token):
        # create serializer object
        s = Serializer(current_app.config['SECRET_KEY'])
        # try and except block to catch exceptions
        try:
            # load token
            user_id = s.loads(token)['user_id']
        except:
            return None # return none if exception
        return User.query.get(user_id) # return user id if no exceptions

    
class Post(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) # 100 char max, not null
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # not null, default, always use utc time for consistency
    content = db.Column(db.Text, nullable=False) # not null
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # not null

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"