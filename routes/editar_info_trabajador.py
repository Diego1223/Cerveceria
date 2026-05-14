from flask import Blueprint, render_template

editar_info_trabajador_bp = Blueprint("editar_trabajador", __name__)

@editar_info_trabajador_bp.route("/editar_info_trabajador")
def info_trabajador():
    return render_template("editar_info_trabajador.html")
