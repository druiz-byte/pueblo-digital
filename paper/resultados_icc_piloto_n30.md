# Resultados — piloto ICC (CIS 3575), n=30, panel v2, Haiku

Tandas `entrevista/resultados/encuesta_2026-09-22_113350.json` (versión A) y
`encuesta_2026-09-22_113408.json` (versión B). 30/30 Personas, 0 vacías, 0 sin parsear.
Preregistro: `preregistro_icc_cis3575.md`. **n=30: direcciones sí, magnitudes no.**

## Marcador del preregistro

| | predicción | resultado | veredicto |
|---|---|---|---|
| H1 | "Igual" < 15 % en P3 | **96,7 %** | **REFUTADA** (falsación ≥40 % cumplida) |
| H2 | \|Δ A−B\| < 8 p.p. en el reparto Mejor/Peor | **61,5 / 32,1 / 18,8** | **REFUTADA** (falsación ≥20 en 2 de 3) |
| H3 | DAM(P17) < DAM(P8) | 14,9 < 20,0 | ✔ confirmada |
| H4 | P18 "No" ≥ 97 % | 100,0 % | ✔ confirmada |
| H5 | P15 "Más" ≥ 90 % | **"Menos" 86,7 %** | **REFUTADA, en dirección opuesta** |
| H6 | concentración ≥ 85 % | 81,9 (real CAE 64,5) | parcial: excede al real, no llega al umbral |

Tres de seis refutadas. Las tres refutaciones valen más que las tres confirmaciones.

## H1 — la explicación del "centro vacío" no se sostiene

El 2026-09-22, en la pregunta de impuestos del CIS, la categoría central se quedó en
**0,0 %** (real 47,7 %) y se formuló como que el punto medio es conducta de respuesta
—satisficing, ambivalencia— que un simulador de actitudes no puede generar.

Aquí, con la misma familia de instrumento, ocurre lo contrario: **"Igual" se lleva el
96,7 % en P3** (real CAE 62,8 %), 76,7 % en P12 y 63,3 % en P8.

**El panel no evita el centro ni lo busca: colapsa sobre una casilla, y cuál sea depende
del ítem.** Con impuestos la casilla dominante del discurso es "mucho"; con la situación
del propio hogar a seis meses es "igual". La regla que sobrevive es la concentración,
no una dirección. La hipótesis del satisficing queda retirada como explicación general
y se reporta como refutada por este piloto, no se reescribe.

## H2 — el hallazgo principal: sin casilla intermedia no hay posición, hay abdicación

| | A: con "Igual" | B: sin "Igual" | REAL CAE (sin "Igual" ofrecida) |
|---|---|---|---|
| P3 | Igual 96,7 · Peor 3,3 | **NS/NC 56,7** · Mejor 26,7 · Peor 16,7 | Igual 62,8 · Peor 20,5 · Mejor 16,0 · NS/NC 0,6 |
| P12 | Igual 76,7 · Peor 13,3 · Mejor 10,0 | Mejor 50,0 · **NS/NC 33,3** · Peor 16,7 | Igual 44,4 · Mejor 31,2 · Peor 23,6 · NS/NC 0,8 |
| P8 | Igual 63,3 · Peor 33,3 · NS 3,3 | **NS/NC 46,7** · Peor 43,3 · Mejor 10,0 | Peor 41,8 · Mejor 31,4 · Igual 23,3 · NS/NC 3,6 |

El entrevistado real, **sin que se le ofrezca la casilla**, produce "Igual"
espontáneamente en el 62,8 % de los casos: es una respuesta sustantiva ("mi situación
sigue como estaba"). La Persona LLM, ante el mismo estímulo, produce **"No lo sé"** en
el 56,7 % (real 0,6 %).

Los dos se niegan a elegir polo, pero por razones opuestas: **el humano afirma una
posición intermedia; el modelo abdica de la pregunta.** Lo que falta en el panel no es
varianza: es posición. Cuando existe la casilla de mínimo compromiso, la ocupa; cuando
no existe, se refugia en el no-sabe.

Consecuencia operativa, y es la que debe ir al paper: **retirar una casilla de la lista
mueve el reparto Mejor/Peor 61,5 puntos en P3.** El resultado del panel depende más del
diseño del instrumento que de quién sea la Persona. Para segmentación o conjoint, donde
el diseño de las listas de niveles es el método, esto es descalificatorio por sí solo.

## H5 — error de dirección, no de concentración: P15

Enunciado: *"El crecimiento de los precios en España durante este último año ha sido del
3,2 %. ¿Crees que los precios crecerán durante el próximo año más, menos o igual?"*

| | Más | Igual | Menos | NS/NC |
|---|--:|--:|--:|--:|
| panel | 6,7 | 0,0 | **86,7** | 6,7 |
| real CAE | **69,3** | 23,4 | 4,9 | 2,4 |

**DAM 43,0** — el peor valor por ítem de todo el proyecto. No es compresión: es inversión.

Mecanismo propuesto (a contrastar con las 1.000): el enunciado entrega un ancla numérica
y el modelo la trata como un problema de razonamiento — "3,2 % es una inflación alta,
lo esperable es que se modere" — en vez de responder como responde un ciudadano, que
extrapola su experiencia de precios al alza. **El modelo razona sobre la pregunta en
lugar de contestarla como la persona.** Es un modo de fallo distinto del colapso de
varianza y merece nombre propio en la sección de resultados.

## H3 y H4 — el panel acierta donde no hay nada que saber

| ítem | techo corr_max | DAM vs CAE |
|---|--:|--:|
| P18 intención de compra de vivienda | 0,289 | **4,0** (panel: "No" 100,0) |
| P10 bienes duraderos | 0,252 | 13,4 |
| P17 precio de la vivienda | **0,041** | 14,9 |
| P8 economía española | **0,468** | **20,0** |
| P15 inflación | 0,202 | 43,0 |

El orden del DAM es prácticamente el inverso del orden del techo. El mejor DAM del
piloto (P18, 4,0) se obtiene emitiendo una sola respuesta para las 30 Personas. El peor
de los ítems no invertidos (P8, 20,0) es justo donde el perfil más informa. **Confirma
H3: el acierto agregado del panel es independiente de la información disponible en el
perfil — mide coincidencia con el tópico, no capacidad predictiva.**

## Incidencia técnica a corregir antes de las 1.000

`server.py:247` construye el ejemplo de formato con `chr(66 + (i+j) % 4)`, sin mirar
cuántas opciones tiene la pregunta. En este piloto ha mostrado **letras inexistentes**:
P17 de la versión A (ejemplo `4:E`, letras válidas A-D) y P8 de la versión B
(ejemplo `3:D`, letras válidas A-C). No parece haber arrastrado — P17 respondió A al
90 % — y el ancla de formato ya quedó descartada experimentalmente con el test de
rotación de opciones, pero es un defecto del instrumento y debe acotarse al número real
de opciones antes de lanzar las tandas grandes.

## Pendiente

1. Corregir el ejemplo fuera de rango.
2. Relanzar A y B con **n=1.000** y las mismas Personas. En la serie de Haiku la
   concentración sube con N, así que las magnitudes se moverán; las direcciones no.
3. V de Cramér respuesta × (ideología, ingresos, edad, tenencia de vivienda) en A, para
   saber si en este dominio el panel usa el perfil (Ikuspegi: V(voto)=0,36) o no lo usa
   en absoluto (impuestos: V=0 por varianza nula).
4. Repetir P15 sin el ancla numérica del enunciado, para aislar el mecanismo de la
   inversión.
