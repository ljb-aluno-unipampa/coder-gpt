from flask import Blueprint, render_template
from .auth import login_required

web_bp = Blueprint("web", __name__)

@web_bp.route("/")
@login_required
def index():
    return render_template("index.html")

@web_bp.route("/firewall")
@login_required
def firewall():
    return render_template("firewall.html")

@web_bp.route("/dhcp")
@login_required
def dhcp():
    return render_template("dhcp.html")
