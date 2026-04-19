#Aqui iran los endpoints principales de el sidebar
from flask import Blueprint, render_template
from auth.login_required import login_required
from werkzeug.security import generate_password_hash
from database.conectar import db
main = Blueprint("main", __name__)

@main.route("/")
def login():
    return render_template("login.html")

@main.route("/registrarse")
def registrarse():
    return render_template("registrarse.html")

@main.route("/index")
@login_required
def index():
    return render_template("index.html")

