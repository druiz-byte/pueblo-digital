# -*- coding: utf-8 -*-
"""PREDICCIONES CON PROMPT ANTI-CONCENTRACIÓN — el contraste que faltaba.

Idéntico a `generar_predicciones_full.py` en TODO (mismo perfil de 12 predictores,
mismos 7 bloques, mismo modelo, mismos encuestados) salvo en una cosa: se añade al
prompt de encuesta la instrucción anti-concentración, **exactamente el mismo texto**
que se usó en el hueco 3 sobre Ikuspegi (se importa de `entrevista/lanzar_robustez.py`,
no se copia, para que no puedan divergir).

POR QUÉ IMPORTA. Sobre Ikuspegi ese prompt **mejoró** la fidelidad agregada
(DAM 15,7 → 14,8 · concentración 83,7 → 79,4). Pero Ikuspegi no tiene microdatos, así
que allí no se pudo comprobar lo decisivo: **si repartir la distribución mejora o
empeora el acierto persona a persona.** El Deustobarómetro sí tiene el microdato y
permite el emparejamiento 1:1, así que aquí se puede medir.

La Proposición 1 predice que no puede mejorar: repartir varianza no crea información
donde no la hay, y añadir ruido alrededor de la misma media condicional es atenuación
estricta. Si se confirma —agregado mejor, individual peor— es la demostración más
limpia posible del corolario de separabilidad.

Salida:  predicciones_deusto_anticonc.json   (mismo formato que la de referencia)
Uso:     python generar_predicciones_anticonc.py --muestra 300     ← PAREADO con la de referencia
         python generar_predicciones_anticonc.py                    (los 1.000)

⚠ Requiere API: ejecutar en el PC de David. Reanudable (guarda cada 25 encuestados).
⚠ Los 300 de la tanda de referencia son los 300 PRIMEROS del fichero, así que
  `--muestra 300` reproduce exactamente el mismo conjunto y el contraste es pareado.
"""
import sys, csv, json
from pathlib import Path

RAIZ   = Path(__file__).resolve().parent.parent
ENTREV = RAIZ / "entrevista"
sys.path.insert(0, str(ENTREV))
sys.path.insert(0, str(Path(__file__).parent))

import server                                          # noqa: E402
from lanzar_robustez import PROMPT_ANTICONC            # noqa: E402  (mismo texto, no copiado)
from generar_predicciones_full import (                # noqa: E402  (misma construcción de perfil)
    build_prompt_enriquecido, persona, CSV, TMPLS,
)

OUT = Path(__file__).parent / "predicciones_deusto_anticonc.json"


def main():
    muestra = None
    if "--muestra" in sys.argv:
        muestra = int(sys.argv[sys.argv.index("--muestra") + 1])
    if not server.ANTHROPIC_API_KEY:
        sys.exit("✗ Falta ANTHROPIC_API_KEY en entrevista/.env")
    if server.GEMINI_API_KEY or server.GROQ_API_KEY:
        sys.exit("✗ Comenta GEMINI_API_KEY/GROQ_API_KEY en .env para usar Claude")

    # las dos únicas diferencias con la tanda de referencia
    server.build_system_prompt = build_prompt_enriquecido
    server.EXTRA_INSTRUCCIONES = PROMPT_ANTICONC

    bloques = [(p.name, json.loads(p.read_text(encoding="utf-8"))["preguntas"]) for p in TMPLS]
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    if muestra:
        rows = rows[:muestra]              # los MISMOS que la tanda de referencia
    n_preg = sum(len(qs) for _, qs in bloques)

    print("══ Predicciones con prompt ANTI-CONCENTRACIÓN ══")
    print(f"  modelo ........ {server.ANTHROPIC_MODEL}")
    print(f"  encuestados ... {len(rows)} (los mismos que predicciones_deusto_full.json)")
    print(f"  preguntas ..... {n_preg} en {len(bloques)} bloques")
    print(f"  prompt extra .. SÍ — {len(PROMPT_ANTICONC.split())} palabras")
    print("  referencia .... Pearson escalas 0,123 · kappa_w ordinales 0,100 · "
          "kappa nominales 0,231\n")

    salida = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    vacios = 0

    for k, row in enumerate(rows, 1):
        rid = str(row["id"])
        salida.setdefault(rid, {})
        p = persona(row)
        for bname, preguntas in bloques:
            if bname in salida[rid]:
                continue
            try:
                resp, _ = server._ask_persona(p, preguntas)
                salida[rid][bname] = resp
                if not resp:
                    vacios += 1
            except Exception as e:
                print(f"  aviso id={rid} {bname}: {e}")
        if k % 25 == 0:
            print(f"  {k}/{len(rows)}  (bloques vacíos hasta ahora: {vacios})")
            OUT.write_text(json.dumps(salida, ensure_ascii=False), encoding="utf-8")

    OUT.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = len(rows) * len(bloques)
    print(f"\nOK → {OUT.name}  ({len(salida)} encuestados)")
    print(f"bloques vacíos: {vacios}/{tot} ({100*vacios/max(tot,1):.1f} %)")
    if vacios / max(tot, 1) > 0.02:
        print("⛔ Más del 2 % de bloques vacíos: revisa antes de analizar.")
    print("\n══ Análisis ══")
    print("  python acuerdo_individual.py --pred predicciones_deusto_anticonc.json")
    print("  python comparar_anticonc.py")


if __name__ == "__main__":
    main()
