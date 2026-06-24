import csv
import json
import shlex
import subprocess
from pathlib import Path

import requests
from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__, url_prefix="/api")

LEASES_FILE = Path("/opt/gateway/data/kea-leases.csv")
KEA_CONFIG_FILE = Path("/etc/kea/kea-dhcp4.conf")
KEA_CA_URL = "http://127.0.0.1:8000"


def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout


def forward_rules():
    output = run_command(["nft", "-a", "-j", "list", "chain", "inet", "filter", "forward"])
    rules = []
    for item in json.loads(output).get("nftables", []):
        rule = item.get("rule")
        if rule:
            rules.append(rule)
    return rules


@api_bp.route("/health")
def health():
    return jsonify({"status": "ok"})


@api_bp.route("/dhcp/status")
def dhcp_status():
    try:
        response = requests.post(
            KEA_CA_URL,
            json={"command": "status-get", "service": ["dhcp4"]},
            timeout=5,
        )
        return jsonify(response.json()), response.status_code
    except requests.RequestException as exc:
        return jsonify({"status": "error", "detail": str(exc)}), 503


@api_bp.route("/dhcp/config")
def dhcp_config():
    if not KEA_CONFIG_FILE.exists():
        return jsonify({"error": "kea-dhcp4.conf nao encontrado"}), 404
    try:
        return jsonify(json.loads(KEA_CONFIG_FILE.read_text()))
    except json.JSONDecodeError as exc:
        return jsonify({"error": "configuracao invalida", "detail": str(exc)}), 500


@api_bp.route("/dhcp/leases")
def dhcp_leases():
    if not LEASES_FILE.exists():
        return jsonify([])

    with LEASES_FILE.open(newline="") as leases:
        return jsonify(list(csv.DictReader(leases)))


@api_bp.route("/firewall")
def firewall():
    try:
        ruleset = run_command(["nft", "-j", "list", "ruleset"])
        return jsonify(json.loads(ruleset))
    except subprocess.CalledProcessError as exc:
        return jsonify({"error": "falha ao consultar nftables", "detail": exc.stderr}), 500
    except json.JSONDecodeError as exc:
        return jsonify({"error": "saida nftables invalida", "detail": str(exc)}), 500


@api_bp.route("/firewall/rules")
def firewall_rules():
    try:
        return jsonify(forward_rules())
    except subprocess.CalledProcessError as exc:
        return jsonify({"error": "falha ao consultar cadeia forward", "detail": exc.stderr}), 500


@api_bp.route("/firewall", methods=["POST"])
def firewall_add():
    from flask import request

    payload = request.get_json(silent=True) or {}
    expression = payload.get("expression")

    if not expression:
        return jsonify({"error": "campo expression e obrigatorio"}), 400

    try:
        command = ["nft", "add", "rule", "inet", "filter", "forward"] + shlex.split(expression)
        subprocess.run(command, capture_output=True, text=True, check=True)
        handles = [rule.get("handle") for rule in forward_rules() if rule.get("handle") is not None]
        return jsonify({"status": "created", "handle": max(handles, default=None)}), 201
    except ValueError as exc:
        return jsonify({"error": "expressao invalida", "detail": str(exc)}), 400
    except subprocess.CalledProcessError as exc:
        return jsonify({"error": "falha ao adicionar regra", "detail": exc.stderr}), 400


@api_bp.route("/firewall/<int:handle>", methods=["DELETE"])
def firewall_delete(handle):
    try:
        subprocess.run(
            ["nft", "delete", "rule", "inet", "filter", "forward", "handle", str(handle)],
            capture_output=True,
            text=True,
            check=True,
        )
        return jsonify({"status": "deleted", "handle": handle})
    except subprocess.CalledProcessError as exc:
        return jsonify({"error": "falha ao remover regra", "detail": exc.stderr}), 400


@api_bp.route("/network")
def network():
    try:
        addresses = json.loads(run_command(["ip", "-j", "addr", "show"]))
        routes = json.loads(run_command(["ip", "-j", "route", "show"]))
        return jsonify({"interfaces": addresses, "routes": routes})
    except subprocess.CalledProcessError as exc:
        return jsonify({"error": "falha ao consultar rede", "detail": exc.stderr}), 500
