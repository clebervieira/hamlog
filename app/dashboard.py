import logQSO
import flask

from app import app
from app.forms import RegistrationForm, LoginForm
from flask import render_template, request, url_for, flash, redirect


@app.route("/admin/dashboard")
def dashboard():
    return render_template("/dashboard/dashboard.html", title='Dashboard')


@app.route("/admin/addqso")
def addqso():
    return render_template("/dashboard/addqso.html", title='QSO Forms')


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


@app.route('/submitqso', methods=['POST'])
def submitqso():
    log = logQSO.LogNewQSO("call_sign", "signal_sent", "signal_received")
    jsonPost=flask.request.json
    log.write_qso(jsonPost["callSign"],jsonPost["signalSent"],jsonPost["signalReceived"])
    return "<h1>QSO sent</h1>"


@app.route("/admin/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('/dashboard/register.html', title='Register', form=form)


@app.route("/admin/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'clebervieira@gmail.com' and form.password.data == 'chiclete':
            flash('You have been logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('/dashboard/login.html', title='Login', form=form)