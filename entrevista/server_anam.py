# -*- coding: utf-8 -*-
"""Servidor de la app de entrevista con avatar sobre ANAM (anam.ai), panel v2.

Igual que server_v2.py (panel v2 + prompt v2 + /api/chat con Claude), pero en vez
de LiveAvatar usa Anam: expone /api/anam/session?id=NN que empareja la Persona con
su cara+voz (emparejar.py) y mina un token de sesión de Anam en el servidor con la
clave ANAM_API_KEY. El frontend inicializa el SDK de Anam con ese token y hace
client.talk(texto) con la respuesta que genera Claude.

Arranque:  python server_anam.py
Requiere en entrevista/.env:  ANAM_API_KEY=...  y  ANTHROPIC_API_KEY=...
"""
import os
import json
from pathlib import Path
from http.server import HTTPServer

import server                                    # .env, motor, /api/chat, estáticos
from prompt_v2 import build_system_prompt_v2
from emparejar import cargar_catalogo, elegir_avatar

ANAM_API = "https://api.anam.ai"

# ── Panel v2 + prompt v2 (idéntico a server_v2.py) ──────────────────────────
_here = Path(__file__).parent / "pv_agentes_v2.json"
_up = Path(__file__).parent.parent / "pv_agentes_v2.json"
V2 = _here if _here.exists() else _up
server.agents = json.loads(V2.read_text(encoding="utf-8"))["poblacion"]
server.build_system_prompt = build_system_prompt_v2

ANAM_API_KEY = os.environ.get("ANAM_API_KEY", "")
# server.py ya carga el .env; recogemos la clave de ahí si no está en el entorno
if not ANAM_API_KEY:
    _env = Path(__file__).parent / ".env"
    if _env.exists():
        for _l in _env.read_text(encoding="utf-8").splitlines():
            if _l.strip().startswith("ANAM_API_KEY="):
                ANAM_API_KEY = _l.split("=", 1)[1].strip()

_AGENTES_POR_ID = {str(a.get("id")): a for a in server.agents}


class AnamHandler(server.Handler):
    """Añade /api/anam/session; el resto de rutas las hereda de server.Handler."""

    def do_GET(self):
        if not self._authorized():
            return
        p = self.path.split("?")[0]
        if p in ("/anam", "/anam.html"):
            return self.serve_static("anam.html")
        return super().do_GET()

    def do_POST(self):
        p = self.path.split("?")[0]
        if p == "/api/anam/session":
            return self._anam_session()
        return super().do_POST()

    def _anam_session(self):
        body = self.read_body()
        pid = str(body.get("id") or body.get("agentId") or "")
        persona = _AGENTES_POR_ID.get(pid)
        if persona is None:
            return self.send_err(404, "No hay Persona con id=%s" % pid)
        if not ANAM_API_KEY:
            return self.send_err(500, "ANAM_API_KEY no configurada en el servidor.")

        cfg = elegir_avatar(persona)
        if not cfg["avatarId"]:
            return self.send_err(
                409, "La celda %s no tiene cara en el catálogo. Ejecuta "
                     "anam_setup.py crear <carpeta>." % cfg["celda"])

        payload = {"personaConfig": {
            "name": persona.get("nombre", "Persona"),
            "avatarId": cfg["avatarId"],
            "avatarModel": cfg["avatarModel"],
            "voiceId": cfg["voiceId"],
            "languageCode": cfg["languageCode"],
            # Desactiva el cerebro propio de Anam: la respuesta la genera Claude
            # (/api/chat) y se envía con talk(). Sin este campo Anam rechaza el
            # token como "legacy".
            "llmId": "CUSTOMER_CLIENT_V1",
        }}
        status, data = server.http_json(
            "%s/v1/auth/session-token" % ANAM_API, method="POST", body=payload,
            headers={"Authorization": "Bearer %s" % ANAM_API_KEY,
                     "Content-Type": "application/json"})
        if status != 200:
            return self.send_json({"error": data, "match": cfg}, status)
        return self.send_json({
            "sessionToken": data.get("sessionToken"),
            "match": cfg,
            "persona": {"id": persona.get("id"), "nombre": persona.get("nombre")},
        })


def main():
    cargar_catalogo()  # falla pronto si el catálogo no existe
    print("[ok] Panel v2 (Anam): %d Personas (%s)" % (len(server.agents), V2.name))
    if not ANAM_API_KEY:
        print("[aviso] ANAM_API_KEY no configurada")
    if not server.ANTHROPIC_API_KEY:
        print("[aviso] ANTHROPIC_API_KEY no configurada")
    httpd = HTTPServer(("", server.PORT), AnamHandler)
    print("Pueblo Digital — Entrevistador con avatar (Anam)")
    print("   Escuchando en el puerto %s" % server.PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Servidor detenido.")


if __name__ == "__main__":
    main()
