from flask import Blueprint, jsonify, request, session
from database.conectar import db
from auth.admin import is_admin
editar_stock_bp = Blueprint("editar_stock", __name__)

#Esta API se usara para mostrar en el frontend los datos necesarios, la otra sera para mandarlos a la base de datos
@editar_stock_bp.route("/editar_stockV/<int:id>", methods=["GET"])
@is_admin
def editar_stock(id):
    try:
        db.cursor.execute("SELECT id, descripcion, existencias FROM productos WHERE id = %s", (id, ))
        datos = db.cursor.fetchone()

        return jsonify(datos), 200 

    except Exception as e:
        return jsonify({
            "mensaje": "Error interno del servidor"
        }), 500
     
@is_admin
def actualizar_stock():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"mensaje": "Json invalido"}), 400
        
        
        id_producto = data.get("id_producto")
        cantidad = int(data.get("cantidad"))
        tipo = data.get("tipo_movimiento") #entrada o salida
        motivo = data.get("motivo")
        firma = data.get("firma")
        descripcion = data.get("descripcion")

        #Sacamos el id del usuario del session - Usa cookies
        id_usuario = session.get("user_id")
        if tipo not in ["entrada", "salida"]:
            return jsonify({
                "mensaje": "Tipo invalido"
            }), 400
        

        #Obtener el stock actual
        db.cursor.execute(
            "SELECT existencias FROM productos WHERE id= %s", (id_producto, )
        )

        resultado = db.cursor.fetchone()

        if not resultado:
            return jsonify({
                "mensaje": "Producto no existe"
            }), 404
        
        stock_actual = resultado["existencias"]
        
        if tipo == "salida" and stock_actual < cantidad:
            return jsonify({
                "mensaje": "Stock insuficiente" 
            }), 400
        
        #Insert en historial
        db.cursor.execute("""
            INSERT INTO historial_stock (id_usuario, id_producto, tipo_movimiento, cantidad, motivo, firma, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id_usuario, id_producto, tipo, cantidad, motivo, firma, descripcion))


        #Actualizar stock
        if tipo == "entrada":
            db.cursor.execute("""
                UPDATE productos
                SET existencias = existencias + %s
                WHERE id = %s
            """ , (cantidad, id_producto))
        else:
            db.cursor.execute("""
                UPDATE productos
                SET existencias = existencias - %s
                WHERE id = %s
            """, (cantidad, id_producto))

        #Confirmar cambios
        db.connection.commit()
        return jsonify({
            "mensaje": "Stock actualizado correctamente"
        }), 200
    
    except Exception as e:
        #Rollback - si algo sale mal revierte todos los cambios
        db.connection.rollback()
        
        return jsonify({
            "mensaje": f"Ocurrio un error en el servidor {e}"
        }), 500