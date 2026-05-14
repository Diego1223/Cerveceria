from flask import Blueprint, jsonify
from database.conectar import db
from auth.admin import is_admin
trabajadores_api = Blueprint("trabajadores_api", __name__)

@trabajadores_api.route("/trabajadores")
def trabajadores():
    try:
        #Where admin = 2 porque esos son trabajadores, el 1 son administradores
        db.cursor.execute("SELECT id, nombre, correo, rfc, numero_seguro_social, antiguedad FROM usuarios WHERE admin = 2")
        trabajadores = db.cursor.fetchall()
        return jsonify(trabajadores), 200
    
    except Exception as e:
        return jsonify({
            "mensaje": "Ocurrio un error en el servidor"
        }), 500