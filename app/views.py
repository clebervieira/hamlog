import logQSO
from app import app

from flask import render_template

@app.route("/")
def index():
    return render_template("/public/index.html")

@app.route("/qso")
def qso():
    my_qso = logQSO.ReadQSO.read_qso("")
    return render_template("/public/qso.html", my_qso=my_qso)

@app.route('/readqso', methods=['GET'])
def readqso():
    #jsonPost=flask.request.json
    #logQSO.LogNewQSO.write_qso(jsonPost[""],jsonPost["callSign"],jsonPost["signalReceived"],jsonPost["signalSent"])
    my_qso = logQSO.ReadQSO.read_qso("")
    return my_qso
