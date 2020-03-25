from app import app

from flask import render_template

@app.route("/")
def index():
        return render_template("/public/index.html")

@app.route("/qso")
def qso():
        return render_template("/public/qso.html")
