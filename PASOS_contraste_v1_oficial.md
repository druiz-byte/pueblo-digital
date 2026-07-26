# Cerrar el contraste v1 vs v2 (mismas plantillas oficiales)

**Objetivo:** relanzar el panel **v1** (`pv_agentes.json`) con las **7 plantillas oficiales**
(`barometro_digital_1..7`, 152 preguntas), las mismas que ya usó la v2 el 2026-07-14,
y calcular el DAM v1 vs v2 lado a lado. Hoy la comparación (14,0 vs 16,7) mezcla el
cambio de panel con el cambio de plantillas; esto lo aísla.

Todo se ejecuta **en tu PC** (la API de Anthropic no es accesible desde el sandbox de Claude).

---

## 0. Comprobar el `.env` (una vez)

En `entrevista/.env`:
- `ANTHROPIC_API_KEY=...` válida y **descomentada**.
- `GEMINI_API_KEY` y `GROQ_API_KEY` **comentadas** (con `#` delante). Si no, el lanzador aborta a propósito.

## 1. Prueba corta (recomendada, ~1 min, unos céntimos)

```
cd entrevista
python lanzar_barometro.py --muestra 20
```

Verifica que sale `vacías: 0 · sin parsear: 0` en cada bloque. Estas 7 salidas de 20
Personas **no molestan** al contraste final (el agregador ignora todo lo que tenga < 500 Personas).

## 2. Tanda completa v1 (1.000 Personas, ~30-45 min, ~15-20 $)

```
cd entrevista
python lanzar_barometro.py
```

Lanza los 7 bloques en secuencia sobre el panel **v1**. Guarda 7 ficheros nuevos en
`resultados/encuesta_<fecha_de_hoy>_*.json`, etiquetados por bloque. Al terminar imprime
un resumen con los nombres.

## 3. Contraste v1 vs v2 en una sola tabla

```
cd entrevista
python contraste_v1_vs_v2.py --v1 AAAA-MM-DD --v2 2026-07-14
```

Sustituye `AAAA-MM-DD` por **la fecha de hoy** (la de la tanda del paso 2; p.ej. `2026-07-16`).
El script busca, por cada bloque, la tanda completa (>= 500 Personas) de cada fecha, calcula
el DAM con la **misma lógica** que `comparar_deustobarometro.py` y escribe
`resultados/contraste_v1_vs_v2.md` con una tabla:

| Bloque | Preg. | DAM v1 | DAM v2 | Δ (v2−v1) |

y una fila **GLOBAL**. Δ negativo = la v2 se acerca más al real (mejora atribuible al panel).

---

## Notas

- **Referencia v2 ya calculada** (para que sepas qué esperar en la columna DAM v2):
  B1 economía 11,7 · B2 bienestar 14,4 · B3 miedos 18,7 · B4 turismo 26,9 ·
  B5 política 10,1 · B6 geopolítica 23,7 · B7 perfil 11,3 · **GLOBAL ≈ 13,9** (152 preg.).
- El global sale sobre **152** preguntas (incluye el Bloque 7 de perfil/validación). El
  "14,0 sobre 143" de la bitácora excluía ese bloque 7. Da casi igual; si lo quieres
  idéntico a lo documentado, ignora la fila del Bloque 7 al leer el global.
- Si algún bloque quedó a medias (n < 500), el agregador avisa de qué falta y no calcula
  hasta que relances ese bloque: `python lanzar_barometro.py N` (N = número de bloque).
- No hay riesgo de pisar los resultados de la v2: los ficheros llevan marca de tiempo y
  se distinguen por fecha.

## Qué me traes de vuelta

El fichero `resultados/contraste_v1_vs_v2.md` (o solo la fila GLOBAL). Con eso cerramos el
punto pendiente nº 1 del proyecto y tenemos la mejora del panel aislada y limpia para el artículo.
