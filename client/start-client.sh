#!/bin/bash

set -e

echo "=================================="
echo "Client starting..."
echo "=================================="

IFACE=eth0

echo "[1/4] Removing Docker IP"

ip addr flush dev ${IFACE} || true

echo "[2/4] Cleaning routes"

ip route flush dev ${IFACE} || true

echo "[3/4] Bringing interface up"

ip link set ${IFACE} up

echo "[4/4] Requesting DHCP lease"

dhclient -v ${IFACE}

tail -f /dev/null