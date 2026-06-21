# AVALIACAO-RAPIDA.md

# Avaliação Rápida do Artefato

Este documento permite validar o funcionamento básico do artefato em aproximadamente 5 minutos.

O objetivo é verificar:

* implantação do ambiente;
* inicialização dos containers;
* funcionamento da API;
* atribuição de endereços DHCP;
* NAT;
* persistência de leases.

---

# Pré-Requisitos

Sistema operacional:

* Linux x86_64

Software:

* Docker 27+
* Docker Compose v2+

Verificação:

```bash
docker --version
docker compose version
```

---

# Passo 1 — Obter o Código

```bash
git clone https://github.com/ljb-aluno-unipampa/coder-gpt.git

cd coder-gpt
```

---

# Passo 2 — Configuração Inicial

Criar arquivo de configuração:

```bash
cp .env.example .env
```

Caso necessário, ajustar:

```bash
LAN_CIDR
LAN_IP
DOCKER_LAN_GATEWAY
DHCP_POOL_START
DHCP_POOL_END
```

---

# Passo 3 — Construção das Imagens

```bash
docker compose build
```

Tempo esperado:

* 1 a 5 minutos (dependendo da conexão e hardware).

Resultado esperado:

```text
Successfully built
Successfully tagged
```

---

# Passo 4 — Inicialização

```bash
docker compose up -d
```

Verificar:

```bash
docker compose ps
```

Resultado esperado:

```text
NAME      STATUS
gw        Up
client1   Up
client2   Up
```

---

# Passo 5 — Verificar API

Executar:

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

# Passo 6 — Verificar DHCP

Consultar endereço recebido pelo cliente:

```bash
docker exec client1 ip -4 addr show eth0
```

Resultado esperado:

```text
inet 192.168.x.x
```

onde o endereço pertence ao pool DHCP configurado.

---

# Passo 7 — Verificar Leases

No gateway:

```bash
docker exec gw \
cat /opt/gateway/data/kea-leases.csv
```

Resultado esperado:

```text
address,hwaddr,...
192.168.x.x,...
```

Deve existir pelo menos um lease associado a client1.

---

# Passo 8 — Verificar NAT

Executar:

```bash
docker exec client1 \
curl -I https://example.org
```

Resultado esperado:

```text
HTTP/2 200
```

ou

```text
HTTP/1.1 200 OK
```

---

# Passo 9 — Verificar Logs

Gateway:

```bash
docker logs gw --tail 50
```

Cliente:

```bash
docker logs client1 --tail 50
```

Resultado esperado:

* inicialização sem erros fatais;
* lease DHCP obtido;
* serviços Kea ativos.

---

# Critérios de Aprovação

O artefato é considerado funcional quando:

* [ ] Containers iniciam corretamente;
* [ ] Endpoint /api/health responde;
* [ ] Cliente recebe endereço DHCP;
* [ ] Lease é registrado pelo Kea;
* [ ] Cliente possui acesso externo através do gateway.

---

# Encerramento

Parar o ambiente:

```bash
docker compose down
```

Remover todos os dados persistidos:

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

# Tempo Médio de Avaliação

| Etapa         | Tempo   |
| ------------- | ------- |
| Clone         | < 1 min |
| Build         | 1–5 min |
| Inicialização | < 1 min |
| Testes        | < 2 min |
| Total         | ~5 min  |

---

# Artefato

Docker Gateway Lab

Laboratório Reprodutível para DHCP, NAT e Firewall utilizando Docker, Kea DHCP Server, nftables e Flask.