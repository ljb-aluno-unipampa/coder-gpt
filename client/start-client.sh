#!/bin/bash

set -e

echo
echo "======================================="
echo "DHCP Client Bootstrap"
echo "======================================="
echo

IFACE=eth0

echo "[1/5] Limpando configuração Docker"

ip addr flush dev ${IFACE} || true

ip route flush dev ${IFACE} || true

echo "[2/5] Subindo interface"

ip link set ${IFACE} up

echo "[3/5] Aguardando gateway"

sleep 5

echo "[4/5] Solicitando lease"

dhclient -v ${IFACE}

echo "[5/5] Lease obtido"

ip addr show ${IFACE}

echo
echo "Rotas:"
ip route

echo
tail -f /dev/null