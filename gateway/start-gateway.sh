#!/bin/bash

set -e

echo "=================================="
echo "Gateway starting..."
echo "=================================="

mkdir -p /opt/gateway/data
mkdir -p /opt/gateway/generated

echo "[1/5] Enabling IPv4 forwarding"

sysctl -w net.ipv4.ip_forward=1

echo "[2/5] Detecting interfaces"

LAN_IF=$(ip -o addr show | grep "${LAN_IP}" | awk '{print $2}')

WAN_IF=$(ip route | grep default | awk '{print $5}' | head -n1)

echo "LAN_IF=${LAN_IF}"
echo "WAN_IF=${WAN_IF}"

echo "[3/5] Creating minimal nftables rules"

cat >/tmp/ruleset.nft <<EOF
flush ruleset

table inet filter {

    chain forward {
        type filter hook forward priority 0;

        policy accept;
    }
}

table ip nat {

    chain postrouting {
        type nat hook postrouting priority 100;

        oifname "${WAN_IF}" masquerade
    }
}
EOF

nft -f /tmp/ruleset.nft

echo "[4/5] Starting placeholder API"

cat >/opt/gateway/app.py <<'EOF'
from flask import Flask

app = Flask(__name__)

@app.route("/health")
def health():
    return {
        "status": "ok"
    }

app.run(host="0.0.0.0", port=5000)
EOF

echo "[5/5] Starting Flask"

python3 /opt/gateway/app.py