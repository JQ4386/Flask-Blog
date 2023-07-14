from flask import render_template, flash, redirect, url_for, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# dummy data
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

# routes - url paths for our app to navigate to different pages

# home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home', posts=posts)

# about page
@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # if user is logged in, redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # create user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # add user to db
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been create! You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if user is logged in, redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
         # check if user exists
        user = User.query.filter_by(email=form.email.data).first()

        # if user exists and password matches
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # login user
            login_user(user, remember=form.remember.data)
            # redirect to page user was trying to access before login
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            # flash unsuccessful login message
            flash(f'Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

# logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# account route
@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')