# -*- coding: utf-8 -*-
"""Techo predictivo v2: idéntico en método a techo_predictivo.py, con dos mejoras
de reproducibilidad exigibles en revisión:
  1) SEMILLA POR ÍTEM (no compartida) -> el resultado de una pregunta no depende
     de cuántas preguntas se hayan evaluado antes.
  2) CV REPETIDA (R repeticiones de 5-fold) -> se reporta media y desviación,
     porque un solo 5-fold tiene ruido de ±0,04 en R², comparable a la señal.
Variable de entorno MATCH=orig|fix selecciona el mapeo etiqueta->opción.
"""
import os, sys, json, hashlib
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
import acuerdo_individual as A
T = A.T
import techo_predictivo as TP          # reutiliza construir_X, _ridge, objetivo

MODO = os.environ.get("MATCH", "fix")
R_REP = int(os.environ.get("REP", "20"))
K = 5
X_ALL = TP.X_ALL

if MODO == "orig":                      # restaura el matcher con el bug, para el contraste
    import unicodedata
    def _nm(s):
        s = unicodedata.normalize("NFKD", s or "")
        return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()
    def _m(ops, lab):
        for j, op in enumerate(ops):
            if _nm(op) == _nm(lab) or _nm(lab) in _nm(op) or _nm(op) in _nm(lab):
                return j
        return None
    T._match_opcion = _m

def _seed(tag):
    return int(hashlib.md5(str(tag).encode()).hexdigest()[:8], 16)

def r2_rep(X, y, tag):
    n = len(y)
    if n < 50 or y.std() == 0:
        return float("nan"), float("nan")
    vals = []
    for r in range(R_REP):
        rng = np.random.default_rng(_seed(tag) + r)
        idx = rng.permutation(n); folds = np.array_split(idx, K)
        sse = sst = 0.0
        for f in folds:
            tr = np.setdiff1d(idx, f)
            b = TP._ridge(X[tr], y[tr])
            sse += ((y[f] - X[f] @ b) ** 2).sum()
            sst += ((y[f] - y[tr].mean()) ** 2).sum()
        if sst > 0:
            vals.append(1 - sse / sst)
    return (float(np.mean(vals)), float(np.std(vals))) if vals else (float("nan"),)*2

def acc_rep(X, y, tag):
    n = len(y); clases = np.unique(y)
    if n < 50 or len(clases) < 2:
        return float("nan"), float("nan")
    accs = []
    for r in range(R_REP):
        rng = np.random.default_rng(_seed(tag) + r)
        idx = rng.permutation(n); folds = np.array_split(idx, K)
        ok = tot = 0
        for f in folds:
            tr = np.setdiff1d(idx, f)
            S = np.column_stack([X[f] @ TP._ridge(X[tr], (y[tr] == c).astype(float)) for c in clases])
            ok += (clases[S.argmax(1)] == y[f]).sum(); tot += len(f)
        accs.append(ok / tot)
    _, cnt = np.unique(y, return_counts=True)
    return float(np.mean(accs)), float(cnt.max() / n)

def main():
    filas = []
    for e in T.CW:
        var = e.get("var")
        tag = f"{e['bloque']}|{e['qi']}|{var}"
        r = {"bloque": e["bloque"], "qi": e["qi"], "var": var,
             "texto": str(e["texto"])[:70], "circular": var in TP.CIRCULARES if var else False}
        dat, modo = TP.objetivo(e); r["modo"] = modo
        if modo == "multi":
            accs, bases = [], []
            for k2, (v, c) in enumerate(zip(e["vars"], e.get("codigos", []))):
                if v is None or v not in T.df.columns: continue
                a, b = acc_rep(X_ALL, (T.df[v] == c).astype(float).values, tag + f"|{k2}")
                if a == a: accs.append(a); bases.append(b)
            if accs:
                r.update(acierto=float(np.mean(accs))*100, base_moda=float(np.mean(bases))*100)
                r["delta"] = r["acierto"] - r["base_moda"]
            filas.append(r); continue
        if dat is None: filas.append(r); continue
        y, keep = dat; X = X_ALL[keep]; r["n"] = int(len(y))
        if modo in ("escala", "ordinal"):
            m, s = r2_rep(X, y, tag)
            r["R2"] = m; r["R2_sd"] = s
            r["corr_max"] = float(np.sqrt(max(m, 0.0))) if m == m else float("nan")
        else:
            a, b = acc_rep(X, y, tag)
            r["acierto"] = a*100 if a == a else float("nan")
            r["base_moda"] = b*100 if b == b else float("nan")
            r["delta"] = r["acierto"] - r["base_moda"]
        filas.append(r)
    out = Path(__file__).parent / f"techo_v2_{MODO}.json"
    out.write_text(json.dumps(filas, ensure_ascii=False, indent=1), encoding="utf-8")
    print("->", out.name, len(filas), "filas")

if __name__ == "__main__":
    main()
