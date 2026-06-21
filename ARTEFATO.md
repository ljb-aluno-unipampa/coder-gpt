# ARTEFATO.md

# Informações do Artefato

## Título

Docker Gateway Lab: Laboratório Reprodutível para DHCP, NAT e Firewall utilizando Kea DHCP, nftables e Docker

---

# Resumo

Este artefato implementa um ambiente experimental reproduzível para pesquisa e ensino em administração de redes.

O sistema consiste em:

* Gateway Ubuntu 24.04
* Kea DHCPv4 Server
* Kea Control Agent
* nftables
* API REST em Flask
* Interface Web Administrativa
* Clientes Linux conectados a uma LAN isolada

Todo o ambiente é implantado utilizando Docker Compose.

---

# Objetivo Científico

O artefato foi desenvolvido para apoiar experimentos relacionados a:

* DHCP
* NAT
* Firewalls
* Gerência de Redes
* Infraestrutura como Código
* Virtualização de Redes

O objetivo principal é permitir que pesquisadores reproduzam cenários controlados de configuração e gerenciamento de redes sem necessidade de hardware dedicado.

---

# Escopo do Artefato

O artefato reproduz integralmente:

* topologia de rede;
* configuração DHCP;
* configuração NAT;
* aplicação dinâmica de firewall;
* reservas DHCP;
* reconfiguração de parâmetros.

O artefato não depende de equipamentos físicos.

---

# Requisitos

## Hardware

Mínimo:

* 2 vCPUs
* 4 GB RAM
* 5 GB livres

Recomendado:

* 4 vCPUs
* 8 GB RAM

---

## Software

* Linux x86_64
* Docker 27 ou superior
* Docker Compose v2

---

# Instalação

```bash
git clone <repositorio>
cd docker-gateway-lab

cp .env.example .env

docker compose build

docker compose up -d
```

---

# Validação Funcional

## Verificar containers

```bash
docker compose ps
```

Resultado esperado:

* gw
* client1
* client2

em execução.

---

## Verificar API

```bash
curl http://localhost:8080/api/health
```

Resultado esperado:

```json
{
  "status": "ok"
}
```

---

## Verificar DHCP

```bash
docker exec client1 ip a
```

Resultado esperado:

endereço IP obtido do pool DHCP.

---

## Verificar Leases

```bash
docker exec gw \
cat /opt/gateway/data/kea-leases.csv
```

Resultado esperado:

lease ativo do cliente.

---

## Verificar NAT

```bash
docker exec client1 curl https://example.org
```

Resultado esperado:

conteúdo HTML retornado.

---

# Experimentos Disponíveis

## Experimento 1

DHCP Dinâmico

Objetivo:
Validar distribuição automática de endereços.

---

## Experimento 2

NAT

Objetivo:
Validar acesso externo através do gateway.

---

## Experimento 3

Firewall

Objetivo:
Aplicar regras de bloqueio e liberação dinamicamente.

---

## Experimento 4

Reservas DHCP

Objetivo:
Associar IP fixo a um MAC específico.

---

## Experimento 5

Reconfiguração

Objetivo:
Modificar parâmetros de rede através do arquivo .env.

---

# Resultados Esperados

Ao final dos experimentos deve ser possível observar:

* obtenção dinâmica de endereços;
* persistência de leases;
* tradução de endereços (NAT);
* filtragem de tráfego;
* reservas DHCP funcionais.

---

# Reprodutibilidade

O ambiente foi projetado para ser reproduzido em qualquer host Linux compatível com Docker.

Nenhum equipamento físico especializado é necessário.

---

# Limitações Conhecidas

* IPv4 apenas;
* única subnet LAN;
* autenticação simples;
* ausência de TLS;
* ausência de alta disponibilidade.