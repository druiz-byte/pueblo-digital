# -*- coding: utf-8 -*-
"""Servidor de la app de entrevista con avatar, version v2.

Sirve las Personas del panel v2 (pv_agentes_v2.json) y usa el prompt v2.
Requiere las variables de entorno HEYGEN_API_KEY y ANTHROPIC_API_KEY.
Arranque: python server_v2.py
"""
import json
from pathlib import Path
from http.server import HTTPServer

import server                                   # carga .env, motor, rutas y frontend
from prompt_v2 import build_system_prompt_v2

# 1) Cargar el panel v2. Busca el fichero junto al script (Render) o en la
#    carpeta padre (entorno local).
_here = Path(__file__).parent / "pv_agentes_v2.json"
_up = Path(__file__).parent.parent / "pv_agentes_v2.json"
V2 = _here if _here.exists() else _up
server.agents = json.loads(V2.read_text(encoding="utf-8"))["poblacion"]

# 2) Usar el generador de prompt v2 (lo usa /api/chat).
server.build_system_prompt = build_system_prompt_v2

print("[ok] Panel v2 cargado: %d Personas (%s)" % (len(server.agents), V2.name))
if not server.LIVEAVATAR_API_KEY:
    print("[aviso] HEYGEN_API_KEY (LiveAvatar) no configurada")
if not server.ANTHROPIC_API_KEY:
    print("[aviso] ANTHROPIC_API_KEY no configurada")

httpd = HTTPServer(("", server.PORT), server.Handler)
print("Pueblo Digital v2 - Entrevistador con avatar")
print("   Escuchando en el puerto %s" % server.PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Servidor detenido.")
