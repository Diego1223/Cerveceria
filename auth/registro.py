from flask import Flask, request, jsonify, Blueprint
from werkzeug.security import generate_password_hash
from database.conectar import db

registro_api = Blueprint("registro_api", __name__)

@registro_api.route("/registro", methods=["POST"])
def registro():
    data = request.get_json() or {}
    print(data)
    nombre = data.get("nombre")
    correo = data.get("correo")
    password = data.get("password")
    
    if not correo or not password:
        return jsonify({
            "mensaje": "Correo o contraseña obligatorios"
        }), 400
    #Verificar si el usuario ya existe
    db.cursor.execute("SELECT * FROM usuarios WHERE correo =%s", (correo,))
    if db.cursor.fetchone():
        return jsonify({
            "mensaje": "El usuario ya existe"
        }), 409
    
    #Crear hash de la contraseña
    hash_password = generate_password_hash(password)

    #Insertar en la BD
    db.cursor.execute(
        "INSERT INTO usuarios (correo, contrasena, nombre) VALUES (%s, %s, %s)", (correo, hash_password, nombre)
    )

    db.connection.commit()

    return jsonify({
        "mensaje": "Usuario registrado correctamente"
    }), 200
