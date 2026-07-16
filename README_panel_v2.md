# Panel v2 — cómo lanzarlo y contrastarlo

Panel reconstruido anclando cada Persona en un **encuestado real** e inyectando los bloques con **más llaves de enlace** (5-6 en vez de 4). Objetivo: medir si mejora la predicción del Deustobarómetro real frente a la v1.

## Qué se ha construido (ya hecho)

- `construir_panel_v2.py` — pipeline de construcción (solo datos, sin API). **Ya ejecutado.**
- `pv_agentes_v2.json` — las 1.000 Personas v2.
- `entrevista/prompt_v2.py` — generador de prompt adaptado al esquema v2.
- `entrevista/lanzar_barometro_v2.py` — lanzador (mismo motor que la v1, con el panel y el prompt v2).

### Cómo se construyó cada Persona
1. **Ancla — Sociómetro Vasco 83** (3.030 reales): remuestreo ponderado por `wt` → sociodemográfico + político + euskera de un encuestado real (opción B, correlaciones intactas). Voto = recuerdo 2020 (P23) con respaldo de intención 2024 (P21).
2. **Inyección ESS España** (medios + bienestar): kNN por `sexo × edad × educación × laboral × ideología` (969/1.000 emparejadas a 5 llaves).
3. **Inyección Capital Social 2022** (confianza, redes, participación, cohesión): kNN por `sexo × edad × provincia × clase` (1.000/1.000 a 4 llaves).

## Cómo lanzar el barómetro (en el ordenador de David)

La API de Claude no funciona en el entorno de Cowork, así que esto se ejecuta en tu máquina:

```bash
cd entrevista
# .env con ANTHROPIC_API_KEY válida y GEMINI_API_KEY/GROQ_API_KEY comentadas
python lanzar_barometro_v2.py            # 6 bloques × 1.000 Personas (~15-20 $, ~30-45 min con Haiku)
python lanzar_barometro_v2.py --muestra 50   # prueba rápida
python lanzar_barometro_v2.py 3          # solo el bloque 3
```

Guarda un archivo por bloque en `entrevista/resultados/`.

## Cómo contrastar con el real

Igual que con la v1 (la herramienta ya existe):

```bash
python comparar_deustobarometro.py resultados/<archivo_bloqueN>.json > resultados/contraste_v2_bloque N.md
```

Compara el **DAM medio global** con el de la v1 (**16,7 p.p.**, tanda 2026-07-08). Si el trabajo ha funcionado, debería bajar, sobre todo en los bloques que dependían de medios/bienestar/confianza.

## Validación previa hecha (sin API)

La coherencia entre bloques mejora respecto a la v1: donde la v1 daba **interés político plano** entre bandas ideológicas (34/34/38 % "poco interesado"), la v2 ya diferencia (izquierda 38 % "bastante interesado"), y la confianza en políticos y la participación social también gradúan con la ideología. Las correlaciones que antes se rompían en las costuras entre encuestas ahora se sostienen.

## Avisos metodológicos (para el artículo)

- **Comparación de pipeline, no de un solo factor.** v1 (sintético + 4 llaves + Gizaker/EBP) vs v2 (ancla real + más llaves + ESS/Capital Social). No aísla una única variable; si se quiere, se puede hacer una ablación posterior.
- **Medios y bienestar del ESS** se emparejan con toda la muestra española (submuestra vasca = 671): reflejan la estructura española, no específicamente vasca.
- **Capital Social** aporta índices 0-10 ya construidos (no ítems crudos) y no incluye educación como llave.
- **Voto** más ruidoso que en la v1 (el Sociómetro 83 es preelectoral): ~50 % abstención/NS-NC. La señal política la sostienen también ideología, nacionalismo e identidad.
- **Religión y "principales problemas"** no están en el ancla (quedan vacíos).
