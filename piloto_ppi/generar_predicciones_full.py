# -*- coding: utf-8 -*-
"""GENERA PREDICCIONES f(X_i) para las 152 preguntas (7 bloques) — versión PPI completo.

Para cada encuestado REAL del Deustobarómetro construye una Persona con SU perfil
(solo los predictores sociodemográficos + ideología/nacionalismo/voto) y lanza el
LLM (Haiku) a responder los 7 bloques del Barómetro digital, obteniendo la
predicción f_i emparejada 1:1 con su respuesta real Y_i (que vive en el .sav).

ANTI-CIRCULARIDAD: en el prompt NO se inyecta ninguna de las variables que se
predicen; solo van los 12 predictores de `predictores_deusto.csv`. Aun así, el
Bloque 7 (perfil) y las escalas de ideología/nacionalismo/voto SÍ son predictores
inyectados: en el análisis (true_ppi_full.py) se marcan como validación, no ganancia.

Salida:  predicciones_deusto_full.json  ->  {id_real: {bloque.json: {qi: 'A'..}}}
Uso:     python generar_predicciones_full.py --muestra 300
         python generar_predicciones_full.py            (los 1000)

Ejecutar en el ordenador de David (ANTHROPIC_API_KEY en entrevista/.env, GEMINI/
GROQ comentadas). Coste ~igual que una tanda del barómetro (~15-25 $).
"""
import sys, csv, json
from pathlib import Path

RAIZ   = Path(__file__).resolve().parent.parent
ENTREV = RAIZ / "entrevista"
sys.path.insert(0, str(ENTREV))
import server                                   # noqa: E402
from prompt_v2 import build_system_prompt_v2    # noqa: E402

CSV   = RAIZ / "predictores_deusto.csv"
TMPLS = sorted((ENTREV / "encuestas").glob("barometro_digital_*.json"))
OUT   = Path(__file__).parent / "predicciones_deusto_full.json"


def to_num(s):
    s = (s or "").strip()
    return int(s) if s.isdigit() else None


def build_prompt_enriquecido(a):
    """Envuelve build_system_prompt_v2 e inyecta religión y voto 2020 (el lugar de
    nacimiento ya lo renderiza la plantilla base). Solo añade lo que exista para no
    ensuciar el prompt con 'N/D'. No toca prompt_v2.py (compartido con la app)."""
    base = build_system_prompt_v2(a)
    extra = []
    rel = a.get("religion")
    if rel and rel != "N/D":
        extra.append(f"- Postura en materia religiosa: {rel}")
    v20 = a.get("voto_autonomicas_2020")
    if v20 and v20 != "N/D":
        extra.append(f"- Voto autonómicas 2020: {v20}")
    if not extra:
        return base
    marca = "\n\nINSTRUCCIONES DE RESPUESTA:"
    bloque = "\n\nPERFIL SOCIODEMOGRÁFICO ADICIONAL:\n" + "\n".join(extra)
    return base.replace(marca, bloque + marca, 1) if marca in base else base + bloque


def persona(row):
    """Perfil con SOLO los 12 predictores. Todo lo predicho queda fuera (N/D)."""
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
        # --- campos REALES añadidos para enriquecer el perfil (no se predicen en B1-B6): ---
        "nacimiento": row.get("nacimiento") or "N/D",
        "religion": row.get("religion") or "N/D",
        "voto_autonomicas_2020": row.get("voto_autonomicas_2020") or "N/D",
        # --- deliberadamente NO incluidos (se predicen): ---
        "valoracion_politica_pv": "N/D", "valoracion_economia_pv": "N/D",
        "interes_politica": "N/D", "identidad": "N/D", "preferencia_territorial": "N/D",
        "problemas_dinero": "N/D", "principales_problemas": [],
        "perfil_mediatico": None, "perfil_bienestar": None, "perfil_social": None,
    }


def main():
    muestra = None
    if "--muestra" in sys.argv:
        muestra = int(sys.argv[sys.argv.index("--muestra") + 1])
    if not server.ANTHROPIC_API_KEY:
        sys.exit("✗ Falta ANTHROPIC_API_KEY en entrevista/.env")
    if server.GEMINI_API_KEY or server.GROQ_API_KEY:
        sys.exit("✗ Comenta GEMINI_API_KEY/GROQ_API_KEY en .env para usar Claude Haiku")

    server.build_system_prompt = build_prompt_enriquecido
    bloques = [(p.name, json.loads(p.read_text(encoding="utf-8"))["preguntas"]) for p in TMPLS]
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    if muestra:
        rows = rows[:muestra]
    n_preg = sum(len(qs) for _, qs in bloques)
    print(f"Prediciendo {n_preg} preguntas × {len(rows)} encuestados "
          f"({len(bloques)} bloques) con {server.MODEL if hasattr(server,'MODEL') else 'Haiku'}…")

    # reanudable: si ya existe salida parcial, se continúa
    salida = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}

    for k, row in enumerate(rows, 1):
        rid = str(row["id"])
        salida.setdefault(rid, {})
        p = persona(row)
        for bname, preguntas in bloques:
            if bname in salida[rid]:      # ya hecho (reanudación)
                continue
            try:
                resp, _ = server._ask_persona(p, preguntas)   # {qi_str: 'A'..}
                salida[rid][bname] = resp
            except Exception as e:
                print(f"  aviso id={rid} {bname}: {e}")
        if k % 25 == 0:
            print(f"  {k}/{len(rows)}")
            OUT.write_text(json.dumps(salida, ensure_ascii=False), encoding="utf-8")

    OUT.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK -> {OUT.name}  ({len(salida)} encuestados)")


if __name__ == "__main__":
    main()
