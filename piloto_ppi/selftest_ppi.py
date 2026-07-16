# -*- coding: utf-8 -*-
"""Self-test Monte Carlo del motor PPI++: valida insesgadez, cobertura y eficiencia."""
import numpy as np
from ppi_engine import estimar_opcion

rng = np.random.default_rng(7)
OPCIONES = ["Muy buena", "Buena", "Regular", "Mala", "Muy mala"]
# Verdad poblacional (marginal real, tipo bloque 5 Q0)
THETA = np.array([0.018, 0.334, 0.439, 0.111, 0.056+0.043])  # ultima agrupa Muy mala+NS
THETA = THETA / THETA.sum()

def genera_poblacion(M):
    """Y real ~ THETA. Prediccion f: correlacionada con Y pero SESGADA (imita al panel)."""
    Y = rng.choice(OPCIONES, size=M, p=THETA)
    f = np.empty(M, dtype=object)
    p_acuerdo = 0.55                       # el panel acierta el 55% individual
    sesgo = np.array([0.01,0.45,0.30,0.14,0.10]); sesgo/=sesgo.sum()  # marginal sesgada del panel
    for i in range(M):
        if rng.random() < p_acuerdo:
            f[i] = Y[i]
        else:
            f[i] = rng.choice(OPCIONES, p=sesgo)
    return Y, f

# --- Verdad de referencia (gran poblacion) ---
Ybig, _ = genera_poblacion(2_000_000)
theta_true = {c: float((Ybig==c).mean()) for c in OPCIONES}

N_UNLAB = 1000     # tamaño del panel (no etiquetado)
N_LAB   = 120      # muestra real etiquetada (pequeña)
REPS    = 600
alpha   = 0.05

cov_ppi={c:0 for c in OPCIONES}; cov_cl={c:0 for c in OPCIONES}
w_ppi={c:[] for c in OPCIONES}; w_cl={c:[] for c in OPCIONES}
bias_ppi={c:[] for c in OPCIONES}; bias_imp={c:[] for c in OPCIONES}

for _ in range(REPS):
    Yl, fl = genera_poblacion(N_LAB)          # etiquetado: real + prediccion
    _, fu   = genera_poblacion(N_UNLAB)       # no etiquetado: solo prediccion
    for c in OPCIONES:
        r = estimar_opcion(Yl, fl, fu, c, alpha=alpha)
        tt = theta_true[c]
        if r["ppi_lo"] <= tt <= r["ppi_hi"]: cov_ppi[c]+=1
        if r["clasico_lo"] <= tt <= r["clasico_hi"]: cov_cl[c]+=1
        w_ppi[c].append(r["ppi_ancho"]); w_cl[c].append(r["clasico_ancho"])
        bias_ppi[c].append(r["ppi_pt"]-tt); bias_imp[c].append(r["imputacion_pt"]-tt)

print(f"REPS={REPS}  n_lab={N_LAB}  N_unlab={N_UNLAB}  alpha={alpha} (cobertura objetivo 95%)\n")
print(f"{'opcion':10} {'theta':>6} {'covPPI':>7} {'covCLA':>7} {'wPPI':>7} {'wCLA':>7} {'red%':>6} {'biasPPI':>8} {'biasIMP':>8}")
for c in OPCIONES:
    print(f"{c:10} {theta_true[c]:6.3f} {100*cov_ppi[c]/REPS:6.1f}% {100*cov_cl[c]/REPS:6.1f}% "
          f"{np.mean(w_ppi[c]):7.4f} {np.mean(w_cl[c]):7.4f} {100*(1-np.mean(w_ppi[c])/np.mean(w_cl[c])):5.1f} "
          f"{np.mean(bias_ppi[c]):+8.4f} {np.mean(bias_imp[c]):+8.4f}")

red_media = np.mean([100*(1-np.mean(w_ppi[c])/np.mean(w_cl[c])) for c in OPCIONES])
print(f"\nReduccion media de ancho de IC (PPI++ vs clasico): {red_media:.1f}%")
print("VALIDEZ: cobertura PPI++ y clasico deben rondar 95%. Bias PPI++ ~0; Bias IMP grande (sesgo del panel).")
