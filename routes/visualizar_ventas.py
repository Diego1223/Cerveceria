from flask import Blueprint, render_template

visualizar_ventas_route_bp = Blueprint("visualizar_V", __name__)

@visualizar_ventas_route_bp.route("/visualizar_ventas")
def visualizar():
    return render_template("visualizar_ventas.html")