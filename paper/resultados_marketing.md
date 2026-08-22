# Fase 1 — El subcorpus de marketing del Deustobarómetro

**44 ítems de marketing + 10 de contraste político.** Sin API: relectura de resultados ya
generados (techo n=1.000 · acuerdo individual n=300 · tanda agregada n=1.000).
Selección **ex ante por constructo**, definida en `marketing_items.json`.

## Cómo se mide cada columna

| columna | qué es |
|---|---|
| **techo lin** | `corr_max = √R²_OOS`, ridge, CV 5-fold **repetida 20 veces**, semilla por ítem |
| **techo GBM** | igual pero con gradient boosting: capta no linealidades que el ridge pierde |
| **alcanzado** | correlación de **Pearson** panel↔real, la misma métrica que el techo |
| **Δ vs moda** | acierto del panel menos el de "responder siempre la moda real" |
| **DAM** | desviación absoluta media panel vs real, por opción |
| **conc.** | cuota de la opción más elegida, panel vs real |

> No se usa **Spearman**: en ítems con ~90 % de casos en una categoría se dispara por el
> tratamiento de empates y llega a superar el techo, lo que es imposible por construcción.
> Con Spearman el bloque de retrenchment daba un absurdo 367 % del techo.

## Resumen por constructo

| constructo | ítems | techo lin | techo GBM | alcanzado (Pearson) | % del techo GBM | Δ vs moda | DAM p.p. | conc. panel | conc. real | exceso |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| A · Retrenchment de consumo | 13 | 0.122 | 0.134 | 0.149 ± 0.048 | 112 % | -5.3 | 13.7 | 84.0 | 70.5 | +13.5 |
| B · Decisión de viaje | 5 | 0.175 | 0.137 | 0.051 ± 0.079 | 38 % | -12.4 | 26.9 | 84.8 | 49.9 | +34.9 |
| C · Satisfacción de servicio | 16 | 0.228 | 0.254 | 0.072 ± 0.028 | 28 % | -3.2 | 9.4 | 54.5 | 21.4 | +33.1 |
| D · Confianza de marca | 10 | 0.326 | 0.351 | 0.217 ± 0.070 | 62 % | -5.7 | 8.5 | 47.3 | 19.8 | +27.6 |
| E · (contraste) Confianza política | 10 | 0.354 | 0.399 | 0.202 ± 0.064 | 51 % | -5.7 | 10.1 | 45.5 | 21.2 | +24.3 |
| **TOTAL MARKETING** | **44** | **0.216** | **0.234** | **0.127 ± 0.031** | **54 %** | **-5.3** | **12.4** | **65.0** | **38.8** | **+26.3** |

## Los cuatro resultados

**1 · El techo de marketing es más bajo que el político.** Confianza de marca (0,35) y confianza
política (0,40) son parecidas, pero **retrenchment de consumo (0,13)** y **decisión de viaje (0,14)**
quedan muy por debajo. El perfil sociodemográfico informa *menos* sobre la conducta de consumo que
sobre la actitud política — justo al revés de lo que necesitaría la promesa comercial del panel
sintético, y al revés de donde la literatura ha puesto sus benchmarks.

**2 · El panel alcanza el 54 % del techo, y en consumo no alcanza nada porque no hay nada.** En
retrenchment el techo (0,134) y lo alcanzado (0,149) son ambos indistinguibles de cero a nivel de
ítem (ver la sección de anomalía). La lectura correcta no es "el panel va bien en consumo", es
**"en consumo no hay señal que capturar desde el perfil"**.

**3 · Δ vs moda negativo en los cuatro constructos.** El panel es peor que responder siempre la
categoría más frecuente. El peor caso es decisión de viaje, **−12,4 p.p.**, y dentro de él la
pregunta por la razón del abandono de viaje (**−26,7 p.p.**, kappa 0,00).

**4 · Colapso de varianza en los cuatro.** La opción más elegida se lleva **65,0 %** en el panel
frente al **38,8 %** real: **+26,2 p.p. de exceso**. Ningún ítem de B, C, D o E tiene exceso
negativo. El caso extremo es la multirrespuesta de efectos del turismo: **99,9 % vs 41,2 %**.

## Anomalía detectada y resuelta: ítems que "superan" su techo

Dos ítems de retrenchment (p6_5, p6_9) daban un Pearson por encima de su techo lineal, lo que es
imposible por construcción. Tres comprobaciones:

1. **Techo no lineal.** Con gradient boosting el techo de p6_5 sube de 0,141 a **0,234**, dentro del
   intervalo del valor observado. El ridge infraestimaba: la relación perfil→respuesta no es lineal
   en este bloque.
2. **Bootstrap del Pearson** (5.000 réplicas). Con ~90 % de los casos en una categoría, el error
   nominal de Fisher es demasiado optimista. Los IC reales son enormes:

   | var | n | % moda real | Pearson | IC 95 % bootstrap |
   |---|--:|--:|--:|---|
   | p6_5 | 292 | 86,6 % | 0,295 | [0,129 · 0,446] |
   | p6_9 | 291 | 92,4 % | 0,164 | **[−0,037 · 0,416]** |
   | p6_3 | 298 | 89,3 % | 0,194 | **[−0,034 · 0,421]** |
   | p6_4 | 293 | 87,0 % | 0,143 | **[−0,005 · 0,312]** |

   En p6_9, p6_3 y p6_4 **el intervalo incluye el cero**: esas correlaciones no son distinguibles
   de la nada, y menos aún "superiores al techo".
3. **Los 300 encuestados con predicción son los 300 primeros del fichero** (verificado: 300/300),
   no una submuestra aleatoria. Hay que declararlo.

**Conclusión:** ningún ítem supera su techo de forma real. Pero el episodio deja dos exigencias
para el paper: (a) el techo del paper debe ser el **no lineal**, o al menos reportar ambos;
(b) a nivel de ítem, con n≈300 y asimetría del 90 %, **las correlaciones individuales no son
interpretables** — sólo lo son los agregados por constructo.

## Qué hay que corregir en el material previo

- La afirmación **"el panel alcanza el 65 % del techo"** (bitácora y `CLAUDE.md`) compara un
  Spearman (0,15) con un techo Pearson (0,24). Con métricas homogéneas y techo no lineal, en el
  subcorpus de marketing es el **54 %**. La cifra global del proyecto debe recalcularse igual.
- El techo global pasa de **corr máx 0,24 a 0,22** (lineal) tras corregir el bug de mapeo
  (`incidencia_mapeo_idx_real.md`).

## Sesgo de selección

Los 44 ítems **no son una muestra aleatoria** de las 152 preguntas: se eligieron por constructo de
marketing. La diferencia con el piloto de Ikuspegi es que aquí la selección es **ex ante y por
contenido**, no por resultado, y el grupo de contraste político (E) se define con el mismo criterio
para poder comparar. Aun así hay que declararlo en el paper.

## Detalle por ítem

| var | c | n | R² lin | ±sd | techo lin | techo GBM | Pearson | Δ vs moda | DAM | conc. P | conc. R | ítem |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|
| p6_1 | A | 981 | 0.037 | 0.010 | 0.193 | 0.000 | 0.080 | -0.3 | 23.2 | 96.7 | 39.6 | Indica si en el último mes, y como consecuencia de tu si |
| p6_10 | A | 976 | 0.006 | 0.014 | 0.077 | 0.160 | 0.081 | -3.0 | 3.1 | 91.9 | 86.3 | Indica si en el último mes, y como consecuencia de tu si |
| p6_11 | A | 952 | 0.145 | 0.013 | 0.380 | 0.366 | 0.287 | -0.4 | 12.3 | 96.3 | 71.8 | Indica si en el último mes, y como consecuencia de tu si |
| p6_12 | A | 962 | 0.071 | 0.012 | 0.267 | 0.263 | — | +0.0 | 11.1 | 99.9 | 77.7 | Indica si en el último mes, y como consecuencia de tu si |
| p6_13 | A | 972 | 0.026 | 0.012 | 0.162 | 0.217 | 0.090 | -25.9 | 25.8 | 54.6 | 79.0 | Indica si en el último mes, y como consecuencia de tu si |
| p6_2 | A | 985 | -0.009 | 0.011 | 0.000 | 0.000 | 0.153 | -14.8 | 15.3 | 47.7 | 59.1 | Indica si en el último mes, y como consecuencia de tu si |
| p6_3 | A | 978 | -0.029 | 0.013 | 0.000 | 0.000 | 0.194 | -0.7 | 27.8 | 97.3 | 43.4 | Indica si en el último mes, y como consecuencia de tu si |
| p6_4 | A | 970 | 0.066 | 0.016 | 0.257 | 0.247 | 0.143 | -3.4 | 4.1 | 93.3 | 85.2 | Indica si en el último mes, y como consecuencia de tu si |
| p6_5 | A | 973 | 0.020 | 0.016 | 0.141 | 0.234 | 0.295 | -3.1 | 6.1 | 91.9 | 79.7 | Indica si en el último mes, y como consecuencia de tu si |
| p6_6 | A | 977 | -0.004 | 0.013 | 0.000 | 0.085 | 0.193 | -13.5 | 18.6 | 47.2 | 80.9 | Indica si en el último mes, y como consecuencia de tu si |
| p6_7 | A | 975 | -0.011 | 0.014 | 0.000 | 0.000 | 0.133 | -2.0 | 6.1 | 77.8 | 65.7 | Indica si en el último mes, y como consecuencia de tu si |
| p6_8 | A | 976 | 0.009 | 0.015 | 0.093 | 0.163 | -0.019 | -0.3 | 18.1 | 99.6 | 63.4 | Indica si en el último mes, y como consecuencia de tu si |
| p6_9 | A | 966 | 0.000 | 0.020 | 0.014 | 0.000 | 0.164 | -1.0 | 6.7 | 98.4 | 85.0 | Indica si en el último mes, y como consecuencia de tu si |
| MULTI:barometro_digital_4_turismo.json:1 | B | — | — | — | — | — | — | -0.7 | 36.0 | 99.9 | 41.2 | ¿Crees que el turismo tiene alguno de los siguientes efe |
| p13 | B | 1000 | 0.009 | 0.013 | 0.097 | 0.000 | 0.090 | -2.3 | 18.6 | 59.5 | 33.1 | ¿En qué medida ha aumentado en los últimos años tu miedo |
| p14 | B | 1000 | — | — | — | — | 0.084 | -5.3 | 31.6 | 77.1 | 37.6 | ¿Has descartado o modificado un viaje en los últimos dos |
| p15 | B | 267 | — | — | — | — | -0.087 | -26.7 | 18.3 | 91.3 | 73.0 | ¿Cuál fue la principal razón? |
| p16 | B | 941 | 0.064 | 0.014 | 0.253 | 0.274 | 0.118 | -15.3 | 30.1 | 96.0 | 64.4 | ¿En qué medida crees que el aumento de turistas afecta a |
| p8_1 | C | 990 | 0.014 | 0.010 | 0.116 | 0.154 | -0.038 | +0.7 | 13.9 | 63.5 | 38.1 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_10 | C | 970 | 0.056 | 0.011 | 0.236 | 0.233 | 0.042 | -1.7 | 12.6 | 52.7 | 19.5 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_11 | C | 932 | 0.113 | 0.011 | 0.336 | 0.354 | 0.209 | -4.2 | 8.1 | 36.4 | 17.6 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_12 | C | 940 | 0.057 | 0.016 | 0.238 | 0.227 | 0.124 | -2.6 | 9.6 | 61.4 | 23.2 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_13 | C | 928 | 0.038 | 0.012 | 0.194 | 0.259 | 0.094 | -0.4 | 9.7 | 73.2 | 20.2 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_14 | C | 886 | 0.071 | 0.012 | 0.267 | 0.269 | 0.098 | -2.0 | 7.1 | 42.2 | 23.0 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_15 | C | 953 | 0.012 | 0.014 | 0.108 | 0.084 | 0.069 | -8.8 | 8.1 | 44.1 | 20.2 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_16 | C | 939 | 0.047 | 0.012 | 0.216 | 0.236 | 0.020 | -8.2 | 8.5 | 46.0 | 25.3 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_2 | C | 962 | 0.079 | 0.010 | 0.281 | 0.282 | 0.117 | -1.0 | 10.3 | 53.1 | 17.8 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_3 | C | 930 | 0.076 | 0.014 | 0.276 | 0.320 | 0.074 | -1.8 | 8.3 | 58.4 | 19.0 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_4 | C | 972 | 0.032 | 0.012 | 0.178 | 0.232 | 0.049 | -1.4 | 8.4 | 56.0 | 21.3 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_5 | C | 955 | 0.053 | 0.015 | 0.231 | 0.286 | 0.026 | -1.7 | 8.8 | 68.3 | 19.2 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_6 | C | 986 | 0.060 | 0.014 | 0.245 | 0.268 | 0.100 | -6.4 | 8.6 | 37.5 | 19.4 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_7 | C | 958 | 0.050 | 0.012 | 0.223 | 0.291 | 0.124 | -1.7 | 8.1 | 46.8 | 16.8 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_8 | C | 985 | 0.060 | 0.013 | 0.246 | 0.255 | 0.041 | -8.5 | 9.5 | 68.9 | 18.4 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p8_9 | C | 971 | 0.063 | 0.014 | 0.251 | 0.320 | 0.004 | -2.1 | 10.3 | 63.7 | 23.2 | ¿Qué valoración le das a cada uno de los siguientes serv |
| p21_10 | D | 960 | 0.088 | 0.010 | 0.296 | 0.326 | 0.132 | -2.8 | 12.1 | 58.1 | 28.8 | ¿En qué medida confías en cada una de las siguientes org |
| p21_11 | D | 982 | 0.025 | 0.012 | 0.159 | 0.233 | 0.114 | -8.5 | 8.8 | 48.0 | 19.5 | ¿En qué medida confías en cada una de las siguientes org |
| p21_15 | D | 969 | 0.168 | 0.006 | 0.409 | 0.435 | 0.232 | -5.2 | 10.1 | 57.5 | 18.4 | ¿En qué medida confías en cada una de las siguientes org |
| p21_16 | D | 962 | 0.199 | 0.010 | 0.446 | 0.446 | 0.209 | -11.3 | 9.3 | 54.6 | 18.7 | ¿En qué medida confías en cada una de las siguientes org |
| p21_17 | D | 975 | 0.007 | 0.012 | 0.081 | 0.172 | 0.134 | -2.4 | 9.8 | 54.4 | 18.2 | ¿En qué medida confías en cada una de las siguientes org |
| p21_18 | D | 975 | 0.105 | 0.011 | 0.323 | 0.361 | 0.197 | -7.2 | 7.8 | 39.6 | 20.5 | ¿En qué medida confías en cada una de las siguientes org |
| p21_19 | D | 981 | 0.079 | 0.009 | 0.282 | 0.302 | 0.114 | -13.6 | 6.2 | 45.6 | 17.3 | ¿En qué medida confías en cada una de las siguientes org |
| p21_4 | D | 959 | 0.174 | 0.014 | 0.417 | 0.407 | 0.266 | -2.8 | 5.5 | 25.5 | 15.9 | ¿En qué medida confías en cada una de las siguientes org |
| p21_5 | D | 962 | 0.072 | 0.006 | 0.269 | 0.237 | 0.259 | -4.9 | 7.4 | 58.3 | 20.4 | ¿En qué medida confías en cada una de las siguientes org |
| p21_9 | D | 976 | 0.335 | 0.009 | 0.579 | 0.594 | 0.515 | +1.4 | 8.4 | 31.6 | 19.8 | ¿En qué medida confías en cada una de las siguientes org |
| p21_1 | E | 978 | 0.127 | 0.012 | 0.356 | 0.411 | 0.009 | -10.6 | 13.1 | 45.8 | 19.3 | ¿En qué medida confías en cada una de las siguientes org |
| p21_12 | E | 956 | 0.053 | 0.013 | 0.230 | 0.326 | 0.202 | -7.0 | 10.1 | 29.7 | 17.6 | ¿En qué medida confías en cada una de las siguientes org |
| p21_13 | E | 977 | 0.140 | 0.010 | 0.375 | 0.386 | 0.230 | -10.3 | 12.3 | 47.1 | 18.6 | ¿En qué medida confías en cada una de las siguientes org |
| p21_14 | E | 966 | 0.098 | 0.012 | 0.313 | 0.343 | 0.092 | -2.1 | 11.2 | 76.0 | 23.7 | ¿En qué medida confías en cada una de las siguientes org |
| p21_2 | E | 979 | 0.196 | 0.010 | 0.443 | 0.470 | 0.348 | -18.5 | 9.0 | 36.3 | 18.3 | ¿En qué medida confías en cada una de las siguientes org |
| p21_20 | E | 974 | 0.089 | 0.009 | 0.298 | 0.337 | 0.130 | -3.1 | 10.8 | 48.0 | 20.3 | ¿En qué medida confías en cada una de las siguientes org |
| p21_3 | E | 979 | 0.177 | 0.013 | 0.421 | 0.485 | 0.148 | +0.0 | 12.4 | 55.3 | 35.1 | ¿En qué medida confías en cada una de las siguientes org |
| p21_6 | E | 978 | 0.165 | 0.009 | 0.406 | 0.442 | 0.337 | -0.7 | 6.4 | 35.6 | 19.1 | ¿En qué medida confías en cada una de las siguientes org |
| p21_7 | E | 966 | 0.140 | 0.012 | 0.374 | 0.424 | 0.249 | -5.6 | 7.2 | 37.3 | 18.7 | ¿En qué medida confías en cada una de las siguientes org |
| p21_8 | E | 982 | 0.102 | 0.011 | 0.320 | 0.369 | 0.276 | +1.0 | 8.5 | 43.9 | 20.9 | ¿En qué medida confías en cada una de las siguientes org |