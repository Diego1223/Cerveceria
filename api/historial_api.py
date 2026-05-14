from flask import Blueprint, jsonify
from database.conectar import db
from auth.admin import is_admin
historial_bp = Blueprint("historial_api", __name__)

@historial_bp.route("/mostrar_historial", methods=["GET"])
@is_admin
def mostrar_historial():
    try:
        db.cursor.execute("SELECT * FROM historial_stock")
        datos = db.cursor.fetchall()

        return jsonify(datos), 200
    
    except Exception as e:
        return jsonify({
            "mensaje": f"Error interno del servidor {e}"
        }), 500