# Cerveceria

## Editar un producto en existencia
Se tendra que poner el motivo, con firma de autorizado y si es merma o robo

## Eliminar productos en existencia
De igual forma se tendran que ingresar los motivos de la eliminación del producto. No todos podran eliminar ni editar productos

## Movimientos en eliminar o editar Stock
Al eliminar o quitar el stock lo que haremos es guardar el historial para poder consultar donde hubo cambios

## Arquitectura tabla historial - Registro de acciones
NO es una tabla intermedia, es una tabla de eventos (auditoria). Cada fila es una accion
- Usuario -> historial (1:N) | Un usuario puede hacer muchos movimientos
- Producto -> historial (1:N) | Un producto puede tener muchos movimientos
Esto solo guarda el historial, nosotros tendremos que actualizar la tabla de productos para actualizar el stock


## Uso de cookies apartir de session flask
Session es una manera en que el servidor recuerde informacion sobre un usuario entre distintas peticciones HTTP
- http es stateless (sin estado), cada request es independiente
- la session le permite al servidor recordar quien eres despues de que inicies sesion

## Funcionamiento interno de la aplicacion
Para administradores se mostrara el sistema de gestion; sin embargo para los trabajadores que inicien sesion se mostrara el sistema de ventas normaldd

# Usuarios registrados
| nombre | correo | password | rol |
| --- | --- | --- | --- |
| juan | juan@gmail.com | juanito12 | admin(1) |
| alejandro | alejandro@gmail | alejandro | empleado (2) |
| alonso | alonso@gmail.com | alonso | empleado (2) |

# Pedidos al CEDIS. Reglas de negocio 
Se rechazaran pedidos al CEDIS por los siguientes motivos. Maximos de stock 250
- La sucursal todavia tiene suficiente inventario
- El pedido que hace el SaaS excede el maximo permitido 
- El CEDIS no cuenta con suficiente stock
- Pedido duplicado. Solo se hacen pedidos diarios
Inventario minimo: Si baja de 20 se puede solicitar mas producto, caso contrario tiene mas de 150 no se permite

Ejemplo 
|ID | Producto     | Cantidad | Estado
| --- | --- | --- | --- |
|1  | Six Modelo   | 20       | 🟢 Aprobado |
|2  | Tecate       | 40       | 🔴 Rechazado |
|3  | Indio        | 15       | 🟡 En tránsito |
|4  | XX Lager     | 30       | 🔵 Entregado |


# Consultas SQL explicadas
En esta consula sql estamos haciendo un JOIN entre dos tablas
- FROM inventario_cedis ic (ic es un alias mas corto para identificar a la tabla inventario_cedis)
- INNER JOIN, se une la tabla productos con la tabla inventario_cedis, y se le agrega el alias que es p
- ON p.id = ic.producto_id es la condicion de union, significa busca en la tabla productos el registro donde el id sea igual al producto_id guardado en inventario_cedis

´´´Mysql
    SELECT 
        ic.id,
        p.descripcion,
        p.codigo,
        ic.stock
    FROM inventario_cedis ic
    INNER JOIN productos p
        ON p.id = ic.producto_id;
´´´

En cuanto a la arquitectura de la tabla inventario_cedis, solo puede existir un producto a la vez, por lo tanto agregamos esto
ADD CONSTRAINT agrega una restriccion llamada uk_producto_cedis, uk hace referencia a Unique Key. UNIQUE (producto_id) indica que los valores de producto_id deben ser unicos
´´´sql
    ALTER TABLE inventario_cedis
    ADD CONSTRAINT uk_producto_cedis
    UNIQUE(producto_id);
´´´


#Transacciones SQL
Las transacciones son un conjunto de operaciones SQL que se comportan como una sola unidad, si todo sale bien se ejecuta si algo sale mal hace rollback y regresamos al punto de inicio
