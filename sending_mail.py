from app import mail, app
from flask_mail import Message
from flask import render_template
import os
import filetype
from flask_login import current_user
from forms import LoginForm, RegisterForm, Asset_selector, repair_request

def send_mail():
    msg = Message("Hello",
                  sender="filip@hertsens.eu",
                  recipients=["garage@hertsens.eu"])
    mail.send(msg)

def send_repair_request(request, recipients=["garage@hertsens.eu"]):
    print(request.description)
    msg = Message("Repair request",
                  sender="filip@hertsens.eu",
                  recipients=recipients)
    msg.html = render_template('email/repair_request.html',request=request)
    file_filenames = request.files.split(';\n')
    for file_filename in file_filenames:
        # file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_filename)
        file_name = os.path.join('uploads', file_filename)
        mimetype =filetype.guess(file_name)
        with open(file_name, "rb") as fp:
            msg.attach(file_name, mimetype.mime, fp.read())
    mail.send(msg)