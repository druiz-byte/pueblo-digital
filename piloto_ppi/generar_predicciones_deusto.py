# -*- coding: utf-8 -*-
"""
GENERA PREDICCIONES f(X_i) DIRECTAS (versión limpia, requiere API) — para David.

Para cada encuestado REAL del Deustobarómetro construye una Persona con SU perfil
y lanza el LLM (Haiku) a responder el Bloque 5, obteniendo la predicción f_i
emparejada 1:1 con la respuesta real Y_i => montaje PPI++ ideal.

ANTI-CIRCULARIDAD: NO se inyectan en el prompt las variables que se predicen
(valoración política p18, democracia p20, confianza institucional p21).

Lee 'predictores_deusto.csv' (raíz del proyecto), ya convertido desde el .sav
(no requiere pyreadstat). Ejecutar en el ordenador de David con ANTHROPIC_API_KEY
en entrevista/.env.

Salida: entrevista/predicciones_deusto_bloque5.json  -> {id_real: {q_index: 'A'..}}
Uso:    python generar_predicciones_deusto.py --muestra 300
        python generar_predicciones_deusto.py            (los 1000)
"""
import sys, csv, json
from pathlib import Path

ENTREV = Path(__file__).resolve().parent
sys.path.insert(0, str(ENTREV))
import server
from prompt_v2 import build_system_prompt_v2

CSV  = ENTREV.parent / "predictores_deusto.csv"
TMPL = ENTREV / "encuestas" / "barometro_digital_5_politica_democracia.json"
OUT  = ENTREV / "predicciones_deusto_bloque5.json"

def to_num(s):
    s=(s or "").strip()
    return int(s) if s.isdigit() else None

def persona(row):
    """Perfil para el prompt v2. OMITE a propósito las variables objetivo (p18/p20/p21)."""
    return {
        "nombre": "Encuestado", "apellidos": f"#{row['id']}",
        "provincia": row.get("provincia") or "País Vasco",
        "edad": int(float(row["edad"])),
        "genero": row.get("genero") or "N/D",
        "nivel_estudios": row.get("nivel_estudios") or "N/D",
        "situacion_laboral": row.get("situacion_laboral") or "N/D",
        "clase_social": row.get("clase_social") or "N/D",
        "lengua_encuesta": row.get("lengua_encuesta") or "Castellano",
        "habitat": row.get("habitat") or "N/D",
        "euskera": "N/D",
        "voto_autonomicas_2024": row.get("voto_autonomicas_2024") or "N/D",
        "ideologia_0_10": to_num(row.get("ideologia_0_10")),
        "escala_nacionalismo_0_10": to_num(row.get("escala_nacionalismo_0_10")),
        # --- deliberadamente NO incluidos (circulares): ---
        "valoracion_politica_pv": "N/D", "valoracion_economia_pv": "N/D",
        "interes_politica": "N/D", "identidad": "N/D", "preferencia_territorial": "N/D",
        "nacimiento": "N/D", "problemas_dinero": "N/D", "principales_problemas": [],
        "perfil_mediatico": None, "perfil_bienestar": None, "perfil_social": None,
    }

def main():
    muestra = None
    if "--muestra" in sys.argv:
        muestra = int(sys.argv[sys.argv.index("--muestra")+1])
    server.build_system_prompt = build_system_prompt_v2
    preguntas = json.loads(TMPL.read_text(encoding="utf-8"))["preguntas"]
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    if muestra: rows = rows[:muestra]
    print(f"Generando predicciones para {len(rows)} encuestados (bloque 5, {len(preguntas)} preguntas)…")
    salida = {}
    for k, row in enumerate(rows, 1):
        try:
            resp, _txt = server._ask_persona(persona(row), preguntas)   # (resps, text)
            salida[row["id"]] = resp
        except Exception as e:
            print(f"  aviso id={row['id']}: {e}")
        if k % 25 == 0:
            print(f"  {k}/{len(rows)}"); OUT.write_text(json.dumps(salida, ensure_ascii=False), encoding="utf-8")
    OUT.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK -> {OUT}  ({len(salida)} encuestados)")

if __name__ == "__main__":
    main()
