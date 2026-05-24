from flask import Blueprint, jsonify
from database.conectar import db


cobro_api_bp = Blueprint("cobro_api", __name__)

@cobro_api_bp.route("/buscar_producto/<codigo>")
def cobro(codigo):
    try:
        db.cursor.execute("SELECT * FROM productos WHERE codigo = %s", (codigo, ))
        producto = db.cursor.fetchall()

        if not producto:
            return jsonify({
                "mensaje": "El producto no existe"
            }), 404
        return jsonify(producto), 200

    except Exception as e:
        return jsonify({
            "mensaje": "Error interno del servidor"
        }), 500