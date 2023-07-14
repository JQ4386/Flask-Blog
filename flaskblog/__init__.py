from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'a1ba33631eaf7e72e61b84652553a933a185d5e9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) 
login_manager.login_view = 'login' # set login route
login_manager.login_message_category = 'danger' # bootstrap class for flash message

# import below to avoid circular imports
from flaskblog import routes