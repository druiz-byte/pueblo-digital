# -*- coding: utf-8 -*-
"""TECHO PREDICTIVO: ¿cuánto de cada pregunta del barómetro es explicable desde un
perfil sociodemográfico? Es el LÍMITE SUPERIOR de cualquier panel digital.

IDEA. Las 1.000 personas reales no responden todas igual: hay variación. Parte es
sistemática (capturable desde el perfil) y parte es idiosincrasia individual. El R²
mide qué fracción es sistemática. Como una Persona digital se construye SOLO con el
perfil, no puede saber más de lo que el perfil contiene:

        corr_máxima_alcanzable = sqrt(R²)

Si el techo de una pregunta es R²=0,15 -> corr <= 0,39 POR MUCHO que se mejore el
modelo, el prompt o las encuestas donantes. Distingue "fallo del pipeline" de
"límite de información".

MÉTODO (honesto, sin sobreajuste):
  - R² FUERA DE MUESTRA por validación cruzada 5-fold (meter muchos predictores
    infla el R² dentro de muestra y daría un techo falsamente alto).
  - Ridge suave para estabilidad numérica con dummies colineales.
  - escalas 0-10 y ordinales -> R² OOS (la distancia tiene sentido).
  - nominales -> clasificador one-vs-rest; se reporta ACIERTO OOS vs baseline MODA.
  - multi -> por opción binaria, acierto medio vs baseline.
  - Las preguntas que SON predictores (p36, p38, p40-p46) se marcan CIRCULAR: su
    techo es ~1 por construcción y no cuenta.

Uso:  python techo_predictivo.py
"""
import sys, json, re
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import acuerdo_individual as A          # trae el stub de ppi_py y las utilidades
T = A.T                                 # true_ppi_full: df (.sav), CW (crosswalk)

AQUI = Path(__file__).parent
df = T.df
RNG = np.random.default_rng(0)
K = 5                                   # folds
LAMBDA = 1.0                            # ridge

# Predictores que un perfil construido desde fuentes EXTERNAS podría contener.
CATEG = ["sexo", "prov", "lengua", "p4", "p40", "p41", "p42", "p45", "p46"]
NUMER = ["edad"]
ESCAL = ["p36", "p38"]                  # ideología y nacionalismo (0-10, 11+ = NS)
CIRCULARES = set(CATEG) | set(ESCAL) | {"edad"}


def construir_X():
    """Matriz de diseño: dummies para categóricas, edad (+edad²), escalas con flag NS."""
    cols, nombres = [np.ones(len(df))], ["intercepto"]
    for v in CATEG:
        if v not in df.columns:
            continue
        vals = df[v]
        for u in sorted(x for x in vals.dropna().unique()):
            cols.append((vals == u).astype(float).values)
            nombres.append(f"{v}={u:g}")
    for v in NUMER:
        x = df[v].astype(float).values
        m = np.nanmean(x); x = np.where(np.isnan(x), m, x)
        z = (x - x.mean()) / (x.std() or 1)
        cols += [z, z ** 2]; nombres += [v, f"{v}^2"]
    for v in ESCAL:
        x = df[v].astype(float).values
        ns = (~np.isfinite(x)) | (x > 10)
        xx = np.where(ns, np.nan, x)
        m = np.nanmean(xx); xx = np.where(np.isnan(xx), m, xx)
        cols += [(xx - m) / (np.nanstd(xx) or 1), ns.astype(float)]
        nombres += [v, f"{v}_NS"]
    return np.column_stack(cols), nombres


X_ALL, NOMBRES = construir_X()


def _ridge(Xtr, ytr):
    p = Xtr.shape[1]
    R = LAMBDA * np.eye(p); R[0, 0] = 0.0
    return np.linalg.solve(Xtr.T @ Xtr + R, Xtr.T @ ytr)


def r2_oos(X, y):
    """R² fuera de muestra (5-fold). Compara contra la media del TRAIN."""
    n = len(y)
    if n < 50 or y.std() == 0:
        return float("nan")
    idx = RNG.permutation(n); folds = np.array_split(idx, K)
    sse = sst = 0.0
    for f in folds:
        tr = np.setdiff1d(idx, f)
        b = _ridge(X[tr], y[tr])
        pred = X[f] @ b
        sse += ((y[f] - pred) ** 2).sum()
        sst += ((y[f] - y[tr].mean()) ** 2).sum()
    return float(1 - sse / sst) if sst > 0 else float("nan")


def acc_oos(X, y):
    """Clasificador lineal one-vs-rest. Devuelve (acierto OOS, acierto de la moda)."""
    n = len(y)
    clases = np.unique(y)
    if n < 50 or len(clases) < 2:
        return float("nan"), float("nan")
    idx = RNG.permutation(n); folds = np.array_split(idx, K)
    ok = tot = 0
    for f in folds:
        tr = np.setdiff1d(idx, f)
        S = np.column_stack([X[f] @ _ridge(X[tr], (y[tr] == c).astype(float)) for c in clases])
        ok += (clases[S.argmax(1)] == y[f]).sum(); tot += len(f)
    _, cnt = np.unique(y, return_counts=True)
    return float(ok / tot), float(cnt.max() / n)


def objetivo(e):
    """Devuelve (y, modo) para una pregunta del crosswalk."""
    ops = [T._nm(o) for o in e["opciones"]]
    ids = list(df.index)
    if e["tipo"] == "multi":
        return None, "multi"
    y, keep = [], []
    for i in ids:
        v = T._idx_real(e, i)
        if v is None:
            continue
        y.append(v); keep.append(df.index.get_loc(i))
    if not y:
        return None, None
    y = np.array(y, float); keep = np.array(keep)
    if e["tipo"] == "escala":
        return (y, keep), "escala"
    ordinal = A.es_ordinal(ops)
    ns = {j for j, o in enumerate(ops) if A.NS_RE.search(o)}
    m = np.array([v not in ns for v in y])
    return (y[m], keep[m]), ("ordinal" if ordinal else "nominal")


def main():
    filas = []
    for e in T.CW:
        var = e.get("var")
        circ = var in CIRCULARES if var else False
        r = {"bloque": e["bloque"], "var": var, "texto": str(e["texto"])[:70],
             "circular": circ}
        dat, modo = objetivo(e)
        r["modo"] = modo
        if modo == "multi":
            accs, bases = [], []
            for v, c in zip(e["vars"], e.get("codigos", [])):
                if v is None or v not in df.columns:
                    continue
                yb = (df[v] == c).astype(float).values
                a, b = acc_oos(X_ALL, yb)
                if a == a:
                    accs.append(a); bases.append(b)
            if accs:
                r["acierto"] = float(np.mean(accs)) * 100
                r["base_moda"] = float(np.mean(bases)) * 100
                r["delta"] = r["acierto"] - r["base_moda"]
            filas.append(r); continue
        if dat is None:
            filas.append(r); continue
        y, keep = dat
        X = X_ALL[keep]
        r["n"] = int(len(y))
        if modo in ("escala", "ordinal"):
            r2 = r2_oos(X, y)
            r["R2"] = r2
            r["corr_max"] = float(np.sqrt(max(r2, 0.0)))
        else:
            a, b = acc_oos(X, y)
            r["acierto"] = a * 100 if a == a else float("nan")
            r["base_moda"] = b * 100 if b == b else float("nan")
            r["delta"] = r["acierto"] - r["base_moda"]
        filas.append(r)

    lim = [f for f in filas if not f["circular"]]
    esc = [f for f in lim if f.get("modo") in ("escala", "ordinal") and "R2" in f]
    nom = [f for f in lim if f.get("modo") == "nominal" and "acierto" in f]
    mul = [f for f in lim if f.get("modo") == "multi" and "acierto" in f]
    cir = [f for f in filas if f["circular"] and "R2" in f]

    L = ["# Techo predictivo del barómetro desde un perfil sociodemográfico", "",
         "¿Cuánta de la variación entre personas es explicable desde el perfil?",
         "**`corr_max = sqrt(R²)` es el límite de CUALQUIER panel digital**: una Persona",
         "construida solo con el perfil no puede saber más de lo que el perfil contiene.", "",
         f"Predictores ({len(NOMBRES)} columnas): sexo, edad(+²), provincia, lengua, situación",
         "laboral, estudios, religión, nacimiento, voto 2024, voto 2020, ideología 0-10,",
         "nacionalismo 0-10 (+flags NS). R² **fuera de muestra**, validación cruzada 5-fold.", ""]

    if esc:
        r2s = np.array([f["R2"] for f in esc]); cms = np.array([f["corr_max"] for f in esc])
        L += ["## Resumen", "",
              f"- **Escalas y ordinales ({len(esc)} preguntas):** R² medio fuera de muestra "
              f"**{np.nanmean(r2s):.3f}** -> **corr máxima media {np.nanmean(cms):.2f}**",
              f"  - mediana R² {np.nanmedian(r2s):.3f} · p90 {np.nanpercentile(r2s,90):.3f} · "
              f"máx {np.nanmax(r2s):.3f}",
              f"  - preguntas con R² <= 0 (el perfil no predice nada): "
              f"**{int((r2s<=0).sum())}/{len(esc)}**"]
    if nom:
        d = np.array([f["delta"] for f in nom])
        L += [f"- **Nominales ({len(nom)}):** acierto "
              f"{np.nanmean([f['acierto'] for f in nom]):.0f}% vs moda "
              f"{np.nanmean([f['base_moda'] for f in nom]):.0f}% (**{np.nanmean(d):+.1f} p.p.**)"]
    if mul:
        d = np.array([f["delta"] for f in mul])
        L += [f"- **Multi-respuesta ({len(mul)}):** acierto medio por opción "
              f"{np.nanmean([f['acierto'] for f in mul]):.0f}% vs moda "
              f"{np.nanmean([f['base_moda'] for f in mul]):.0f}% (**{np.nanmean(d):+.1f} p.p.**)"]
    if cir:
        L += [f"- *(control)* las {len(cir)} preguntas que SON predictores dan R² "
              f"{np.nanmean([f['R2'] for f in cir]):.2f} — circulares, no cuentan."]
    L += [""]

    # por bloque
    L += ["## Techo por bloque (escalas + ordinales)", "",
          "| bloque | preg | R² medio | corr máx |", "|---|--:|--:|--:|"]
    for b in sorted({f["bloque"] for f in esc}):
        g = [f for f in esc if f["bloque"] == b]
        L.append(f"| {b[:30]} | {len(g)} | {np.nanmean([x['R2'] for x in g]):.3f} | "
                 f"{np.nanmean([x['corr_max'] for x in g]):.2f} |")
    L += ["", "## Preguntas ordenadas por techo (escalas + ordinales)", "",
          "| R² | corr máx | n | var | pregunta |", "|--:|--:|--:|---|---|"]
    for f in sorted(esc, key=lambda z: -(z["R2"] if z["R2"] == z["R2"] else -9)):
        L.append(f"| {f['R2']:.3f} | {f['corr_max']:.2f} | {f.get('n','')} | "
                 f"{f.get('var')} | {f['texto'][:52]} |")

    out = AQUI / "techo_predictivo.md"
    out.write_text("\n".join(L), encoding="utf-8")
    (AQUI / "techo_predictivo.json").write_text(
        json.dumps(filas, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n".join(L[:40]))
    print(f"\n→ {out}")


if __name__ == "__main__":
    main()
