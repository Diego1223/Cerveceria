#Esta API consultara todos los productos disponibles de nuestra tienda
from database.conectar import db
from flask import Blueprint, jsonify

productos_bp = Blueprint("productos", __name__)

@productos_bp.route("/numProductos", methods=["GET"])
def num_productos():
    try:
        db.cursor.execute("SELECT COUNT(*) AS total_registros FROM productos")
        resultado = db.cursor.fetchone()
        return jsonify({
            "mensaje": "Valido",
            "numero_productos": resultado
        }), 200
    except Exception as e:
        return jsonify({
            "mensaje": "Error interno del servidor"
        }), 500
    
