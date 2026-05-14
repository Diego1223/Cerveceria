from flask import Blueprint, render_template

cobro_bp = Blueprint("cobro", __name__)

@cobro_bp.route("/cobro")
def cobro_route():
    return render_template("cobro.html")