from flask import Flask, redirect
from flask_login import login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy  import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuCategory, MenuView, MenuLink, SubMenuCategory
from flask_login import LoginManager
from flask_babelex import Babel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'filip@hertsens.eu'
app.config['MAIL_PASSWORD'] = 'GE022022!'
app.config['MAIL_DEFAULT_SENDER'] = '"MyApp" <garage@hertsens.eu>'

app.config['USER_APP_NAME'] = "Flask-User Basic App"
app.config['USER_ENABLE_EMAIL'] = True
app.config['USER_ENABLE_USERNAME'] = False
app.config['USER_EMAIL_SENDER_NAME'] = "Flask-User Basic App"
app.config['USER_EMAIL_SENDER_EMAIL'] = 'garage@hertsens.eu'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
admin = Admin(app)


babel = Babel(app)

db.create_all()

from app import views