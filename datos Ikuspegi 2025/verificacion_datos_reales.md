# Verificación de los datos reales — Ikuspegi 2025 (piloto de 13 preguntas)

El informe de Ikuspegi **no publica tablas**: los porcentajes viven como etiquetas
de datos dentro de los gráficos. Se han extraído con `pdfplumber` y verificado
uno a uno contra el texto narrativo del propio informe. Este documento deja la
trazabilidad opción a opción.

## Criterios

1. **Suma = 100 ± 0,6** (redondeo a un decimal). Toda pregunta la cumple.
2. **Doble fuente siempre que existe**: etiqueta del gráfico + cifra citada en el
   texto. Cuando ambas coinciden, el dato es firme.
3. **Residuo declarado**: si el gráfico omite la etiqueta de una categoría muy
   pequeña, el valor se reconstruye como `100 − suma del resto` y se marca.
4. **Nada se infiere de la posición en gráficos apilados sin contrastar la suma**:
   pdfplumber devuelve las etiquetas de barras apiladas en orden espacial, no
   lógico, y en al menos un caso (Gráfico 43, P10) el orden sale desordenado.
   Por eso P10 **queda fuera del piloto** pese a tener dato.

## Tabla de verificación

| Preg. | Gráfico (pág.) | Suma | Estado | Observación |
|---|---|---:|---|---|
| P3 | G5 (30) | 100,0 | ✅ doble fuente | "No son suficientes" = 1,2 por residuo, **confirmado** por el texto p. 29 ("un 4,7 % valora que son pocas o no suficientes"; 4,7 − 3,5 = 1,2) |
| P5 | G7 (32) | 100,0 | ⚠ residuo no confirmado | Gráfico da 9,8 / 21,5 / 56,2 / 9,5 / 2,5. "No son suficientes" = 0,5 por residuo, sin cita textual que lo confirme |
| P6 | G8 (34) | 99,9 | ✅ doble fuente | Las cuatro cifras están literalmente en el texto p. 34 (1,3 · 7,3 · 90,0 · 1,3) |
| P8c | G28 (61) | 100,0 | ✅ doble fuente | 77,9 acuerdo · 7,7 indecisión · 13,3 desacuerdo citados en el texto p. 61. NS/NC = 1,1 por residuo |
| P8f | G12 (41) | 99,9 | ✅ etiquetas completas | 33,3 / 23,0 / 40,8 / 2,8 |
| P8n | G27 (60) | 100,0 | ✅ etiquetas nominativas | Único gráfico con etiqueta pegada al nombre de la categoría: Acuerdo 70,2 · Indecisión 20,0 · Desacuerdo 7,5 · Ns/Nc 2,3. Texto p. 60 idéntico |
| P11 | G11 (39) | 100,0 | ✅ doble fuente | "Prohibir por completo" = 2,7 lo da el texto p. 38, no el gráfico |
| P12 | G13 (42) | 100,0 | ✅ doble fuente | Las cinco cifras están en el texto p. 42 |
| P13 | G14 (43) | 99,9 | ✅ doble fuente | Las cinco cifras están en el texto p. 43 |
| P20 | G24 (57) | 100,0 | ⚠ residuo no confirmado | 69,2 y 29,2 confirmados en el texto p. 57. NS/NC = 1,6 por residuo |
| P22j | G26 (59) | 100,0 | ✅ doble fuente | Texto p. 59: "73,7 % de acuerdo, 11,5 % en desacuerdo, 13 % indecisión, 1,8 % no se pronuncia" |
| P26 | G25 (59) | — | ✅ media | El informe **solo publica la media** (5,3 en 2025), no la distribución. Se compara media contra media |
| P36 | G40 (82) | 99,9 | ✅ etiquetas completas | 88,8 / 8,8 / 2,3 |

**Error de verificación:** 13/13 preguntas con suma dentro de ±0,6 p.p.; 11 con
doble fuente, 2 con un residuo menor (≤1,6 p.p.) sin confirmación textual.

## Discrepancia detectada y descartada del piloto

**P8a** ("los sueldos bajan como consecuencia de la llegada de personas que
vienen a vivir y trabajar", Gráfico 28, p. 61). Las etiquetas del gráfico en
orden de segmento dan `14,3 · 9,2 · 71,7 · 4,8` (Acuerdo · Indecisión ·
Desacuerdo · Ns/Nc), pero el texto de la p. 61 dice "un 4,8 % de la población se
muestra dubitativo", lo que asignaría la indecisión al 4,8 y el Ns/Nc al 9,2.
Ambas lecturas suman 100, así que la suma no desempata. **Excluida del piloto**
hasta poder contrastarla con la publicación de otro año o con Ikuspegi.

Nota análoga en **P22i** (mismo gráfico): 13,0 · 16,0 · 69,6 con residuo 1,4;
el texto habla de "un 17,3 % que muestra indecisión o no sabe/no contesta"
(16,0 + 1,4 = 17,4), lo que **sí** valida el orden de segmento. Es la razón por
la que la lectura por orden de segmento es probablemente la correcta también en
P8a, pero no lo suficiente para darla por firme.

## Umbral de ruido

El dato real viene de **n = 600**, con error muestral **±4,0 p.p.** (95 %,
P=Q=0,5). El panel tiene n = 1.000 pero es sintético: no aporta precisión
adicional al contraste. **Una diferencia panel-real por debajo de ~4 p.p. no es
distinguible de ruido muestral** y no debe interpretarse como acierto ni como
fallo. El comparador marca con ⚠ el rango 4-10 p.p. y con ❌ lo superior.

## Baselines tontos (calculados sobre estas 13 preguntas)

Referencia obligatoria: cualquier DAM del panel debe compararse contra estrategias
que no usan información alguna sobre la Persona.

| Estrategia | DAM medio | Qué hace |
|---|---:|---|
| **Uniforme** | **19,7 p.p.** | Reparte las respuestas a partes iguales entre las opciones |
| **Moda** | **17,0 p.p.** | Todas las Personas eligen la opción más votada en el dato real |

Contexto: el Deustobarómetro dio **DAM 13,4** (panel v1) / **13,9** (v2) sobre
152 preguntas. Si la réplica de Ikuspegi no baja claramente de ~17 p.p., el panel
no está aportando nada sobre adivinar la moda.

**Advertencia metodológica (heredada del frente PPI++):** un DAM bajo mide
únicamente el ajuste de la *distribución agregada*. Se puede clavar el histograma
con acierto individual nulo. El DAM no dice nada sobre si cada Persona responde
como respondería su equivalente real.

## Reproducir la extracción

```python
import pdfplumber
with pdfplumber.open('Datos kiuspegi 2025.pdf') as pdf:
    print(pdf.pages[29].extract_text())   # Gráfico 5, P3
```

Los números aparecen como texto plano en la fila del año correspondiente
(`2025 19,0 26,8 45,3 3,5 4,2`).
