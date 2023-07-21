from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                      RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    # if user is logged in, redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
        flash(f'Your account has been create! You are now able to log in!', 'success') #green alert
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    # if user is logged in, redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            # flash unsuccessful login message
            flash(f'Login unsuccessful. Please check email and password.', 'danger') #red alert
    return render_template('login.html', title='Login', form=form)

# logout route
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))  # Avoid Post/Redirect/Get pattern
    elif request.method == 'GET':
        # populate form with current user info
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

# user posts route
@users.route('/user/<string:username>')
def user_posts(username):
    # get page number from query string
    page = request.args.get('page', 1, type=int)
    # get user by username
    user = User.query.filter_by(username=username).first_or_404()
    # get posts by user
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=1)
    return render_template('user_posts.html', posts=posts, user=user)

# reset password request route
@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # check if user is logged in. If so, redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    # if form is valid
    if form.validate_on_submit():
        # get user by email
        user = User.query.filter_by(email=form.email.data).first()
        # send reset email
        send_reset_email(user)
        # flash message
        flash('If an account with that email exists, you will receive an email with instructions to reset your password.', 'info') # blue alert
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

# reset password route (similar to register route, but with token)
@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # verify token
    user = User.verify_reset_token(token)
    # if token is invalid or expired
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    # if token is valid
    form = ResetPasswordForm()

    # similar to register route
    if form.validate_on_submit():
        # hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # update user's password
        user.password = hashed_password
        # commit changes to db
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
