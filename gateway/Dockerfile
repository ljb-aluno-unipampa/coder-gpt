FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    kea-dhcp4-server \
    kea-ctrl-agent \
    nftables \
    python3 \
    python3-pip \
    python3-venv \
    iproute2 \
    iputils-ping \
    curl \
    jq \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip

RUN pip install \
    flask \
    python-dotenv \
    requests

WORKDIR /opt/gateway

COPY start-gateway.sh .
COPY templates templates
COPY gwapi.py .
COPY gwapi_app gwapi_app


RUN chmod +x start-gateway.sh

CMD ["/opt/gateway/start-gateway.sh"]