# -*- coding: utf-8 -*-
"""Diagnóstico de la clave Gemini: hace UNA llamada y muestra el error completo.

Uso: python test_gemini.py
Lee GEMINI_API_KEY y GEMINI_MODEL de .env (misma carpeta).
"""
import json, os, urllib.request, urllib.error
from pathlib import Path

# cargar .env
for line in (Path(__file__).parent / '.env').read_text(encoding='utf-8').splitlines():
    line = line.strip()
    if line and not line.startswith('#') and '=' in line:
        k, _, v = line.partition('=')
        os.environ.setdefault(k.strip(), v.strip())

KEY   = os.environ.get('GEMINI_API_KEY', '')
MODEL = os.environ.get('GEMINI_MODEL', 'gemini-3.5-flash')
print(f'Clave: ...{KEY[-6:]}  Modelo: {MODEL}\n')

def llamada(url, body=None):
    req = urllib.request.Request(
        url, method='POST' if body else 'GET',
        data=json.dumps(body).encode() if body else None,
        headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}
    except Exception as e:
        return 0, {'error': str(e)}

# 1) llamada mínima de generación
status, data = llamada(
    'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions',
    {'model': MODEL, 'max_tokens': 20,
     'messages': [{'role': 'user', 'content': 'Di solo "hola".'}]})
print(f'== Generación: HTTP {status} ==')
print(json.dumps(data, ensure_ascii=False, indent=2)[:2500])
