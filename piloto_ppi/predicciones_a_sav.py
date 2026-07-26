# -*- coding: utf-8 -*-
"""Convierte las predicciones del panel (predicciones_deusto_full.json) en ficheros
.sav de SPSS, codificados EXACTAMENTE igual que el Deustobarómetro original, para
poder compararlos directamente en SPSS.

Reutiliza `crosswalk_ppi.json` (pregunta ↔ variable(s) del .sav + tipo) — el mismo
crosswalk verificado (152/152, error 0,58 p.p.) que usa true_ppi_full.py — y copia
del .sav original las etiquetas de variable y de valor, de modo que:

  - cada pregunta del panel se guarda en la MISMA variable (p2, p18, p8_1, p1_1…),
  - con los MISMOS códigos y etiquetas (1='Muy buena', etc.),
  - categóricas 1..N · escalas 0-10 · multirrespuesta 1=mencionado / perdido=no.

Salidas (en piloto_ppi/):
  - panel_predicho_<N>.sav        : N filas, solo las respuestas del panel.
  - comparacion_real_vs_panel.sav : 2N filas = los N encuestados reales (sus
                                    respuestas verdaderas del .sav) + los N del
                                    panel, con variable `fuente` (1=real, 2=panel).
                                    Es el fichero para comparar en SPSS (Segmentar
                                    archivo por `fuente`, o FREQUENCIES … BY fuente).

Uso:
  python predicciones_a_sav.py
  python predicciones_a_sav.py --pred predicciones_deusto_full_v1perfilpobre.json  # prueba
"""
import sys, json, unicodedata
from pathlib import Path
import numpy as np
import pandas as pd
import pyreadstat

DIR  = Path(__file__).resolve().parent
RAIZ = DIR.parent
SAV  = RAIZ / "Datos Deustobarometro verano 2026.sav"
CW   = json.loads((DIR / "crosswalk_ppi.json").read_text(encoding="utf-8"))
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

PREDF = DIR / "predicciones_deusto_full.json"
if "--pred" in sys.argv:
    PREDF = DIR / sys.argv[sys.argv.index("--pred") + 1]


def nm(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


def letra_idx(L):
    i = LETTERS.find((L or "").strip()[:1])
    return i if i >= 0 else None


def codigo_por_opcion(op, vvl):
    """Devuelve el código del .sav cuya etiqueta corresponde a la opción `op`.
    Prioridad: exacta > NS/NC > subcadena. Si no hay VVL, None (se resuelve por
    posición fuera)."""
    if not vvl:
        return None
    o = nm(op)
    # exacta
    for code, lab in vvl.items():
        if nm(lab) == o:
            return code
    # NS/NC
    if o.startswith("no lo se") or o in ("ns/nc", "ns", "nsnc", "prefiero no contestar"):
        for code, lab in vvl.items():
            if nm(lab).startswith("no lo se") or "prefiero no contestar" in nm(lab):
                return code
    # subcadena (evitando que "buena" capture "muy buena": exige longitud cercana)
    mejor = None
    for code, lab in vvl.items():
        l = nm(lab)
        if l and (l == o or l in o or o in l):
            if mejor is None or abs(len(l) - len(o)) < mejor[1]:
                mejor = (code, abs(len(l) - len(o)))
    return mejor[0] if mejor else None


def main():
    if not PREDF.exists():
        sys.exit(f"✗ No existe {PREDF.name}. Genérala con generar_predicciones_full.py.")
    df, meta = pyreadstat.read_sav(str(SAV))
    df = df.set_index(df["id"].astype(int))
    VVL   = meta.variable_value_labels
    LABS  = meta.column_names_to_labels
    ORDEN = list(df.columns)                       # orden original de variables

    pred = {int(k): v for k, v in json.loads(PREDF.read_text(encoding="utf-8")).items()}
    ids = sorted(pred)
    N = len(ids)
    print(f"Predicciones: {N} encuestados · {PREDF.name}")

    # --- precalcular, por pregunta del crosswalk, cómo decodificar la letra ---
    # value labels de salida (para las de Bloque 7 sin etiqueta en el .sav las creamos)
    out_vvl = {}
    # mapa opción->código por variable categórica
    op2code = {}     # var -> {idx_opcion: codigo}
    for e in CW:
        if e["tipo"] == "cat":
            var = e.get("var")
            if not var:
                continue
            vvl = VVL.get(var)
            m = {}
            for j, op in enumerate(e["opciones"]):
                c = codigo_por_opcion(op, vvl)
                if c is None:                        # sin etiqueta -> por posición (1..N)
                    c = float(j + 1)
                m[j] = c
            op2code[var] = m
            # etiquetas de salida
            if vvl:
                out_vvl[var] = dict(vvl)
            else:
                out_vvl[var] = {float(j + 1): op for j, op in enumerate(e["opciones"])}
        elif e["tipo"] == "multi":
            for v in e.get("vars", []):
                if v and VVL.get(v):
                    out_vvl[v] = dict(VVL[v])

    # --- construir la fila del panel para cada encuestado ---
    def fila_panel(i):
        row = {}
        for e in CW:
            b, qi = e["bloque"], str(e["qi"])
            ans = pred.get(i, {}).get(b, {}).get(qi)
            if ans is None:
                continue
            if e["tipo"] == "cat":
                var = e.get("var")
                fidx = letra_idx(ans)
                if var and fidx is not None and fidx < len(e["opciones"]):
                    row[var] = op2code[var].get(fidx, np.nan)
            elif e["tipo"] == "escala":
                var = e.get("var")
                fidx = letra_idx(ans)
                if var and fidx is not None and 0 <= fidx <= 10:
                    row[var] = float(fidx)
            else:  # multi: 1=mencionado, resto perdido (como el original)
                letras = [x for x in str(ans).replace(" ", "").split(",") if x]
                for j, (v, c) in enumerate(zip(e.get("vars", []), e.get("codigos", []))):
                    if v is None:
                        continue
                    if LETTERS[j] in letras:
                        row[v] = c
        return row

    # variables que realmente aparecen (en orden original)
    filas_panel = [fila_panel(i) for i in ids]
    vars_usadas = [v for v in ORDEN if any(v in f for f in filas_panel)]

    def df_desde(filas, id_list):
        data = {"id": [float(i) for i in id_list]}
        for v in vars_usadas:
            data[v] = [f.get(v, np.nan) for f in filas]
        return pd.DataFrame(data)

    panel_df = df_desde(filas_panel, ids)

    # --- fichero 1: solo panel ---
    out1 = DIR / f"panel_predicho_{N}.sav"
    col_labels1 = {"id": "Identificador único"}
    col_labels1.update({v: (LABS.get(v) or v) for v in vars_usadas})
    pyreadstat.write_sav(panel_df, str(out1),
                         column_labels=[col_labels1.get(c, c) for c in panel_df.columns],
                         variable_value_labels={v: out_vvl[v] for v in vars_usadas if v in out_vvl})
    print(f"  → {out1.name}  ({len(panel_df)} filas, {len(vars_usadas)} variables)")

    # --- fichero 2: comparación real + panel con `fuente` ---
    filas_real = []
    for i in ids:
        r = {}
        for v in vars_usadas:
            val = df.loc[i, v] if v in df.columns else np.nan
            if val == val:      # no NaN
                r[v] = float(val)
        filas_real.append(r)
    real_df = df_desde(filas_real, ids)

    comb = pd.concat([real_df.assign(fuente=1.0), panel_df.assign(fuente=2.0)],
                     ignore_index=True)
    comb = comb[["fuente", "id"] + vars_usadas]
    out2 = DIR / "comparacion_real_vs_panel.sav"
    col_labels2 = {"fuente": "Fuente (1=Deustobarómetro real, 2=Panel sintético)",
                   "id": "Identificador único"}
    col_labels2.update({v: (LABS.get(v) or v) for v in vars_usadas})
    vvl2 = {v: out_vvl[v] for v in vars_usadas if v in out_vvl}
    vvl2["fuente"] = {1.0: "Deustobarómetro real", 2.0: "Panel sintético"}
    pyreadstat.write_sav(comb, str(out2),
                         column_labels=[col_labels2.get(c, c) for c in comb.columns],
                         variable_value_labels=vvl2)
    print(f"  → {out2.name}  ({len(comb)} filas = {N} reales + {N} panel · variable `fuente`)")

    # --- chequeo rápido: comparar % de una categórica clave real vs panel ---
    for v in ("p18", "p2"):
        if v in vars_usadas:
            def dist(d):
                s = d[v].dropna(); return {int(k): round(100*c/len(s),1) for k,c in s.value_counts().items()}
            print(f"  check {v}: real={dist(real_df)}  panel={dist(panel_df)}")


if __name__ == "__main__":
    main()
