# Preregistro — experimentos de robustez (huecos 2, 3 y 6)

**Escrito el 2026-08-21, ANTES de lanzar ninguna tanda.** Mismo procedimiento que funcionó en la
17ª sesión con el panel v2: fijar las predicciones por escrito para que el resultado no se pueda
racionalizar después.

**Compromiso:** se reportan las cuatro métricas para las tres variantes, salgan como salgan, y este
fichero no se edita después de lanzar. Las conclusiones van en `resultados/robustez.md`.

---

## Diseño

Las mismas **13 preguntas** de Ikuspegi 2025, el mismo **panel v1** (`pv_agentes.json`, 1.000
Personas), el mismo motor y el mismo parseo. **Sólo cambia una cosa por tanda.**

| exp | hueco | qué cambia | comando |
|---|---|---|---|
| `modelo` | 2 | Haiku 4.5 → modelo frontera | `python lanzar_robustez.py --exp modelo --modelo claude-opus-5` |
| `prompt` | 3 | instrucciones anti-concentración | `python lanzar_robustez.py --exp prompt` |
| `temp` | 6 | `temperature` explícita a 0.0 | `python lanzar_robustez.py --exp temp --temperature 0.0` |

### Métricas, fijadas de antemano

Sólo estas cuatro, y en este orden de importancia. No se añadirán otras después de ver los datos.

1. **Concentración de la opción modal** — *la métrica principal.* Es la operacionalización directa
   de la Proposición 2.
2. **DAM** agregado.
3. **% NS-NC**.
4. **Nº medio de opciones distintas usadas por pregunta.**

### Referencias

| | DAM | concentración | NS-NC | opciones/preg. |
|---|--:|--:|--:|--:|
| **v1 · Haiku (referencia)** | **15,7** | **83,7** | **1,4** | **4,3** |
| v2 · Haiku (perfil enriquecido) | 18,2 | 88,8 | 0,9 | 2,7 |
| Baseline moda | 17,0 | — | — | — |
| Baseline uniforme | 19,7 | — | — | — |
| Suelo de ruido (panel perfecto) | 0,8 | — | — | — |
| **REAL (Ikuspegi, n=600)** | — | **61,5** | **3,4** | — |

---

## Hueco 2 · Modelo frontera

**Razonamiento previo.** La tesis del paper sostiene que el techo es **informacional** y que el
colapso de varianza es una propiedad de la generación condicionada a persona, no de la capacidad del
modelo. La literatura apoya la invariancia: Argyle et al. usaron GPT-3, Bisbee et al. GPT-3.5/4,
Wang/Park GPT-4o, y los sesgos persisten en todos. Si eso es cierto, un modelo frontera puede
mejorar el seguimiento de instrucciones y el formato, pero no debe recuperar la varianza.

| # | Predicción | Rango |
|---|---|---|
| H2.1 | El DAM **no mejora de forma relevante** | 14,0 – 17,5 |
| H2.2 | La concentración **sigue muy por encima del 61,5 real** | 76 – 88 |
| H2.3 | Las dos opciones "cero de mil" siguen prácticamente vacías: P11 *"permitir la entrada sin ningún obstáculo legal"* (real 34,2 %) y P13 *"acoger sin restricciones"* (real 31,3 %) | < 3 % ambas |
| H2.4 | La dirección seguirá siendo correcta (P8f: Vox > PP > PNV > EH Bildu) | se mantiene |

**Qué falsaría la tesis:** concentración **< 70** y DAM **< 12**. Si eso ocurre, el colapso es
dependiente del modelo, la Proposición 2 hay que reescribirla y el paper cambia de tesis: pasaría a
ser *"los modelos pequeños colapsan y los grandes no"*, que sigue siendo publicable pero es otro
artículo.

**Resultado más incómodo posible:** que mejore *algo* pero no lo bastante — concentración 72-76.
Entonces habría que reportar una mejora parcial y matizar la afirmación de invariancia al modelo.
Se reportará tal cual, sin redondear a favor.

---

## Hueco 3 · Prompt anti-concentración

**El prompt** (en `lanzar_robustez.py`, constante `PROMPT_ANTICONC`) ataca los tres mecanismos
observados: legitima explícitamente las posturas minoritarias y los extremos de escala, prohíbe
refugiarse en la opción intermedia "por descarte", y declara NS/NC como respuesta válida.

⚠ **No dice en ningún momento cuál es la distribución real ni cuántas opciones usar.** Hacerlo
sería filtrar la respuesta y el experimento no valdría nada. Esto hay que declararlo en el paper.

| # | Predicción | Rango |
|---|---|---|
| H3.1 | El **NS-NC sube** hacia el 3,4 % real. Es lo más fácil de mover porque se autoriza de forma explícita | 2,5 – 5,0 |
| H3.2 | La concentración **baja pero no llega al 61,5 real** | 70 – 80 |
| H3.3 | El DAM mejora **poco**, y puede seguir sin batir con holgura al baseline de la moda (17,0) | 13,0 – 16,0 |
| H3.4 | Las opciones usadas por pregunta **suben** desde 4,3 | 4,8 – 6,0 |
| H3.5 | Las opciones "cero de mil" **se despegan del cero pero siguen muy por debajo del real** | 3 – 15 % (real 34,2 y 31,3) |

**Qué falsaría la tesis:** concentración ≈ 62 y DAM ≈ 8. Sería la evidencia de que el colapso es un
artefacto del prompt por defecto y es corregible. La Proposición 2 tendría que reformularse como
*"el prompting estándar induce colapso, y es evitable"*, lo cual **también es un buen paper** — pero
uno con una recomendación práctica en vez de un límite.

**Predicción sobre la interpretación:** aunque baje la concentración, espero que el **Δ vs moda a
nivel individual siga siendo ≈ 0 o negativo**, porque repartir mejor la varianza no crea información
donde no la hay (Proposición 1). Si la concentración baja y el acuerdo individual no mejora, es la
confirmación más limpia posible de que los dos límites son independientes.

---

## Hueco 6 · Temperature

**Razonamiento previo.** Hasta ahora ninguna llamada fijaba `temperature`, así que corría al **1.0**
por defecto de la API: el escenario de **máxima varianza** disponible. Bajarla debería empeorar el
colapso, no mejorarlo.

| # | Predicción | Rango |
|---|---|---|
| H6.1 | Con `temperature=0.0` la concentración **sube** respecto a 83,7 | 86 – 95 |
| H6.2 | El DAM **empeora** respecto a 15,7 | 16 – 20 |
| H6.3 | Las opciones usadas por pregunta **bajan** desde 4,3 | 2,5 – 4,0 |

**Para qué sirve:** cierra de antemano la objeción *"¿no será que estáis usando decodificación
codiciosa?"*. Si T=0 empeora y T=1 (por defecto) ya colapsa, el colapso no es de decodificación.

---

## Riesgos metodológicos declarados

- **Comparaciones múltiples.** Tres variantes × cuatro métricas = 12 contrastes. No se aplicará
  corrección formal porque no hay contraste de hipótesis nulas al uso, pero **las métricas y los
  rangos están fijados aquí** para evitar el jardín de senderos que se bifurcan.
- **El piloto de 13 preguntas está sesgado a favor del panel** (5 de 12 son política migratoria, su
  mejor bloque). Ya declarado en la 17ª sesión. Cualquier mejora observada es, por tanto, un techo
  optimista.
- **Una sola tanda por variante.** No hay repeticiones, así que no se puede separar el efecto del
  ruido de muestreo del LLM. Con n=1.000 el error de la concentración es pequeño, pero conviene no
  interpretar diferencias de menos de ~2 p.p.
- **Coste.** La tanda de Haiku costó 0,2-0,3 $. Un modelo frontera está uno o dos órdenes de
  magnitud por encima. **Lanzar primero `--muestra 30`** y comprobar que el formato se parsea antes
  de gastar las 1.000.

---

## Predicciones de David

**Registradas el 2026-08-22, antes de lanzar las tandas de 1.000.** Literales, sin editar. Las
observaciones que le hice antes de registrarlas están debajo, y **David decidió mantener sus cifras
tal cual**, que es lo correcto: un preregistro que se retoca tras la crítica ya no es un preregistro.

| # | Experimento | Métrica | Predicción | Razonamiento de David |
|---|---|---|--:|---|
| D2.1 | Hueco 2 · Opus n=1.000 | DAM | 22 | |
| D2.2 | Hueco 2 · Opus n=1.000 | Concentración | 62 | se mantiene |
| D2.3 | Hueco 2 · Opus n=1.000 | NS-NC % | 2 | debería haber algo |
| D2.4 | Hueco 2 · Opus n=1.000 | Opciones/pregunta | 1 | debería bajar al aumentar el n |
| D2.5 | Hueco 2 · Opus n=1.000 | P11 "sin obstáculo legal" (real 34,2) | 40 | |
| D2.6 | Hueco 2 · Opus n=1.000 | P13 "sin restricciones" (real 31,3) | 35 | |
| D3.1 | Hueco 3 · prompt anti-conc. | DAM | 18 | |
| D3.2 | Hueco 3 · prompt anti-conc. | Concentración | 58 | disminuye |
| D3.3 | Hueco 3 · prompt anti-conc. | NS-NC % | 2 | |
| D3.4 | Hueco 3 · prompt anti-conc. | Opciones/pregunta | 1,1 | |
| D3.5 | Hueco 3 · prompt anti-conc. | P11 (real 34,2) | 34 | |
| D3.6 | Hueco 3 · prompt anti-conc. | P13 (real 31,3) | 31 | |
| D6.1 | Hueco 6 · temperature 0.0 | DAM | 15 | |
| D6.2 | Hueco 6 · temperature 0.0 | Concentración | 90 | |
| D6.3 | Hueco 6 · temperature 0.0 | NS-NC % | 5 | |
| D6.4 | Hueco 6 · temperature 0.0 | Opciones/pregunta | 3 | |

**Criterio de falsación de David:** *"que la DAM baje de 10, que la concentración sea menor a 50,
que la NS-NC % sea 0"*.

### Observaciones formuladas ANTES de lanzar (Claude, 2026-08-22)

Se dejan constancia aquí porque afectan a cómo hay que leer el contraste, no para corregir nada.

1. **D2.4 y D3.4 (opciones/pregunta = 1 y 1,1) predicen algo casi imposible con la métrica tal como
   está definida.** La métrica cuenta cuántas opciones reciben **al menos un voto**, así que **crece
   con N**: con Haiku fue 3,2 con n=30 y 4,3 con n=1.000. El razonamiento anotado ("debería bajar al
   aumentar el n") supone lo contrario. Un valor de 1 exigiría que las 1.000 Personas eligieran
   exactamente la misma opción en las trece preguntas. **Estas dos predicciones fallarán casi con
   seguridad, y el fallo será de la métrica elegida, no del juicio sustantivo.**
   ▸ *Métrica alternativa sugerida y no adoptada:* número **efectivo** de opciones (inverso del
   índice de Herfindahl sobre las cuotas), que sí decrece cuando la masa se concentra y sería lo que
   David parece tener en mente. Si interesa, se puede calcular *a posteriori* sobre las mismas
   tandas, declarándola explícitamente como métrica exploratoria añadida después.
2. **Las predicciones del hueco 2 son mutuamente inconsistentes.** D2.2 (concentración 62 ≈ el 61,5
   real), D2.5 (40, por encima del 34,2 real) y D2.6 (35, por encima del 31,3 real) describen un
   panel que reproduce la distribución real casi exactamente; pero D2.1 predice un DAM de **22**,
   peor que Haiku (15,7) y peor que el baseline de la moda (17,0). Si la distribución coincide, el
   DAM es bajo por construcción. **Al menos una de las dos tiene que fallar.**
3. **La tercera condición de falsación de David va en dirección contraria a la prevista.** Un
   NS-NC de **0** es el panel negándose a usar "no sé", lo cual **confirma** el colapso en lugar de
   falsarlo — y ya se observó en el piloto de Opus n=30 (0,0 %). Tomada al pie de la letra, la tesis
   ya estaría falsada por un resultado que la respalda. Se registra tal cual; al evaluar se
   interpretará junto con las otras dos condiciones (DAM < 10 y concentración < 50), que sí apuntan
   en la dirección correcta.

**Valor de estas discrepancias.** Que dos preregistros independientes difieran tanto —Claude predice
que el frontera no arregla nada, David que lo arregla casi del todo— hace el contraste mucho más
informativo que si ambos hubiéramos apostado por lo mismo. Sea cual sea el resultado, alguien se
equivoca de forma medible.

---

## Bitácora de ejecución

▸ *Rellenar después de cada tanda. No modificar nada de lo anterior.*

| fecha | exp | modelo | n | vacías | DAM | conc. | NS-NC | opc./preg. | fichero | válida |
|---|---|---|--:|--:|--:|--:|--:|--:|---|---|
| 2026-08-21 | modelo | claude-opus-5 | 30 | **50 %** | 14,2 | 80,0 | 0,0 | 2,6 | `encuesta_2026-08-21_224759.json` | ⛔ **NO** |
| 2026-08-21 | modelo | claude-opus-5 | 30 | **70 %** | — | — | — | — | `encuesta_2026-08-21_225546.json` | ⛔ **NO** |
| 2026-08-21 | modelo | claude-opus-5 | 30 | **70 %** | — | — | — | — | `encuesta_2026-08-21_230138.json` | ⛔ **NO** — `errores: {}` → destapó la causa real |
| 2026-08-21 | modelo | claude-opus-5 | 30 | **0 %** | **12,9** | **76,4** | **0,0** | **2,8** | `encuesta_2026-08-21_230548.json` | ✅ **SÍ** (piloto) |

---

## ★ RESULTADOS DEFINITIVOS — las tres tandas de 1.000 (2026-08-22)

Las tres válidas, **0 % de Personas vacías** en las tres.

| tanda | DAM | concentración | NS-NC % | opciones/preg. | nº efectivo | P11 extremo | P13 extremo | fichero |
|---|--:|--:|--:|--:|--:|--:|--:|---|
| **v1 · Haiku (referencia)** | 15,7 | 83,7 | 1,4 | 4,3 | 1,66 | **0,0** | **0,0** | `..._2026-08-08_101241` |
| **Hueco 3 · prompt anti-conc.** | 14,8 | **79,4** | 2,0 | 4,5 | 1,73 | **0,0** | **0,0** | `..._2026-08-22_111025` |
| **Hueco 6 · temperature 0.0** | 15,8 | 84,1 | 1,1 | 4,2 | 1,64 | **0,0** | **0,0** | `..._2026-08-22_111207` |
| **Hueco 2 · Opus 5** | **11,8** | **75,0** | **0,0** | 3,6 | 2,03 | **3,0** | **7,8** | `..._2026-08-22_112821` |
| *Baseline moda* | 17,0 | — | — | — | — | — | — | |
| **REAL (Ikuspegi)** | — | **61,5** | **3,4** | — | — | **34,2** | **31,3** | |

*P11 = "permitir la entrada sin ningún obstáculo legal" · P13 = "acogerlas sin restricciones".*
*Nº efectivo = 1/Herfindahl sobre las cuotas; **métrica exploratoria añadida a posteriori**, es la
que David tenía en mente en D2.4/D3.4 y no la que estaba definida. Se declara como tal.*

### Contraste con lo preregistrado — Claude

| # | Rango | Observado | |
|---|---|--:|---|
| H2.1 DAM | 14,0 – 17,5 | **11,8** | ❌ falla, mejora mucho más de lo previsto |
| H2.2 Concentración | 76 – 88 | **75,0** | ❌ falla por 1 punto |
| H2.3 Extremos < 3 % | < 3 % ambas | 3,0 y **7,8** | ❌ falla; P11 en el borde, P13 claramente fuera |
| H2.4 Dirección se mantiene | — | sí, **reforzada** | ✅ acierta |
| H3.1 NS-NC | 2,5 – 5,0 | **2,0** | ❌ falla por poco |
| H3.2 Concentración | 70 – 80 | **79,4** | ✅ acierta |
| H3.3 DAM | 13,0 – 16,0 | **14,8** | ✅ acierta |
| H3.4 Opciones/preg. | 4,8 – 6,0 | **4,5** | ❌ falla por poco |
| H3.5 Extremos 3-15 % | 3 – 15 % | **0,0 y 0,0** | ❌ falla de pleno |
| H6.1 Concentración | 86 – 95 | **84,1** | ❌ falla por poco |
| H6.2 DAM | 16 – 20 | **15,8** | ❌ falla por poco |
| H6.3 Opciones/preg. | 2,5 – 4,0 | **4,2** | ❌ falla por poco |

**3 aciertos claros de 12.** El patrón de los fallos es sistemático y hay que decirlo: **subestimé
al modelo frontera y sobreestimé el efecto de la temperature.**

**Criterio de falsación de Claude** (concentración < 70 **y** DAM < 12): DAM 11,8 **sí**,
concentración 75,0 **no**. Se cumple una de las dos → **la tesis NO queda falsada**, pero éste es
literalmente el *"resultado más incómodo posible"* que dejé escrito antes de lanzar: mejora
sustancial pero insuficiente. Toca reportarlo como tal y matizar la invariancia al modelo.

### Contraste con lo preregistrado — David

| # | Predicción | Observado | |
|---|--:|--:|---|
| D2.1 DAM | 22 | 11,8 | ❌ |
| D2.2 Concentración | 62 | 75,0 | ❌ |
| D2.3 NS-NC | 2 | 0,0 | ❌ |
| D2.4 Opciones/preg. | 1 | 3,6 | ❌ *(fallo de métrica, ya anticipado)* |
| D2.5 P11 | 40 | 3,0 | ❌ |
| D2.6 P13 | 35 | 7,8 | ❌ |
| D3.1 DAM | 18 | 14,8 | ❌ |
| D3.2 Concentración | 58 | 79,4 | ❌ |
| **D3.3 NS-NC** | **2** | **2,0** | ✅ **exacto** |
| D3.4 Opciones/preg. | 1,1 | 4,5 | ❌ *(fallo de métrica)* |
| D3.5 P11 | 34 | 0,0 | ❌ |
| D3.6 P13 | 31 | 0,0 | ❌ |
| **D6.1 DAM** | **15** | **15,8** | ✅ prácticamente exacto |
| D6.2 Concentración | 90 | 84,1 | ❌ por poco |
| D6.3 NS-NC | 5 | 1,1 | ❌ |
| D6.4 Opciones/preg. | 3 | 4,2 | ❌ |

**La hipótesis central de David —que el modelo frontera corrige el colapso— queda refutada:**
concentración 75,0 frente a su 62, y extremos en 3,0 y 7,8 frente a sus 40 y 35.

**Criterio de falsación de David:** DAM < 10 **no** (11,8) · concentración < 50 **no** (75,0) ·
NS-NC = 0 **sí** (Opus da 0,0). Se cumple sólo la condición que se había señalado *antes de lanzar*
como orientada al revés: un NS-NC de cero confirma el colapso, no lo falsa. Con las otras dos, la
tesis se sostiene.

### ✅ HUECOS 2, 3 y 6 CERRADOS (2026-08-22)

Los tres experimentos están hechos con n=1.000 y son válidos. **Decisión: no se harán más tandas.**
El seguimiento del hueco 3 a nivel individual está en `preregistro_anticonc_individual.md` y resultó
**inconcluyente por manipulación débil** — el prompt apenas transporta al Deustobarómetro.

### Los cuatro hallazgos

**1 · La temperature no hace absolutamente nada.** 15,8 / 84,1 / 1,1 / 4,2 frente a la referencia
15,7 / 83,7 / 1,4 / 4,3: diferencias de décimas en las cuatro métricas, y los extremos siguen en
0,0. **El hueco 6 queda cerrado de forma más limpia de lo previsto:** no es que la decodificación
codiciosa empeore el colapso, es que **la temperature es irrelevante**. La objeción "¿no será que
usáis greedy decoding?" queda muerta.

**2 · El prompt mueve el centro pero no toca los polos.** Se le dice explícitamente que las
posturas minoritarias y los extremos de escala son legítimos, y el modelo **redistribuye masa entre
las opciones moderadas** — en P11, de 12,1/85,9 pasa a 39,6/58,0 — bajando la concentración a 79,4
y subiendo el NS-NC a 2,0. **Pero las dos opciones extremas siguen exactamente en 0,0 %.**
Es el resultado más elegante de los tres: *se le da permiso explícito para usar los polos y no los
usa*. El colapso no es un artefacto del prompt por defecto.

**3 · Opus sí despega los polos del cero, por primera vez en todo el proyecto — pero poco.**
P11 0,0 → **3,0** (real 34,2) y P13 0,0 → **7,8** (real 31,3): recupera en torno al **9 %** y al
**25 %** de la masa polar. Y simultáneamente **arrasa la cola con más saña que Haiku**: "prohibir
por completo" 2,0 → 0,0 · "acoger hasta un número limitado" 0,8 → 0,1 · "no acogerlas en ningún
caso" 0,7 → 0,0. Usa **menos** opciones (3,6 vs 4,3) pero mejor calibradas entre las dominantes
(nº efectivo 2,03 vs 1,66). **Caracterización precisa: el modelo frontera mejora el reparto entre
las opciones mayoritarias y elimina la cola todavía más.**

**4 · La dirección se refuerza con Opus.** Acuerdo con la expulsión por delito, por voto:

| | Vox | PP | PSE | PNV | EH Bildu | Podemos |
|---|--:|--:|--:|--:|--:|--:|
| Haiku | 91 % | 66 % | 18 % | 18 % | 6 % | 0 % |
| **Opus** | **100 %** | **91 %** | **38 %** | **41 %** | **17 %** | **3 %** |

El gradiente político es más pronunciado, no menos. **H2.4 confirmada:** el modelo usa el perfil, y
el modelo mejor lo usa más.

### Qué cambia en el paper

- **Hay que matizar la invariancia al modelo.** El DAM de Opus (11,8) es **el mejor número que ha
  producido el proyecto** y bate al baseline de la moda por 5,2 puntos. No se puede seguir diciendo
  que el modelo no importa: importa, y bastante.
- **La Proposición 2 sobrevive con una formulación más fina.** El colapso **se atenúa** con la
  capacidad del modelo pero **no desaparece**: concentración 75,0 frente al 61,5 real (+13,5 de
  exceso), NS-NC **peor** que con Haiku (0,0 vs 1,4), y los polos siguen borrados en un 91 % y un
  75 %.
- **Las tres intervenciones fallan en cosas distintas, y eso es un resultado de diseño fuerte:**
  temperature no hace nada · el prompt sólo mueve el centro · el modelo despega los polos un poco y
  destruye la cola aún más. Ninguna de las tres recupera la varianza.
- **Limitación a declarar:** con Ikuspegi no hay microdatos, así que **no se puede contrastar la
  predicción sobre el acuerdo individual** (que la concentración baje sin que mejore el Δ vs moda).
  Ese contraste sólo es posible en el Deustobarómetro. Sigue siendo el pendiente más interesante.

---

## Resultado del piloto n=30 — hueco 2 (modelo frontera)

**Comparación pareada:** las mismas 30 Personas que la tanda de referencia de Haiku (misma semilla,
verificado 30/30 coincidentes). Sólo cambia el modelo.

| métrica | Haiku n=30 | **Opus n=30** | Haiku n=1.000 | REAL |
|---|--:|--:|--:|--:|
| DAM | 15,1 | **12,9** | 15,7 | — |
| Concentración modal | 81,7 | **76,4** | 83,7 | **61,5** |
| NS-NC % | 1,1 | **0,0** | 1,4 | **3,4** |
| Opciones usadas / pregunta | 3,2 | **2,8** | 4,3 | — |

### Contraste con lo preregistrado

| # | Predicción | Rango | Observado | |
|---|---|---|--:|---|
| H2.1 | El DAM no mejora de forma relevante | 14,0 – 17,5 | **12,9** | ❌ **FALLA** — mejora más de lo previsto |
| H2.2 | La concentración sigue muy por encima del 61,5 real | 76 – 88 | **76,4** | ✅ acierta, en el borde inferior |
| H2.3 | Las dos opciones "cero de mil" siguen vacías | < 3 % ambas | **0,0 % ambas** | ✅ **acierta de pleno** |
| H2.4 | La dirección se mantiene | — | — | ⬜ **no evaluable con n=30** (celdas de 1-6 personas) |

**Criterio de falsación (concentración < 70 **y** DAM < 12): NO se cumple.** La tesis sobrevive,
pero con una mejora parcial real que hay que reportar sin adornos.

### Lectura — el hallazgo se afina, no se cae

**El modelo frontera redistribuye masa entre las opciones centrales, pero no resucita los extremos.**

- **P11** (política de entrada): la concentración cae de 83,3 a **50,0** y el DAM de 27,8 a 16,6 —
  Opus reparte 50/50 entre dos opciones donde Haiku ponía 83/12. Mejora sustancial.
  **Pero "permitir la entrada sin ningún obstáculo legal" sigue en 0,0 % frente al 34,2 % real.**
- **P13** (asilo y refugio): **empeora**. Concentración 96,7 → **100,0**: las 30 Personas eligen la
  misma opción. "Acogerlas sin restricciones" sigue en **0,0 % frente al 31,3 % real**.
- **NS-NC baja a 0,0 %** (real 3,4 %) y las opciones distintas usadas bajan de 3,2 a 2,8: en dos de
  las cuatro métricas, el modelo frontera va **a peor**.
- El DAM sólo mejora en **5 de 12** preguntas.

**Formulación precisa para el paper:** el colapso de varianza no es una compresión uniforme hacia el
centro que un modelo mejor pueda deshacer. Es específicamente **la borradura de los polos**, y ésa
sobrevive intacta al cambio de modelo. La mejora del DAM viene de repartir mejor entre opciones
moderadas, que es justo lo que *no* hace falta para las tareas que dependen de la heterogeneidad.

### Cautelas antes de sacar conclusiones

1. **Es n=30.** Los rangos preregistrados se escribieron para n=1.000. La propia referencia de Haiku
   difiere entre tamaños (DAM 15,1 vs 15,7 · concentración 81,7 vs 83,7), así que ±1 punto es ruido
   esperable.
2. **La concentración SUBE con N** en la serie de Haiku (81,7 → 83,7). Si eso se repite, Opus a
   n=1.000 saldrá peor que este 76,4. **No dar por bueno el resultado hasta la tanda completa.**
3. H2.1 falló. Se reporta como fallo, no se reinterpreta el rango a posteriori.
### Incidencia — tres tandas descartadas antes de dar con la causa

Las tres primeras pruebas de 30 Personas con el modelo frontera devolvieron **50 %, 70 % y 70 % de
Personas vacías**; las de referencia tuvieron 0 %. Ninguna es válida y sus métricas no deben
citarse: estaban calculadas sobre las supervivientes, autoseleccionadas por el propio fallo.

**Causa real:** una línea de `server.py` leía **sólo el primer bloque** de la respuesta de la API:

```python
return (data.get('content') or [{}])[0].get('text', '').strip()
```

Un modelo con razonamiento devuelve primero un bloque `thinking` y el texto en un bloque posterior,
así que `content[0]['text']` era cadena vacía. Con Haiku nunca se notó porque no emite bloque de
razonamiento: `content[0]` *era* el texto.

Encaja con todo lo observado: fallaba ~70 % pero no el 100 % (el modelo razona antes de contestar
sólo en algunas Personas), no había ningún error HTTP que registrar (**`errores: {}`**),
`raw_sin_parsear` era 0, y empeoraba al bajar hilos y añadir reintentos porque nunca fue un problema
de red.

**Arreglado, y verificado con la cuarta tanda (0 % de vacías, 30/30 con las 13 respuestas):**

1. Se concatenan **todos** los bloques de tipo `text`. Probado sobre respuestas simuladas de los
   cuatro tipos posibles.
2. **`max_tokens` sube a 2.048 cuando el modelo no es Haiku:** los tokens de razonamiento cuentan
   como salida y los 130 calculados para 13 preguntas no dejaban margen.
3. Un 200 sin texto ahora se registra con `stop_reason`, tipos de bloque y `usage`.
4. `server.py` acumula el **recuento de errores por tipo** y una muestra de mensajes en el propio
   fichero de resultados (`errores`, `errores_muestra`). Fue lo que permitió descartar la API.
5. `lanzar_robustez.py` avisa si se supera el 2 % de vacías; `comparar_robustez.py` marca ⛔ esas
   tandas para que no se cuelen en la tabla.
6. Se añadieron además 8 reintentos con backoff y concurrencia adaptada al modelo (20 hilos con
   Haiku, 4 con un frontera). No eran la causa, pero son buena práctica y se quedan.
7. El mismo patrón de lectura estaba en `/api/chat` y también se corrigió.

**Las tandas de referencia no están afectadas:** todas corrieron con Haiku, que no emite bloques de
razonamiento, así que la extracción era correcta. Las cifras publicadas siguen siendo válidas.

▸ **Ninguna predicción de este preregistro se modificó** durante la incidencia.

▸ **Esto merece ir al paper.** Un artefacto de implementación que descarta el 70 % de la muestra
**sin producir ningún error** es el tipo de fallo silencioso que puede colarse en un estudio de
encuestados sintéticos. Lo que lo detectó no fue el código: fue **tener una tanda de referencia con
0 % de vacías** con la que comparar.
