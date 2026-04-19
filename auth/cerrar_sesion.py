from flask import redirect, Blueprint,session

cerrar_sesion_bp = Blueprint("cerrar_sesion", __name__)

@cerrar_sesion_bp.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear()
    return redirect("/")