from flask import render_template

#Esto nos da pagina de errores personalizados
#OJO tiene que estar fuera del debug mode
def register_error_handlers(app):
    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template("errors/500.html"), 500

    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template("errors/404.html"), 404