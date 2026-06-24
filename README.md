# Docker Gateway Lab

## Artefato de Pesquisa

**Titulo do artefato/artigo:** Docker Gateway Lab: Laboratorio Reprodutivel para DHCP, NAT e Firewall utilizando Kea DHCP, nftables e Docker.

**Resumo:** este artefato disponibiliza um laboratorio de redes executado com Docker Compose. O ambiente cria um gateway Ubuntu 24.04 conectado simultaneamente a uma WAN Docker e a uma LAN isolada. O gateway executa Kea DHCPv4, Kea Control Agent, nftables e uma aplicacao Flask para inspecao operacional. Dois clientes Linux conectados apenas a LAN recebem enderecos dinamicos, usam o gateway como rota padrao e acessam redes externas por NAT.

O objetivo do artefato e apoiar avaliacao, ensino e experimentacao em DHCP, NAT, firewall, gerencia de redes e infraestrutura como codigo, sem exigir hardware dedicado.

---

# Estrutura do README.md

Este README esta organizado para orientar revisores desde a preparacao do ambiente ate a reproducao dos principais resultados:

* **Estrutura do Repositorio**
* **Informacoes Basicas**
* **Dependencias**
* **Preocupacoes com Seguranca**
* **Instalacao**
* **Teste Minimo**
* **Experimentos**
* **LICENSE**

---

# Estrutura do Repositorio

```text
.
├── docker-compose.yml
├── .env.example
├── README.md
├── ARTEFATO.md
├── AVALIACAO-RAPIDA.md
├── TOPOLOGIAS-DE-IMPLANTACAO.md
├── LICENSE
│
├── gateway/
│   ├── Dockerfile
│   ├── start-gateway.sh
│   ├── gwapi.py
│   ├── firewall.py
│   ├── dhcp_service.py
│   ├── reconfigure.py
│   │
│   ├── gwapi_app/
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── auth.py
│   │   ├── web.py
│   │   ├── config.py
│   │   ├── logging_config.py
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── firewall.html
│   │   └── dhcp.html
│   │
│   ├── templates/
│   │   ├── kea-dhcp4.conf.tpl
│   │   └── kea-ctrl-agent.conf.tpl
│   │
│   ├── generated/
│   │   └── ruleset.nft
│   │
│   └── data/
│       └── kea-leases.csv
│
└── client/
    ├── Dockerfile
    └── start-client.sh
```

Papel dos principais arquivos:

* `docker-compose.yml`: define gateway, clientes, WAN e LAN isolada.
* `gateway/start-gateway.sh`: detecta interfaces, gera configuracoes, aplica nftables e inicia Kea, Control Agent e Flask.
* `gateway/templates/`: modelos usados para gerar configuracao do Kea.
* `gateway/gwapi_app/api.py`: endpoints REST para saude, DHCP, rede e firewall.
* `gateway/data/`: persistencia de leases DHCP.
* `gateway/generated/`: artefatos gerados em tempo de execucao, incluindo ruleset nftables.
* `client/start-client.sh`: remove a configuracao inicial do Docker e solicita lease DHCP.

---

# Informacoes Basicas

## Topologia

```text
                Internet / Host Docker
                         |
                    rede wan
                         |
                 +---------------+
                 |      gw       |
                 | Ubuntu 24.04  |
                 | Kea + nftables|
                 | Flask API     |
                 +-------+-------+
                         |
                    rede lan
                 internal: true
                         |
              +----------+----------+
              |                     |
           client1               client2
```

## Componentes

### Gateway `gw`

Responsavel por:

* identificar a interface LAN a partir de `LAN_IP`;
* identificar a interface WAN a partir da rota padrao;
* habilitar `net.ipv4.ip_forward`;
* gerar `/etc/kea/kea-dhcp4.conf`;
* iniciar `kea-dhcp4` e `kea-ctrl-agent`;
* aplicar NAT via `nftables`;
* expor a API Flask na porta interna `5000`, publicada no host como `WEB_PORT`.

### Clientes `client1` e `client2`

Hosts Ubuntu conectados exclusivamente a LAN. O script de entrada remove o endereco inicial criado pelo Docker e solicita configuracao de rede via DHCP.

## Ambiente de Execucao

Requisitos minimos:

* Host Linux x86_64.
* Docker Engine 20.10 ou superior.
* Docker Compose v2 ou superior.
* Acesso a Internet no build e nos experimentos de NAT.
* 2 vCPUs.
* 4 GB RAM.
* 5 GB livres em disco.

Ambiente usado na validacao local:

* Docker `29.5.3`.
* Docker Compose `v5.1.4`.
* Imagens base `ubuntu:24.04`.

---

# Dependencias

## Dependencias do Host

Obrigatorias:

* Docker Engine.
* Docker Compose.
* Git.

Recomendadas para avaliacao:

* `curl`.
* `jq`.

## Dependencias dos Containers

### Gateway

Instaladas pelo `gateway/Dockerfile`:

* `kea-dhcp4-server`
* `kea-ctrl-agent`
* `nftables`
* `python3`
* `python3-pip`
* `python3-venv`
* `iproute2`
* `iputils-ping`
* `curl`
* `jq`
* `net-tools`

Dependencias Python instaladas no venv `/opt/venv`:

* `flask`
* `python-dotenv`
* `requests`

### Clientes

Instaladas pelo `client/Dockerfile`:

* `isc-dhcp-client`
* `iproute2`
* `iputils-ping`
* `curl`
* `jq`
* `net-tools`

## Recursos Externos

O artefato nao utiliza benchmark externo nem servico de terceiros obrigatorio. A Internet e usada para:

* baixar pacotes Ubuntu durante o build;
* baixar pacotes Python via PyPI;
* testar NAT com destinos publicos como `8.8.8.8` e `https://example.org`.

As versoes de pacotes Ubuntu e Python sao resolvidas no momento do build. Em validacao local, o Kea iniciou como versao `2.4.1`.

---

# Preocupacoes com Seguranca

Este artefato e experimental. Nao deve ser exposto diretamente a Internet.

Riscos principais:

* O container `gw` executa com `privileged: true`, pois manipula interfaces, encaminhamento IPv4 e nftables.
* A API Flask e publicada no host em `WEB_PORT`, por padrao `8080`.
* A interface web usa autenticacao por sessao simples, com credenciais vindas de `.env`.
* Endpoints REST de firewall permitem adicionar/remover regras nftables dentro do container gateway. Use apenas em ambiente controlado.
* Nao ha TLS nativo.
* O ruleset gerado usa `flush ruleset` dentro do namespace do container. Mesmo assim, recomenda-se executar o artefato em VM ou host de laboratorio.

Medidas recomendadas:

* Executar em maquina descartavel ou VM.
* Alterar `ADMIN_USER`, `ADMIN_PASSWORD` e `SECRET_KEY` antes de qualquer avaliacao em rede compartilhada.
* Nao publicar `WEB_PORT` em interface publica.
* Encerrar o ambiente apos a avaliacao:

```bash
docker compose down --remove-orphans
```

---

# Instalacao

## 1. Clonar o Repositorio

```bash
git clone <repositorio>
cd coder-gpt
```

## 2. Criar Arquivo de Ambiente

```bash
cp .env.example .env
```

Parametros principais:

```text
LAN_CIDR=192.168.100.0/24
LAN_IP=192.168.100.254
DOCKER_LAN_GATEWAY=192.168.100.1
DHCP_SUBNET=192.168.100.0/24
DHCP_POOL_START=192.168.100.100
DHCP_POOL_END=192.168.100.200
DHCP_DNS=8.8.8.8,1.1.1.1
DHCP_DOMAIN=lab.local
WEB_PORT=8080
ADMIN_USER=admin
ADMIN_PASSWORD=admin123
```

## 3. Construir e Executar

```bash
docker compose up --build -d
```

## 4. Verificar Estado Inicial

```bash
docker compose ps
```

Resultado esperado:

```text
gw        Up
client1   Up
client2   Up
```

A API deve estar disponivel em:

```text
http://localhost:8080/api/health
```

A interface web deve estar disponivel em:

```text
http://localhost:8080/login
```

Credenciais padrao:

```text
admin / admin123
```

---

# Teste Minimo

Este teste verifica se o artefato foi instalado corretamente. Tempo esperado apos o build: menos de 2 minutos.

## 1. Saude da API

```bash
curl http://localhost:8080/api/health
```

Resultado esperado:

```json
{"status":"ok"}
```

## 2. Lease DHCP no Cliente

```bash
docker exec client1 ip -4 addr show eth0
docker exec client1 ip route
```

Resultado esperado:

* endereco `192.168.100.100/24` ou outro dentro do pool configurado;
* rota padrao via `192.168.100.254`.

## 3. Registro de Lease no Gateway

```bash
docker exec gw head -n 5 /opt/gateway/data/kea-leases.csv
curl http://localhost:8080/api/dhcp/leases
```

Resultado esperado:

* arquivo CSV com cabecalho do Kea;
* pelo menos um lease referente aos clientes.

## 4. NAT

```bash
docker exec client1 ping -c 2 8.8.8.8
docker exec client1 curl -I https://example.org
```

Resultado esperado:

* ping com `0% packet loss`;
* resposta HTTP de `example.org`.

---

# Experimentos

Os experimentos abaixo cobrem as principais reivindicacoes implementadas neste artefato. A execucao completa deve levar poucos minutos em um host ja preparado.

---

## Reivindicacao #1 — O ambiente cria uma LAN isolada com clientes configurados por DHCP

### Objetivo

Demonstrar que os clientes nao usam configuracao manual persistente e recebem endereco, rota e parametros de rede do Kea DHCPv4 executado no gateway.

### Arquivos Relevantes

* `docker-compose.yml`
* `client/start-client.sh`
* `gateway/templates/kea-dhcp4.conf.tpl`
* `gateway/start-gateway.sh`

### Comandos

```bash
docker compose ps
docker logs gw | grep DHCP4_LEASE_ALLOC
docker exec client1 ip -4 addr show eth0
docker exec client2 ip -4 addr show eth0
curl http://localhost:8080/api/dhcp/leases
```

### Recursos Esperados

* Memoria: menos de 1 GB para execucao.
* Disco: leases persistidos em `gateway/data/kea-leases.csv`.
* Tempo: menos de 30 segundos apos os containers estarem ativos.

### Resultado Esperado

* `client1` e `client2` recebem IPs dentro de `DHCP_POOL_START` e `DHCP_POOL_END`.
* O gateway registra eventos `DHCP4_LEASE_ALLOC`.
* `/api/dhcp/leases` retorna os leases observados no arquivo CSV.

---

## Reivindicacao #2 — O gateway realiza NAT para acesso externo dos clientes

### Objetivo

Demonstrar que a rede LAN e interna ao Docker e que o acesso externo dos clientes ocorre atraves do gateway.

### Arquivos Relevantes

* `docker-compose.yml`
* `gateway/start-gateway.sh`
* `gateway/generated/ruleset.nft`

### Comandos

```bash
docker exec gw sysctl net.ipv4.ip_forward
docker exec gw nft list ruleset
docker exec client1 ip route
docker exec client1 ping -c 2 8.8.8.8
docker exec client1 curl -I https://example.org
```

### Recursos Esperados

* Trafego de rede baixo.
* CPU baixa, exceto durante o build.
* Tempo: menos de 1 minuto.

### Resultado Esperado

* `net.ipv4.ip_forward = 1`.
* Ruleset nftables com regra `masquerade` na interface WAN.
* Cliente com rota padrao via `LAN_IP`.
* Acesso externo funcional.

---

## Reivindicacao #3 — O firewall pode ser observado e alterado dinamicamente pela API

### Objetivo

Demonstrar que o avaliador consegue consultar o ruleset nftables e inserir/remover uma regra temporaria na cadeia `forward`.

### Arquivos Relevantes

* `gateway/gwapi_app/api.py`
* `gateway/start-gateway.sh`
* `gateway/generated/ruleset.nft`

### Comandos

Listar ruleset:

```bash
curl http://localhost:8080/api/firewall
curl http://localhost:8080/api/firewall/rules
```

Adicionar regra temporaria inofensiva:

```bash
curl -X POST http://localhost:8080/api/firewall \
  -H 'Content-Type: application/json' \
  -d '{"expression":"ip saddr 192.168.100.250 drop"}'
```

Remover a regra criada, substituindo `<HANDLE>` pelo handle retornado:

```bash
curl -X DELETE http://localhost:8080/api/firewall/<HANDLE>
```

### Recursos Esperados

* Tempo: menos de 30 segundos.
* Uso irrelevante de CPU/RAM.

### Resultado Esperado

* `GET /api/firewall` retorna o ruleset em JSON.
* `POST /api/firewall` retorna `status: created` e um `handle`.
* `DELETE /api/firewall/<HANDLE>` retorna `status: deleted`.

### Observacao Operacional

As regras adicionadas por API sao temporarias. Elas desaparecem quando o gateway e recriado ou quando o ruleset base e reaplicado.

---

## Reivindicacao #4 — O Kea Control Agent permite inspecao operacional do DHCP

### Objetivo

Demonstrar que o gateway executa o Kea Control Agent e que a API Flask consegue consultar o estado do servico DHCP.

### Arquivos Relevantes

* `gateway/templates/kea-ctrl-agent.conf.tpl`
* `gateway/gwapi_app/api.py`
* `gateway/dhcp_service.py`

### Comandos

```bash
curl http://localhost:8080/api/dhcp/status
curl http://localhost:8080/api/dhcp/config
docker logs gw | grep CTRL_AGENT_STARTED
```

### Recursos Esperados

* Tempo: menos de 30 segundos.
* Uso irrelevante de CPU/RAM.

### Resultado Esperado

* `/api/dhcp/status` retorna resposta do Control Agent.
* `/api/dhcp/config` retorna a configuracao efetiva gerada para o Kea.
* Logs do gateway mostram `CTRL_AGENT_STARTED`.

---

## Reivindicacao #5 — Parametros de rede podem ser reproduzidos por arquivo de ambiente

### Objetivo

Demonstrar que a topologia e o pool DHCP sao parametrizados por `.env`, permitindo repetir cenarios com outra faixa de enderecos.

### Arquivos Relevantes

* `.env.example`
* `.env`
* `docker-compose.yml`
* `gateway/templates/kea-dhcp4.conf.tpl`

### Procedimento

Edite `.env`, por exemplo:

```text
DHCP_POOL_START=192.168.100.120
DHCP_POOL_END=192.168.100.130
```

Recrie o ambiente:

```bash
docker compose down --remove-orphans
docker compose up --build -d
```

Verifique:

```bash
curl http://localhost:8080/api/dhcp/config
docker exec client1 ip -4 addr show eth0
```

### Recursos Esperados

* Build incremental rapido.
* Menos de 1 GB RAM em execucao.

### Resultado Esperado

* A configuracao gerada do Kea reflete o novo pool.
* Clientes recebem enderecos dentro da nova faixa.

---

# Endpoints Principais

```text
GET    /api/health
GET    /api/network
GET    /api/dhcp/status
GET    /api/dhcp/config
GET    /api/dhcp/leases
GET    /api/firewall
GET    /api/firewall/rules
POST   /api/firewall
DELETE /api/firewall/<handle>
```

Interface web:

```text
GET /login
GET /
GET /firewall
GET /dhcp
```

---

# Limpeza do Ambiente

Parar containers:

```bash
docker compose down --remove-orphans
```

Remover dados persistidos:

```bash
docker compose down -v
rm -f gateway/data/kea-leases.csv
rm -f gateway/generated/ruleset.nft
```

Reconstrucao completa:

```bash
docker compose down --remove-orphans
docker compose build --no-cache
docker compose up -d
```

---

# Limitacoes Conhecidas

* Suporte apenas a IPv4.
* Uma subnet LAN por execucao.
* API REST sem TLS.
* Interface web simples.
* Regras adicionadas por API nao sao persistidas como politica permanente.
* Reservas DHCP aparecem como direcao de extensao do artefato, mas nao sao reivindicacao principal validada neste README.
* Nao ha alta disponibilidade.

---

# LICENSE

Este projeto esta licenciado sob BSD 3-Clause License. Consulte `LICENSE` para o texto integral.
