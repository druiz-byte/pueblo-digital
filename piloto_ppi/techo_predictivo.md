> ## ⚠ FICHERO OBSOLETO — NO CITAR (2026-08-21)
> Contiene un **error de mapeo etiqueta→opción** que colapsaba 29 de las 89 preguntas
> categóricas en una sola categoría (de ahí los `nan` de p6). Cifras corregidas en
> **`techo_predictivo_v2.md`**; diagnóstico completo en **`../paper/incidencia_mapeo_idx_real.md`**.
> Corrección del titular: **corr máxima 0,24 → 0,22** (el techo es aún más bajo).
> Se conserva como registro histórico de lo que se afirmó antes de esa fecha.

# Techo predictivo del barómetro desde un perfil sociodemográfico

¿Cuánta de la variación entre personas es explicable desde el perfil?
**`corr_max = sqrt(R²)` es el límite de CUALQUIER panel digital**: una Persona
construida solo con el perfil no puede saber más de lo que el perfil contiene.

Predictores (68 columnas): sexo, edad(+²), provincia, lengua, situación
laboral, estudios, religión, nacimiento, voto 2024, voto 2020, ideología 0-10,
nacionalismo 0-10 (+flags NS). R² **fuera de muestra**, validación cruzada 5-fold.

## Resumen

- **Escalas y ordinales (100 preguntas):** R² medio fuera de muestra **0.080** -> **corr máxima media 0.24**
  - mediana R² 0.052 · p90 0.202 · máx 0.389
  - preguntas con R² <= 0 (el perfil no predice nada): **14/100**
- **Nominales (35):** acierto 65% vs moda 58% (**+7.5 p.p.**)
- **Multi-respuesta (9):** acierto medio por opción 78% vs moda 77% (**+1.1 p.p.**)
- *(control)* las 2 preguntas que SON predictores dan R² 1.00 — circulares, no cuentan.

## Techo por bloque (escalas + ordinales)

| bloque | preg | R² medio | corr máx |
|---|--:|--:|--:|
| barometro_digital_1_situacion_ | 24 | 0.024 | 0.15 |
| barometro_digital_2_bienestar_ | 23 | 0.034 | 0.16 |
| barometro_digital_3_miedos.jso | 4 | 0.059 | 0.21 |
| barometro_digital_4_turismo.js | 1 | 0.085 | 0.29 |
| barometro_digital_5_politica_d | 45 | 0.099 | 0.28 |
| barometro_digital_7_perfil_val | 3 | 0.371 | 0.61 |

## Preguntas ordenadas por techo (escalas + ordinales)

| R² | corr máx | n | var | pregunta |
|--:|--:|--:|---|---|
| 0.389 | 0.62 | 1000 | p44_1 | ¿Cuál es tu nivel de conocimiento del euskera?: Lect |
| 0.364 | 0.60 | 1000 | p44_2 | ¿Cuál es tu nivel de conocimiento del euskera?: Escr |
| 0.359 | 0.60 | 1000 | p44_3 | ¿Cuál es tu nivel de conocimiento del euskera?: Conv |
| 0.358 | 0.60 | 976 | p21_9 | ¿En qué medida confías en cada una de las siguientes |
| 0.342 | 0.58 | 887 | p26_3 | Indica tu grado de acuerdo con cada una de las sigui |
| 0.289 | 0.54 | 834 | p26_1 | Indica tu grado de acuerdo con cada una de las sigui |
| 0.229 | 0.48 | 805 | p26_2 | Indica tu grado de acuerdo con cada una de las sigui |
| 0.214 | 0.46 | 962 | p21_16 | ¿En qué medida confías en cada una de las siguientes |
| 0.213 | 0.46 | 979 | p21_2 | ¿En qué medida confías en cada una de las siguientes |
| 0.194 | 0.44 | 880 | p39_6 | Y en la misma escala, ¿dónde colocarías a los siguie |
| 0.190 | 0.44 | 885 | p39_7 | Y en la misma escala, ¿dónde colocarías a los siguie |
| 0.181 | 0.43 | 979 | p21_3 | ¿En qué medida confías en cada una de las siguientes |
| 0.179 | 0.42 | 959 | p21_4 | ¿En qué medida confías en cada una de las siguientes |
| 0.172 | 0.41 | 969 | p21_15 | ¿En qué medida confías en cada una de las siguientes |
| 0.164 | 0.41 | 978 | p21_6 | ¿En qué medida confías en cada una de las siguientes |
| 0.161 | 0.40 | 925 | p12_3 | En qué medida estás de acuerdo con cada una de las s |
| 0.135 | 0.37 | 977 | p21_13 | ¿En qué medida confías en cada una de las siguientes |
| 0.135 | 0.37 | 800 | p23 | ¿En qué medida consideras necesario un nuevo estatut |
| 0.124 | 0.35 | 966 | p21_7 | ¿En qué medida confías en cada una de las siguientes |
| 0.119 | 0.35 | 956 | p18 | ¿Cómo calificarías la situación política general del |
| 0.118 | 0.34 | 957 | p20_2 | Si tuvieras que valorar con una nota de 0 a 10 la ca |
| 0.117 | 0.34 | 978 | p21_1 | ¿En qué medida confías en cada una de las siguientes |
| 0.106 | 0.33 | 905 | p37_6 | Y en la misma escala, ¿dónde colocarías a los siguie |
| 0.106 | 0.32 | 966 | p21_14 | ¿En qué medida confías en cada una de las siguientes |
| 0.104 | 0.32 | 975 | p21_18 | ¿En qué medida confías en cada una de las siguientes |
| 0.104 | 0.32 | 932 | p8_11 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.096 | 0.31 | 982 | p21_8 | ¿En qué medida confías en cada una de las siguientes |
| 0.090 | 0.30 | 974 | p21_20 | ¿En qué medida confías en cada una de las siguientes |
| 0.090 | 0.30 | 886 | p8_14 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.085 | 0.29 | 941 | p16 | ¿En qué medida crees que el aumento de turistas afec |
| 0.081 | 0.28 | 930 | p8_3 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.081 | 0.28 | 981 | p21_19 | ¿En qué medida confías en cada una de las siguientes |
| 0.076 | 0.28 | 962 | p21_5 | ¿En qué medida confías en cada una de las siguientes |
| 0.075 | 0.27 | 958 | p8_7 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.067 | 0.26 | 960 | p21_10 | ¿En qué medida confías en cada una de las siguientes |
| 0.065 | 0.26 | 962 | p8_2 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.063 | 0.25 | 971 | p8_9 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.062 | 0.25 | 940 | p8_12 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.061 | 0.25 | 970 | p8_10 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.061 | 0.25 | 979 | p7_6 | ¿Con qué frecuencia has pasado por los siguientes es |
| 0.060 | 0.25 | 956 | p21_12 | ¿En qué medida confías en cada una de las siguientes |
| 0.056 | 0.24 | 986 | p8_6 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.054 | 0.23 | 985 | p8_8 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.052 | 0.23 | 984 | p7_8 | ¿Con qué frecuencia has pasado por los siguientes es |
| 0.051 | 0.22 | 928 | p8_13 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.048 | 0.22 | 931 | p12_1 | En qué medida estás de acuerdo con cada una de las s |
| 0.046 | 0.21 | 939 | p8_16 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.045 | 0.21 | 955 | p8_5 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.043 | 0.21 | 981 | p7_5 | ¿Con qué frecuencia has pasado por los siguientes es |
| 0.043 | 0.21 | 892 | p37_3 | Y en la misma escala, ¿dónde colocarías a los siguie |
| 0.041 | 0.20 | 985 | p7_2 | ¿Con qué frecuencia has pasado por los siguientes es |
| 0.041 | 0.20 | 881 | p39_1 | Y en la misma escala, ¿dónde colocarías a los siguie |
| 0.037 | 0.19 | 930 | p29_2 | Indica tu grado de acuerdo con cada una de las sigui |
| 0.036 | 0.19 | 870 | p37_5 | Y en la misma escala, ¿dónde colocarías a los siguie |
| 0.036 | 0.19 | 881 | p37_2 | Y en la misma escala, ¿dónde colocarías a los siguie |
| 0.035 | 0.19 | 901 | p37_7 | Y en la misma escala, ¿dónde colocarías a los siguie |
| 0.035 | 0.19 | 890 | p26_4 | Indica tu grado de acuerdo con cada una de las sigui |
| 0.034 | 0.19 | 972 | p8_4 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.029 | 0.17 | 980 | p7_3 | ¿Con qué frecuencia has pasado por los siguientes es |
| 0.029 | 0.17 | 881 | p37_4 | Y en la misma escala, ¿dónde colocarías a los siguie |
| 0.028 | 0.17 | 978 | p7_7 | ¿Con qué frecuencia has pasado por los siguientes es |
| 0.028 | 0.17 | 985 | p2 | ¿Cómo calificarías la situación económica del País V |
| 0.025 | 0.16 | 959 | p20_1 | Si tuvieras que valorar con una nota de 0 a 10 la ca |
| 0.022 | 0.15 | 920 | p12_2 | En qué medida estás de acuerdo con cada una de las s |
| 0.017 | 0.13 | 930 | p19 | ¿Y cómo crees que será la situación política del Paí |
| 0.017 | 0.13 | 941 | p29_1 | Indica tu grado de acuerdo con cada una de las sigui |
| 0.012 | 0.11 | 987 | p7_4 | ¿Con qué frecuencia has pasado por los siguientes es |
| 0.010 | 0.10 | 953 | p8_15 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.007 | 0.08 | 990 | p8_1 | ¿Qué valoración le das a cada uno de los siguientes  |
| 0.004 | 0.07 | 1000 | p13 | ¿En qué medida ha aumentado en los últimos años tu m |
| 0.003 | 0.05 | 981 | p7_1 | ¿Con qué frecuencia has pasado por los siguientes es |
| 0.002 | 0.05 | 592 | p5 | ¿Crees que es probable que en los próximos seis mese |
| 0.001 | 0.02 | 890 | p37_1 | Y en la misma escala, ¿dónde colocarías a los siguie |
| -0.000 | 0.00 | 982 | p21_11 | ¿En qué medida confías en cada una de las siguientes |
| -0.004 | 0.00 | 975 | p21_17 | ¿En qué medida confías en cada una de las siguientes |
| -0.006 | 0.00 | 877 | p39_3 | Y en la misma escala, ¿dónde colocarías a los siguie |
| -0.010 | 0.00 | 1000 | p9_5 | ¿Crees que los inmigrantes que viven en el País Vasc |
| -0.011 | 0.00 | 1000 | p9_2 | ¿Crees que los inmigrantes que viven en el País Vasc |
| -0.011 | 0.00 | 1000 | p9_3 | ¿Crees que los inmigrantes que viven en el País Vasc |
| -0.013 | 0.00 | 1000 | p9_1 | ¿Crees que los inmigrantes que viven en el País Vasc |
| -0.013 | 0.00 | 881 | p39_2 | Y en la misma escala, ¿dónde colocarías a los siguie |
| -0.025 | 0.00 | 1000 | p9_6 | ¿Crees que los inmigrantes que viven en el País Vasc |
| -0.032 | 0.00 | 1000 | p9_4 | ¿Crees que los inmigrantes que viven en el País Vasc |
| -0.033 | 0.00 | 956 | p3 | Y dentro de un año, ¿cómo crees que será la situació |
| -0.033 | 0.00 | 1000 | p9_7 | ¿Crees que los inmigrantes que viven en el País Vasc |
| -0.067 | 0.00 | 868 | p39_4 | Y en la misma escala, ¿dónde colocarías a los siguie |
| -0.071 | 0.00 | 853 | p39_5 | Y en la misma escala, ¿dónde colocarías a los siguie |
| nan | nan | 981 | p6_1 | Indica si en el último mes, y como consecuencia de t |
| nan | nan | 985 | p6_2 | Indica si en el último mes, y como consecuencia de t |
| nan | nan | 978 | p6_3 | Indica si en el último mes, y como consecuencia de t |
| nan | nan | 970 | p6_4 | Indica si en el último mes, y como consecuencia de t |
| nan | nan | 973 | p6_5 | Indica si en el último mes, y como consecuencia de t |
| nan | nan | 977 | p6_6 | Indica si en el último mes, y como consecuencia de t |
| nan | nan | 975 | p6_7 | Indica si en el último mes, y como consecuencia de t |
| nan | nan | 976 | p6_8 | Indica si en el último mes, y como consecuencia de t |
| nan | nan | 966 | p6_9 | Indica si en el último mes, y como consecuencia de t |
| nan | nan | 976 | p6_10 | Indica si en el último mes, y como consecuencia de t |
| nan | nan | 952 | p6_11 | Indica si en el último mes, y como consecuencia de t |
| nan | nan | 962 | p6_12 | Indica si en el último mes, y como consecuencia de t |
| nan | nan | 972 | p6_13 | Indica si en el último mes, y como consecuencia de t |