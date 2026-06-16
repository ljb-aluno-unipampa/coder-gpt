import json
from pathlib import Path

STATE_FILE = Path("/opt/gateway/data/firewall_state.json")

DEFAULT_STATE = {
    "default_policy": "drop",
    "groups": {
        "manual_blocked": [],
        "manual_allowed": []
    },
    "rules": []
}

def load_state():
    if not STATE_FILE.exists():
        save_state(DEFAULT_STATE)
    return json.loads(STATE_FILE.read_text())

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

def generate_ruleset(state):
    return "flush ruleset\n# TODO: gerar nftables dinamicamente\n"
