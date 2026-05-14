from flask import Flask, Blueprint, render_template

trabajadores_bp = Blueprint("trabajadores_route", __name__)

@trabajadores_bp.route("/lista_trabajadores")
def lista_trabajadores():
    return render_template("trabajadores.html")