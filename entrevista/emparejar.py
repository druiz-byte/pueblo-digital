# -*- coding: utf-8 -*-
"""Emparejador determinista Persona → (cara Anam, voz).

Objetivo: que NO haya que elegir avatar ni voz a mano. A partir de tres campos
que ya trae cada Persona del panel v2 (genero, edad, lengua_encuesta) se calcula
la celda demográfica (género × franja de edad) y el idioma, y se devuelven el
avatarId y voiceId del catálogo `avatares_catalogo.json`.

Determinista: dentro de una celda con varias caras, la Persona recibe siempre la
misma (id mod nº_caras). Sin API: se puede probar sobre las 1.000 Personas ya.

Uso como módulo:
    from emparejar import elegir_avatar
    cfg = elegir_avatar(persona)   # dict con avatarId, voiceId, languageCode, ...

Uso por línea de comandos (diagnóstico sobre el panel):
    python emparejar.py            # distribución por celda + huecos del catálogo
"""
import json
from pathlib import Path

_AQUI = Path(__file__).parent
_CATALOGO = None


def cargar_catalogo(ruta=None):
    """Carga (y cachea) el catálogo de avatares/voces."""
    global _CATALOGO
    if _CATALOGO is None or ruta is not None:
        p = Path(ruta) if ruta else (_AQUI / "avatares_catalogo.json")
        _CATALOGO = json.loads(p.read_text(encoding="utf-8"))
    return _CATALOGO


# ── Normalización de los campos de la Persona ───────────────────────────────
def franja_edad(edad):
    """Franja de edad → sufijo de celda. Bordes: 30, 50, 65."""
    try:
        e = int(edad)
    except (TypeError, ValueError):
        return "31_50"                      # franja modal como defecto seguro
    if e <= 30:
        return "18_30"
    if e <= 50:
        return "31_50"
    if e <= 65:
        return "51_65"
    return "66_plus"


def clave_genero(genero):
    """genero → h / m / x (No binario u otros)."""
    g = (genero or "").strip().lower()
    if g.startswith("hombre") or g in ("h", "varón", "varon", "masculino"):
        return "h"
    if g.startswith("mujer") or g in ("m", "femenino"):
        return "m"
    return "x"


def clave_idioma(persona):
    """lengua_encuesta → cas / eus."""
    lengua = (persona.get("lengua_encuesta") or "").strip().lower()
    return "eus" if lengua.startswith("eus") else "cas"


def clave_celda(persona):
    return "%s_%s" % (clave_genero(persona.get("genero")),
                      franja_edad(persona.get("edad")))


# ── Selección de cara y voz ─────────────────────────────────────────────────
def _lista_caras(celdas, celda, gen):
    """Caras de la celda; si 'x' está vacía, cae a la celda 'm' de igual edad."""
    caras = celdas.get(celda) or []
    if not caras and gen == "x":
        alt = "m_" + celda.split("_", 1)[1]
        caras = celdas.get(alt) or []
        celda = alt if caras else celda
    return caras, celda


def elegir_avatar(persona, catalogo=None):
    """Devuelve la configuración de avatar/voz emparejada con la Persona.

    Claves del dict devuelto:
      avatarId       str | None   (None si el catálogo aún no tiene caras)
      avatarModel    str          ('cara-4')
      voiceId        str | None
      languageCode   str          ('es' / 'eu')
      ttsExterno     str | None   (p.ej. 'azure:eu-ES-AinhoaNeural' para euskera)
      celda          str          celda usada (tras posible fallback)
      idioma         str          'cas' / 'eus'
      claveVoz       str          p.ej. 'cas_h'
    """
    cat = catalogo or cargar_catalogo()
    gen = clave_genero(persona.get("genero"))
    celda = clave_celda(persona)
    idioma = clave_idioma(persona)
    clave_voz = "%s_%s" % (idioma, gen)

    caras, celda_final = _lista_caras(cat["celdas"], celda, gen)
    avatar_id = None
    if caras:
        avatar_id = caras[int(persona.get("id", 0)) % len(caras)]

    # La entrada de voz puede ser un dict (una voz) o una lista (varias voces
    # que rotan por id, como las caras).
    voz_entry = cat["voces"].get(clave_voz) or cat["voces"].get("%s_m" % idioma) or {}
    if isinstance(voz_entry, list):
        voz = voz_entry[int(persona.get("id", 0)) % len(voz_entry)] if voz_entry else {}
    else:
        voz = voz_entry

    return {
        "avatarId":     avatar_id,
        "avatarModel":  cat.get("avatar_model", "cara-4"),
        "voiceId":      voz.get("voiceId"),
        "languageCode": voz.get("languageCode", "es"),
        "ttsExterno":   voz.get("tts_externo"),
        "celda":        celda_final,
        "idioma":       idioma,
        "claveVoz":     clave_voz,
    }


# ── Diagnóstico ─────────────────────────────────────────────────────────────
def _diagnostico():
    from collections import Counter
    ruta_panel = _AQUI.parent / "pv_agentes_v2.json"
    poblacion = json.loads(ruta_panel.read_text(encoding="utf-8"))["poblacion"]
    cat = cargar_catalogo()

    celdas = Counter()
    voces = Counter()
    sin_cara = 0
    for p in poblacion:
        cfg = elegir_avatar(p, cat)
        celdas[cfg["celda"]] += 1
        voces[cfg["claveVoz"]] += 1
        if cfg["avatarId"] is None:
            sin_cara += 1

    print("Personas: %d\n" % len(poblacion))
    print("Reparto por celda (género × edad):")
    for c in sorted(celdas):
        n_caras = len(cat["celdas"].get(c) or [])
        estado = "%d caras" % n_caras if n_caras else "SIN CARAS (rellenar catálogo)"
        print("  %-10s %4d Personas   [%s]" % (c, celdas[c], estado))
    print("\nReparto por voz (idioma × género):")
    for v in sorted(voces):
        print("  %-8s %4d Personas" % (v, voces[v]))
    print("\nPersonas sin cara asignada (catálogo incompleto): %d/%d" %
          (sin_cara, len(poblacion)))
    if sin_cara == 0:
        print("Catálogo completo: todas las Personas tienen cara.")
    else:
        print("Ejecuta anam_setup.py para crear/enlazar avatares y rellenar el catálogo.")


if __name__ == "__main__":
    _diagnostico()
