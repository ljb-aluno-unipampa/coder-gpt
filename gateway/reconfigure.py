#!/usr/bin/env python3
import ipaddress

print("Reconfiguração interativa (protótipo)")
cidr = input("LAN_CIDR: ")
try:
    ipaddress.ip_network(cidr, strict=False)
    print("CIDR válido")
except Exception as e:
    print("Erro:", e)
