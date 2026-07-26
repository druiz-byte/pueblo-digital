# -*- coding: utf-8 -*-
"""Enriquece predictores_deusto.csv con 3 campos REALES del Deustobarómetro que no
se estaban usando en la generación PPI, para intentar subir la correlación del panel:

  - nacimiento              (p42, + ccaa_otra / pais_otra para el lugar concreto)
  - religion                (p41)
  - voto_autonomicas_2020   (p46)

Estas variables NO se predicen en ninguno de los 7 bloques del barómetro digital
salvo el Bloque 7 (perfil/validación), así que inyectarlas en el prompt NO es
circular para los bloques 1-6 (que son los que miden la ganancia PPI). El Bloque 7
ya se trata como validación, no como ganancia.

Las variables p41/p42/p46 NO traen etiquetas de valor en el .sav; los códigos se
mapean por posición a las opciones de la plantilla barometro_digital_7, verificado
alineando las frecuencias del .sav con los `datos_reales` (coinciden 1:1) y el join
por `id` validado contra la columna voto_autonomicas_2024 ya existente (1000/1000).

Se hace un backup del CSV original y se reescribe predictores_deusto.csv añadiendo
las 3 columnas al final (los 12 predictores previos quedan intactos).

Uso:  python enriquecer_predictores.py        (requiere pyreadstat + el .sav)
Se ejecutó una vez en el entorno de Claude; David NO necesita volver a correrlo
(el CSV enriquecido ya viaja por OneDrive). Se conserva por reproducibilidad.
"""
import csv, shutil
from pathlib import Path
import pyreadstat

RAIZ = Path(__file__).resolve().parent.parent
SAV  = RAIZ / "Datos Deustobarometro verano 2026.sav"
CSV  = RAIZ / "predictores_deusto.csv"
BAK  = RAIZ / "predictores_deusto_backup_pre_enriq.csv"

# --- mapas código -> etiqueta (por posición, verificados contra datos_reales) ---
RELIG = {1: "Católico/a", 2: "Creyente de otras confesiones", 3: "Indiferente",
         4: "Agnóstico/a", 5: "Ateo/a"}                       # 6 = NS/NC -> N/D
VOTO2020 = {1: "PNV/ EAJ", 2: "EH Bildu", 3: "PSE", 4: "Elkarrekin Podemos",
            5: "PP", 6: "Vox", 7: "Otros", 8: "Voté nulo", 9: "Voté en blanco",
            10: "No voté", 11: "No lo recuerdo", 12: "Prefiero no contestar"}
NUEVAS = ["nacimiento", "religion", "voto_autonomicas_2020"]


def _int(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


def main():
    df, meta = pyreadstat.read_sav(str(SAV))
    CCAA = meta.variable_value_labels.get("ccaa_otra", {})   # {codigo: "Andalucía"...}
    PAIS = meta.variable_value_labels.get("pais_otra", {})

    extra = {}   # id -> {nacimiento, religion, voto_autonomicas_2020}
    for r in df.itertuples():
        rid = str(_int(r.id))
        # --- nacimiento (p42 + detalle) ---
        p42 = _int(r.p42)
        if p42 == 1:
            nac = "En el País Vasco"
        elif p42 == 2:
            cc = CCAA.get(getattr(r, "ccaa_otra"))
            nac = f"En otra Comunidad Autónoma ({cc})" if cc else "En otra Comunidad Autónoma"
        elif p42 == 3:
            pa = PAIS.get(getattr(r, "pais_otra"))
            nac = f"En otro país fuera de España ({pa})" if pa else "En otro país fuera de España"
        else:
            nac = "N/D"
        # --- religión (p41) ---
        rel = RELIG.get(_int(r.p41), "N/D")
        # --- voto 2020 (p46) ---
        v20 = VOTO2020.get(_int(r.p46), "N/D")
        extra[rid] = {"nacimiento": nac, "religion": rel, "voto_autonomicas_2020": v20}

    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    campos = list(rows[0].keys()) + [c for c in NUEVAS if c not in rows[0]]
    faltan = 0
    for row in rows:
        e = extra.get(str(_int(row["id"])))
        if e is None:
            faltan += 1
            e = {c: "N/D" for c in NUEVAS}
        row.update(e)

    if not BAK.exists():
        shutil.copy(CSV, BAK)
    with CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(rows)

    # --- informe rápido de cobertura ---
    def cob(c):
        vals = [r[c] for r in rows if r.get(c) not in (None, "", "N/D")]
        return len(vals), len(rows)
    print(f"OK -> {CSV.name} (+{len(NUEVAS)} columnas). Backup: {BAK.name}. sin match: {faltan}")
    for c in NUEVAS:
        n, tot = cob(c)
        print(f"   {c:24} cobertura {n}/{tot} ({100*n/tot:.1f}%)")


if __name__ == "__main__":
    main()
