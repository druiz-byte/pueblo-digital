# Robustez — modelo frontera, prompt anti-concentración y temperature

Cuatro métricas del diagnóstico de la 17ª sesión sobre las mismas 13 preguntas
de Ikuspegi 2025 y el mismo panel v1. **Sólo cambia una cosa por tanda.**

| tanda | n | vacías | DAM | concentración | NS-NC % | opciones/preg. | fichero |
|---|--:|--:|--:|--:|--:|--:|---|
| v1 (pv_agentes.json) | 1000 | 0 % | 15.7 | 83.7 | 1.4 | 4.3 | `encuesta_2026-08-08_101241.json` |
| v2 (pv_agentes_v2.json) | 1000 | 0 % | 18.2 | 88.8 | 0.9 | 2.7 | `encuesta_2026-08-08_102423.json` |
| prompt · haiku-4-5-20251001 · anti-conc | 1000 | 0 % | 14.8 | 79.4 | 2.0 | 4.5 | `encuesta_2026-08-22_111025.json` |
| temp · haiku-4-5-20251001 · T=0.0 | 1000 | 0 % | 15.8 | 84.1 | 1.1 | 4.2 | `encuesta_2026-08-22_111207.json` |
| modelo · opus-5 | 1000 | 0 % | 11.8 | 75.0 | 0.0 | 3.6 | `encuesta_2026-08-22_112821.json` |
| *Baseline moda* | — | — | 17.0 | — | — | — | |
| *Baseline uniforme* | — | — | 19.7 | — | — | — | |
| *Suelo de ruido (panel perfecto)* | — | — | 0.8 | — | — | — | |
| *REAL (Ikuspegi 2025, n=600)* | — | — | — | 61.5 | 3.4 | — | |

⛔ = **tanda no válida**: más del 2 % de Personas vacías. Las de referencia
tuvieron 0 %. Casi siempre es límite de tasa de la API; repetir con menos hilos.

## Cómo leerla

- **DAM**: más bajo es mejor. La referencia v1/Haiku es **15,7**; el baseline tonto
  de la moda es **17,0**. Si una variante no baja de 17,0, no aporta nada.
- **Concentración**: cuota de la opción más elegida. El real es **61,5**; la referencia
  v1/Haiku **83,7**. Es la métrica del colapso de varianza: si el modelo frontera o el
  prompt funcionan, ESTA es la que tiene que bajar.
- **NS-NC**: el real es **3,4 %**; la referencia da **1,4 %**.
- **opciones/pregunta**: cuántas de las disponibles llega a usar el panel. Referencia
  v1 **4,3**, v2 **2,7**.

> Contrastar contra `../paper/preregistro_robustez.md`, donde están las predicciones
> registradas **antes** de lanzar.