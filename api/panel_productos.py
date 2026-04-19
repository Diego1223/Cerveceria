#Esta API es para mostrar todos los productos, unidades y contenido
from flask import Blueprint, jsonify
from database.conectar import db

panel_productos_bp = Blueprint("panel_productos", __name__)

@panel_productos_bp.route("/panel_productos", methods=["GET"])
def panel():
    try:
        db.cursor.execute("SELECT * FROM productos")
        productos = db.cursor.fetchall() 
        return jsonify({
            "mensaje": "Productos",
            "productos": productos
        }), 200  
    except Exception as e:
        return jsonify({
            "mensaje": "Error interno del servidor"
        }), 500
     