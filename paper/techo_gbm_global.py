# -*- coding: utf-8 -*-
"""Techo NO LINEAL (gradient boosting) sobre TODAS las escalas/ordinales.
Reanudable: guarda cada ítem y, al agotar el presupuesto de tiempo, sale.
Volver a lanzarlo continúa donde lo dejó."""
import sys, json, time
from pathlib import Path
import numpy as np
AQ = Path(__file__).resolve().parent
PP = AQ.parent; sys.path.insert(0, str(PP/"piloto_ppi"))
import acuerdo_individual as A, techo_predictivo as TP
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import KFold
T = A.T; X = TP.X_ALL
OUT = AQ/"techo_gbm_global.json"
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 150.0
R_REP = 3

res = json.loads(OUT.read_text()) if OUT.exists() else {}
t0 = time.time(); nuevos = 0

def r2_gbm(Xm, y):
    v = []
    for r in range(R_REP):
        sse = sst = 0.0
        for tr, te in KFold(5, shuffle=True, random_state=r).split(Xm):
            m = HistGradientBoostingRegressor(max_iter=150, learning_rate=.08, max_depth=3,
                    min_samples_leaf=40, early_stopping=False,
                    random_state=r).fit(Xm[tr], y[tr])
            p = m.predict(Xm[te])
            sse += ((y[te]-p)**2).sum(); sst += ((y[te]-y[tr].mean())**2).sum()
        if sst > 0: v.append(1-sse/sst)
    return float(np.mean(v)) if v else float("nan")

for e in T.CW:
    k = str((e["bloque"], e["qi"]))
    if k in res: continue
    if time.time()-t0 > BUDGET: break
    dat, modo = TP.objetivo(e)
    if modo not in ("escala", "ordinal") or dat is None:
        res[k] = None; continue
    y, keep = dat
    if len(y) < 50 or y.std() == 0:
        res[k] = None; continue
    r2 = r2_gbm(X[keep], y)
    res[k] = dict(var=e.get("var"), modo=modo, n=int(len(y)), R2_gbm=r2,
                  corr_max_gbm=float(np.sqrt(max(r2, 0))),
                  circular=(e.get("var") in TP.CIRCULARES) if e.get("var") else False)
    nuevos += 1
OUT.write_text(json.dumps(res, indent=1))
hechos = sum(1 for v in res.values() if v)
pend = sum(1 for e in T.CW if str((e["bloque"], e["qi"])) not in res)
print(f"+{nuevos} nuevos | ítems con techo GBM: {hechos} | pendientes: {pend}")
