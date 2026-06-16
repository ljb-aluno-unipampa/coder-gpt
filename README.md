# Docker Gateway Lab

## Artefato de Pesquisa

Laboratório reprodutível para experimentação de DHCP, NAT, Firewall e Gerência de Redes utilizando Docker, Kea DHCP Server, nftables e Flask.

---

# Resumo

O Docker Gateway Lab é um ambiente reprodutível para experimentos de redes de computadores.

O artefato implementa um gateway virtual baseado em Ubuntu 24.04 executando:

* Kea DHCPv4 Server
* Kea Control Agent
* nftables
* API REST em Flask
* Interface Web Administrativa

O gateway conecta uma rede LAN isolada a uma rede WAN, permitindo avaliar:

* distribuição dinâmica de endereços IP;
* reservas DHCP;
* NAT;
* filtragem de tráfego;
* gerenciamento remoto de regras;
* reconfiguração de parâmetros de rede.

---

# Objetivo

O objetivo deste artefato é fornecer um laboratório reproduzível para ensino, pesquisa e experimentação em:

* Administração de Redes
* DHCP
* Firewalls
* Network Address Translation (NAT)
* Gerência de Infraestrutura
* Redes Definidas por Software
* Automação de Redes

---

# Arquitetura

## Visão Lógica

```
                INTERNET
                     |
                WAN Docker
                     |
              +-------------+
              | Gateway GW  |
              |-------------|
              | Kea DHCP    |
              | nftables    |
              | Flask API   |
              +-------------+
                     |
                LAN Docker
                     |
          +----------+----------+
          |                     |
      client1               client2
```

---

# Componentes

## Gateway

Responsável por:

* roteamento IPv4;
* NAT;
* firewall;
* DHCP;
* API REST;
* interface administrativa.

## Client1

Host Linux conectado exclusivamente à LAN.

Obtém endereço IP via DHCP.

## Client2

Host Linux conectado exclusivamente à LAN.

Obtém endereço IP via DHCP.

---

# Estrutura do Repositório

```text
.
├── docker-compose.yml
├── .env.example
├── README.md
│
├── gateway/
│   ├── Dockerfile
│   ├── start-gateway.sh
│   ├── gwapi.py
│   ├── reconfigure.py
│   │
│   ├── gwapi_app/
│   │   ├── auth.py
│   │   ├── api.py
│   │   ├── firewall.py
│   │   ├── dhcp.py
│   │   └── dhcp_service.py
│   │
│   ├── templates/
│   ├── generated/
│   └── data/
│
└── client/
    ├── Dockerfile
    └── start-client.sh
```

---

# Requisitos

## Hardware

Mínimo recomendado:

* 2 CPUs
* 4 GB RAM
* 5 GB livres em disco

## Software

* Linux
* Docker 27+
* Docker Compose v2+

---

# Instalação

Clonar o repositório:

```bash
git clone <repositorio>
cd docker-gateway-lab
```

Criar arquivo de configuração:

```bash
cp .env.example .env
```

Construir imagens:

```bash
docker compose build
```

Executar:

```bash
docker compose up -d
```

---

# Verificação Inicial

Verificar containers:

```bash
docker compose ps
```

Resultado esperado:

* gw
* client1
* client2

em estado UP.

---

# Endpoint de Saúde

```bash
curl http://localhost:8080/api/health
```

Resposta esperada:

```json
{
  "status": "ok"
}
```

---

# Persistência

Os seguintes dados são persistidos:

* leases DHCP;
* reservas DHCP;
* estado do firewall;
* configurações geradas.

Diretórios:

```text
gateway/data
gateway/generated
```

---

# Experimentos Reproduzíveis

## Experimento 1 – DHCP Dinâmico

Objetivo:

Verificar obtenção automática de endereço IP.

Passos:

```bash
docker exec client1 ip a
```

Resultado esperado:

Endereço IP pertencente ao pool DHCP.

---

## Experimento 2 – NAT

Objetivo:

Verificar acesso à Internet através do gateway.

Passos:

```bash
docker exec client1 curl https://example.org
```

Resultado esperado:

Recebimento do conteúdo remoto.

---

## Experimento 3 – Leases DHCP

Objetivo:

Verificar persistência dos leases.

Passos:

```bash
docker exec gw \
cat /opt/gateway/data/kea-leases.csv
```

Resultado esperado:

Registro do lease dos clientes.

---

## Experimento 4 – Firewall

Objetivo:

Bloquear tráfego utilizando regras dinâmicas.

Resultado esperado:

Perda de conectividade conforme regra aplicada.

---

## Experimento 5 – Reservas DHCP

Objetivo:

Associar endereço IP fixo a um MAC específico.

Resultado esperado:

Cliente recebe sempre o mesmo endereço.

---

# Endpoints Principais

## API

### Saúde

```text
GET /api/health
```

### Firewall

```text
GET    /api/firewall
POST   /api/firewall
PUT    /api/firewall/<id>
DELETE /api/firewall/<id>
```

### DHCP

```text
GET /dhcp/status
GET /dhcp/config
GET /dhcp/leases
POST /dhcp/apply
```

---

# Segurança

O artefato é destinado a uso experimental.

Não deve ser exposto diretamente à Internet.

Recomendações:

* alterar credenciais padrão;
* restringir acesso à interface administrativa;
* executar em ambiente isolado;
* revisar regras de firewall antes da implantação.

---

# Limitações Conhecidas

* suporte apenas a IPv4;
* uma única subnet LAN;
* autenticação básica;
* ausência de TLS nativo;
* sem alta disponibilidade.

---

# Limpeza do Ambiente

Parar containers:

```bash
docker compose down
```

Remover volumes:

```bash
docker compose down -v
```

Reconstrução completa:

```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

---

# Reprodutibilidade

O artefato foi projetado para permitir reprodução completa dos experimentos utilizando exclusivamente:

* Docker;
* Docker Compose;
* Ubuntu 24.04;
* Kea DHCP;
* nftables;
* Python 3.

Nenhuma infraestrutura externa é necessária além do acesso à Internet para obtenção das imagens e pacotes.
