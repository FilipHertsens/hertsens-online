from flask import Flask, flash, render_template, redirect, url_for, abort, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_user import roles_required, UserManager, UserMixin
from flask_babelex import Babel
from buttons import navbuttons
import datetime


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
login_manager.login_view = 'login'
admin = Admin(app)
babel = Babel(app)

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('roles_id', db.Integer(), db.ForeignKey('roles.id'))
    )

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    email = db.Column(db.String(50, collation='NOCASE'), unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(200))
    roles = db.relationship('Role', secondary='user_roles', backref='premissions')

    def __repr__(self):
        return '{}{}'.format(self.first_name, self.last_name)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    list_navButtons = db.Column(db.Text)

    def __repr__(self):
        return '{}'.format(self.name)


user_manager = UserManager(app, db, User)
db.create_all()


class MyModelView(ModelView):
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))
    def is_accessible(self):
        if current_user.is_active:
            roless = current_user.roles
            for x in roless:
                if x.name == 'Admin':
                    return current_user.is_authenticated
                else:
                    return abort(404)
            return abort(404)
        else:
            return abort(404)
    def get_edit_userForm(self):
        form_user = ModelView(User, db.session).get_edit_form()
        print(form_user)
        del form_user.password
        return form_user

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    first_name = StringField('First name', validators=[InputRequired(), Length(min=4, max=15)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html',user=current_user, form=form, buttons=navbuttons())

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))
            else:
                error = 'Invalid password for this user'
        else:
            error = f'No user with {form.email.data} as email'
    return render_template('login.html', form=form, error=error,user=current_user, buttons=navbuttons())

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                       password=hashed_password,email_confirmed_at=datetime.datetime.utcnow())
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('signup.html', form=form,user=current_user, buttons=navbuttons())

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.first_name, buttons=navbuttons())

@app.route('/data')
@roles_required('Admin')
def an():
    return render_template('dashboard.html', name=current_user.last_name, buttons=navbuttons())

@app.route('/base')
def base():
    return render_template('base.html', buttons=navbuttons())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)