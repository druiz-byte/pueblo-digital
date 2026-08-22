# -*- coding: utf-8 -*-
"""Informe Fase 1 — subcorpus de marketing. Reproducible: sólo lee JSON ya generados."""
import json, numpy as np
from pathlib import Path
AQ = Path(__file__).parent
F = json.loads((AQ/"resultados_marketing.json").read_text(encoding="utf-8"))
GB = {v["var"]: v for v in json.loads((AQ/"techo_gbm.json").read_text(encoding="utf-8")).values() if v.get("var")}
ORDEN = ["A · Retrenchment de consumo","B · Decisión de viaje","C · Satisfacción de servicio",
         "D · Confianza de marca","E · (contraste) Confianza política"]
MKT = set(ORDEN[:4])
def m(g,k):
    v=[x[k] for x in g if x.get(k) is not None and x[k]==x[k]]
    return (float(np.mean(v)), float(np.std(v)/np.sqrt(len(v)))) if v else (float("nan"),)*2
def mg(g,k):
    v=[GB[x["var"]][k] for x in g if x["var"] in GB and k in GB[x["var"]]]
    return float(np.mean(v)) if v else float("nan")

L=["# Fase 1 — El subcorpus de marketing del Deustobarómetro","",
"**44 ítems de marketing + 10 de contraste político.** Sin API: relectura de resultados ya",
"generados (techo n=1.000 · acuerdo individual n=300 · tanda agregada n=1.000).",
"Selección **ex ante por constructo**, definida en `marketing_items.json`.","",
"## Cómo se mide cada columna","",
"| columna | qué es |","|---|---|",
"| **techo lin** | `corr_max = √R²_OOS`, ridge, CV 5-fold **repetida 20 veces**, semilla por ítem |",
"| **techo GBM** | igual pero con gradient boosting: capta no linealidades que el ridge pierde |",
"| **alcanzado** | correlación de **Pearson** panel↔real, la misma métrica que el techo |",
"| **Δ vs moda** | acierto del panel menos el de \"responder siempre la moda real\" |",
"| **DAM** | desviación absoluta media panel vs real, por opción |",
"| **conc.** | cuota de la opción más elegida, panel vs real |","",
"> No se usa **Spearman**: en ítems con ~90 % de casos en una categoría se dispara por el",
"> tratamiento de empates y llega a superar el techo, lo que es imposible por construcción.",
"> Con Spearman el bloque de retrenchment daba un absurdo 367 % del techo.","",
"## Resumen por constructo","",
"| constructo | ítems | techo lin | techo GBM | alcanzado (Pearson) | % del techo GBM | Δ vs moda | DAM p.p. | conc. panel | conc. real | exceso |",
"|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
def fila(g,nom,bold=False):
    lin,_=m(g,"corr_max"); gb=mg(g,"corr_max_gbm"); pe,pes=m(g,"pearson")
    dl,_=m(g,"delta"); dl = m(g,"delta_techo")[0] if dl!=dl else dl
    dam,_=m(g,"dam"); cp,_=m(g,"conc_panel"); cr,_=m(g,"conc_real")
    pct = pe/gb*100 if gb==gb and gb>0 else float("nan")
    b="**" if bold else ""
    return (f"| {b}{nom}{b} | {b}{len(g)}{b} | {b}{lin:.3f}{b} | {b}{gb:.3f}{b} | "
            f"{b}{pe:.3f} ± {1.96*pes:.3f}{b} | {b}{pct:.0f} %{b} | {b}{dl:+.1f}{b} | "
            f"{b}{dam:.1f}{b} | {b}{cp:.1f}{b} | {b}{cr:.1f}{b} | {b}+{cp-cr:.1f}{b} |")
for c in ORDEN: L.append(fila([f for f in F if f["constructo"]==c], c))
L.append(fila([f for f in F if f["constructo"] in MKT], "TOTAL MARKETING", True))

L+=["","## Los cuatro resultados","",
"**1 · El techo de marketing es más bajo que el político.** Confianza de marca (0,35) y confianza",
"política (0,40) son parecidas, pero **retrenchment de consumo (0,13)** y **decisión de viaje (0,14)**",
"quedan muy por debajo. El perfil sociodemográfico informa *menos* sobre la conducta de consumo que",
"sobre la actitud política — justo al revés de lo que necesitaría la promesa comercial del panel",
"sintético, y al revés de donde la literatura ha puesto sus benchmarks.","",
"**2 · El panel alcanza el 54 % del techo, y en consumo no alcanza nada porque no hay nada.** En",
"retrenchment el techo (0,134) y lo alcanzado (0,149) son ambos indistinguibles de cero a nivel de",
"ítem (ver la sección de anomalía). La lectura correcta no es \"el panel va bien en consumo\", es",
"**\"en consumo no hay señal que capturar desde el perfil\"**.","",
"**3 · Δ vs moda negativo en los cuatro constructos.** El panel es peor que responder siempre la",
"categoría más frecuente. El peor caso es decisión de viaje, **−12,4 p.p.**, y dentro de él la",
"pregunta por la razón del abandono de viaje (**−26,7 p.p.**, kappa 0,00).","",
"**4 · Colapso de varianza en los cuatro.** La opción más elegida se lleva **65,0 %** en el panel",
"frente al **38,8 %** real: **+26,2 p.p. de exceso**. Ningún ítem de B, C, D o E tiene exceso",
"negativo. El caso extremo es la multirrespuesta de efectos del turismo: **99,9 % vs 41,2 %**.","",
"## Anomalía detectada y resuelta: ítems que \"superan\" su techo","",
"Dos ítems de retrenchment (p6_5, p6_9) daban un Pearson por encima de su techo lineal, lo que es",
"imposible por construcción. Tres comprobaciones:","",
"1. **Techo no lineal.** Con gradient boosting el techo de p6_5 sube de 0,141 a **0,234**, dentro del",
"   intervalo del valor observado. El ridge infraestimaba: la relación perfil→respuesta no es lineal",
"   en este bloque.",
"2. **Bootstrap del Pearson** (5.000 réplicas). Con ~90 % de los casos en una categoría, el error",
"   nominal de Fisher es demasiado optimista. Los IC reales son enormes:","",
"   | var | n | % moda real | Pearson | IC 95 % bootstrap |",
"   |---|--:|--:|--:|---|",
"   | p6_5 | 292 | 86,6 % | 0,295 | [0,129 · 0,446] |",
"   | p6_9 | 291 | 92,4 % | 0,164 | **[−0,037 · 0,416]** |",
"   | p6_3 | 298 | 89,3 % | 0,194 | **[−0,034 · 0,421]** |",
"   | p6_4 | 293 | 87,0 % | 0,143 | **[−0,005 · 0,312]** |","",
"   En p6_9, p6_3 y p6_4 **el intervalo incluye el cero**: esas correlaciones no son distinguibles",
"   de la nada, y menos aún \"superiores al techo\".",
"3. **Los 300 encuestados con predicción son los 300 primeros del fichero** (verificado: 300/300),",
"   no una submuestra aleatoria. Hay que declararlo.","",
"**Conclusión:** ningún ítem supera su techo de forma real. Pero el episodio deja dos exigencias",
"para el paper: (a) el techo del paper debe ser el **no lineal**, o al menos reportar ambos;",
"(b) a nivel de ítem, con n≈300 y asimetría del 90 %, **las correlaciones individuales no son",
"interpretables** — sólo lo son los agregados por constructo.","",
"## Qué hay que corregir en el material previo","",
"- La afirmación **\"el panel alcanza el 65 % del techo\"** (bitácora y `CLAUDE.md`) compara un",
"  Spearman (0,15) con un techo Pearson (0,24). Con métricas homogéneas y techo no lineal, en el",
"  subcorpus de marketing es el **54 %**. La cifra global del proyecto debe recalcularse igual.",
"- El techo global pasa de **corr máx 0,24 a 0,22** (lineal) tras corregir el bug de mapeo",
"  (`incidencia_mapeo_idx_real.md`).","",
"## Sesgo de selección","",
"Los 44 ítems **no son una muestra aleatoria** de las 152 preguntas: se eligieron por constructo de",
"marketing. La diferencia con el piloto de Ikuspegi es que aquí la selección es **ex ante y por",
"contenido**, no por resultado, y el grupo de contraste político (E) se define con el mismo criterio",
"para poder comparar. Aun así hay que declararlo en el paper.","",
"## Detalle por ítem","",
"| var | c | n | R² lin | ±sd | techo lin | techo GBM | Pearson | Δ vs moda | DAM | conc. P | conc. R | ítem |",
"|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|"]
def s(x,f="{:.3f}"): return f.format(x) if x is not None and x==x else "—"
for c in ORDEN:
    for f in sorted([x for x in F if x["constructo"]==c], key=lambda z: str(z["var"])):
        d=f.get("delta") if f.get("delta") is not None else f.get("delta_techo")
        g=GB.get(f["var"],{})
        L.append(f"| {f['var']} | {c[0]} | {f.get('n') or '—'} | {s(f.get('R2'))} | {s(f.get('R2_sd'))} | "
                 f"{s(f.get('corr_max'))} | {s(g.get('corr_max_gbm'))} | {s(f.get('pearson'))} | "
                 f"{s(d,'{:+.1f}')} | {s(f.get('dam'),'{:.1f}')} | {s(f.get('conc_panel'),'{:.1f}')} | "
                 f"{s(f.get('conc_real'),'{:.1f}')} | {f['texto'][:56]} |")
(AQ/"resultados_marketing.md").write_text("\n".join(L),encoding="utf-8")
print("\n".join(L[:30]))
