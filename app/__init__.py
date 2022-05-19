from flask import Flask, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, current_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy  import SQLAlchemy
from flask_admin import Admin
from flask_mail import Message
from flask_mail import Mail
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuCategory, MenuView, MenuLink, SubMenuCategory
from flask_login import LoginManager
from flask_babelex import Babel
from flask_migrate import Migrate
from datetime import timedelta
from flask_user import UserManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['USE_SESSION_FOR_NEXT'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'filip@hertsens.eu'
app.config['MAIL_PASSWORD'] = 'GE022022!'
app.config['MAIL_DEFAULT_SENDER'] = ('Hertsens Online','garage@hertsens.eu')

app.config['USER_APP_NAME'] = "Hertsens Online"
app.config['USER_ENABLE_EMAIL'] = True
app.config['USER_ENABLE_USERNAME'] = False
app.config['USER_EMAIL_SENDER_NAME'] = "Hertsens Online"
app.config['USER_EMAIL_SENDER_EMAIL'] = 'garage@hertsens.eu'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')



mail = Mail()
mail.init_app(app)
admin = Admin(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)
babel = Babel(app)

from app import views