# -*- coding: utf-8 -*-
"""Utilidad para preparar Anam (anam.ai) y rellenar avatares_catalogo.json.

⚠ SE EJECUTA EN EL PC DE DAVID (necesita red a api.anam.ai y la clave ANAM_API_KEY).
El sandbox de Claude no llega a la API de Anam, igual que con Anthropic.

Requisitos:
  pip install requests
  En entrevista/.env:  ANAM_API_KEY=...    (créala en https://lab.anam.ai)

Subcomandos:
  python anam_setup.py voces
      Lista las voces disponibles en tu organización (id + nombre). Copia los
      IDs de las voces en castellano (y euskera si las hubiera) a
      avatares_catalogo.json → "voces".

  python anam_setup.py avatares
      Lista los avatares ya existentes (stock + los tuyos), con id y nombre.

  python anam_setup.py crear <carpeta_imagenes>
      Crea un avatar por cada imagen de la carpeta y lo añade a la celda que
      indique su nombre de fichero. Convención de nombre:
          <celda>__<loquesea>.png     p.ej.  m_66_plus__aitor.png
      Celdas válidas: h_18_30 h_31_50 h_51_65 h_66_plus
                      m_18_30 m_31_50 m_51_65 m_66_plus
                      x_18_30 x_31_50 x_51_65 x_66_plus
      Escribe los avatarId devueltos en avatares_catalogo.json → "celdas".
      Specs de imagen (Cara 4): cuadrada ≥1152x1152, fondo liso, expresión
      neutra, boca cerrada, cabeza+hombros, manos fuera de plano, <4.5MB.

  python anam_setup.py token <id_persona>
      Prueba de humo: calcula el emparejamiento de esa Persona y pide a Anam un
      token de sesión con su cara+voz. Verifica que catálogo y clave funcionan.
"""
import sys
import json
import os
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Falta 'requests'. Instala con: pip install requests")

from emparejar import cargar_catalogo, elegir_avatar

AQUI = Path(__file__).parent
CATALOGO_PATH = AQUI / "avatares_catalogo.json"
API = "https://api.anam.ai"

CELDAS_VALIDAS = {
    "h_18_30", "h_31_50", "h_51_65", "h_66_plus",
    "m_18_30", "m_31_50", "m_51_65", "m_66_plus",
    "x_18_30", "x_31_50", "x_51_65", "x_66_plus",
}


def _api_key():
    # Carga simple del .env (sin dependencias)
    env = AQUI / ".env"
    if env.exists():
        for linea in env.read_text(encoding="utf-8").splitlines():
            if linea.strip().startswith("ANAM_API_KEY="):
                return linea.split("=", 1)[1].strip()
    return os.environ.get("ANAM_API_KEY", "")


def _headers(key):
    return {"Authorization": "Bearer %s" % key}


def _guardar_catalogo(cat):
    CATALOGO_PATH.write_text(
        json.dumps(cat, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_voces(key):
    r = requests.get("%s/v1/voices" % API, headers=_headers(key), timeout=30)
    r.raise_for_status()
    data = r.json()
    voces = data.get("data", data) if isinstance(data, dict) else data
    print("Voces disponibles (%d):" % len(voces))
    for v in voces:
        print("  %-40s  %s  %s" % (
            v.get("id"), v.get("displayName") or v.get("name", ""),
            v.get("languageCode") or v.get("language") or ""))


def cmd_avatares(key):
    r = requests.get("%s/v1/avatars" % API, headers=_headers(key), timeout=30)
    r.raise_for_status()
    data = r.json()
    avs = data.get("data", data) if isinstance(data, dict) else data
    print("Avatares disponibles (%d):" % len(avs))
    for a in avs:
        tags = ",".join(a.get("displayTags") or [])
        print("  %-40s  %-28s  %s" % (
            a.get("id"), a.get("displayName", ""), tags))


def cmd_crear(key, carpeta):
    carpeta = Path(carpeta)
    if not carpeta.is_dir():
        sys.exit("No existe la carpeta: %s" % carpeta)
    cat = cargar_catalogo()
    imgs = [p for p in sorted(carpeta.iterdir())
            if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
    if not imgs:
        sys.exit("No hay imágenes (.png/.jpg/.webp) en %s" % carpeta)

    creados = 0
    for img in imgs:
        celda = img.stem.split("__", 1)[0]
        if celda not in CELDAS_VALIDAS:
            print("  [salto] %s: prefijo de celda no válido (%s)" % (img.name, celda))
            continue
        with open(img, "rb") as fh:
            r = requests.post(
                "%s/v1/avatars" % API, headers=_headers(key),
                data={"displayName": img.stem[:50], "avatarModel": "cara-4"},
                files={"imageFile": (img.name, fh)}, timeout=120)
        if r.status_code == 403:
            sys.exit("403: crear avatares custom requiere plan superior en Anam. "
                     "Revisa tu plan o usa la galería stock (subcomando 'avatares').")
        if r.status_code not in (200, 201):
            print("  [error] %s: HTTP %s %s" % (img.name, r.status_code, r.text[:200]))
            continue
        avatar_id = r.json().get("id")
        cat["celdas"].setdefault(celda, [])
        if avatar_id not in cat["celdas"][celda]:
            cat["celdas"][celda].append(avatar_id)
        creados += 1
        print("  [ok] %s → %s (celda %s)" % (img.name, avatar_id, celda))

    _guardar_catalogo(cat)
    print("\nCreados %d avatares. Catálogo actualizado: %s" % (creados, CATALOGO_PATH.name))


def cmd_token(key, id_persona):
    panel = json.loads((AQUI.parent / "pv_agentes_v2.json").read_text(encoding="utf-8"))
    persona = next((p for p in panel["poblacion"] if str(p.get("id")) == str(id_persona)), None)
    if persona is None:
        sys.exit("No hay Persona con id=%s" % id_persona)
    cfg = elegir_avatar(persona)
    print("Persona %s (%s, %s, %s años) → celda %s, voz %s" % (
        id_persona, persona.get("nombre"), persona.get("genero"),
        persona.get("edad"), cfg["celda"], cfg["claveVoz"]))
    if not cfg["avatarId"]:
        sys.exit("Esa celda aún no tiene cara en el catálogo. Ejecuta 'crear' primero.")
    body = {"personaConfig": {
        "name": persona.get("nombre", "Persona"),
        "avatarId": cfg["avatarId"], "avatarModel": cfg["avatarModel"],
        "voiceId": cfg["voiceId"], "languageCode": cfg["languageCode"],
        "llmId": "CUSTOMER_CLIENT_V1"}}
    r = requests.post("%s/v1/auth/session-token" % API, headers=_headers(key),
                      json=body, timeout=30)
    print("HTTP %s" % r.status_code)
    print(r.text[:400])


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    key = _api_key()
    if not key:
        sys.exit("Falta ANAM_API_KEY en entrevista/.env o en el entorno.")
    cmd = sys.argv[1]
    if cmd == "voces":
        cmd_voces(key)
    elif cmd == "avatares":
        cmd_avatares(key)
    elif cmd == "crear" and len(sys.argv) >= 3:
        cmd_crear(key, sys.argv[2])
    elif cmd == "token" and len(sys.argv) >= 3:
        cmd_token(key, sys.argv[2])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
