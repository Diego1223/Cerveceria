#Verificar si el usuario es admin
from functools import wraps
from database.conectar import db
from flask import session, redirect, url_for

def is_admin_db(user_id):
    db.cursor.execute("SELECT admin FROM usuarios WHERE id = %s", (user_id,))
    resultado = db.cursor.fetchone()
    #Si no encontro nada en la db no es admin
    if resultado is None:
        return  False
    # Esto compara 1 == 1 - True
    #1 == 0 o 2 - False
    return resultado["admin"] == 1

#f - es la ruta que vas a proteger
def is_admin(f):
    @wraps(f)
    def admin(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("main.login"))
        
        id_usuario = session["user_id"]

        if not is_admin_db(id_usuario):
            return redirect(url_for("cobro.cobro_route"))
        #Si es admin se ejecuta la funcion original
        return f(*args, **kwargs)
    return admin