from flask import request, session, Blueprint, jsonify
from werkzeug.security import check_password_hash
from database.conectar import db

login = Blueprint("/login", __name__)



@login.route("/login", methods=["POST"])
def verificar_login():
    data = request.get_json()
    correo = data.get("correo")
    password = data.get("password")
    
    if not correo or not password:
        return jsonify({
            "mensaje": "Favor de confirmar los datos"
        }), 400
        
    try:
        db.cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo, ))
        usuario = db.cursor.fetchone()
        
        if usuario and check_password_hash(usuario["contrasena"], password):
            session["user_id"] = usuario["id"]
            session["nombre"] = usuario["nombre"]
            return jsonify({
                "mensaje": "Login correcto"
            }), 200
            
        return jsonify({
            "mensaje": "Usuario o contrasena incorrectos"
        }), 401

                
    except Exception as e:
        print("Error ", e)
        return jsonify({
            "mensaje": "Error interno del servidor"
        }), 500