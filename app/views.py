import logQSO
from app import app
from flask import render_template


posts = [
    {
        'author': 'Cleber Vieira',
        'title': 'WWDX Contest',
        'content': 'Info about radio setup and band plan',
        'date_posted': 'March 17, 2020'
    },
    {
        'author': 'Cleber Vieira',
        'title': 'WWDX Contest Log',
        'content': 'List of contact during contest',
        'date_posted': 'March 20, 2020'
    },
]
@app.route("/")
def index():
    return render_template("/public/index.html", title='Home')


@app.route("/qso")
def qso():
    log = logQSO.LogNewQSO("call_sign", "signal_sent", "signal_received")
    view_log = log.build_string()
    return render_template("/public/qso.html", view_log=view_log, title='QSO List')


@app.route("/blog")
def blog():
    return render_template("/public/blog.html", title='Blog', posts=posts)

#POSTMAN route
@app.route('/readqso', methods=['GET'])
def readqso():
    log = logQSO.LogNewQSO("call_sign", "signal_sent", "signal_received")
    view_log = log.build_string()
    return view_log
