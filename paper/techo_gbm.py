# -*- coding: utf-8 -*-
"""Techo NO LINEAL (gradient boosting) para el subcorpus de marketing.
El techo lineal puede infraestimar si la relación perfil→respuesta no es lineal.
Cierra el hueco 7 del esquema, restringido a los ítems que van al paper."""
import sys, json
from pathlib import Path
import numpy as np
PP = Path(__file__).resolve().parent.parent; PIL = PP/"piloto_ppi"
sys.path.insert(0, str(PIL))
import acuerdo_individual as A, techo_predictivo as TP
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
from sklearn.model_selection import KFold
T = A.T; X = TP.X_ALL
ITEMS = json.loads((Path(__file__).parent/"marketing_items.json").read_text(encoding="utf-8"))["items"]
KEYS = {(i["bloque"], i["qi"]) for i in ITEMS}

def r2_gbm(Xm, y, R=5):
    v = []
    for r in range(R):
        sse = sst = 0.0
        for tr, te in KFold(5, shuffle=True, random_state=r).split(Xm):
            m = HistGradientBoostingRegressor(max_iter=200, learning_rate=.06, max_depth=3,
                                              min_samples_leaf=30, random_state=r).fit(Xm[tr], y[tr])
            p = m.predict(Xm[te])
            sse += ((y[te]-p)**2).sum(); sst += ((y[te]-y[tr].mean())**2).sum()
        if sst > 0: v.append(1-sse/sst)
    return float(np.mean(v)) if v else float("nan")

def acc_gbm(Xm, y, R=3):
    accs = []
    for r in range(R):
        ok = tot = 0
        for tr, te in KFold(5, shuffle=True, random_state=r).split(Xm):
            if len(np.unique(y[tr])) < 2: continue
            m = HistGradientBoostingClassifier(max_iter=150, learning_rate=.08, max_depth=3,
                                               min_samples_leaf=30, random_state=r).fit(Xm[tr], y[tr])
            ok += (m.predict(Xm[te]) == y[te]).sum(); tot += len(te)
        if tot: accs.append(ok/tot)
    return float(np.mean(accs)) if accs else float("nan")

out = {}
for e in T.CW:
    if (e["bloque"], e["qi"]) not in KEYS: continue
    dat, modo = TP.objetivo(e)
    if modo == "multi" or dat is None: continue
    y, keep = dat; Xm = X[keep]
    if len(y) < 50 or y.std() == 0: continue
    if modo in ("escala", "ordinal"):
        r2 = r2_gbm(Xm, y)
        out[str((e["bloque"], e["qi"]))] = dict(var=e.get("var"), R2_gbm=r2,
                                                corr_max_gbm=float(np.sqrt(max(r2, 0))))
    else:
        _, c = np.unique(y, return_counts=True)
        out[str((e["bloque"], e["qi"]))] = dict(var=e.get("var"), acc_gbm=acc_gbm(Xm, y)*100,
                                                moda=float(c.max()/len(y))*100)
    print(".", end="", flush=True)
json.dump(out, open(Path(__file__).parent/"techo_gbm.json", "w"), indent=1)
print(f"\n→ techo_gbm.json ({len(out)} ítems)")
