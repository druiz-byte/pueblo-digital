# Diagnóstico del piloto Ikuspegi — panel v1, n=30

**Tanda:** `encuesta_2026-08-08_100747.json` · panel v1 (`pv_agentes.json`) · claude-haiku-4-5 · 13 preguntas · 30 Personas · 0 vacías, 0 sin parsear.
**Contraste completo:** `contraste_ikuspegi_piloto_n30.md`

> ⚠ **n=30.** El propio panel introduce ruido de muestreo grande. Todo lo que sigue
> es señal preliminar; el patrón de concentración es el hallazgo robusto, las cifras
> exactas de DAM no lo son.

## Los cuatro números

| Medida | DAM (p.p.) |
|---|---:|
| **Panel v1 (n=30)** | **15,1** |
| Baseline moda (todos eligen la opción más votada) | 17,0 |
| Baseline uniforme | 19,7 |
| **Suelo de ruido** — un panel *perfecto* muestreado con n=30 | **4,5** |

Dos lecturas, ambas incómodas:

- El panel bate a la moda por **1,9 p.p.** Con n=30 esa ventaja está dentro del
  ruido. **A día de hoy no hay evidencia de que el panel aporte nada sobre adivinar
  la respuesta mayoritaria.**
- Un panel perfecto con n=30 daría 4,5, no 0. El exceso atribuible al panel es
  **15,1 − 4,5 ≈ 10,6 p.p.** Ese es el error real a explicar.

Referencia: en el Deustobarómetro el panel v1 dio DAM 13,4 sobre 152 preguntas.

## El hallazgo: sobreconcentración

La Persona sintética se agolpa en una sola opción mucho más de lo que lo hace la
población real.

| Preg. | Opción top del panel | Panel % | Real % |
|---|---|---:|---:|
| P13 | "Acogerlas si se comprueba que están perseguidas" | 96,7 | 40,3 |
| P8c | Acuerdo (necesitamos inmigrantes en algunos sectores) | 93,3 | 77,9 |
| P36 | Sí, son vascos y vascas | 93,3 | 88,8 |
| P11 | "Otros requisitos legales" | 83,3 | 17,8 |
| P20 | Mismos derechos y obligaciones | 83,3 | 69,2 |
| P8n | **Indecisión** (conciliación) | 80,0 | 20,0 |
| P5 | "Son adecuadas" | 76,7 | 56,2 |
| P3 | "Son bastantes" | 73,3 | 26,8 |
| P12 | "Regularizar solo a las que tengan trabajo" | 70,0 | 44,3 |
| P22j | **Indecisión** (envejecimiento) | 70,0 | 13,0 |
| **Media** | | **81,7** | **61,5** |

**20 puntos de exceso de concentración.** El panel no reproduce la dispersión de
opiniones: colapsa. Es la misma patología que vimos en el Deustobarómetro con p18
("Regular" 86 %), ahora medida limpiamente en un cuestionario nuevo.

Síntoma asociado: **NS/NC = 0,0 % en las 13 preguntas** (el real va del 1,1 % al
10,0 %). La Persona sintética siempre tiene opinión.

Y en la escala 0-10 (P26) el 80 % de las Personas se sitúa en 5 o 6. Media panel
4,83 vs real 5,30.

## El sesgo: el panel imagina una sociedad vasca menos abierta de lo que es

Las dos peores preguntas son las dos afirmaciones *positivas* sobre inmigración,
y el panel falla igual en ambas: se refugia en "ni acuerdo ni desacuerdo" donde
la sociedad vasca real está mayoritariamente de acuerdo.

| | Panel acuerdo | Real acuerdo | Panel indecisión | Real indecisión |
|---|---:|---:|---:|---:|
| P8n conciliación familiar y laboral | 13,3 | **70,2** | 80,0 | 20,0 |
| P22j solución al envejecimiento | 16,7 | **73,7** | 70,0 | 13,0 |

Y en las preguntas de política migratoria el panel evita sistemáticamente la
posición comprometida y elige la opción cualificada:

| | Panel | Real |
|---|---:|---:|
| P11 "Permitir la entrada sin ningún obstáculo legal" | **0,0** | 34,2 |
| P12 "Regularizarlas a todas" | 6,7 | 41,5 |
| P13 "Acogerlas sin restricciones" | **0,0** | 31,3 |

Tres opciones que un tercio o más de la población vasca respalda, y por las que
**ninguna o casi ninguna** de las 30 Personas se decanta.

Esto no es solo ruido de muestreo: son las tres opciones más comprometidas del
cuestionario y las tres caen a cero a la vez. Es el patrón de aplanamiento y
moderación que la literatura de *perils* describe para las Personas LLM, aquí con
una consecuencia sustantiva concreta: **el panel retrata a Euskadi como más tibia
ante la inmigración de lo que el dato real muestra que es.**

## Dónde acierta (y por qué no cuenta mucho)

P36 (3,0), P6 (5,0), P5 (6,8), P8c (7,7): las cuatro preguntas de consenso
abrumador, donde el real ya está en 78-90 % sobre una opción. Ahí acertar es
barato — el baseline de la moda también acierta. La prueba: P6 tiene DAM 5,0 en
el panel y 5,0 en el baseline de la moda. Exactamente lo mismo.

## Siguiente paso

1. **Lanzar las 1.000** (`python lanzar_ikuspegi.py`, ~0,2 $, ~4 min). Baja el
   suelo de ruido de 4,5 a **0,8 p.p.** y convierte estas señales en cifras
   defendibles. Hazlo **sin tocar el prompt**: es la línea base honesta.
2. Con el resultado en mano, decidir si merece la pena una variante de prompt que
   ataque la sobreconcentración (p. ej. instrucción explícita de que NS/NC y las
   posiciones minoritarias son respuestas legítimas). **Si la variante mejora, es
   material del artículo, no una corrección**: mide cuánta de la infidelidad es
   del anclaje sociodemográfico y cuánta del comportamiento del modelo.
3. Sigue pendiente P8a/P22i: la ambigüedad de lectura del Gráfico 28 documentada
   en `verificacion_datos_reales.md`.
