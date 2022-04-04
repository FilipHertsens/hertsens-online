from app import app, db, login_manager
from flask import render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from flask_user import roles_required
from forms import LoginForm, RegisterForm
from tables import User
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    form = LoginForm()
    user = User.query.filter_by(email='filip@hertsens.eu').first()
    print(user)
    return render_template('index.html',user=current_user, form=form)

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
    return render_template('login.html', form=form, error=error,user=current_user)

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

    return render_template('signup.html', form=form,user=current_user)


@app.route('/checks')
@login_required
def dashboard():
    return render_template('checks.html', user=current_user)


@app.route('/data')
@roles_required('Admin')
def an():
    return render_template('dashboard.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))