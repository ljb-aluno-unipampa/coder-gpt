FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    isc-dhcp-client \
    iproute2 \
    iputils-ping \
    curl \
    jq \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/client

COPY start-client.sh .

RUN chmod +x start-client.sh

CMD ["/opt/client/start-client.sh"]
