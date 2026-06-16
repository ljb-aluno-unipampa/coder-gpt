{
  "Dhcp4": {

    "interfaces-config": {
      "interfaces": [ "__LAN_IF__" ]
    },

    "lease-database": {
      "type": "memfile",
      "persist": true,
      "name": "/opt/gateway/data/kea-leases.csv"
    },

    "renew-timer": 900,
    "rebind-timer": 1800,
    "valid-lifetime": 3600,

    "subnet4": [
      {
        "id": 1,

        "subnet": "__DHCP_SUBNET__",

        "pools": [
          {
            "pool": "__POOL_START__ - __POOL_END__"
          }
        ],

        "option-data": [
          {
            "name": "routers",
            "data": "__LAN_IP__"
          },
          {
            "name": "domain-name-servers",
            "data": "__DHCP_DNS__"
          },
          {
            "name": "domain-name",
            "data": "__DHCP_DOMAIN__"
          }
        ]
      }
    ]
  }
}