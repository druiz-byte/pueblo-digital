#!/usr/bin/env python3
"""
Descarga de microdatos para el rediseño del panel Pueblo Digital.

Ejecutar en el ordenador de David (tiene salida a internet):
    python descargar_fuentes.py

Descarga en ./datos_fuente/ los ficheros abiertos que tienen URL directa
(Sociómetro Vasco). Para EUSTAT y CIS deja instrucciones, porque su portal
no expone una URL estable (hay que pulsar el enlace de descarga).

Sólo usa la librería estándar (urllib), no hace falta instalar nada.
"""

import os
import urllib.request

DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_fuente")
os.makedirs(DEST, exist_ok=True)

# --- Sociómetro Vasco (Open Data Euskadi) -----------------------------------
# Patrón de URL por ola:  .../od_<AA>sv<NN>/opendata/<AA>sv<NN>.csv
# Cada ola trae CSV, SAV (SPSS/PSPP) y el PDF con el cuestionario/codebook.
# Añade aquí las olas que quieras. La 83 está verificada.
SOCIOMETROS = {
    # nombre_local : (url_csv, url_sav, pagina_catalogo_con_cuestionario)
    "sociometro_83": (
        "https://opendata.euskadi.eus/contenidos/ds_informes_estudios/od_24sv83/opendata/24sv83.csv",
        "https://opendata.euskadi.eus/contenidos/ds_informes_estudios/od_24sv83/opendata/24sv83_etik.sav",
        "https://opendata.euskadi.eus/catalogo/-/informes-estudios/sociometro-83/",
    ),
}


def descargar(url, ruta):
    try:
        print(f"  descargando {os.path.basename(ruta)} ...", end=" ", flush=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r, open(ruta, "wb") as f:
            f.write(r.read())
        print("OK")
    except Exception as e:
        print(f"ERROR: {e}")


def main():
    print(f"Destino: {DEST}\n")
    print("== Sociómetro Vasco ==")
    for nombre, (csv_url, sav_url, pagina) in SOCIOMETROS.items():
        descargar(csv_url, os.path.join(DEST, nombre + ".csv"))
        descargar(sav_url, os.path.join(DEST, nombre + ".sav"))
        print(f"  cuestionario/codebook (PDF) en: {pagina}")
    print("\nRecuerda: ponderar por la columna 'wt'. Municipios <5.000 hab = codigo 999.")

    print("\n== EUSTAT (descarga manual, 2 clics en su portal) ==")
    print("  Portal microdatos:      https://www.eustat.eus/prodserv/fich_microdatos_c.html")
    print("  Bienestar Personal:     https://es.eustat.eus/estadisticas/tema_632/opt_1/tipo_11/temas.html")
    print("  Sociedad Informacion:   https://www.eustat.eus/estadisticas/tema_15/opt_1/tipo_11/ti_encuesta-sobre-la-sociedad-de-la-informacion/temas.html")
    print("  Condiciones de Vida:    https://www.eustat.eus/estadisticas/tema_76/opt_1/tipo_11/ti_encuesta-de-condiciones-de-vida/temas.html")

    print("\n== CIS / ESS (registro o descarga en su portal) ==")
    print("  CIS:  https://www.cis.es")
    print("  ESS:  https://www.europeansocialsurvey.org/data-portal")

    print("\nHecho. Los ficheros con URL directa estan en ./datos_fuente/")


if __name__ == "__main__":
    main()
