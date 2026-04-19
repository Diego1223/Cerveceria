from flask import session, redirect, url_for
from functools import wraps

#Proteccion de rutas
def login_required(f):
    #Sirve para conservar el nombre original y evitar errores
    @wraps(f)
    def decorador(*args, **kwargs):
        #session - diccionario, si no existe user_id el usuario no inicio sesion
        if "user_id" not in session:
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorador

