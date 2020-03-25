import logQSO
from app import app

from flask import render_template

@app.route("/")
def index():
    return render_template("/public/index.html")

@app.route("/qso")
def qso():
    log = logQSO.LogNewQSO("call_sign", "signal_sent", "signal_received")
    view_log = log.build_string()

    return render_template("/public/qso.html", view_log=view_log)

@app.route('/readqso', methods=['GET'])
def readqso():
    log = logQSO.LogNewQSO("call_sign", "signal_sent", "signal_received")
    view_log = log.build_string()
    return view_log
