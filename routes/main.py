#Aqui iran los endpoints principales de el sidebar
from flask import Blueprint, render_template
from auth.login_required import login_required
from auth.admin import is_admin

main = Blueprint("main", __name__)

@main.route("/")
def login():
    return render_template("login.html")

@main.route("/registrarse")
def registrarse():
    return render_template("registrarse.html")

@main.route("/index")
@login_required
@is_admin
def index():
    return render_template("index.html")

@main.route("/pedidos")
@login_required
@is_admin
def pedidos():
    return render_template("pedidos.html")
