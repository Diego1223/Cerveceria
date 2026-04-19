from flask import Blueprint, render_template

historial_movimientos = Blueprint("historial_movimientos", __name__)

@historial_movimientos.route("/historial")
def historial():
    return render_template("historial.html")