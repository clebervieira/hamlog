import logQSO
import flask

from app import app
from app.forms import RegistrationForm, LoginForm

from flask import render_template, request, url_for

app.config['SECRET_KEY'] = '134460b73094491dc7cce1d6de667009'

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


@app.route("/admin/register")
def register():
    form = RegistrationForm()
    return render_template('/dashboard/register.html', title='Register', form=form)

@app.route("/admin/login")
def login():
    form = LoginForm()
    return render_template('/dashboard/login.html', title='Login', form=form)