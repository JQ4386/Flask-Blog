import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail #set constants so app knows how to send emails. Need mail server, username, password.

app = Flask(__name__)
app.secret_key = 'a1ba33631eaf7e72e61b84652553a933a185d5e9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) 
login_manager.login_view = 'users.login' # set login route
login_manager.login_message_category = 'danger' # bootstrap class for flash message

# set email server settings (cannot get authentication to work)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587 #TLS (Transport Layer Security) port, 587 is default
app.config['MAIL_USE_TLS'] = True #encryption (using environment variable to hide sensitive info)
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER') #environment variable for email
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS') #environment variable for password
mail = Mail(app) 

# import below to avoid circular imports
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

# register blueprints
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)