from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)

# home page
@main.route('/')
@main.route('/home')
def home():
    # paginate posts (1 post per page for testing)
    page = request.args.get('page', 1, type=int)
    # order posts by date posted, newest first
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=1)
    return render_template('home.html', title='Home', posts=posts)

# about page
@main.route('/about')
def about():
    return render_template('about.html', title='About')

