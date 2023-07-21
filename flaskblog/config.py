import os

class Config:
    SECRET_KEY = 'a1ba33631eaf7e72e61b84652553a933a185d5e9'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    
    # set email server settings (cannot get authentication to work)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587 #TLS (Transport Layer Security) port, 587 is default
    MAIL_USE_TLS = True #encryption (using environment variable to hide sensitive info)
    MAIL_USERNAME = os.environ.get('EMAIL_USER') #environment variable for email
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS') #environment variable for password

