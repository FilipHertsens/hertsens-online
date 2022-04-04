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

check_answers_check = db.Table('check_answers_check',
    db.Column('check_id', db.Integer(), db.ForeignKey('checks.id')),
    db.Column('check_answers_id', db.Integer(), db.ForeignKey('check_answers.id')))

check_person = db.Table('check_person',
    db.Column('check_id', db.Integer(), db.ForeignKey('checks.id')),
    db.Column('person_id', db.Integer(), db.ForeignKey('person.id')))

check_type = db.Table('check_type',
    db.Column('check_id', db.Integer(), db.ForeignKey('checks.id')),
    db.Column('Asset_type_id', db.Integer(), db.ForeignKey('asset_type.id')))

check_model = db.Table('check_model',
    db.Column('check_id', db.Integer(), db.ForeignKey('checks.id')),
    db.Column('Asset_model_id', db.Integer(), db.ForeignKey('asset_model.id')))

check_assets = db.Table('check_assets',
    db.Column('check_id', db.Integer(), db.ForeignKey('checks.id')),
    db.Column('asset_id', db.Integer(), db.ForeignKey('asset.id')))

check_no_assets = db.Table('check_no_assets',
    db.Column('check_id', db.Integer(), db.ForeignKey('checks.id')),
    db.Column('asset_id', db.Integer(), db.ForeignKey('asset.id')))

check_aggregaten = db.Table('check_aggregaten',
    db.Column('check_id', db.Integer(), db.ForeignKey('checks.id')),
    db.Column('aggregaat_id', db.Integer(), db.ForeignKey('aggregaat.id')))

check_cat_checks = db.Table('check_cat_checks',
    db.Column('check_id', db.Integer(), db.ForeignKey('checks.id')),
    db.Column('check_cat_id', db.Integer(), db.ForeignKey('check_cat.id')))

check_roles = db.Table('check_roles',
    db.Column('check_id', db.Integer(), db.ForeignKey('checks.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

check_brands = db.Table('check_brands',
    db.Column('check_id', db.Integer(), db.ForeignKey('checks.id')),
    db.Column('asset_brands_id', db.Integer(), db.ForeignKey('asset_brands.id')))

person_type_person = db.Table('person_type_person',
    db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
    db.Column('person_type_id', db.Integer(), db.ForeignKey('person_type.id')))

type_asset_type = db.Table('type_asset_type',
    db.Column('asset_id', db.Integer(), db.ForeignKey('asset.id')),
    db.Column('asset_type_id', db.Integer(), db.ForeignKey('asset_type.id')))

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


class Asset_model(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    asset_id = db.relationship('Asset', backref='asset_model')
    def __repr__(self):
        return '{}'.format(self.name)


class Asset_type(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    def __repr__(self):
        return '{}'.format(self.name)


class Aggregaat(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
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
    wacs_id = db.Column(db.Integer(), unique=True)
    name = db.Column(db.String(50), unique=True)
    vin = db.Column(db.String(50), unique=True)
    licenseplate = db.Column(db.String(50))
    milles = db.Column(db.Integer())
    brand = db.Column(db.Integer, db.ForeignKey('asset_brands.id'))
    model = db.Column(db.Integer, db.ForeignKey('asset_model.id'))
    status = db.Column(db.Integer, db.ForeignKey('asset_status.id'))
    aggregaten = db.relationship('Aggregaat', secondary='asset_aggregaat', backref='assets')
    types = db.relationship('Asset_type', secondary='type_asset_type', backref='types')
    def __repr__(self):
        return '{}'.format(self.name)




class Person(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    email = db.Column(db.String(50, collation='NOCASE'), unique=True)
    telegram_id = db.Column(db.String(50))
    email_confirmed_at = db.Column(db.DateTime())
    type = db.relationship('Person_type', secondary='person_type_person', backref='persons')
    def __repr__(self):
        return '{}{}'.format(self.first_name, self.last_name)


class Person_type(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    def __repr__(self):
        return '{}'.format(self.name)


class Checks(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(25), unique=True)
    description = db.Column(db.Text)
    photo = db.Column(db.Boolean, default=False, nullable=True)
    photo_sporadic = db.Column(db.Boolean, default=False, nullable=True)
    answers = db.relationship('Check_answers', secondary='check_answers_check', backref='checks')
    incl_person = db.relationship('Person', secondary='check_person', backref='checks')
    incl_type = db.relationship('Asset_type', secondary='check_type', backref='checks')
    incl_model = db.relationship('Asset_model', secondary='check_model', backref='checks')
    incl_assets = db.relationship('Asset', secondary='check_assets', backref='checks')
    incl_aggregaten = db.relationship('Aggregaat', secondary='check_aggregaten', backref='checks')
    excl_assets = db.relationship('Asset', secondary='check_no_assets', backref='nochecks')
    incl_cat_checks = db.relationship('Check_cat', secondary='check_cat_checks', backref='checks')
    incl_roles = db.relationship('Role', secondary='check_roles', backref='checks')
    incl_brands = db.relationship('Asset_brands', secondary='check_brands', backref='checks')
    def __repr__(self):
        return '{}'.format(self.name)


class Check_answers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(25), unique=True)
    description = db.Column(db.Text)
    def __repr__(self):
        return '{}'.format(self.name)


class Check_cat(db.Model):
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
admin.add_view(MyModelView(Asset_model, db.session, category="Assets"))
admin.add_view(MyModelView(Aggregaat, db.session, category="Assets"))
admin.add_view(MyModelView(Asset_status, db.session, category="Assets"))

admin.add_sub_category(name="persons", parent_name="Persons")
admin.add_view(MyModelView(Person, db.session, category="Persons"))
admin.add_view(MyModelView(Person_type, db.session, category="Persons"))

admin.add_sub_category(name="checks", parent_name="Checks")
admin.add_view(MyModelView(Checks, db.session, category="Checks"))
admin.add_view(MyModelView(Check_answers, db.session, category="Checks"))
admin.add_view(MyModelView(Check_cat, db.session, category="Checks"))