from flask import Blueprint, render_template
from auth.admin import is_admin

route_productos_bp = Blueprint("route_productos", __name__)

@route_productos_bp.route("/numProductos")
@is_admin
def route_productos():
    return render_template("productos.html")

@route_productos_bp.route("/editar")
@is_admin
def editar():
    return render_template("editar_producto.html")