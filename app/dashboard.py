import logQSO
import flask

from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post, Addqsotodb
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/admin/dashboard")
@login_required
def dashboard():
    return render_template("/dashboard/dashboard.html", title='Dashboard')


@app.route("/admin/addqso")
@login_required
def addqso():
    return render_template("/dashboard/addqso.html", title='QSO Form')

@app.route("/admin/addqsotodb", methods=['GET', 'POST'])
#@login_required
def addqsotodb():
    return render_template("/dashboard/addqsotodb.html", title='QSO to db Form')


#TODO: combine submitqso_form and submitqso(api), also prevent form from submitting blank data (form validation)
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