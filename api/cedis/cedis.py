from flask import Blueprint, jsonify
from database.conectar import db

pedido_cedis_bp = Blueprint("pedido_cedis", __name__)

#API para el select 
@pedido_cedis_bp.route("/mostrar_productos_cedis")
def mostrar_productos_cedis():
    try:
        db.cursor.execute("SELECT descripcion FROM productos")
        resultado = db.cursor.fetchall()
        return jsonify(resultado), 200
        
    except Exception as e:
        print(e)
        return jsonify({
            "mensaje": "Error en el servidor"
        }), 500