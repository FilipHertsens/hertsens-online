from flask import render_template, redirect, url_for, request, flash, current_app, Response
from flask_login import login_user, logout_user, current_user
from flask_user import roles_required
from forms import LoginForm, RegisterForm, Asset_selector, repair_request
from tables import User, Asset, Repair_request, Status_request, Datatable_filters
import datetime
from app import app, db, mail
from werkzeug.security import generate_password_hash, check_password_hash
from functions import uploading_files, logged_in, getLocation, getDatatableFilterBN
from flask_mail import Message
from sending_mail import send_mail, send_repair_request
from API.Balert import get_all_data, fig_band
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pprint import pprint
import json


@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html',user=current_user, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        next_url = request.form.get("next")
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                if next_url:
                    return redirect(next_url)
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
        new_user = User(first_name=form.first_name.data,
                        last_name=form.last_name.data, email=form.email.data,
                       password=hashed_password,email_confirmed_at=datetime.datetime.now())
        db.session.add(new_user)
        db.session.commit()
        flash('Thanks for signing up. \nThe administrator will review it as soon as possible.', "alert alert-warning")
        return redirect(url_for('index'))

    return render_template('signup.html', form=form,user=current_user)


@app.route('/select_asset', methods=['GET', 'POST'])
@logged_in
def select_asset():
    error = None
    form = Asset_selector()
    if form.validate_on_submit():
        asset = Asset.query.filter_by(name=form.autocomplete.data).first()
        if asset != None:
            current_user.current_asset_id = asset.id
            favorite = form.add_favorites.data
            if favorite:
                current_user.favoriteassets.append(asset)
            next_url = request.form.get("next")
            db.session.commit()
            if next_url:
                return redirect(next_url)
        else:
            error = 'No asset withe this name.'
            form = Asset_selector()
            return render_template('select_asset.html', form=form, error=error, user=current_user)
        form = LoginForm()
        return render_template('index.html', user=current_user, form=form, error=error)
    else:
        get_asset = request.args.get("autocomplete")
        next_url = request.args.get("next")
        if get_asset != None:
            current_user.current_asset = Asset.query.filter_by(id=get_asset).first()
            db.session.commit()
            if next_url:
                return redirect(next_url)
            return render_template('index.html', user=current_user, form=form)
        error = None
        return render_template('select_asset.html', form=form, error=error, user=current_user)

@app.route('/logout')
@logged_in
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/js/get/assets')
def getAssets():
    dictAsset = {}
    assets = Asset.query.all()
    for asset in assets:
        dictAsset[asset.id] = {'name':asset.name, 'id':asset.id}
    return dictAsset

@app.route('/js/get/tireimg/<id>')
def tireImg(id):

    fig = fig_band(int(id))
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/checks')
@logged_in
@roles_required('Admin')
def checks():
    if current_user.current_asset_id == None:
        return redirect(url_for('select_asset', next=request.url))
    form = LoginForm()
    return render_template('walkaround.html', user=current_user, form=form)


@app.route('/repairRequest', methods=['GET', 'POST'])
@logged_in
def repairRequest():
    form = repair_request()
    form2 = Asset_selector()
    if form.validate_on_submit():
        uploads = uploading_files(data=form.files.data)

        asset_str = form2.autocomplete.data
        asset = Asset.query.filter_by(name=asset_str).first()
        if asset == None:
            error = 'No asset withe this name.'
            return render_template('repairrequest.html', error=error, user=current_user, form=form, form2=form2)
        r = Repair_request(
            asset=asset,
            description=form.description.data,
            demage_case=form.damage_case.data,
            depannage_required=form.depannage_required.data,
            files=json.dumps(uploads[1]),
            user=current_user,
            status=Status_request.query.filter_by(id=1).first(),
            request_time = datetime.datetime.now()
        )
        db.session.commit()
        flash('Thanks for the repair request. We will get back to you as soon as possible', "alert alert-success")
        # send email
        to = ["garage@hertsens.eu"]
        # send_repair_request(request=r)
        return redirect(url_for('index'))
    error = None
    return render_template('repairrequest.html', error=error, user=current_user, form=form, form2=form2)

@app.route('/tirepressure')
@logged_in
def tirepressure():
    error = None
    if current_user.current_asset_id == None:
        return redirect(url_for('select_asset', next=request.url))
    tyres = get_all_data(name=current_user.current_asset)
    pprint(tyres)
    con_tyres = None
    if tyres != None:
        if '@connected_to_id' in tyres:
            if tyres['@connected_to_id'] != tyres['@id']:
                con_tyres = get_all_data(id=tyres['@connected_to_id'])
    return render_template('tirepressure.html', error=error, user=current_user, tyres=tyres, con_tyres=con_tyres)

@app.route('/account')
@logged_in
def account():
    return render_template('account.html', user=current_user)

@app.route('/assetlocation')
@logged_in
def assetlocation():
    lat, lon = getLocation(current_user.current_asset.id)
    return render_template('assetlocation.html', user=current_user, lat=lat, lon=lon)

@app.route('/assetlist')
@logged_in
def assetlist():
    data = Asset.query.all()
    filter_buttons = getDatatableFilterBN(path='/assetlist', user=current_user)
    return render_template('assetlist.html', user=current_user, data=data, but=filter_buttons, tableKeys=data[0].tableKeys())

@app.route('/repairRequestList')
@logged_in
def repairRequestList():
    data = Repair_request.query.all()
    filter_buttons = getDatatableFilterBN(path='/repairRequestList', user=current_user)
    return render_template('repairrequestslist.html', user=current_user, data=data, but=filter_buttons, tableKeys=data[0].tableKeys())

@app.route('/savesavestates', methods=['POST'])
def savesavestates():
    if request.method == "POST":
        name = request.json['name']
        Datatable_filters(
            path=request.json['path'],
            bnName= name,

            bnValue=request.json['data'],
            user=current_user
        )
        db.session.commit()
        return json.dumps({'succes':f'Filter state saved as {name}'})
