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
nombre: juan
correo: juan@gmail.com
password: juanito12
rol: admin (1)

nombre: alejandro
correo: alejandro@gmail
password: alejandro
rol: empleado (2)

alonso@gmail.com   
alonso 
Trabajador
