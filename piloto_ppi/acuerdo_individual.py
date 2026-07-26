# -*- coding: utf-8 -*-
"""ACUERDO INDIVIDUAL (microdato): respuesta de la persona REAL vs su persona DIGITAL.

Complementa a `true_ppi_full.py`. Aquel mide si coincide la DISTRIBUCIÓN (agregado);
éste mide si coincide CADA PERSONA con su gemelo digital — el criterio 4 de Argyle
("correspondencia de patrones"), el más exigente.

MÉTRICA SEGÚN EL TIPO DE PREGUNTA (la distancia importa: un 7 real vs 8 predicho
NO es el mismo error que 7 vs 1):

  escala 0-10   -> acuerdo exacto, |dif|<=1, MAE, RMSE, Spearman, kappa cuadrático
  cat ORDINAL   -> acuerdo exacto, ±1 categoría, MAE en pasos, kappa cuadrático
  cat NOMINAL   -> acuerdo exacto, kappa de Cohen (sin ±1: no hay orden)
  multi         -> Jaccard y F1 por persona

BASELINE (imprescindible): "predecir siempre la MODA real". El panel colapsa en la
moda (p18 -> 'Regular' 83%), así que el % de acierto crudo engaña: la moda sola ya
acierta ~40%. Lo que cuenta es si el panel SUPERA a la moda (delta > 0) y si kappa > 0.

NS/NC se excluye de las métricas de distancia (en las escalas es la opción L = índice
11: tratarlo como número sería un 11 en una escala 0-10) y se reporta aparte.

Uso:  python acuerdo_individual.py                          # predicciones actuales
      python acuerdo_individual.py --pred predicciones_deusto_full_v1perfilpobre.json
      python acuerdo_individual.py --sav                     # + .sav en formato ANCHO para SPSS
"""
import sys, json, re
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

# true_ppi_full importa ppi_engine -> ppi_py (la librería PPI++). Este análisis NO
# hace inferencia PPI, solo empareja individuos, así que si la librería no está
# instalada se sustituye por un stub y se reutiliza igual el resto (.sav, crosswalk,
# arrays_pregunta). Evita tener que instalar ppi-python solo para esto.
try:
    import ppi_py  # noqa: F401
except ModuleNotFoundError:
    import types
    _s = types.ModuleType("ppi_py")
    for _f in ("ppi_mean_ci", "ppi_mean_pointestimate", "classical_mean_ci"):
        setattr(_s, _f, lambda *a, **k: (_ for _ in ()).throw(
            RuntimeError("ppi_py no instalado (no hace falta para acuerdo_individual)")))
    sys.modules["ppi_py"] = _s

import true_ppi_full as T          # reutiliza .sav, crosswalk, arrays_pregunta

AQUI = Path(__file__).parent
NS_RE = re.compile(r"no lo s|prefiero no|no contesta|ns/nc|no sabe|no procede", re.I)

# Secuencias ordinales conocidas del cuestionario. Si una "cat" encaja, se trata
# como ORDINAL (la distancia entre categorías tiene sentido).
ORDINALES = [
    ["muy buena", "buena", "regular", "mala", "muy mala"],
    ["mucho mejor", "mejor", "igual", "peor", "mucho peor"],
    ["mucho", "bastante", "poco", "nada"],
    ["mucha", "bastante", "poca", "ninguna"],
    ["muy de acuerdo", "de acuerdo", "en desacuerdo", "muy en desacuerdo"],
    ["muy satisfecho", "satisfecho", "insatisfecho", "muy insatisfecho"],
    ["siempre", "casi siempre", "a veces", "casi nunca", "nunca"],
    ["muy alto", "alto", "bajo", "muy bajo"],
    ["muy probable", "probable", "poco probable", "nada probable"],
    ["lo he hecho", "lo he pensado hacer", "ni lo he hecho"],
    ["muy interesado", "bastante interesado", "poco interesado", "nada interesado"],
]


def es_ordinal(ops_norm):
    lim = [o for o in ops_norm if not NS_RE.search(o)]
    if len(lim) < 3:
        return False
    for pat in ORDINALES:
        hits = sum(any(p in o or o in p for p in pat) for o in lim)
        if hits >= max(2, len(lim) - 1):
            return True
    return False


# ---------------- métricas ----------------
def _kappa(a, b, k, pesos=None):
    """Kappa de Cohen sobre índices 0..k-1. pesos: None (nominal) o 'quadratic'."""
    if len(a) == 0:
        return float("nan")
    O = np.zeros((k, k));
    for x, y in zip(a, b):
        O[int(x), int(y)] += 1
    O /= O.sum()
    ra = O.sum(1); rb = O.sum(0)
    E = np.outer(ra, rb)
    if pesos == "quadratic":
        idx = np.arange(k)
        W = (idx[:, None] - idx[None, :]) ** 2 / max((k - 1) ** 2, 1)
    else:
        W = 1.0 - np.eye(k)
    den = (W * E).sum()
    return float("nan") if den == 0 else 1.0 - (W * O).sum() / den


def _spearman(x, y):
    if len(x) < 3:
        return float("nan")
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    if rx.std() == 0 or ry.std() == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def _moda_acierto(y):
    """% de acierto de 'predecir siempre la moda real' (baseline)."""
    if len(y) == 0:
        return float("nan")
    v, c = np.unique(y, return_counts=True)
    return float(c.max() / len(y) * 100)


def evaluar(e, pred):
    ops_norm = [T._nm(o) for o in e["opciones"]]
    out = {"bloque": e["bloque"], "qi": e["qi"], "var": e.get("var"),
           "texto": str(e["texto"])[:80], "tipo": e["tipo"]}
    arr = T.arrays_pregunta(e, pred)

    if arr[0] == "escala":
        _, Y, F = arr
        out["subtipo"] = "escala_0_10"
        out["n"] = int(len(Y))
        if len(Y) == 0:
            return out
        d = np.abs(Y - F)
        out["exacto_%"] = float((d == 0).mean() * 100)
        out["pm1_%"] = float((d <= 1).mean() * 100)
        out["MAE"] = float(d.mean())
        out["RMSE"] = float(np.sqrt((d ** 2).mean()))
        out["sesgo"] = float((F - Y).mean())
        out["spearman"] = _spearman(Y, F)
        out["kappa_w"] = _kappa(Y.astype(int), F.astype(int), 11, "quadratic")
        out["base_moda_%"] = _moda_acierto(Y)
        out["delta_vs_moda"] = out["exacto_%"] - out["base_moda_%"]
        return out

    if arr[0] == "cat":
        _, Ylab, Flab, ops = arr
        ordinal = es_ordinal(ops_norm)
        out["subtipo"] = "cat_ordinal" if ordinal else "cat_nominal"
        # índices en el orden de la plantilla, excluyendo NS/NC
        val = [o for o in ops if not NS_RE.search(o)]
        pos = {o: j for j, o in enumerate(val)}
        pares = [(pos[a], pos[b]) for a, b in zip(Ylab, Flab) if a in pos and b in pos]
        out["n"] = len(pares)
        out["ns_real_%"] = float(np.mean([a not in pos for a in Ylab]) * 100) if len(Ylab) else float("nan")
        out["ns_panel_%"] = float(np.mean([b not in pos for b in Flab]) * 100) if len(Flab) else float("nan")
        if not pares:
            return out
        a = np.array([p[0] for p in pares]); b = np.array([p[1] for p in pares])
        k = len(val)
        d = np.abs(a - b)
        out["exacto_%"] = float((d == 0).mean() * 100)
        out["base_moda_%"] = _moda_acierto(a)
        out["delta_vs_moda"] = out["exacto_%"] - out["base_moda_%"]
        if ordinal:
            out["pm1_%"] = float((d <= 1).mean() * 100)
            out["MAE"] = float(d.mean())          # en "pasos" de categoría
            out["sesgo"] = float((b - a).mean())
            out["spearman"] = _spearman(a, b)
            out["kappa_w"] = _kappa(a, b, k, "quadratic")
        else:
            out["kappa"] = _kappa(a, b, k, None)
        return out

    # multi -> Jaccard / F1 por persona
    _, cols = arr
    cols = [c for c in cols if c is not None]
    if not cols:
        out["subtipo"] = "multi"; out["n"] = 0
        return out
    Ym = np.vstack([c[0] for c in cols]).T
    Fm = np.vstack([c[1] for c in cols]).T
    inter = (Ym * Fm).sum(1); uni = ((Ym + Fm) > 0).sum(1)
    jac = np.where(uni > 0, inter / np.maximum(uni, 1), np.nan)
    prec = np.where(Fm.sum(1) > 0, inter / np.maximum(Fm.sum(1), 1), np.nan)
    rec = np.where(Ym.sum(1) > 0, inter / np.maximum(Ym.sum(1), 1), np.nan)
    f1 = 2 * prec * rec / np.maximum(prec + rec, 1e-9)
    out["subtipo"] = "multi"; out["n"] = int(len(jac))
    out["jaccard"] = float(np.nanmean(jac))
    out["F1"] = float(np.nanmean(f1))
    return out


def main():
    pred_file = None
    if "--pred" in sys.argv:
        pred_file = sys.argv[sys.argv.index("--pred") + 1]
        T.PREDF = AQUI / pred_file
    pred = T.cargar_predicciones()
    ids = sorted(pred)
    print(f"Predicciones: {T.PREDF.name} — {len(ids)} encuestados emparejados 1:1\n")

    filas = [evaluar(e, pred) for e in T.CW]

    # ---- informe ----
    L = ["# Acuerdo individual — persona real vs persona digital",
         "",
         f"Fichero de predicciones: `{T.PREDF.name}` · **n = {len(ids)} encuestados** emparejados 1:1 por `id`.",
         "",
         "Mide si coincide **cada persona** con su gemelo digital (criterio 4 de Argyle,",
         "'correspondencia de patrones'), no si coincide la distribución agregada.",
         "",
         "`delta_vs_moda` = cuánto supera el panel al baseline de responder siempre la",
         "categoría más frecuente. **Si es ≈0 o negativo, el perfil no aporta señal individual.**",
         ""]

    def blq(sub, cols, titulo):
        f = [x for x in filas if x.get("subtipo") == sub and x.get("n", 0) > 0]
        if not f:
            return
        L.append(f"## {titulo}  (n={len(f)} preguntas)")
        L.append("")
        L.append("| " + " | ".join(["pregunta", "var"] + cols) + " |")
        L.append("|" + "---|" * (len(cols) + 2))
        for x in sorted(f, key=lambda z: -(z.get(cols[0], 0) or 0)):
            v = [f"{x.get(c):.2f}" if isinstance(x.get(c), float) else str(x.get(c, "")) for c in cols]
            L.append("| " + " | ".join([x["texto"][:46], str(x.get("var"))] + v) + " |")
        L.append("")
        L.append("**Medias:** " + " · ".join(
            f"{c}={np.nanmean([x.get(c, np.nan) for x in f]):.2f}" for c in cols))
        L.append("")

    blq("escala_0_10", ["spearman", "exacto_%", "pm1_%", "MAE", "sesgo", "kappa_w",
                        "base_moda_%", "delta_vs_moda"], "Escalas 0-10")
    blq("cat_ordinal", ["spearman", "exacto_%", "pm1_%", "MAE", "sesgo", "kappa_w",
                        "base_moda_%", "delta_vs_moda"], "Categóricas ORDINALES")
    blq("cat_nominal", ["exacto_%", "kappa", "base_moda_%", "delta_vs_moda"],
        "Categóricas NOMINALES")
    blq("multi", ["jaccard", "F1"], "Multi-respuesta")

    # resumen ejecutivo
    esc = [x for x in filas if x.get("subtipo") == "escala_0_10" and x.get("n", 0) > 0]
    ordi = [x for x in filas if x.get("subtipo") == "cat_ordinal" and x.get("n", 0) > 0]
    nom = [x for x in filas if x.get("subtipo") == "cat_nominal" and x.get("n", 0) > 0]
    L[9:9] = [
        "## Resumen",
        "",
        f"- **Escalas 0-10** ({len(esc)}): Spearman medio "
        f"**{np.nanmean([x.get('spearman', np.nan) for x in esc]):.2f}** · "
        f"MAE {np.nanmean([x.get('MAE', np.nan) for x in esc]):.2f} puntos · "
        f"dentro de ±1: {np.nanmean([x.get('pm1_%', np.nan) for x in esc]):.0f}%",
        f"- **Cat. ordinales** ({len(ordi)}): kappa ponderado medio "
        f"**{np.nanmean([x.get('kappa_w', np.nan) for x in ordi]):.3f}** · "
        f"acierto {np.nanmean([x.get('exacto_%', np.nan) for x in ordi]):.0f}% "
        f"vs moda {np.nanmean([x.get('base_moda_%', np.nan) for x in ordi]):.0f}% "
        f"(**delta {np.nanmean([x.get('delta_vs_moda', np.nan) for x in ordi]):+.1f}**)",
        f"- **Cat. nominales** ({len(nom)}): kappa medio "
        f"**{np.nanmean([x.get('kappa', np.nan) for x in nom]):.3f}** · "
        f"acierto {np.nanmean([x.get('exacto_%', np.nan) for x in nom]):.0f}% "
        f"vs moda {np.nanmean([x.get('base_moda_%', np.nan) for x in nom]):.0f}% "
        f"(**delta {np.nanmean([x.get('delta_vs_moda', np.nan) for x in nom]):+.1f}**)",
        "",
        "Referencia de kappa (Landis & Koch): <0 nulo · 0-0,20 leve · 0,21-0,40 aceptable ·",
        "0,41-0,60 moderado · >0,60 sustancial.",
        "",
    ]

    out = AQUI / "acuerdo_individual.md"
    out.write_text("\n".join(L), encoding="utf-8")
    (AQUI / "acuerdo_individual.json").write_text(
        json.dumps(filas, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n".join(L[:26]))
    print(f"\n→ {out}")
    print(f"→ {AQUI/'acuerdo_individual.json'}")


if __name__ == "__main__":
    main()
