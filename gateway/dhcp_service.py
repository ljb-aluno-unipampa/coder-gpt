import requests

class KeaService:
    def __init__(self, url="http://127.0.0.1:8000"):
        self.url = url

    def command(self, payload):
        return requests.post(self.url, json=payload, timeout=10).json()

    def status(self):
        return self.command({"command":"status-get","service":["dhcp4"]})
