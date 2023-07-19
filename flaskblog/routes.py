import secrets, os
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
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
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        # create user
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
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
def save_picture(form_picture):
    # generate random filename to avoid collisions
    random_hex = secrets.token_hex(8)
    # get file extension
    _, f_ext = os.path.splitext(form_picture.filename)
    # create filename
    picture_fn = random_hex + f_ext
    # create path to save file to
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # resize image before saving
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # save image to filesystem
    i.save(picture_path)
    # return filename
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
# login_required decorator ensures user is logged in before accessing account page
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            # save picture to filesystem
            picture_file = save_picture(form.picture.data)
            # update user's picture
            current_user.image_file = picture_file
        # update username and email
        current_user.username = form.username.data
        current_user.email = form.email.data
        # commit changes to db
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account')) # Avoid Post/Redirect/Get pattern
    elif request.method == 'GET':
        # populate form with current user info
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    # if form is valid
    if form.validate_on_submit():
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)
