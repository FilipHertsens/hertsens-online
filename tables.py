from app import db, app, admin
from flask import abort, redirect
from flask_user import UserMixin, UserManager
from flask_login import current_user
from buttons import navbuttons
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuCategory, MenuView, MenuLink, SubMenuCategory


user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('roles_id', db.Integer(), db.ForeignKey('roles.id')))

role_navbarbuttons = db.Table('role_navbarbuttons',
    db.Column('roles_id', db.Integer(), db.ForeignKey('roles.id')),
    db.Column('button_id', db.Integer(), db.ForeignKey('navbarbutton.id')))

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

    def get_navbarbuttons(self):
        return navbuttons(self)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    navbarbutton = db.relationship('Navbarbutton', secondary = 'role_navbarbuttons', backref='premissions')

    def __repr__(self):
        return '{}'.format(self.name)


class Navbarbutton(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    type = db.Column(db.String(25))
    href = db.Column(db.String(50))
    navbarcat_id = db.Column(db.Integer, db.ForeignKey('navbarcat.id'))

    def __repr__(self):
        return '{}'.format(self.name)

class Navbarcat(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    buttons = db.relationship('Navbarbutton', backref='navbarcat')

    def __repr__(self):
        return '{}'.format(self.name)

user_manager = UserManager(app, db, User)

class MyModelView(ModelView):
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/login')
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
admin.add_view(MyModelView(Navbarcat, db.session))
admin.add_view(MyModelView(Navbarbutton, db.session))