from flask import Flask
from routes.main import main
from auth.login import login
from auth.registro import registro_api
from auth.cerrar_sesion import cerrar_sesion_bp
from api.productos import productos_bp
from routes.route_productos import route_productos_bp
from api.panel_productos import panel_productos_bp
from api.editar_stock import editar_stock_bp
from routes.historial_movimientos import historial_movimientos
from api.historial_api import historial_bp
from routes.cobro import cobro_bp
from routes.trabajadores import trabajadores_bp
from api.trabajadores_api import trabajadores_api
from routes.editar_info_trabajador import editar_info_trabajador_bp
from api.editar_in_trabajador import editar_info_api_bp
from error_handler import register_error_handlers

app = Flask(__name__)

app.secret_key = "supersecretkey123"

app.register_blueprint(main)
#APIS y endpoints para logs
app.register_blueprint(login, url_prefix="/api")
app.register_blueprint(registro_api, url_prefix="/api")
app.register_blueprint(cerrar_sesion_bp)

app.register_blueprint(route_productos_bp)
app.register_blueprint(productos_bp, url_prefix="/api")
app.register_blueprint(panel_productos_bp, url_prefix="/api")

#Blueprints referentes al historial
app.register_blueprint(historial_movimientos) #endpoint
app.register_blueprint(historial_bp, url_prefix="/api") #apis

#Blueprints referentes a modificacion de stock
app.register_blueprint(editar_stock_bp, url_prefix="/api")

#Blueprints referente a trabajadores que hay registrados
app.register_blueprint(trabajadores_bp)
app.register_blueprint(editar_info_trabajador_bp)
app.register_blueprint(trabajadores_api, url_prefix="/api")
app.register_blueprint(editar_info_api_bp, url_prefix="/api")
# Para los usuarios que no sean admins
app.register_blueprint(cobro_bp)


# Registro de paginas de errores personalizados 
register_error_handlers(app)


if __name__ == "__main__":
    #ponemos el debug=False para hacer las pruebas con el errorhandler 
    app.run(debug=True,port=5000)