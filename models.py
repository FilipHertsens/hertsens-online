import os
from sqla_wrapper import SQLAlchemy

db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    session_token = db.Column(db.String)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    telnr = db.Column(db.String)

    def to_dict(self):
        return{
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'telnr': self.telnr,
            'id': self.id
        }