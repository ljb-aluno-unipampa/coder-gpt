#

# Topologias de Implantação

Este documento descreve como adaptar o Docker Gateway Lab para ambientes reais utilizando Ubuntu 24.04.

---

# Cenário 1 — Gateway com Duas Interfaces Físicas

## Topologia

```
             Internet
                 |
             eth0 (WAN)
                 |
          Ubuntu Gateway
                 |
             eth1 (LAN)
                 |
            Switch LAN
                 |
     +-----------+-----------+
     |                       |
  Cliente A             Cliente B
```

---

# Configuração Netplan

Exemplo:

```yaml
network:
  version: 2

  ethernets:

    eth0:
      dhcp4: true

    eth1:
      addresses:
        - 192.168.100.1/24
```

Aplicar:

```bash
sudo netplan apply
```

---

# Habilitar Encaminhamento

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Persistência:

```text
/etc/sysctl.conf
```

Adicionar:

```text
net.ipv4.ip_forward=1
```

---

# NAT com nftables

Exemplo:

```nft
table ip nat {

    chain postrouting {

        type nat hook postrouting priority 100;

        oifname "eth0" masquerade
    }
}
```

Aplicar:

```bash
sudo nft -f ruleset.nft
```

---

# Instalação do Kea

```bash
sudo apt update

sudo apt install \
    kea-dhcp4-server \
    kea-ctrl-agent
```

---

# Cenário 2 — Gateway com VLANs

## Topologia

```
                 Internet
                     |
                Interface Física
                     |
              +------+------+
              |  VLAN 10    |
              |     WAN     |
              +------+------+
                     |
              +------+------+
              |  VLAN 20    |
              |     LAN     |
              +------+------+
```

---

# Exemplo Netplan

```yaml
network:
  version: 2

  vlans:

    vlan10:
      id: 10
      link: eno1
      dhcp4: true

    vlan20:
      id: 20
      link: eno1

      addresses:
        - 192.168.100.1/24
```

---

# Checklist de Implantação

## Rede

* [ ] WAN funcional
* [ ] LAN configurada
* [ ] gateway configurado

## DHCP

* [ ] Kea iniciado
* [ ] subnet configurada
* [ ] leases gerados

## Firewall

* [ ] nftables carregado
* [ ] NAT funcional
* [ ] regras aplicadas

## Administração

* [ ] API acessível
* [ ] interface web acessível

---

# Diagnóstico

## Verificar Interfaces

```bash
ip a
```

---

## Verificar Rotas

```bash
ip route
```

---

## Verificar DHCP

```bash
journalctl -u kea-dhcp4-server
```

---

## Verificar NAT

```bash
sudo nft list ruleset
```

---

## Verificar Leases

```bash
cat /var/lib/kea/kea-leases4.csv
```

---

# Boas Práticas

* utilizar senhas fortes;
* restringir acesso administrativo;
* manter Ubuntu atualizado;
* realizar backup periódico dos leases e reservas;
* testar regras de firewall antes da implantação em produção;
* utilizar HTTPS quando exposto em redes externas.

---

# Considerações Finais

O Docker Gateway Lab foi projetado como um protótipo reproduzível de pesquisa.

A arquitetura implementada em containers pode ser migrada para um gateway físico Ubuntu 24.04 com alterações mínimas na configuração de rede e nos arquivos do Kea DHCP e nftables.