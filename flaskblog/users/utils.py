import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

# Desc: utility functions for users blueprint

# function for saving profile picture
def save_picture(form_picture):
    # generate random filename to avoid collisions
    random_hex = secrets.token_hex(8)
    # get file extension
    _, f_ext = os.path.splitext(form_picture.filename)
    # create filename
    picture_fn = random_hex + f_ext
    # create path to save file to
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)
    # resize image before saving
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # save image to filesystem
    i.save(picture_path)
    # return filename
    return picture_fn

# function for sending reset email
def send_reset_email(user):
    # generate token
    token = user.get_reset_token()
    # create message (sender, recipients)
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    # create body of message with f-string
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)} # _external=True gives absolute url
If you did not make this request, please ignore this email. No changes will be made.
    ''' 
# make sure to not tab in string or else it will show up in email body
# -> Can use Jinja2 template to create email body for more complex emails
    # send message 
    # mail.send(msg) # uncomment when ready to send email