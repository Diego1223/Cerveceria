from flask import Blueprint, render_template

route_productos_bp = Blueprint("route_productos", __name__)

@route_productos_bp.route("/numProductos")
def route_productos():
    return render_template("productos.html")

@route_productos_bp.route("/editar")
def editar():
    return render_template("editar_producto.html")