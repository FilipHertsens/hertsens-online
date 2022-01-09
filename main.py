from flask import Flask, render_template, request, redirect, url_for, make_response
import hashlib
from models import User, db
import uuid

app = Flask(__name__)
db.create_all()  # create (new) tables in the database


@app.route("/", methods=["GET"])
def index():
    session_token = request.cookies.get("session_token")

    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
        return render_template("index.html", user=user.email)
    else:
        return render_template("login.html")

@app.route("/users", methods=["GET"])
def users():
    session_token = request.cookies.get("session_token")

    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
        return render_template("users.html", user=user.email)
    else:
        return render_template("login.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("user-email")
        password = request.form.get("user-password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(hashed_password)

        user = db.query(User).filter_by(email=email).first()

        if user and hashed_password == user.password:
            # create a random session token for this user
            session_token = str(uuid.uuid4())
            # save the session token in a database
            user.session_token = session_token
            user.save()
            # save user's session token into a cookie
            response = make_response(redirect(url_for('index')))
            response.set_cookie("session_token", session_token, httponly=True, samesite='Strict', max_age=43200)
            return response

        error = 'Invalid Email or Password'
        return render_template('login.html', error=error)

    elif request.method == 'GET':
        return render_template("login.html")


if __name__ == '__main__':
    app.run(use_reloader=True)