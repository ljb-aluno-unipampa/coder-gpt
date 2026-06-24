#!/bin/bash

set -e

echo
echo "======================================="
echo "Docker Gateway Lab"
echo "Gateway Initialization"
echo "======================================="
echo

mkdir -p /opt/gateway/data
mkdir -p /opt/gateway/generated

###########################################
# Detect LAN Interface
###########################################

echo "[1/8] Detectando LAN"

LAN_IF=$(
ip -o -4 addr show \
| grep "${LAN_IP}" \
| awk '{print $2}'
)

if [ -z "$LAN_IF" ]; then
    echo "ERRO: LAN_IF não encontrada"
    ip addr
    exit 1
fi

echo "LAN_IF=${LAN_IF}"

###########################################
# Detect WAN Interface
###########################################

echo "[2/8] Detectando WAN"

WAN_IF=$(
ip route \
| grep default \
| awk '{print $5}' \
| head -n1
)

if [ -z "$WAN_IF" ]; then
    echo "ERRO: WAN_IF não encontrada"
    exit 1
fi

echo "WAN_IF=${WAN_IF}"

###########################################
# Enable Routing
###########################################

echo "[3/8] Habilitando IPv4 Forward"

sysctl -w net.ipv4.ip_forward=1

###########################################
# Generate DHCP Config
###########################################

echo "[4/8] Gerando kea-dhcp4.conf"

sed \
-e "s|__LAN_IF__|${LAN_IF}|g" \
-e "s|__DHCP_SUBNET__|${DHCP_SUBNET}|g" \
-e "s|__POOL_START__|${DHCP_POOL_START}|g" \
-e "s|__POOL_END__|${DHCP_POOL_END}|g" \
-e "s|__LAN_IP__|${LAN_IP}|g" \
-e "s|__DHCP_DNS__|${DHCP_DNS}|g" \
-e "s|__DHCP_DOMAIN__|${DHCP_DOMAIN}|g" \
/opt/gateway/templates/kea-dhcp4.conf.tpl \
> /etc/kea/kea-dhcp4.conf

###########################################
# Generate Control Agent Config
###########################################

echo "[5/8] Gerando kea-ctrl-agent.conf"

cp \
/opt/gateway/templates/kea-ctrl-agent.conf.tpl \
/etc/kea/kea-ctrl-agent.conf

###########################################
# Apply nftables
###########################################

echo "[6/8] Aplicando Firewall"

cat >/opt/gateway/generated/ruleset.nft <<EOF

flush ruleset

table inet filter {

    chain input {
        type filter hook input priority 0;

        policy accept;
    }

    chain forward {
        type filter hook forward priority 0;

        policy accept;
    }

    chain output {
        type filter hook output priority 0;

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

nft -f /opt/gateway/generated/ruleset.nft

###########################################
# Start Kea DHCP4
###########################################

echo "[7/9] Iniciando Kea DHCP4"

mkdir -p /run/kea
mkdir -p /var/run/kea

kea-dhcp4 \
-c /etc/kea/kea-dhcp4.conf &

sleep 3

###########################################
# Start Control Agent
###########################################

echo "[8/9] Iniciando Kea Control Agent"

kea-ctrl-agent \
-c /etc/kea/kea-ctrl-agent.conf &

sleep 2

echo
echo "======================================="
echo "Gateway inicializado"
echo "======================================="
echo

echo "LAN_IF=${LAN_IF}"
echo "WAN_IF=${WAN_IF}"

echo
echo "Lease file:"
echo "/opt/gateway/data/kea-leases.csv"
echo

echo "[9/9] Iniciando API Flask"

cd /opt/gateway

python3 gwapi.py &

wait -n
