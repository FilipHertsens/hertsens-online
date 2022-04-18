from app import db, app, admin
from flask import abort, redirect
from flask_user import UserMixin, UserManager
from flask_login import current_user
from buttons import navbuttons
from flask_admin.contrib.sqla import ModelView
from tables import Checks as Check_table
from tables import Asset, Asset_brands, Asset_model, Asset_status, Asset_type, Check_cat, Person
import time

def liinli(list1,list2):
    for item in list1:
        if item in list2:
            return True
    return False


def getChecks(check_cat, asset):

    checks = Check_table.query.all()
    check_list = []
    model = Asset_model.query.filter_by(id=asset.model)
    brand = Asset_brands.query.filter_by(id=asset.brand)
    for check in checks:
        valid = False

        list1 = [check.incl_type, check.incl_model, check.incl_assets, check.incl_aggregaten, check.incl_brands]
        list2 = [asset.types, model, asset, asset.aggregaten, brand]
        for cat in check.incl_cat_checks:
            if check_cat.name == cat.name:
                valid = True

        for x in range(len(list1)):
            if list1[x] != [] and valid:
                if not liinli(list1[x], list2[x]):
                    valid = False

        if valid:
            check_list.append(check)
    return check_list





check_cat = Check_cat.query.filter_by(name='KOH').first()
asset = Asset.query.filter_by(name='H079 demo banden').first()
start_time = time.time()
print(getChecks(check_cat=check_cat, asset=asset))
print("--- %s seconds ---" % (time.time() - start_time))

