import logQSO
import flask

from app import app

from flask import render_template, request


@app.route("/admin/dashboard")
def dashboard():
    return render_template("/dashboard/dashboard.html")


@app.route("/admin/addqso")
def addqso():
    return render_template("/dashboard/addqso.html")


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

    return render_template("/dashboard/addqso.html")


@app.route('/submitqso', methods=['POST'])
def submitqso():
    log = logQSO.LogNewQSO("call_sign", "signal_sent", "signal_received")
    jsonPost=flask.request.json
    log.write_qso(jsonPost["callSign"],jsonPost["signalSent"],jsonPost["signalReceived"])
    return "<h1>QSO sent</h1>"


