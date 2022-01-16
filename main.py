from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import hashlib
from models import User, db
import uuid
from werkzeug.datastructures import MultiDict

app = Flask(__name__)
db.create_all()  # create (new) tables in the database


@app.route("/", methods=["GET"])
def index():
    session_token = request.cookies.get("session_token")

    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
        if user != None:
            return render_template("index.html", user=user.firstname+' '+user.lastname)
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/users", methods=["GET"])
def users():
    session_token = request.cookies.get("session_token")

    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
        if user != None:
            Users = db.query(*[c for c in User.__table__.c if c.name not in ['password', 'session_token']]).all()
            return render_template("users.html", user=user.firstname+' '+user.lastname, Users=Users)
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie("session_token", expires=0)
    return redirect('/login')


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("user-email")
        password = request.form.get("user-password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
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

@app.route('/getUserdata/<index>')
def getUserdata(index):
    session_token = request.cookies.get("session_token")
    if session_token:
        me = db.query(User).filter_by(session_token=session_token).first()
        user = db.query(User).filter_by(id=index).first()
        return jsonify(user.to_dict(),me.to_dict())
    else:
        return render_template("login.html")

@app.route('/updateUser', methods=['post'])
def updateUser():
    email = request.form.get("email")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    password = request.form.get("password")
    telnr = request.form.get("telnr")
    user = db.query(User).filter_by(email=email).first()
    if user != None:
        user.email = email
        user.firstname = firstname
        user.lastname = lastname
        user.telnr = telnr
        if password != None:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user.password = hashed_password
        user.save()
    else:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        new_user = User(email=email, password=hashed_password, firstname=firstname, lastname=lastname, telnr=telnr)
        new_user.save()
    return redirect('/users')

@app.route('/resetpassword/<index>', methods=['post'])
def resetpassword(index):
    user = db.query(User).filter_by(id=index).first()
    hashed_password = hashlib.sha256('password'.encode()).hexdigest()
    user.password = hashed_password
    user.save()
    return redirect('/users')

@app.route('/deleteUser/<index>')
def deleteUser(index):
    user = db.query(User).filter_by(id=index).first()
    user.delete()
    return redirect('/users')

if __name__ == '__main__':
    app.run()