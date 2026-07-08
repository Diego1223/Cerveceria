from flask import Blueprint, render_template

estado_route_bp = Blueprint("estado_route", __name__)

@estado_route_bp.route("/estado_pedido")
def estado():
    return render_template("estado_pedido.html")