from app import mail, app
from flask_mail import Message
from flask import render_template
import os
from tables import Repair_request
import datetime
import filetype
from flask_login import current_user
from forms import LoginForm, RegisterForm, Asset_selector, repair_request
from threading import Thread

def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail():
    msg = Message("Hello",
                  sender="filip@hertsens.eu",
                  recipients=["garage@hertsens.eu"])
    mail.send(msg)

def send_repair_request(request, recipients=["garage@hertsens.eu"]):
    msg = Message("Repair request",
                  sender="filip@hertsens.eu",
                  recipients=recipients)
    request.description = " <br> ".join(request.description.split("\n"))
    request.time = request.request_time.strftime("%H:%M  %d/%m/%Y")
    msg.html = render_template('email/repair_request.html',request=request)
    if request.files != '':
        file_filenames = request.files.split(';\n')
        for file_filename in file_filenames:
            # file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_filename)
            file_name = os.path.join('uploads', file_filename)
            mimetype =filetype.guess(file_name)
            with open(file_name, "rb") as fp:
                msg.attach(file_name, mimetype.mime, fp.read())
    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()
    return True

