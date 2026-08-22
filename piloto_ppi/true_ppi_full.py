# -*- coding: utf-8 -*-
"""PPI++ COMPLETO — 152 preguntas / 7 bloques.

Combina la muestra real (Deustobarómetro, .sav) con las predicciones generativas
del panel (predicciones_deusto_full.json) para, en cada pregunta, contrastar:
  - Sustitución ingenua (el enfoque "el panel ES la encuesta"): sesgo/DAM.
  - PPI++ (Angelopoulos et al.): estimación VÁLIDA + eficiencia (recorte de IC,
    ahorro de datos), sin coste de sesgo.

Usa el crosswalk `crosswalk_ppi.json` (pregunta -> variable(s) del .sav + tipo) y
el motor validado `ppi_engine.py`. Agrega por bloque y global.

Salida:  informe_ppi_full.md  (tablas por bloque + por pregunta)
Uso:
  python true_ppi_full.py                 # usa predicciones_deusto_full.json
  python true_ppi_full.py --simular 0.55  # sin API: fabrica predicciones con
                                          # esa concordancia, para probar el pipeline

Nota: el Bloque 7 (perfil) y las escalas ideología/nacionalismo/voto son
predictores inyectados -> se marcan como 'circular (validación)', no ganancia.
"""
import sys, json, re, math
from pathlib import Path
import numpy as np
import pyreadstat
from ppi_engine import estimar_opcion, estimar_media

RAIZ = Path(__file__).resolve().parent.parent
SAV  = RAIZ / "Datos Deustobarometro verano 2026.sav"
CW   = json.loads((Path(__file__).parent / "crosswalk_ppi.json").read_text(encoding="utf-8"))
PREDF = Path(__file__).parent / "predicciones_deusto_full.json"
OUT   = Path(__file__).parent / "informe_ppi_full.md"

df, meta = pyreadstat.read_sav(str(SAV))
df = df.set_index(df["id"].astype(int))
VVL = meta.variable_value_labels

NS_GRID = [50, 100, 200]
N_HEAD  = 100          # n etiquetado para la cifra de titular
SEEDS   = range(15)
ALPHA   = 0.05
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"   # escala 0-10 usa A..K; multi puede tener >11 opciones
BLOQUE7 = "barometro_digital_7_perfil_validacion.json"


def letra_a_idx(L):
    i = LETTERS.find((L or "").strip()[:1])
    return i if i >= 0 else None


# ---------- predicciones ----------
def cargar_predicciones(simular=None):
    """Devuelve {id:int -> {bloque -> {qi_str -> letra}}}. Si simular=p, fabrica
    predicciones coherentes con la realidad con concordancia ~p (para probar)."""
    if simular is None:
        raw = json.loads(PREDF.read_text(encoding="utf-8"))
        return {int(k): v for k, v in raw.items()}
    # modo simulación: para cada encuestado y pregunta, con prob p acierta la
    # opción real; si no, elige una opción al azar. Sirve para validar el pipeline.
    rng = np.random.default_rng(0)
    ids = list(df.index[: int(0.6 * len(df))])   # subconjunto "predicho"
    pred = {}
    for e in CW:
        var = e.get("var"); vars_ = e.get("vars"); ops = e["opciones"]
        for i in ids:
            d = pred.setdefault(i, {}).setdefault(e["bloque"], {})
            qi = str(e["qi"])
            # opción real -> letra, con ruido
            real_idx = _idx_real(e, i)
            if real_idx is None:
                idx = rng.integers(len(ops))
            else:
                idx = real_idx if rng.random() < simular else rng.integers(len(ops))
            d[qi] = LETTERS[idx] if idx < len(LETTERS) else "A"
    return pred


def _idx_real(e, i):
    """Índice de opción 'real' del encuestado i (para el modo simulación)."""
    ops = e["opciones"]
    if e["tipo"] == "multi":
        for j, (v, c) in enumerate(zip(e["vars"], e.get("codigos", []))):
            if v is not None and i in df.index and df.loc[i, v] == c:
                return j
        return None
    var = e.get("var")
    if var is None or i not in df.index:
        return None
    val = df.loc[i, var]
    if val != val:
        return None
    if e["tipo"] == "escala":
        return int(val) if 0 <= val <= 10 else None
    lab = VVL.get(var, {}).get(val)
    if lab is None:
        return None
    return _match_opcion(ops, lab)


def _match_opcion(ops, lab):
    """Mapea la ETIQUETA del .sav al índice de opción de la plantilla.

    ⚠ Corrige un bug: la versión previa aceptaba cualquier contención de
    subcadena, de modo que 'Ni lo he hecho, ni lo he pensado hacer' casaba con
    'Lo he hecho' (y 'Buena' con 'Muy buena'). Colapsaba 29 de 89 preguntas
    categóricas en una sola categoría. Ahora: (1) igualdad exacta sobre texto
    normalizado sin puntuación; (2) contención SÓLO si es única."""
    no = [_nm_dur(o) for o in ops]
    nl = _nm_dur(lab)
    if nl in no:
        return no.index(nl)
    cand = [j for j, o in enumerate(no) if nl and (nl in o or o in nl)]
    return cand[0] if len(cand) == 1 else None


def _nm_dur(s):
    import unicodedata, re as _re
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return _re.sub(r"[^a-z0-9]", "", s)


# ---------- construcción de Y, F por pregunta ----------
def arrays_pregunta(e, pred):
    """Devuelve lista de (Y_i, F_i) según tipo, o None. Formatos:
       cat   -> (Ylab[list str], Flab[list str], opciones)
       escala-> (Yf[np], Ff[np])
       multi -> lista por opción de (Yind[np], Find[np])"""
    ops = e["opciones"]; b = e["bloque"]; qi = str(e["qi"])
    ids = [i for i in pred if b in pred[i] and qi in pred[i][b] and i in df.index]

    if e["tipo"] == "cat":
        var = e["var"]; Y = []; F = []
        for i in ids:
            val = df.loc[i, var]
            ylab = VVL.get(var, {}).get(val)
            fidx = letra_a_idx(pred[i][b][qi])
            if ylab is None or fidx is None or fidx >= len(ops):
                continue
            Y.append(_nm(ylab)); F.append(_nm(ops[fidx]))
        return ("cat", np.array(Y, dtype=object), np.array(F, dtype=object),
                [_nm(o) for o in ops])

    if e["tipo"] == "escala":
        var = e["var"]; Y = []; F = []
        for i in ids:
            val = df.loc[i, var]; fidx = letra_a_idx(pred[i][b][qi])
            if val != val or val > 10 or fidx is None or fidx > 10:
                continue
            Y.append(float(val)); F.append(float(fidx))
        return ("escala", np.array(Y), np.array(F))

    # multi
    cols = []
    for j, (v, c) in enumerate(zip(e["vars"], e.get("codigos", []))):
        if v is None:
            cols.append(None); continue
        Y = []; F = []
        for i in ids:
            sel_real = 1.0 if df.loc[i, v] == c else 0.0
            letras = [x for x in pred[i][b][qi].replace(" ", "").split(",") if x]
            sel_pred = 1.0 if LETTERS[j] in letras else 0.0
            Y.append(sel_real); F.append(sel_pred)
        cols.append((np.array(Y), np.array(F)))
    return ("multi", cols)


import unicodedata
def _nm(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


# ---------- métricas PPI por pregunta ----------
def ppi_media_binaria(Y, F, theta):
    """Sesgo ingenuo y reducción de IC (n=N_HEAD) para una media (0/1 o 0-10)."""
    naive = abs(float(np.concatenate([Y, F]).mean() if False else F.mean()) - theta)
    reducs = []; covs = []
    for s in SEEDS:
        rng = np.random.default_rng(s); idx = rng.permutation(len(Y))
        n = min(N_HEAD, len(Y) - 5)
        if n < 10:
            continue
        lab, unl = idx[:n], idx[n:]
        r = estimar_media(Y[lab], F[lab], F[unl], ALPHA)
        reducs.append(r["reduccion_ancho_pct"]); covs.append(r["ppi_lo"] <= theta <= r["ppi_hi"])
    red = float(np.mean(reducs)) if reducs else 0.0
    cov = float(np.mean(covs)) if covs else float("nan")
    return naive, red, cov


def eval_pregunta(e, pred):
    out = arrays_pregunta(e, pred)
    naive_errs = []; reducs = []; covs = []; corr = None
    if out[0] == "cat":
        _, Y, F, ops = out
        if len(Y) < 20:
            return None
        for c in ops:
            theta = float((_col_real_cat(e, c)))     # theta poblacional (todos)
            yb = (Y == c).astype(float); fb = (F == c).astype(float)
            naive_errs.append(abs(fb.mean() - theta))
            n, red, cov = _sweep_bin(yb, fb, theta)
            reducs.append(red); covs.append(cov)
    elif out[0] == "escala":
        _, Y, F = out
        if len(Y) < 20:
            return None
        theta = float(_col_real_escala(e))
        corr = float(np.corrcoef(Y, F)[0, 1]) if len(Y) > 2 and Y.std() > 0 and F.std() > 0 else 0.0
        _, red, cov = ppi_media_binaria(Y, F, theta)
        # DAM ingenua = error de DISTRIBUCIÓN (0..10) en proporción -> p.p. tras ×100,
        # comparable a las categóricas (NO el error de la media, que iría en unidades 0-10).
        naive = _naive_dam_escala(e, F)
        naive_errs.append(naive); reducs.append(red); covs.append(cov)
    else:  # multi
        cols = out[1]
        for j, col in enumerate(cols):
            if col is None:
                continue
            Y, F = col
            if len(Y) < 20:
                continue
            theta = float(_col_real_multi(e, j))
            naive_errs.append(abs(F.mean() - theta))
            n, red, cov = _sweep_bin(Y, F, theta)
            reducs.append(red); covs.append(cov)
    if not naive_errs:
        return None
    return {
        "naive_dam": float(np.mean(naive_errs)),
        "ppi_reduccion": float(np.mean(reducs)) if reducs else 0.0,
        "cobertura": float(np.nanmean(covs)) if covs else float("nan"),
        "corr": corr,
    }


def _sweep_bin(Y, F, theta):
    reducs = []; covs = []
    for s in SEEDS:
        rng = np.random.default_rng(s); idx = rng.permutation(len(Y))
        n = min(N_HEAD, len(Y) - 5)
        if n < 10:
            continue
        lab, unl = idx[:n], idx[n:]
        r = estimar_media(Y[lab], F[lab], F[unl], ALPHA)
        reducs.append(r["reduccion_ancho_pct"]); covs.append(r["ppi_lo"] <= theta <= r["ppi_hi"])
    return N_HEAD, (float(np.mean(reducs)) if reducs else 0.0), (float(np.mean(covs)) if covs else float("nan"))


# ---------- theta poblacional (toda la muestra real) ----------
def _col_real_cat(e, c_norm):
    var = e["var"]; ser = df[var].dropna()
    n = len(ser)
    cnt = sum(1 for val in ser if _nm(VVL.get(var, {}).get(val) or "") == c_norm)
    return 100.0 * cnt / n / 100.0 if n else 0.0   # proporción 0-1


def _col_real_escala(e):
    ser = df[e["var"]].dropna(); ser = ser[ser <= 10]
    return float(ser.mean()) if len(ser) else 0.0


def _naive_dam_escala(e, F):
    """DAM de distribución (0..10) en proporción: media de |pred% − real%| por valor."""
    ser = df[e["var"]].dropna(); ser = ser[ser <= 10]
    if not len(ser) or not len(F):
        return 0.0
    diffs = [abs(float((F == v).mean()) - float((ser == v).mean())) for v in range(11)]
    return float(np.mean(diffs))


def _col_real_multi(e, j):
    v = e["vars"][j]; c = e["codigos"][j]
    if v is None:
        return 0.0
    return float((df[v] == c).mean())


# ---------- main ----------
def main():
    simular = None
    if "--simular" in sys.argv:
        simular = float(sys.argv[sys.argv.index("--simular") + 1])
        print(f"[MODO SIMULACIÓN] concordancia objetivo ~{simular:.0%} (sin API)")
    elif not PREDF.exists():
        sys.exit(f"✗ No existe {PREDF.name}. Genera antes con generar_predicciones_full.py "
                 f"(o prueba el pipeline con --simular 0.55)")
    pred = cargar_predicciones(simular)
    print(f"Encuestados con predicción: {len(pred)}")

    por_bloque = {}
    filas = ["## Detalle por pregunta\n",
             "| Bloque | q | Tipo | Sust. ingenua (DAM p.p.) | PPI++ red. IC % | cobertura | corr |",
             "|---|--:|---|--:|--:|--:|--:|"]
    for e in CW:
        r = eval_pregunta(e, pred)
        if r is None:
            continue
        blk = e["bloque"]
        por_bloque.setdefault(blk, []).append(r)
        blkn = blk.split("barometro_digital_")[1][:10]
        circ = " *" if blk == BLOQUE7 else ""
        corr_s = f"{r['corr']:+.2f}" if r['corr'] is not None else "—"
        filas.append(f"| {blkn}{circ} | {e['qi']} | {e['tipo']} | {100*r['naive_dam']:.1f} | "
                     f"{r['ppi_reduccion']:.1f} | {100*r['cobertura']:.0f}% | {corr_s} |")

    # resumen por bloque
    res = ["# PPI++ completo — sustitución ingenua vs PPI++ (152 preguntas)\n",
           f"- Predicciones: {'SIMULADAS' if simular else PREDF.name}  ·  n etiquetado titular = {N_HEAD}",
           "- **Sust. ingenua (DAM)** = error del panel usado como verdad (lo que da v2 sola).",
           "- **PPI++ red. IC** = recorte medio del intervalo (eficiencia); estimación válida (cobertura ~95%).",
           "- \\* Bloque 7 = perfil inyectado (circular: validación, no ganancia).\n",
           "| Bloque | Preg | Sust. ingenua DAM | PPI++ red. IC media | cobertura media |",
           "|---|--:|--:|--:|--:|"]
    allnaive = []; allred = []
    for blk in sorted(por_bloque):
        rs = por_bloque[blk]
        nd = 100 * np.mean([x["naive_dam"] for x in rs])
        rd = np.mean([x["ppi_reduccion"] for x in rs])
        cv = 100 * np.nanmean([x["cobertura"] for x in rs])
        allnaive += [x["naive_dam"] for x in rs]; allred += [x["ppi_reduccion"] for x in rs]
        nm = blk.split("barometro_digital_")[1].replace(".json", "")[:16]
        circ = " *" if blk == BLOQUE7 else ""
        res.append(f"| {nm}{circ} | {len(rs)} | {nd:.1f} | {rd:.1f}% | {cv:.0f}% |")
    res.append(f"| **GLOBAL** | {len(allnaive)} | **{100*np.mean(allnaive):.1f}** | "
               f"**{np.mean(allred):.1f}%** | — |")

    OUT.write_text("\n".join(res + ["\n"] + filas), encoding="utf-8")
    print("\n".join(res))
    print(f"\n→ {OUT.name}")


if __name__ == "__main__":
    main()
