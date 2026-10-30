# Incidencia — el ejemplo de formato ancla la respuesta

**Fecha: 2026-09-22. Estado: confound confirmado por experimento natural. Afecta a
TODAS las tandas del proyecto. Las cifras del ICC no se publican hasta desconfundir.**

## Qué es el ejemplo de formato

`server.py` pide a la Persona que responda en un formato rígido y le muestra un ejemplo
literal de cómo hacerlo:

```
Encuesta. Responde como tú mismo/a.
Escribe SOLO esto (sin texto adicional):
1:B
2:C
...
(sustituye cada letra por tu elección real)
```

Las letras del ejemplo no son neutras: se generaban con `chr(66 + (i+j) % 4)`, una
rotación fija por posición del ítem, idéntica para las 1.000 Personas.

## El experimento natural

El 2026-09-22 se corrigió esa fórmula (acotarla al número real de opciones). El arreglo
cambió la letra del ejemplo en exactamente **dos** de los siete ítems del ICC, dejando
todo lo demás igual: misma plantilla, mismo panel, mismo modelo, mismos textos, mismo
orden de opciones. Es una manipulación de una sola variable.

| ítem | nº opciones | ejemplo antes | ejemplo después | moda antes (n=30) | moda después (n=1.000) |
|---|--:|:--:|:--:|---|---|
| P3 | 4 | B | B | B 96,7 % | B 98,4 % |
| P12 | 4 | C | C | B 76,7 % | B 77,7 % |
| P8 | 4 | D | D | B 63,3 % | B 50,0 % |
| P17 | 4 | **E** (inválida) | **A** | A 90,0 % | A 99,2 % |
| **P18** | 3 | **B** | **C** | **B 100,0 %** | **C 99,7 %** |
| P10 | 4 | C | C | B 60,0 % | C 52,4 % |
| P15 | 4 | D | D | C 86,7 % | C 96,5 % |

**P18 es la prueba.** Es la única pregunta cuyo ejemplo pasó de una letra válida a otra
letra válida. Su respuesta pasó del 100,0 % en B al 99,7 % en C. Las letras significan:

- B en la lista de P18 = **"No"** → con ejemplo B, el 100 % de las Personas dijo "No".
- C en la lista de P18 = **"No lo sé / prefiero no contestar"** → con ejemplo C, el
  99,7 % dijo "No lo sé".

El dato real de la CAE es No 94,0 · Sí 5,4 · NS/NC 0,6. Es decir: con un ejemplo la
respuesta parecía casi perfecta (DAM 4,0) y con el otro es la peor de la batería
(DAM 66,1). **La misma pregunta, la misma Persona, y la única diferencia es una letra
en la plantilla de formato.**

## Qué NO dice este resultado

El ancla no siempre gana. En 3 de los 7 ítems la moda del panel NO coincide con la letra
del ejemplo ni antes ni después (P12, P8, P15), y en P15 el panel se va a "Menos" con el
96,5 % teniendo el ejemplo en D. El test de rotación de opciones del 2026-09-22 sobre la
pregunta de impuestos tampoco siguió al ejemplo.

La lectura que encaja con todo: **el ejemplo ancla cuando el ítem no tiene señal
—ni tópico dominante en el corpus, ni información en el perfil— y pierde cuando sí la
hay.** P18 pregunta por un plan personal que no está en el perfil de la Persona y sobre
el que el discurso público no dicta respuesta: ahí no hay nada que responder, y el
modelo copia lo que tiene delante.

## Alcance del problema

Va más allá del ICC. Todas las tandas del proyecto se lanzaron con una letra de ejemplo
**fija por posición del ítem e idéntica para las 1.000 Personas**. Eso significa que en
cualquier ítem sin señal, una parte desconocida de la distribución publicada puede ser
el ejemplo y no la Persona. Afecta en principio a Ikuspegi, al barómetro completo y a las
tandas de robustez.

Atenuantes que conviene comprobar, no suponer:
- En Ikuspegi el panel mostró gradiente político correcto (V de Cramér con el voto 0,36),
  lo que es incompatible con una respuesta dictada solo por el formato.
- Los bloques con tópico fuerte (inmigración, impuestos) resistieron el ancla en los
  tests directos.

## Qué se hace ahora

1. **No publicar ninguna cifra del ICC** hasta tener la medición del efecto.
2. **Medirlo.** Se añade `EJEMPLO_LETRAS_ALEATORIO=1` a `server.py`: la letra del ejemplo
   se sortea **por Persona** con semilla determinista a partir de su id, de modo que el
   análisis puede recalcularla sin guardarla. Con 1.000 Personas y 4 opciones quedan
   ~250 por condición.
   La métrica es, por ítem, **la proporción de Personas que responden exactamente la letra
   que les tocó**, contra el 1/n_op esperado por azar. Esa diferencia es el tamaño del
   efecto del formato, ítem a ítem. `analizar_ancla.py` la calcula.
3. **Re-examinar lo publicado** con la misma métrica sobre las plantillas históricas,
   empezando por Ikuspegi.

## Por qué esto mejora el paper en vez de hundirlo

Un panel sintético cuya respuesta depende de una letra de ejemplo no es un panel: es un
eco del prompt. Pero eso, medido y cuantificado, es una contribución metodológica que
nadie ha reportado — y explica por qué algunos benchmarks de fidelidad salen bien.
Encaja como tercer modo de fallo junto al techo de información y al colapso de varianza,
y da una recomendación accionable para cualquiera que monte un panel sintético:
**aleatorizar el formato por respondente y reportar el efecto del ancla como control.**
