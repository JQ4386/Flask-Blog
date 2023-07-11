from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
import secrets

app = Flask(__name__)
app.secret_key = 'a1ba33631eaf7e72e61b84652553a933a185d5e9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# models
class User(db.Model):
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

posts = [
    {
        'author': 'John Doe',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018',
    }, 
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018',
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for { form.username.data }!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


# run the app with: python flaskblog.py
if __name__ == '__main__':
    app.run(debug=True)
