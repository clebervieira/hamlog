import logQSO
import flask

from app import app

from flask import render_template


@app.route("/admin/dashboard")
def dashboard():
    return render_template("/dashboard/dashboard.html")


@app.route("/admin/addqso")
def addqso():
    return render_template("/dashboard/addqso.html")


@app.route('/submitqso', methods=['POST'])
def submitqso():
    log = logQSO.LogNewQSO("call_sign", "signal_sent", "signal_received")
    jsonPost=flask.request.json
    log.write_qso(jsonPost["callSign"],jsonPost["signalSent"],jsonPost["signalReceived"])
    return "<h1>QSO sent</h1>"


