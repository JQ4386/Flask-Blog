from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail #set constants so app knows how to send emails. Need mail server, username, password.
from flaskblog.config import Config

# extensions (outside so that the extension object can be used by multiple apps)
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager() 
login_manager.login_view = 'users.login' # set login route
login_manager.login_message_category = 'danger' # bootstrap class for flash message

mail = Mail() 


# create app factory
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import blueprints
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
