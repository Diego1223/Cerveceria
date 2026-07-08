from flask import Blueprint, jsonify, request, session
from database.conectar import db

pedido_cedis_bp = Blueprint("pedido_cedis", __name__)

#API para el select 
@pedido_cedis_bp.route("/mostrar_productos_cedis", methods=["GET"])
def mostrar_productos_cedis():
    try:
        db.cursor.execute("SELECT descripcion, codigo FROM productos")
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
        usuario_id = session.get("user_id")
        observaciones = data.get("observaciones")
        productos = data.get("productos")
        
        if not productos:
            return jsonify({
                "mensaje": "Pedido a cedis invalido"
            }), 400

        #Limpiar cualquier transaccion vieja 
        if db.connection.in_transaction:
            db.connection.rollback()

        #Iniciamos la transaccion 
        db.connection.start_transaction()
        productos_validos = []

        for x in productos:
            codigo = x.get("codigo")
            #Lo formateamos a int por si llega como string
            cantidad = int(x.get("cantidad"))

            if not codigo or not cantidad:
                db.connection.rollback()
                return jsonify({
                    "mensaje": "Producto incompleto"
                }), 400
            
            if cantidad <= 0:
                db.connection.rollback()
                return jsonify({
                    "mensaje": "La cantidad debe ser mayor a 0"
                }) 
            db.cursor.execute(
                """
                SELECT id, codigo, descripcion FROM productos WHERE codigo = %s
                """, (codigo, )
            )
            resultado_productos = db.cursor.fetchone()

            if resultado_productos is None:
                db.connection.rollback()
                return jsonify({
                    "mensaje": f"Producto {codigo} no existe"
                }), 404
            
            producto_id = resultado_productos["id"]

        
            #Buscar stock del producto en el cedis
            db.cursor.execute("""
                SELECT stock FROM inventario_cedis WHERE producto_id = %s
            """, (producto_id,))

            resultado = db.cursor.fetchone()

            #Verificar que exista el producto
            if resultado is None:
                db.connection.rollback()
                return jsonify({
                    "mensaje": "Producto no encontrado en CEDIS"
                }), 404
            stock = resultado["stock"]

            if cantidad > stock:
                db.connection.rollback()
                return jsonify({
                    "mensaje": f"Stock insuficiente. Disponible {stock}"
                }), 300

        
            productos_validos.append({
                "producto_id": producto_id,
                "cantidad": cantidad
            })

        #Crear pedido
        db.cursor.execute(
            """
                INSERT INTO pedido_cedis (usuario_id, observaciones) VALUES (%s, %s)
            """, (usuario_id, observaciones)
        )
        #lastrowid sirve para obtener el  ID generado automaticamente de la ultima fila insertada
        pedido_id = db.cursor.lastrowid

        #Creando detalles
        for producto in productos_validos:
            db.cursor.execute(
                """
                INSERT INTO detalle_pedido_cedis (pedido_id, producto_id, cantidad) VALUES (%s, %s, %s)
                """, (pedido_id, producto["producto_id"], producto["cantidad"])
            )
        
        #Si todo sale bien commit
        db.connection.commit()
        return jsonify({
            "mensaje": "Pedido creado correctamente",
            "pedido_id": pedido_id
        }), 201
    
    except Exception as e:
        import traceback
        #Vuelve atras
        db.connection.rollback()

        traceback.print_exc()

        return jsonify({
            "mensaje": str(e)
        }), 500

#Mostrar ultimo pedido
#Esto lo usaremos para poder aprobar el pedido
@pedido_cedis_bp.route("/id_pedido_cedis", methods=["GET"])
def obtener_id_pedidoCedis():
    try:
        #ORDER BY id DESC -> ordena de mayor a menor (el mas nuevo primero)
        #LIMIT 1 -> solo devuelve un registro, el mas reciente
        db.cursor.execute("SELECT id FROM pedido_cedis ORDER BY id DESC LIMIT 1")
        resultado = db.cursor.fetchone()

        #Si existe una fila, toma el primer valor (osea el id), si npo existe ninguna fila, asigna None
        id_pedido = resultado["id"] if resultado else None

        return jsonify(id_pedido)
    except Exception as e:
        print("ERROR: ", str(e))
        return jsonify({
            "mensaje": f"Error interno del servidor {e}"
        })
#Ver detalles del pedido cedis, lo usaremos para darle seguimiento al pedido 
@pedido_cedis_bp.route("/visualizar_pedido", methods=["GET"])
def visualizar_pedido():
    try:
        db.cursor.execute("SELECT * FROM pedido_cedis ORDER BY id DESC LIMIT 1")
        data = db.cursor.fetchone()

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "mensaje": f"Error interno del servidor {e}"
        }), 500

#Aprobar pedidos
#Recibimos el id desde la URL
@pedido_cedis_bp.route("/aprobar_pedido/<int:pedido_id>", methods=["PUT"])
def aprobar_pedido(pedido_id):
    try:
        db.connection.start_transaction()

        #Buscar pedido
        db.cursor.execute(
            """
            SELECT estado FROM pedido_cedis WHERE id = %s
            """, (pedido_id, )
        )

        pedido = db.cursor.fetchone()

        if pedido is None:
            db.connection.rollback()
            return jsonify({
                "mensaje": "Pedido no encontrado"
            }), 404
        
        if pedido["estado"] != "PENDIENTE":
            db.connection.rollback()

            return jsonify({
                "mensaje": "El pedido ya fue procesado"
            }), 400
        
        #Obtener detalles
        db.cursor.execute(
            """
                SELECT producto_id, cantidad 
                FROM detalle_pedido_cedis
                WHERE pedido_id = %s
            """, (pedido_id, )
        )

        detalles = db.cursor.fetchall()

        for detalle in detalles:
            producto_id = detalle["producto_id"]
            cantidad = detalle["cantidad"]

            #FOR update bloquea las demas filas hasta terminar la transaccion 
            db.cursor.execute(
                """
                SELECT stock FROM inventario_cedis WHERE producto_id = %s FOR UPDATE
                """, (producto_id, )
            )
            inventario = db.cursor.fetchone()

            if inventario is None:
                db.connection.rollback()
                return jsonify({
                    "mensaje": "Producto no existe en CEDIS"
                }), 404
            
            if inventario["stock"] < cantidad:
                db.connection.rollback()
                return jsonify({
                    "mensaje": "Stock insuficiente"
                }), 400
            
            #Descontar del inventario 
            #Busca el producto con el id que le dimos y solo lo actualiza si tiene al menos
            #10 unidades disponibles
            #Operacion atomica
            db.cursor.execute(
                """
                UPDATE inventario_cedis
                SET stock = stock - %s
                WHERE producto_id = %s 
                AND stock >= 10               
                """, (cantidad, producto_id)
            )

            #Cambiar el estado
            db.cursor.execute(
                """
                UPDATE pedido_cedis
                SET estado = 'APROBADO'
                WHERE id =%s    
                """, (pedido_id,)
            )

            db.connection.commit()
            return jsonify({
                "mensaje": "Pedido aprobado"
            }), 200
        
    except Exception as e:
        return jsonify({
            "mensaje": f"Ocurrio un error {e}"
        }),


@pedido_cedis_bp.route("/recibir_pedido/<int:pedido_id>", methods=["PUT"])
def recibir_pedido(pedido_id):
    try:
        db.connection.start_transaction()
        db.cursor.execute(
            """
            SELECT estado FROM pedido_cedis
            WHERE id = %s
            """, (pedido_id)
        )

        pedido = db.cursor.fetchone()

        if pedido is None:
            db.connection.rollback()
            return jsonify({
                "mensaje": "Pedido no existe"
            }), 404
        
        if pedido["estado"] != "EN_TRANSITO":
            db.connection.rollback()
            return jsonify({
                "mensaje": "El pedido no esta en transito"
            }), 400
        
        #obtener productos
        db.cursor.execute("""
            SELECT producto_id, cantidad 
            FROM detalle_pedido_cedis
            WHERE pedido_id = %s
            """, (pedido_id, ))
        
        detalles = db.cursor.fetchall()

        for detalle in detalles:
            producto_id = detalle["producto_id"]
            cantidad = detalle["cantidad"]

            #Inventario en sucursal
            #FOR UPDATE evita que otras transacciones modifiquen la fila seleccionada hasta que la actual termine
            #con un commit o un rollback
            db.cursor.execute(
            """
                SELECT stock FROM inventario_sucursal WHERE producto_id = %s
                FOR UPDATE
            """, (producto_id,))

            inventario = db.cursor.fetchone()

            if inventario:
                db.cursor.execute("""
                    UPDATE inventario_sucursal
                    SET stock = stock + %s
                    WHERE producto_id = %s
                """, (cantidad,producto_id))
            else:
                db.cursor.execute("""
                    INSERT INTO inventario_sucursal (producto_id, stock)
                    VALUES (%s, %s)
                """, (producto_id, cantidad))
            
            #Cambiar estado
            db.cursor.execute("""
                UPDATE pedido_cedis SET estado = 'ENTREGADO' WHERE id = %s
            """, (pedido_id, ))

            db.connection.commit()

            return jsonify({
                "mensaje": "Pedido recibido correctamente"
            }), 200
        
        
    except Exception as e:
        return jsonify({
            "mensaje": f"Error del servidor {e}"
        }), 500