# -*- coding: utf-8 -*-
"""Prueba rápida de la clave ANTHROPIC_API_KEY del .env. Sin dependencias.
Uso:  python test_anthropic.py
"""
import json
import urllib.request
import urllib.error
from pathlib import Path

env = Path(__file__).parent / ".env"
key = ""
for l in env.read_text(encoding="utf-8").splitlines():
    if l.strip().startswith("ANTHROPIC_API_KEY="):
        key = l.split("=", 1)[1].strip()

if not key:
    raise SystemExit("No hay ANTHROPIC_API_KEY en .env")

print("Clave: %s... (len=%d)" % (key[:12], len(key)))

req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=json.dumps({
        "model": "claude-haiku-4-5",
        "max_tokens": 10,
        "messages": [{"role": "user", "content": "hola"}],
    }).encode("utf-8"),
    headers={
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    },
)
try:
    resp = urllib.request.urlopen(req)
    print("OK", resp.status, "→ la clave es válida.")
except urllib.error.HTTPError as e:
    print("ERROR", e.code)
    print(e.read().decode("utf-8", "ignore")[:400])
