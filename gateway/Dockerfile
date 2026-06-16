FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    kea-dhcp4-server \
    kea-ctrl-agent \
    nftables \
    python3 \
    python3-pip \
    iproute2 \
    iputils-ping \
    curl \
    jq \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install \
    flask \
    python-dotenv \
    requests

WORKDIR /opt/gateway

COPY start-gateway.sh /opt/gateway/

RUN chmod +x /opt/gateway/start-gateway.sh

CMD ["/opt/gateway/start-gateway.sh"]