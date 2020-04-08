import logQSO
from app import app
from app.models import Post, Qso
from flask import render_template, flash



@app.route("/")
def index():
    return render_template("/public/index.html", title='Home')


@app.route("/qso")
def qso():
    log = logQSO.LogNewQSO("call_sign", "signal_sent", "signal_received")
    view_log = log.build_string()
    return render_template("/public/qso.html", view_log=view_log, title='QSO List')

@app.route("/qsolist")
def qso_list():
    logs = Qso.query.all()
    return render_template("/public/qso_list.html", title='QSO List', logs=logs)


@app.route("/blog")
def blog():
    posts = Post.query.all()
    return render_template("/public/blog.html", title='Blog', posts=posts)

#POSTMAN route
@app.route('/readqso', methods=['GET'])
def readqso():
    log = logQSO.LogNewQSO("call_sign", "signal_sent", "signal_received")
    view_log = log.build_string()
    return view_log
