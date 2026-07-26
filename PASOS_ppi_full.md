# PPI++ completo — las 152 preguntas de los 7 bloques

## Comparar en SPSS (nuevo)

- **`equivalencia_preguntas_panel_barometro.md`** (raíz): tabla de las 152 preguntas
  con el texto de la plantilla (lo que ve la Persona) junto a la variable + etiqueta
  del `.sav` original y el error de verificación por opción. Prueba que se pregunta
  y codifica exactamente lo mismo (152/152, error medio 0,58 p.p.).
- **`piloto_ppi/predicciones_a_sav.py`**: convierte `predicciones_deusto_full.json`
  en dos `.sav` con el MISMO esquema, códigos y etiquetas que el original:
  - `panel_predicho_<N>.sav` — solo las respuestas del panel.
  - `comparacion_real_vs_panel.sav` — 2N filas (reales + panel) con variable
    `fuente` (1=Deustobarómetro real, 2=Panel sintético). En SPSS: *Datos ▸
    Segmentar archivo por `fuente`* y FREQUENCIES, o FREQUENCIES … BY fuente.
  Ejecutar **cuando termine la generación** (`python predicciones_a_sav.py`).

---

**Objetivo:** pasar del piloto PPI++ (solo Bloque 5, 5 variables) al barómetro
entero. Para cada pregunta se contrasta la **sustitución ingenua** (el panel como
si fuera la encuesta → sesgo/DAM) frente a **PPI++** (estimación válida + ahorro de
datos), y se agrega por bloque y global.

Todo lo pesado (el crosswalk 152↔.sav) ya está construido y **verificado sin API**.
Solo falta generar las predicciones (paso con API, en tu PC) y calcular.

## ⭐ NUEVO (perfil enriquecido) — hazlo primero

Para intentar subir la correlación (~0,17), el perfil de generación ahora incluye
**3 campos REALES del propio Deustobarómetro** que antes no se usaban:

- **nacimiento** (p42, con el detalle de CCAA/país: "En otra Comunidad Autónoma (Castilla y León)")
- **religion** (p41)
- **voto_autonomicas_2020** (p46)

Ya está todo preparado (no necesitas pyreadstat):

- `predictores_deusto.csv` **ya trae las 3 columnas nuevas** (lo generé desde el
  `.sav` con `piloto_ppi/enriquecer_predictores.py`; backup del original en
  `predictores_deusto_backup_pre_enriq.csv`). Cobertura: nacimiento 100%, religión
  93,6% (el resto es NS/NC → N/D), voto 2020 100%. Códigos verificados alineando
  frecuencias con los `datos_reales` y el join por `id` (1000/1000).
- `generar_predicciones_full.py` **ya inyecta los 3 campos** en el prompt (wrapper
  `build_prompt_enriquecido`; no toca `prompt_v2.py`). No es circular para los
  bloques 1-6 (solo el Bloque 7 pregunta por ellos, y ese ya se trata como validación).
- Las predicciones viejas (perfil pobre) se archivaron en
  `predicciones_deusto_full_v1perfilpobre.json` para que la regeneración arranque
  limpia. **No borres ese archivo**: sirve para comparar el antes/después.

Así que basta con **regenerar los 300 y remedir** (pasos 3 y 4 de abajo).

## Lo que ya está preparado (en `piloto_ppi/`)

- `build_crosswalk.py` → `crosswalk_ppi.json` + `crosswalk_cobertura.md`.
  Mapea cada una de las 152 preguntas a su variable del `.sav` (tipo cat/escala/
  multi) y **se autoverifica**: reconstruye el % real desde el `.sav` y lo compara
  con el `datos_reales` de cada plantilla. Resultado: **152/152 correctas, error
  medio 0,58 p.p.** (≈ perfecto). No necesita API.
- `generar_predicciones_full.py` → predice las 152 preguntas por cada encuestado
  real (requiere API).
- `true_ppi_full.py` → PPI++ por pregunta y bloque (requiere las predicciones).

## Pasos (en tu PC)

**0. Dependencias** (una vez):
```
pip install pyreadstat ppi-python
```

**1. (Opcional, sin API) Reverificar el crosswalk:**
```
cd piloto_ppi
python build_crosswalk.py
```
Debe decir `OK 152/152 · error medio 0.58 p.p.`.

**2. (Sin API) Smoke-test del cálculo PPI:**
```
python true_ppi_full.py --simular 0.55
```
Fabrica predicciones ficticias (55% de acierto) y ejecuta todo el pipeline. Sirve
para confirmar que corre antes de gastar en la generación. Genera un
`informe_ppi_full.md` de prueba (se sobrescribe en el paso 4).

**3. (CON API, ~15-25 $) Generar las predicciones reales:**
```
cd piloto_ppi
python generar_predicciones_full.py --muestra 300     # prueba
python generar_predicciones_full.py                   # los 1.000
```
Requiere `entrevista/.env` con `ANTHROPIC_API_KEY` activa y `GEMINI`/`GROQ`
comentadas (igual que el barómetro). Cada encuestado recibe **solo su perfil de
predictores** (sociodemográficos + ideología/nacionalismo/voto **+ nacimiento,
religión y voto 2020**, los 3 nuevos); **no** se le inyecta ninguna de las 152
respuestas que se predicen en los bloques 1-6 (anti-circularidad). Es
**reanudable**: si se corta, se relanza y sigue. Salida (fichero nuevo, limpio):
`predicciones_deusto_full.json`.

> Si quieres rehacer también los 1.000 más adelante: `python generar_predicciones_full.py`.
> Compara el DAM/correlación del informe nuevo con el de `informe_ppi_full.md`
> anterior (correlación ~0,17) para ver si el enriquecimiento aporta señal.

**4. (Sin API) Calcular PPI++ definitivo:**
```
python true_ppi_full.py
```
Lee las predicciones reales y escribe `informe_ppi_full.md` con:

- Tabla **por bloque**: nº preguntas · *sust. ingenua DAM* (lo que da el panel v2
  solo) · *PPI++ reducción media de IC* (eficiencia) · cobertura media (validez).
- Tabla **por pregunta** (detalle), con correlación en las escalas.

## Cómo leer el informe

- **Sust. ingenua DAM** = cuánto se equivoca el panel si sustituye a la encuesta
  (comparable a las columnas v1/v2 del contraste). Alto = mal.
- **PPI++ red. IC %** = cuánto estrecha PPI++ el intervalo usando el panel como
  ayuda; se traduce en **ahorro de encuestas reales**. La estimación es **válida
  por construcción** (cobertura ~95%), así que su "error" es ~0: el valor no está
  en acertar más, sino en necesitar menos datos.
- **Bloque 7** (perfil) va marcado con `*`: son los predictores inyectados, así que
  es **circular** — cuenta como validación, no como ganancia. Lo mismo aplica a
  las escalas de ideología/nacionalismo/voto dentro de otros bloques.

## Avisos honestos

- **La ganancia de PPI escala con el tamaño del conjunto NO etiquetado (N ≫ n).**
  Con 1.000 encuestados reales el margen es modesto. Para exprimirlo: usar como
  conjunto no etiquetado un **panel sintético grande** (solo predicciones `f`, sin
  `Y` real) además de los reales. Es la mejora natural siguiente (habría que
  ampliar `true_ppi_full.py` para aceptar ese segundo fichero de solo-`f`).
- La correlación individual del panel topa donde el perfil no informa (ya visto en
  el piloto: Gobierno Central y partidos ≈ 0). Ahí PPI++ se repliega al clásico:
  **nunca empeora**.

## Qué me traes de vuelta

`piloto_ppi/informe_ppi_full.md`. Con eso montamos la tabla/figura definitiva para
el artículo: por bloque, "el panel solo se equivoca X" vs "con PPI++ es válido y
ahorra Y% de datos".
