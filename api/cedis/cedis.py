from flask import Blueprint, jsonify, request
from database.conectar import db

pedido_cedis_bp = Blueprint("pedido_cedis", __name__)

#API para el select 
@pedido_cedis_bp.route("/mostrar_productos_cedis", methods=["GET"])
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

@pedido_cedis_bp.route("/crear_pedido", methods=["POST"])
def crear_pedido():
    try: 
        #Obtener los datos enviados desde el front
        data = request.get_json()

        producto_id = data.get("producto_id")
        cantidad_solicitar = data.get("cantidad")

        #Validar los datos
        if not producto_id:
            return jsonify({
                "mensaje": "Debe enviar un producto"
            }), 400

        if not cantidad_solicitar:
            return jsonify({
                "mensaje": "Debe enviar una cantidad"
            }), 400
        
        if cantidad_solicitar <= 0:
            return jsonify({
                "mensaje": "La cantidad debe ser mayor a 0"
            }), 400
        
        #Iniciamos la transaccion 
        db.connection.start_transaction()

        #Buscar stock del producto en el cedis
        db.cursor.execute("""
            SELECT stock FROM inventario_cedis WHERE producto_id = %s
        """, (producto_id, ))

        resultado = db.cursor.fetchone()

        #Verificar que exista el producto
        if resultado is None:
            db.connection.rollback()
            return jsonify({
                "mensaje": "Producto no encontrado en CEDIS"
            }), 404
        
        stock = resultado[0]

        #Validar stock
        if cantidad_solicitar > stock:
            db.connection.rollback()
            return jsonify({
                "mensaje": f"Stock insuficiente. Disponible {stock}"
            }), 400
        
        #Si todo sale bien
        db.connection.commit()
        return jsonify({
            "mensaje": "Validacion exitosa",
            "stock_disponible": stock
        }), 200

    except Exception as e:
        #Vuelve atras
        db.connection.rollback()
        return jsonify({
            "mensaje": f"Error interno del servidor {e}"
        })