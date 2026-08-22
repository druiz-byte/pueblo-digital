# -*- coding: utf-8 -*-
"""Correlación ALCANZADA por el panel, medida como Pearson sobre la MISMA
codificación numérica que usa el techo (corr_max = sqrt(R2_OOS) es Pearson).
Comparar Spearman con sqrt(R2) es incorrecto: en ítems muy asimétricos (p6,
con ~90% en una categoría) el Spearman se dispara por el tratamiento de empates
y llega a superar el techo, que es imposible por construcción."""
import json, sys
from pathlib import Path
import numpy as np
PP = Path(__file__).resolve().parent.parent; PIL = PP/"piloto_ppi"
sys.path.insert(0, str(PIL))
import acuerdo_individual as A
T = A.T

def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 10 or x.std() == 0 or y.std() == 0: return float("nan")
    return float(np.corrcoef(x, y)[0, 1])

pred = T.cargar_predicciones()
out = {}
for e in T.CW:
    arr = T.arrays_pregunta(e, pred)
    key = (e["bloque"], e["qi"])
    if arr[0] == "escala":
        _, Y, F = arr
        out[str(key)] = dict(r=pearson(Y, F), n=int(len(Y)), tipo="escala")
    elif arr[0] == "cat":
        _, Ylab, Flab, ops = arr
        val = [o for o in ops if not A.NS_RE.search(o)]
        pos = {o: j for j, o in enumerate(val)}
        pares = [(pos[a], pos[b]) for a, b in zip(Ylab, Flab) if a in pos and b in pos]
        if len(pares) >= 10:
            a = [p[0] for p in pares]; b = [p[1] for p in pares]
            out[str(key)] = dict(r=pearson(a, b), n=len(pares),
                                 tipo="ordinal" if A.es_ordinal(ops) else "nominal")
json.dump(out, open("pearson_alcanzado.json", "w"), indent=1)
print("ítems con Pearson calculado:", len(out))
