# -*- coding: utf-8 -*-
"""Contraste PAREADO: prompt por defecto vs prompt anti-concentración,
sobre los MISMOS encuestados reales del Deustobarómetro.

Pone lado a lado las dos cosas que en Ikuspegi no se podían medir juntas:

  AGREGADO   concentración modal y DAM      → ¿el prompt reparte la distribución?
  INDIVIDUAL Pearson, kappa y Δ vs moda     → ¿repartirla mejora el acierto persona a persona?

La predicción preregistrada es que **se muevan en direcciones opuestas**: el agregado
mejora y el individual empeora. Si es así, es la demostración limpia del corolario de
separabilidad (§3.5). Si el individual también mejora, el reparto era informativo y hay
que revisar la Proposición 2(b).

No requiere API. Uso:  python comparar_anticonc.py
"""
import json, sys
from pathlib import Path
import numpy as np

AQUI = Path(__file__).parent
sys.path.insert(0, str(AQUI))
import acuerdo_individual as A            # noqa: E402
T = A.T                                   # true_ppi_full

BASE = AQUI / "predicciones_deusto_full.json"
ANTI = AQUI / "predicciones_deusto_anticonc.json"


def metricas(pred_file):
    """Individual (por familia de pregunta) + agregado (concentración modal)."""
    T.PREDF = pred_file
    pred = T.cargar_predicciones()
    filas = [A.evaluar(e, pred) for e in T.CW]
    circ = {"p36", "p38", "p40", "p41", "p42", "p44_1", "p44_2", "p44_3", "p45", "p46"}
    filas = [f for f in filas if f.get("var") not in circ]        # fuera los inyectados

    def sub(st, k):
        v = [f[k] for f in filas if f.get("subtipo") == st and f.get(k) is not None
             and f[k] == f[k]]
        return float(np.mean(v)) if v else float("nan")

    # concentración modal del panel, sobre las mismas preguntas
    concs = []
    for e in T.CW:
        if e.get("var") in circ:
            continue
        arr = T.arrays_pregunta(e, pred)
        if arr[0] == "cat":
            _, _, Flab, ops = arr
            if len(Flab) == 0:
                continue
            _, c = np.unique(Flab, return_counts=True)
            concs.append(100.0 * c.max() / len(Flab))
        elif arr[0] == "escala":
            _, _, F = arr
            if len(F) == 0:
                continue
            _, c = np.unique(F, return_counts=True)
            concs.append(100.0 * c.max() / len(F))

    return {
        "pearson_escalas":  sub("escala_0_10", "spearman"),   # aprox.; el Pearson exacto va aparte
        "exacto_escalas":   sub("escala_0_10", "exacto_%"),
        "pm1_escalas":      sub("escala_0_10", "pm1_%"),
        "MAE_escalas":      sub("escala_0_10", "MAE"),
        "delta_escalas":    sub("escala_0_10", "delta_vs_moda"),
        "kappa_ordinales":  sub("cat_ordinal", "kappa_w"),
        "exacto_ordinales": sub("cat_ordinal", "exacto_%"),
        "delta_ordinales":  sub("cat_ordinal", "delta_vs_moda"),
        "kappa_nominales":  sub("cat_nominal", "kappa"),
        "exacto_nominales": sub("cat_nominal", "exacto_%"),
        "delta_nominales":  sub("cat_nominal", "delta_vs_moda"),
        "concentracion":    float(np.mean(concs)) if concs else float("nan"),
        "n_items":          len(filas),
    }


def main():
    if not ANTI.exists():
        sys.exit(f"✗ Falta {ANTI.name}. Genera primero:\n"
                 f"   python generar_predicciones_anticonc.py --muestra 300")
    B, X = metricas(BASE), metricas(ANTI)

    L = ["# Prompt anti-concentración sobre encuestados reales — contraste pareado", "",
         f"Mismos encuestados, mismas {B['n_items']} preguntas no circulares, mismo modelo.",
         "**Lo único que cambia es la instrucción anti-concentración en el prompt.**", "",
         "| | por defecto | anti-conc. | Δ | dirección esperada |",
         "|---|--:|--:|--:|---|"]

    FILAS = [
        ("**AGREGADO**", None, None, None, ""),
        ("Concentración modal", "concentracion", "baja", "↓ = el prompt funciona", 1),
        ("**INDIVIDUAL · escalas 0-10**", None, None, None, ""),
        ("Acierto exacto %", "exacto_escalas", None, "↓ si el reparto es ruido", 1),
        ("Dentro de ±1 %", "pm1_escalas", None, "↓ si el reparto es ruido", 1),
        ("MAE (puntos)", "MAE_escalas", None, "↑ si el reparto es ruido", 1),
        ("Δ vs moda", "delta_escalas", None, "↓ si el reparto es ruido", 1),
        ("**INDIVIDUAL · ordinales**", None, None, None, ""),
        ("Kappa ponderado", "kappa_ordinales", None, "≈ plano o ↓", 1),
        ("Acierto exacto %", "exacto_ordinales", None, "↓", 1),
        ("Δ vs moda", "delta_ordinales", None, "↓ (más negativo)", 1),
        ("**INDIVIDUAL · nominales**", None, None, None, ""),
        ("Kappa", "kappa_nominales", None, "≈ plano o ↓", 1),
        ("Δ vs moda", "delta_nominales", None, "↓ — pierde el único positivo", 1),
    ]
    for fila in FILAS:
        if fila[1] is None:
            L.append(f"| {fila[0]} | | | | |"); continue
        etq, k = fila[0], fila[1]
        b, x = B[k], X[k]
        L.append(f"| {etq} | {b:.3f} | {x:.3f} | {x-b:+.3f} | {fila[3]} |")

    L += ["", "## Lectura", "",
          "- Si la **concentración baja** y el **acuerdo individual empeora**, los dos límites son",
          "  independientes: repartir la distribución no crea información. Es la confirmación",
          "  directa del corolario de separabilidad, y significa que **optimizar la métrica que",
          "  reporta la industria daña la propiedad que necesitan las aplicaciones.**",
          "- Si la concentración baja y el acuerdo individual **también mejora**, el reparto era",
          "  informativo: el prompt por defecto estaba suprimiendo variación real ligada al perfil.",
          "  Habría que revisar la Proposición 2(b) y sería una buena noticia para el método.",
          "- Si no se mueve nada, el prompt no transporta del cuestionario de Ikuspegi al",
          "  Deustobarómetro y hay que decirlo.", "",
          "> Predicciones preregistradas en `../paper/preregistro_anticonc_individual.md`."]

    out = AQUI / "comparar_anticonc.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n→ {out.name}")


if __name__ == "__main__":
    main()
