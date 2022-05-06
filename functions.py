from app import app
import datetime
from werkzeug.utils import secure_filename
import os
from PIL import Image
from flask_login import current_user
from functools import wraps
from flask import render_template, redirect, url_for, request, session
import platform

def uploading_files(data):
    files_filenames = ''
    x=1
    try:
        for file in data:
            if files_filenames != '':
                files_filenames += ';\n'
            if file.filename != '':
                ex = file.filename.split('.')[-1]
                filename = str(datetime.datetime.now().strftime("%d%m%Y_%H%M%S"))
                file_filename = secure_filename(f'{current_user.current_asset.name}__{int(x)}__{filename}')
                mimetype = file.headers['Content-Type']
                if 'image' in mimetype:
                    img = Image.open(file)
                    new_size_ratio = 960/img.size[0]
                    if new_size_ratio < 1:
                        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)),
                                     Image.ANTIALIAS)
                    if file.filename.split('.')[-1][1] != 'jpg':
                        # change the extension to JPEG
                        file_filename = f"{file_filename}.jpg"
                    img.save(os.path.join(app.config['UPLOAD_FOLDER'], file_filename), quality=90, optimize=True)
                else:
                    file_filename = f"{file_filename}.{ex}"
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