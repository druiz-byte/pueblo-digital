# -*- coding: utf-8 -*-
"""FASE 1 — Subcorpus de marketing del Deustobarómetro.

Reúne, restringido a los ítems de marketing, las tres piezas del argumento:
  (1) TECHO      corr_max = sqrt(R2_OOS)              [techo_v2_fix.json]
  (2) ALCANZADO  correlación individual panel vs real [acuerdo_individual.json]
  (3) COLAPSO    DAM y concentración modal, n=1.000   [tanda 2026-07-16]
Sin API: sólo relee resultados ya generados.
"""
import json, sys, glob
from pathlib import Path
import numpy as np

PP = Path(__file__).resolve().parent.parent   # raíz del proyecto
ENT = PP/"entrevista"; PIL = PP/"piloto_ppi"
sys.path.insert(0, str(ENT)); sys.path.insert(0, str(PIL))
from comparar_deustobarometro import norm, real_por_opcion

# ---------------------------------------------------------------- constructos
RETRENCH = [f"p6_{i}" for i in range(1, 14)]
VIAJE    = ["p13", "p14", "p15", "p16"]          # + multi de turismo (var None)
SERVICIO = [f"p8_{i}" for i in range(1, 17)]
MARCA    = ["p21_4","p21_5","p21_9","p21_10","p21_11",
            "p21_15","p21_16","p21_17","p21_18","p21_19"]
POLITICO = ["p21_1","p21_2","p21_3","p21_6","p21_7",
            "p21_8","p21_12","p21_13","p21_14","p21_20"]

CONSTRUCTO = {}
for v in RETRENCH: CONSTRUCTO[v] = "A · Retrenchment de consumo"
for v in VIAJE:    CONSTRUCTO[v] = "B · Decisión de viaje"
for v in SERVICIO: CONSTRUCTO[v] = "C · Satisfacción de servicio"
for v in MARCA:    CONSTRUCTO[v] = "D · Confianza de marca"
for v in POLITICO: CONSTRUCTO[v] = "E · (contraste) Confianza política"
MKT = {"A · Retrenchment de consumo","B · Decisión de viaje",
       "C · Satisfacción de servicio","D · Confianza de marca"}

# ------------------------------------------------------------------- crosswalk
CW = json.loads((PIL/"crosswalk_ppi.json").read_text(encoding="utf-8"))
MULTI_TURISMO = [e for e in CW
                 if e["bloque"].startswith("barometro_digital_4") and e["tipo"] == "multi"]
for e in MULTI_TURISMO:
    CONSTRUCTO[f"MULTI:{e['bloque']}:{e['qi']}"] = "B · Decisión de viaje"

def clave(e):
    v = e.get("var")
    return v if v else f"MULTI:{e['bloque']}:{e['qi']}"

ITEMS = [e for e in CW if clave(e) in CONSTRUCTO]
print(f"ítems del subcorpus: {len(ITEMS)}  "
      f"(marketing {sum(1 for e in ITEMS if CONSTRUCTO[clave(e)] in MKT)})")

# --------------------------------------------------------------- (1) el techo
TECHO = {(f["bloque"], f["qi"]): f for f in
         json.loads((PIL/"techo_v2_fix.json").read_text(encoding="utf-8"))}
# ------------------------------------------------------- (2) acuerdo individual
ACU = {(f["bloque"], f["qi"]): f for f in
       json.loads((PIL/"acuerdo_individual.json").read_text(encoding="utf-8"))}
# Pearson alcanzado, comparable con corr_max (que es Pearson)
PEAR = {eval(k): v for k, v in json.loads(Path(__file__).parent/"pearson_alcanzado.json".read_text()).items()}

# -------------------------------------------------- (3) tanda de 1.000 Personas
tandas = {}
for p in sorted(glob.glob(str(ENT/"resultados"/"encuesta_2026-07-16_12*.json"))):
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    if d.get("done", 0) >= 500:
        tandas[d["plantilla"]] = d
print(f"tandas de 1.000 cargadas: {len(tandas)}")

PLANT = {p.name: json.loads(p.read_text(encoding="utf-8"))
         for p in (ENT/"encuestas").glob("barometro_digital_*.json")}

def panel_y_real(e):
    """(% panel por opción, % real por opción) para una pregunta del crosswalk."""
    d = tandas.get(e["bloque"])
    if not d: return None, None
    q = PLANT[e["bloque"]]["preguntas"][e["qi"] - 1]
    ops = q["opciones"]; k = int(q.get("multiple") or 1)
    cnt = [0]*len(ops); n = 0
    for r in d["results"]:
        resp = (r.get("resps") or {}).get(str(e["qi"]))
        if not resp: continue
        letras = [x.strip() for x in str(resp).replace(" ", "").split(",") if x.strip()]
        hit = False
        for L in letras[:k]:
            j = ord(L[0].upper()) - 65
            if 0 <= j < len(ops): cnt[j] += 1; hit = True
        if hit: n += 1
    if not n: return None, None
    panel = [c/n*100 for c in cnt]
    dr = q.get("datos_reales")
    real = [real_por_opcion(o, dr) for o in ops] if dr else [None]*len(ops)
    return panel, real

filas = []
for e in ITEMS:
    kk = clave(e); c = CONSTRUCTO[kk]; key = (e["bloque"], e["qi"])
    t = TECHO.get(key, {}); a = ACU.get(key, {})
    panel, real = panel_y_real(e)
    dam = conc_p = conc_r = None
    if panel and real and any(x is not None for x in real):
        pares = [(p, r) for p, r in zip(panel, real) if r is not None]
        dam = float(np.mean([abs(p-r) for p, r in pares]))
        conc_p = max(p for p, _ in pares); conc_r = max(r for _, r in pares)
    filas.append(dict(var=kk, constructo=c, modo=t.get("modo") or e["tipo"],
        n=t.get("n"), R2=t.get("R2"), R2_sd=t.get("R2_sd"), corr_max=t.get("corr_max"),
        spearman=a.get("spearman"), pearson=(PEAR.get(key) or {}).get("r"),
        kappa=a.get("kappa_w", a.get("kappa")),
        exacto=a.get("exacto_%"), moda=a.get("base_moda_%"), delta=a.get("delta_vs_moda"),
        acc_techo=t.get("acierto"), moda_techo=t.get("base_moda"), delta_techo=t.get("delta"),
        dam=dam, conc_panel=conc_p, conc_real=conc_r,
        texto=str(e["texto"])[:80]))

json.dump(filas, open("resultados_marketing.json","w"), ensure_ascii=False, indent=1)
print(f"→ resultados_marketing.json  ({len(filas)} filas)")

# ------------------------------------------------------------------- resumen
def mm(g, k):
    v = [x[k] for x in g if x.get(k) is not None and x[k] == x[k]]
    return float(np.mean(v)) if v else float("nan")

print(f"\n{'constructo':36} {'n':>3} {'corrmax':>8} {'pears':>7} {'%techo':>7} "
      f"{'delta':>7} {'DAM':>6} {'concP':>6} {'concR':>6}")
orden = ["A · Retrenchment de consumo","B · Decisión de viaje",
         "C · Satisfacción de servicio","D · Confianza de marca",
         "E · (contraste) Confianza política"]
for c in orden:
    g = [f for f in filas if f["constructo"] == c]
    cm, sp = mm(g,"corr_max"), mm(g,"pearson")
    pct = sp/cm*100 if cm==cm and cm>0 and sp==sp else float("nan")
    dl = mm(g,"delta"); dl = mm(g,"delta_techo") if dl!=dl else dl
    print(f"{c:36} {len(g):3d} {cm:8.3f} {sp:7.3f} {pct:6.0f}% "
          f"{dl:+7.2f} {mm(g,'dam'):6.1f} {mm(g,'conc_panel'):6.1f} {mm(g,'conc_real'):6.1f}")
mk = [f for f in filas if f["constructo"] in MKT]
cm, sp = mm(mk,"corr_max"), mm(mk,"pearson")
print(f"{'TOTAL MARKETING':36} {len(mk):3d} {cm:8.3f} {sp:7.3f} {sp/cm*100:6.0f}% "
      f"{mm(mk,'delta'):+7.2f} {mm(mk,'dam'):6.1f} {mm(mk,'conc_panel'):6.1f} {mm(mk,'conc_real'):6.1f}")
