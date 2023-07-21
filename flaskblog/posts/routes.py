from flask import (render_template, url_for, flash,
                     redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

# new post route
@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    # if form is valid
    if form.validate_on_submit():
        # create post
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        # add post to db
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

# posts route
@posts.route('/post/<int:post_id>')
def post(post_id):
    # get post by id
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# update post route
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)  # get post by id
    # check if user is author of post
    if post.author != current_user:
        abort(403)
    form = PostForm()
    # if form is valid
    if form.validate_on_submit():
        # update post
        post.title = form.title.data
        post.content = form.content.data
        # commit changes to db
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    # populate form with current post info
    elif request.method == 'GET':
        form.title.data = post.title  # populate form with current post title
        form.content.data = post.content  # populate form with current post content
    return render_template('create_post.html', title='Update Post', 
                            form=form, legend='Update Post')

# delete post route
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # check if user is author of post
    if post.author != current_user:
        abort(403)
    # delete post
    db.session.delete(post)
    db.session.commit()

    # flash message
    flash('Your post has been deleted!', 'success') 
    return redirect(url_for('main.home'))
