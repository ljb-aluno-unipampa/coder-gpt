from flask import Blueprint, jsonify
from .dhcp_service import KeaService

dhcp_bp = Blueprint("dhcp_api", __name__, url_prefix="/dhcp")

@dhcp_bp.route("/status")
def status():
    return jsonify(KeaService().status())
