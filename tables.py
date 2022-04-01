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

asset_aggregaat = db.Table('asset_aggregaat',
    db.Column('asset_id', db.Integer(), db.ForeignKey('asset.id')),
    db.Column('aggregaat_id', db.Integer(), db.ForeignKey('aggregaat.id')))

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
    new_tab = db.Column(db.Boolean, default=False, nullable=True)
    href = db.Column(db.String(50),)
    navbarcat_id = db.Column(db.Integer, db.ForeignKey('navbarcat.id'))
    def __repr__(self):
        return '{}'.format(self.name)


class Navbarcat(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    buttons = db.relationship('Navbarbutton', backref='navbarcat')
    def __repr__(self):
        return '{}'.format(self.name)


class Asset_brands(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    asset_id = db.relationship('Asset', backref='asset_brands')
    def __repr__(self):
        return '{}'.format(self.name)


class Asset_type(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    asset_id = db.relationship('Asset', backref='asset_type')
    def __repr__(self):
        return '{}'.format(self.name)


class Aggregaat(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    #assets = db.relationship('Asset', secondary='asset_aggregaat', backref='premissions')
    def __repr__(self):
        return '{}'.format(self.name)


class Asset_status(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    asset_id = db.relationship('Asset', backref='asset_status')
    def __repr__(self):
        return '{}'.format(self.name)

class Asset(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    vin = db.Column(db.String(50), unique=True)
    licenseplate = db.Column(db.String(50), unique=True)
    milles = db.Column(db.Integer())
    brand = db.Column(db.Integer, db.ForeignKey('asset_brands.id'))
    type = db.Column(db.Integer, db.ForeignKey('asset_type.id'))
    status = db.Column(db.Integer, db.ForeignKey('asset_status.id'))
    aggregaten = db.relationship('Aggregaat', secondary='asset_aggregaat', backref='assets')
    def __repr__(self):
        return '{}'.format(self.name)

class Person(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    email = db.Column(db.String(50, collation='NOCASE'), unique=True)
    telegram_id = db.Column(db.String(50))
    email_confirmed_at = db.Column(db.DateTime())
    def __repr__(self):
        return '{}{}'.format(self.first_name, self.last_name)

class Person_type(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    def __repr__(self):
        return '{}'.format(self.name)

user_manager = UserManager(app, db, User)

""" 
to update db
open terminal
    1   flask db head
    2   flask db migrate -m 'name versie'
    3   flask db upgrade
"""


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

admin.add_sub_category(name="users", parent_name="Users")
admin.add_view(MyModelView(User, db.session, category="Users"))
admin.add_view(MyModelView(Role, db.session, category="Users"))
admin.add_view(MyModelView(Navbarcat, db.session, category="Users"))
admin.add_view(MyModelView(Navbarbutton, db.session, category="Users"))

admin.add_sub_category(name="assets", parent_name="Assets")
admin.add_view(MyModelView(Asset, db.session, category="Assets"))
admin.add_view(MyModelView(Asset_brands, db.session, category="Assets"))
admin.add_view(MyModelView(Asset_type, db.session, category="Assets"))
admin.add_view(MyModelView(Aggregaat, db.session, category="Assets"))
admin.add_view(MyModelView(Asset_status, db.session, category="Assets"))

admin.add_sub_category(name="persons", parent_name="Persons")
admin.add_view(MyModelView(Person, db.session, category="Persons"))
admin.add_view(MyModelView(Person_type, db.session, category="Persons"))
