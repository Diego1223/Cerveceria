from flask import Blueprint, jsonify, request
from auth.admin import is_admin
from database.conectar import db


editar_info_api_bp = Blueprint("editar_info_api", __name__)

@editar_info_api_bp.route("/editar_trabajadorView/<int:id>", methods=["GET"])
@is_admin
def editar_trabajador(id):
    try:
        db.cursor.execute ("SELECT nombre, correo, rfc, numero_seguro_social, antiguedad FROM usuarios WHERE id = %s", (id, ))
        datos = db.cursor.fetchone()
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({
            "mensaje": f"Error interno del servidor {e}"
        }), 500
    
@editar_info_api_bp.route("/editar_trabajador/", methods=["PUT"])
def actualizar_trabajador():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "mensaje": "Json Invalido"
            }), 400
        
        id_trabajador = data.get("id_trabajador")
        nombre = data.get("nombre")
        correo = data.get("correo")
        rfc = data.get("rfc")
        seguro_social = data.get("seguro_social")

        db.cursor.execute("""
            UPDATE usuarios
            SET 
                nombre = %s,
                correo = %s,
                rfc = %s,
                numero_seguro_social = %s
            WHERE id = %s        
        """, (nombre, correo, rfc,seguro_social, id_trabajador))
        db.connection.commit()


        return jsonify({
            "mensaje": "Informacion del trabajador actualizada correctamente"
        }) 
    except Exception as e:
        return jsonify({
            "mensaje": f"Error interno del servidor {e}"
        }), 500