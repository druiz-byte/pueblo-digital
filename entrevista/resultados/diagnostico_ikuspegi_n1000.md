# Réplica del Barómetro Ikuspegi 2025 con el panel v1 — n=1.000

**Tanda:** `encuesta_2026-08-08_101241.json` · panel v1 (`pv_agentes.json`) · claude-haiku-4-5 · 13 preguntas × 1.000 Personas · 0 vacías, 0 sin parsear.
**Contraste completo:** `contraste_ikuspegi_piloto_n1000.md` · **Piloto previo (n=30):** `diagnostico_ikuspegi_n30.md`

---

## 1. El resultado en cuatro cifras

| Medida | DAM (p.p.) |
|---|---:|
| **Panel v1 (n=1.000)** | **15,7** |
| Baseline moda (todos eligen la opción más votada del real) | 17,0 |
| Baseline uniforme | 19,7 |
| Suelo de ruido (panel *perfecto* con n=1.000) | 0,8 |

**El panel gana 1,3 p.p. al baseline de la moda.** Sobre un suelo de 0,8, el error
atribuible al panel es **14,9 p.p.**

Y no es que n=30 fuera pesimista: **el resultado empeora al escalar** (15,1 → 15,7).
El piloto pequeño fue afortunado, no injusto. La cifra de referencia del proyecto
(Deustobarómetro, panel v1: DAM 13,4) queda confirmada como el orden de magnitud
del método, no como un mal día.

Además, el panel **acierta la moda en 8 de 12 preguntas**: en las 4 restantes, el
baseline tonto de la moda sería literalmente mejor que el panel.

## 2. El mecanismo: sobreconcentración

| | Panel | Real |
|---|---:|---:|
| % medio de la opción más votada | **83,7** | **61,5** |
| NS/NC medio | 1,4 | 3,4 |

**22 puntos de exceso de concentración.** Y sube con N (81,7 con n=30 → 83,7 con
n=1.000): no es ruido de muestra pequeña, es el comportamiento estable del modelo.

| Preg. | Opción top del panel | Panel % | Real % |
|---|---|---:|---:|
| P6 | Aumentará | 99,0 | 90,0 |
| P13 | "Acogerlas si se comprueba que están perseguidas" | **98,5** | 40,3 |
| P8c | Acuerdo | 97,3 | 77,9 |
| P36 | Sí, son vascos y vascas | 95,3 | 88,8 |
| P20 | Mismos derechos y obligaciones | 91,4 | 69,2 |
| P11 | "Otros requisitos legales" | **85,9** | 17,8 |
| P3 | "Son bastantes" | **83,4** | 26,8 |

## 3. La consecuencia sustantiva: cero de mil

Tres opciones que **un tercio o más de la población vasca respalda**, y el número
de Personas sintéticas que las eligen:

| Opción | Personas (de 1.000) | Real |
|---|---:|---:|
| P11 "Permitir la entrada sin poner ningún obstáculo legal" | **0** | 34,2 % |
| P13 "Acogerlas sin restricciones" | **0** | 31,3 % |
| P12 "Regularizarlas a todas, darles papeles" | 124 | 41,5 % |

Y en el extremo contrario, la misma compresión:

| Opción | Panel | Real |
|---|---:|---:|
| P3 "Son demasiadas" | 3,0 % | 19,0 % |
| P20 "Prioridad para las personas autóctonas" | 8,4 % | 29,2 % |

**El panel borra los dos extremos del debate migratorio vasco a la vez.** No es un
sesgo ideológico en una dirección: es aplanamiento hacia el centro cualificado.

## 4. Y sin embargo, el panel SÍ usa el perfil

Este es el punto que cambia el diagnóstico respecto a lo que asumíamos. V de Cramér
entre la respuesta y cada variable del perfil (media de las 13 preguntas):

| Variable | V media | V máx |
|---|---:|---:|
| **voto** | **0,36** | 0,47 (P11) |
| euskera | 0,19 | 0,28 |
| nivel de estudios | 0,16 | 0,20 |
| clase social | 0,13 | 0,16 |
| género | 0,11 | 0,15 |
| grupo de edad | 0,08 | 0,14 |
| provincia | 0,07 | 0,11 |

Y la dirección es **correcta**. P8f ("si comete un delito, expulsión"), % de acuerdo:

| Electorado | Panel acuerdo |
|---|---:|
| Vox | 90,6 % |
| PP | 65,7 % |
| PNV | 17,5 % |
| EH Bildu | 5,5 % |

P3 "son demasiadas": Vox 50,0 % · PP 20,0 % · PNV 0,5 % · EH Bildu 1,2 %.

**El panel no ignora a la Persona y no confunde la izquierda con la derecha.** Ordena
bien. Lo que hace mal es el rango: comprime a todo el mundo dentro de una banda
estrecha de respuestas razonables y solo mueve las colas pequeñas.

La prueba más clara está en P11. Los electorados más favorables a la inmigración
dan **0 %** a la opción más abierta:

| Electorado | "Sin ningún obstáculo legal" | "Otros requisitos legales" |
|---|---:|---:|
| Elkarrekin Podemos | 0,0 % | 100,0 % |
| Sumar | 0,0 % | 100,0 % |
| EH Bildu | 0,0 % | 96,9 % |
| PNV | 0,0 % | 91,8 % |

Un 34,2 % de la población vasca real elige esa opción. Ninguna de las 1.000 Personas
lo hace, ni siquiera las que por perfil deberían ser las primeras.

## 5. El caso P26: la media correcta por las razones equivocadas

Pregunta 0-10 sobre los efectos de la inmigración:

- **Media panel 5,15 · media real 5,30 · error 0,15.** Excelente, en apariencia.
- Distribución del panel: `5 = 49,9 % · 6 = 36,5 % · 3 = 7,6 %` — el **86,4 %** de
  las Personas se sitúa en 5 o 6, y **ninguna** de las 1.000 puntúa 8, 9 o 10.

Una población en la que el 19 % cree que hay "demasiados" inmigrantes no puede
tener una distribución que sea un pico en 5-6 sin cola alta. **La media es correcta
porque los errores se cancelan, no porque la distribución lo sea.**

Es la ilustración más limpia que tenemos de la distinción central del artículo, y
llega desde un cuestionario independiente: *se puede clavar el agregado sin acertar
a nadie*. Aquí ni siquiera hace falta bajar al microdato para verlo — basta mirar
la varianza.

## 6. Qué añade Ikuspegi al artículo

Es una **replicación externa** del hallazgo, sobre un instrumento distinto (otro
equipo, otro tema, otra casa de campo, n=600) y con el mismo panel v1:

1. **El DAM se sostiene** (15,7 aquí vs 13,4 en el Deustobarómetro) — el método
   tiene un techo estable, no depende del cuestionario.
2. **El fallo es de varianza, no de sesgo ni de anclaje.** El panel ordena bien a
   las Personas por perfil (V = 0,36 con voto) pero no reproduce la dispersión de
   la población. Esto refina la tesis del techo de información: el problema no es
   solo que el perfil no informe, es que **el modelo colapsa la respuesta aunque el
   perfil informe**.
3. **Tiene una consecuencia política medible.** El panel retrata a Euskadi como más
   tibia ante la inmigración de lo que es: borra el 34 % que defiende la entrada
   libre, el 31 % que acogería sin restricciones y el 19 % que ve demasiada
   inmigración. Un panel sintético usado para diseñar política pública habría
   informado mal en las dos direcciones.

## 7. Control con el panel v2 — predicciones registradas antes de mirar

`lanzar_ikuspegi_v2.py` repite las mismas 13 preguntas con `pv_agentes_v2.json`.
**No se lanza para ver si la v2 gana**, sino como **control que licencia la
afirmación central**: si el fallo fuera del perfil, un perfil materialmente
distinto (otro anclaje, otros donantes, otras variables) daría otra cosa.

### Qué cambia entre v1 y v2, en lo que importa aquí

| | v1 | v2 |
|---|---|---|
| **Religión** | Católico/a 362 · Ateo/a 272 · Agnóstico/a 141 · Indiferente 143 | **"No especificada" en las 1.000** |
| **Voto identificable a partido** | ~50 % (PNV 194, EH Bildu 163, PSE 120…) | ~50 %, pero 256 Abstención + 244 Ns/Nc |
| **`principales_problemas`** | Poblado (21 vacíos) | **Vacío en las 1.000** |
| **Perfil mediático** | Dieta informativa completa, confianza en 7 medios, desinformación percibida | Solo min/día de noticias y uso de internet |
| **Identidad subjetiva** | — | **Sí** (Únicamente vasco/a 206 … Únicamente español/a 56) |
| **Inseguridad económica** | — | **`problemas_dinero`** (278 con problemas para llegar a fin de mes) |
| **Seguridad percibida** | — | **`seguridad_percibida`** (97 se sienten inseguros) |
| **Capital social** | — | **`perfil_social`** completo, 1.000/1.000: confianza generalizada, redes, cohesión, corrupción percibida |

Hay argumentos en las dos direcciones, y son específicos de este cuestionario:

- **A favor de la v2:** confianza generalizada, inseguridad económica y seguridad
  percibida son los correlatos canónicos de las actitudes hacia la inmigración en
  la literatura (Putnam, trabajos sobre ESS). La v1 no los tiene. Si alguna vez
  el perfil enriquecido iba a marcar diferencia, es aquí y no en el Deustobarómetro.
- **En contra de la v2:** pierde la religión (y el cuestionario tiene P21e templos,
  P22e prácticas religiosas, P22h abandono de la religión), pierde casi todo el
  perfil mediático — y Ikuspegi dedica una sección entera al discurso mediático como
  determinante — y sobre todo **degrada el voto**, que es justamente la variable con
  la que el panel más discrimina (V = 0,36, máx 0,47).

### Predicciones (registradas antes de lanzar)

1. **DAM v2 en el rango 14,5-17,5**, es decir, dentro de ±1,5 p.p. de la v1 (15,7).
   Sin diferencia práctica, replicando el resultado del Deustobarómetro (13,4 vs 13,9).
2. **Concentración v2 en 83,7 ± 3 p.p.** (real: 61,5). Esta es la predicción que
   importa.
3. **P11 "sin ningún obstáculo legal" y P13 "acogerlas sin restricciones" siguen
   por debajo del 5 %** (real: 34,2 % y 31,3 %).
4. **V de Cramér con voto por debajo de la de v1 (0,36)**, por la degradación del
   voto en v2.

**Qué falsaría el diagnóstico:** que la concentración baje de 75 % o que P11/P13
suban por encima del 15 %. Si eso ocurre, el fallo *sí* era de perfil y no del
modelo, y habría que reescribir la sección 4. Es el resultado que más nos
interesaría encontrar, y por eso se registra antes.

### RESULTADO (`encuesta_2026-08-08_102423.json`, 1.000 Personas v2, 0 vacías/sin parsear)

**El diagnóstico no se falsa: se refuerza, y con un giro que no esperaba.**

| Predicción | Resultado | |
|---|---|---|
| 1. DAM v2 en 14,5-17,5 | **18,2** | ❌ falla, y por arriba |
| 2. Concentración 83,7 ± 3 | **88,8** | ❌ falla, y por arriba |
| 3. P11/P13 por debajo del 5 % | **0,0 y 0,0** | ✅ |
| 4. V con voto < 0,36 | **0,31** | ✅ |

Las dos predicciones que fallan lo hacen **en la dirección contraria a la
falsación**: la v2 no descolapsa nada, colapsa **más**.

| | v1 | **v2** | Real |
|---|---:|---:|---:|
| **DAM** | 15,7 | **18,2** | — |
| Concentración media (opción top) | 83,7 | **88,8** | 61,5 |
| NS/NC medio | 1,4 | **0,9** | 3,4 |
| **Opciones distintas usadas (media por pregunta)** | 4,3 | **2,7** | — |
| Moda acertada | 8/12 | 8/12 | — |

**La v2 es peor que el baseline de la moda (17,0).** Sustituir el panel v1 por el
v2 en este cuestionario es peor que no tener panel y contestar siempre lo que
contesta la mayoría.

El indicador más elocuente es el último: **la v2 usa 2,7 opciones por pregunta de
media**. Casos límite: P8c 100 % "Acuerdo" · P13 100 % una sola opción · P6 99,9 % ·
P36 99,1 %. Un cuestionario de 5 opciones respondido con 2.

Y las opciones comprometidas se hunden todavía más:

| Opción | v1 | **v2** | Real |
|---|---:|---:|---:|
| P11 "sin ningún obstáculo legal" | 0,0 | **0,0** | 34,2 |
| P13 "acogerlas sin restricciones" | 0,0 | **0,0** | 31,3 |
| P12 "regularizarlas a todas" | 12,4 | **2,2** | 41,5 |
| P3 "son demasiadas" | 3,0 | **0,0** | 19,0 |
| P20 "prioridad para las autóctonas" | 8,4 | **2,6** | 29,2 |

En P3 y P11/P13 la v2 deja **tres opciones en cero absoluto sobre 1.000 Personas**,
dos de ellas respaldadas por un tercio de la población vasca real.

La dirección sigue siendo correcta (P8f, acuerdo con la expulsión: PP 76,9 % ·
PSE 13,3 % · EH Bildu 9,3 % · Elkarrekin Podemos 0 %). Otra vez: **ordena bien,
comprime más**.

### ¿Es un artefacto de la degradación del voto en la v2?

Interpretación alternativa legítima: la v2 tiene 500 Personas sin partido
(256 abstención + 244 Ns/Nc) y el voto es la variable que más discrimina.
Control: repetir el cálculo **solo sobre las Personas con voto a un partido**.

| | n | DAM | Concentración |
|---|---:|---:|---:|
| v1, todas | 1.000 | 15,7 | 83,7 |
| v1, solo con partido | 637 | **14,7** | 81,9 |
| v2, todas | 1.000 | 18,2 | 88,8 |
| v2, solo con partido | 475 | **17,9** | **89,0** |

**No es el voto.** Restringiendo a Personas con partido en ambos paneles, la v2
sigue 3,2 p.p. por detrás y su concentración no baja (89,0). La brecha es del
perfil completo, no de la variable política.

### Lectura

La v2 aporta exactamente las variables que la literatura señala como predictores
canónicos de las actitudes hacia la inmigración — confianza generalizada,
inseguridad económica, seguridad percibida, cohesión social — y el resultado es
**peor**. Añadir información al perfil no mejoró la fidelidad distribucional: la
empeoró, y por la vía de estrechar aún más el abanico de respuestas.

Esto replica y **amplifica** el hallazgo del Deustobarómetro (v1 13,4 vs v2 13,9,
Δ +0,4; aquí Δ **+2,5**). Con dos instrumentos independientes apuntando en la
misma dirección, "más estructura ≠ mejor predicción" deja de ser una anécdota del
Deustobarómetro y pasa a ser un resultado del proyecto.

**Consecuencia para el argumento del artículo:** ya no hace falta apoyarse solo en
el techo de información. Se puede afirmar algo más fuerte y directamente
observado — *dado un perfil que ya ordena bien a las Personas, enriquecerlo no
recupera la varianza perdida; el colapso lo pone el modelo.* La v2 es el control
que licencia esa frase.

**Cautela que hay que declarar:** la v2 no es "v1 + más campos". Gana capital
social, identidad e inseguridad económica, pero **pierde religión (1.000/1.000 sin
dato)**, casi todo el perfil mediático y `principales_problemas`. No es un
experimento limpio de dosis de información; es un perfil *distinto*. Lo que queda
firmemente establecido es lo negativo: **un perfil materialmente distinto y más
rico en las dimensiones canónicas no descolapsa nada.**

## 8. ¿Y si solo miramos las preguntas que el perfil sí informa?

Pregunta de David. Respuesta corta: **cambia mucho, y en las dos direcciones a la
vez.** Métrica correcta aquí no es el DAM sino **Δ vs moda** (DAM del baseline
menos DAM del panel): mide lo que el panel *añade*, no lo que acierta.

Clasificación a priori de las 12 preguntas con dato real:

| Grupo | n | V(voto) | DAM v1 | DAM moda | **Δ v1** | **Δ v2** |
|---|---:|---:|---:|---:|---:|---:|
| **A · Política migratoria** (P8f, P11, P12, P13, P20) | 5 | 0,42 | 18,0 | 24,0 | **+6,0** | +5,0 |
| **B · Valores e identidad** (P8c, P8n, P22j, P36) | 4 | 0,36 | 16,9 | 11,6 | **−5,3** | −10,3 |
| **C · Percepción factual** (P3, P5, P6) | 3 | 0,29 | 10,3 | 12,6 | **+2,3** | +0,6 |
| **Total** | 12 | 0,37 | 15,7 | 17,0 | **+1,3** | −1,2 |

Tres lecturas:

**1. Sí, el panel aporta donde el perfil informa — y bastante.** En política
migratoria el panel gana **6,0 p.p.** al baseline de la moda, contra los +1,3 del
conjunto. Es el mismo patrón que el Deustobarómetro (bloque político, el mejor:
DAM 10,1). El resultado global de +1,3 es la media entre un grupo donde el panel
funciona y otro donde es activamente peor que no tener panel.

**2. Pero "donde aporta más" no es "donde acierta más".** El DAM del grupo A (18,0)
es **peor** que el global (15,7). El panel gana Δ ahí porque son las preguntas con
distribución real dispersa (baseline moda 24,0), y son exactamente aquellas en las
que su sobreconcentración duele más en términos absolutos. Gana la comparación y
pierde la foto.

**3. El grupo B es el desastre: Δ = −5,3.** Son preguntas de consenso real
(baseline moda 11,6, el mejor de los tres) donde el panel **colapsa en la opción
equivocada**: P22j y P8n se van a "Indecisión" (70 % y 75 %) cuando la sociedad
vasca está de acuerdo (73,7 % y 70,2 %). Aquí no es que el panel disperse mal:
es que elige mal la moda y encima con toda la masa encima.

### Lo que NO se sostiene

La hipótesis natural —"a más uso del perfil, más aporta el panel"— **no aparece en
los datos**: `corr(V(voto), Δ vs moda) = +0,10` en v1 y **−0,21** en v2. Cruzando
las 12 preguntas una a una, que el panel discrimine más por voto no predice que
lo haga mejor. Compárese con `corr(concentración real, Δ) = −0,33`: **el Δ lo
explica mejor la forma de la distribución real que el uso del perfil.**

### Dos avisos importantes

**(a) El piloto NO es una selección aleatoria del cuestionario, y está sesgado a
favor del panel.** Elegí estas 13 por limpieza del dato real, y el resultado son
**5 de 12 preguntas de política migratoria** — el bloque donde v1 históricamente
va mejor. En el cuestionario completo de 39 preguntas ese bloque pesa mucho menos
(hay baterías enteras de distancia social P17, derechos P18/P19, pautas culturales
P21, simpatía P23). **La cifra de 15,7 es probablemente optimista; escalar a 39
debería empeorarla.**

**(b) No podemos medir "informada" como es debido, y hay que decirlo.** Con el
Deustobarómetro sí pudimos (`techo_predictivo.py`: R² fuera de muestra de cada
pregunta sobre el perfil, usando el `.sav`). De Ikuspegi **solo tenemos porcentajes
agregados**, no microdatos. La V de Cramér que uso aquí mide cuánto usa el perfil
**el panel**, no cuánto lo informa **la realidad** — es un proxy y además algo
circular.

→ **Acción recomendada:** pedir a Ikuspegi los microdatos del Barómetro 2025
(UPV/EHU; la petición académica de microdatos anonimizados es estándar y el
informe indica que el fichero SPSS existe). Con ellos se podría correr
`techo_predictivo.py` sobre actitudes hacia la inmigración y contestar esta
pregunta de verdad: **cuál es el techo de información para este dominio y qué
fracción alcanza el panel** — el equivalente del 0,24 / 65 % que ya tenemos para
el Deustobarómetro, en un dominio independiente. Sería, con diferencia, la mejor
pieza que le falta al artículo.

## 9. Pendiente

1. **Variante de prompt contra la sobreconcentración.** Instrucción explícita de que
   las posiciones minoritarias y el NS/NC son respuestas legítimas, y de que no debe
   refugiarse en la opción intermedia. Relanzar las mismas 13 preguntas y medir.
   Si el DAM baja, cuantifica cuánta infidelidad es del anclaje y cuánta del
   comportamiento del modelo — **material del artículo, no una corrección**.
2. **Robustez de modelo:** repetir con un modelo frontera (Opus/Sonnet) sobre estas
   13 preguntas. Es la propuesta que ya estaba en la bitácora y aquí sale barata
   (13 preguntas, no 152).
3. Ampliar a las 39 preguntas si la variante de prompt mueve algo. Si no, no merece
   la pena: el resultado ya está establecido con 13.
4. Sigue abierta la ambigüedad de lectura de **P8a/P22i** (Gráfico 28) documentada
   en `datos Ikuspegi 2025/verificacion_datos_reales.md`.
