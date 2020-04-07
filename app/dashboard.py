import logQSO
import flask
import secrets
import os
from PIL import Image
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, AddQSOtoDbForm, UpdateAccountForm
from app.models import User, Post, Addqsotodb
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/admin/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("/dashboard/account.html", title='Account', image_file=image_file, form=form)


@app.route("/admin/dashboard")
@login_required
def dashboard():
    return render_template("/dashboard/dashboard.html", title='Dashboard')


@app.route("/admin/addqso")
@login_required
def addqso():
    return render_template("/dashboard/addqso.html", title='QSO Form')

@app.route("/admin/addqsotodb", methods=['GET', 'POST'])
@login_required
def addqsotodb():
    form = AddQSOtoDbForm()
    if form.validate_on_submit():
        addqso = Addqsotodb(callsign=form.callsign.data, signal_sent=form.signal_sent.data, signal_received=form.signal_received.data, custom_sent=form.custom_sent.data, custom_received=form.custom_received.data, frequency_used=form.frequency_used.data)
        db.session.add(addqso)
        db.session.commit()
        flash('QSO added to db!', 'success')
        return redirect(url_for('addqsotodb'))
    return render_template("/dashboard/addqsotodb.html", title='QSO to db Form', form=form)


@app.route('/submitqso_form', methods=["GET", "POST"])
def submitqso_form():
    log = logQSO.LogNewQSO("call_sign", "signal_sent", "signal_received")

    if request.method == "POST":

        req = request.form

        callSign = req["callSign"]
        signalSent = req.get("signalSent")
        signalReceived = request.form["signalReceived"]

        log.write_qso(callSign, signalSent, signalReceived)

    return render_template("/dashboard/addqso.html", tittle='QSO')

#POSTMAN routes
@app.route('/submitqso', methods=['POST'])
def submitqso():
    log = logQSO.LogNewQSO("call_sign", "signal_sent", "signal_received")
    jsonPost=flask.request.json
    log.write_qso(jsonPost["callSign"],jsonPost["signalSent"],jsonPost["signalReceived"])
    return "<h1>QSO sent</h1>"


@app.route("/admin/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('/dashboard/register.html', title='Register', form=form)


@app.route("/admin/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('/dashboard/login.html', title='Login', form=form)

@app.route("/admin/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

