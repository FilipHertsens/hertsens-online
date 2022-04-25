from app import app
import datetime
from werkzeug.utils import secure_filename
import os
from flask_login import current_user
from functools import wraps
from flask import render_template, redirect, url_for, request, session

def uploading_files(data):
    files_filenames = ''
    x=1
    try:
        for file in data:
            if files_filenames != '':
                files_filenames += ';\n'
            if file.filename != '':
                filename = str(datetime.datetime.now().strftime("%d%m%Y_%H%M%S"))
                ex = file.filename.split('.')[-1]
                file_filename = secure_filename(f'{current_user.current_asset.name}__{int(x)}__{filename}.{ex}')
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_filename))
                files_filenames += file_filename
                x+=1
        return True, files_filenames
    except:
        return False, ''


def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_active:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))
    return decorated_func