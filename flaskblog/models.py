from datetime import datetime
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

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) # 100 char max, not null
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # not null, default, always use utc time for consistency
    content = db.Column(db.Text, nullable=False) # not null
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # not null

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"