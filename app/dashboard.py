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
    jsonPost=flask.request.json
    logQSO.LogNewQSO.write_qso(jsonPost[""],jsonPost["callSign"],jsonPost["signalReceived"],jsonPost["signalSent"])
    return "<h1>QSO sent</h1>"


