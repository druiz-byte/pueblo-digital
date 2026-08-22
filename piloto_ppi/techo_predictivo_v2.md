# Techo predictivo v2 (CORREGIDO) — Deustobarómetro verano 2026

> **Sustituye a `techo_predictivo.md`, que contenía un error de mapeo.** Ver
> `paper/incidencia_mapeo_idx_real.md`. Cambios de método respecto a la v1:
> (1) mapeo etiqueta→opción corregido; (2) **semilla por ítem** (el resultado de una
> pregunta ya no depende de cuántas se evaluaron antes); (3) **CV 5-fold repetida 20
> veces**, se reporta la desviación.

## Resumen

- **Escalas y ordinales (100 preguntas):** R² medio OOS **0.072** → **corr máxima media 0.22**
  - mediana 0.048 · p90 0.178 · máx 0.394
  - preguntas con R² ≤ 0: **15/100**
  - **sd media del R² entre repeticiones de CV: 0.013** — comparable a la propia señal en los ítems de techo bajo; por eso hay que repetir la CV.
- **Nominales (35):** acierto 56 % vs moda 49 % (**+7.9 p.p.**)

## Efecto del arreglo (mismo método, sólo cambia el mapeo)

| | antes (bug) | después |
|---|--:|--:|
| R² medio | 0.0789 | 0.0718 |
| corr máxima | 0.240 | 0.225 |
| ítems válidos | 87 | 100 |
| ítems con R² ≤ 0 | 11 | 15 |
| Δ nominales vs moda | +7.53 | +7.88 |

## Techo por bloque (escalas + ordinales)

| bloque | preg | R² medio | corr máx |
|---|--:|--:|--:|
| barometro_digital_1_situacion_econ | 24 | 0.027 | 0.14 |
| barometro_digital_2_bienestar_poli | 23 | 0.031 | 0.16 |
| barometro_digital_3_miedos.json | 4 | 0.043 | 0.17 |
| barometro_digital_4_turismo.json | 1 | 0.064 | 0.25 |
| barometro_digital_5_politica_democ | 45 | 0.100 | 0.28 |
| barometro_digital_7_perfil_validac | 3 | 0.370 | 0.61 |

## Preguntas ordenadas por techo

| R² | ±sd | corr máx | n | var | pregunta |
|--:|--:|--:|--:|---|---|
| 0.394 | 0.006 | 0.63 | 1000 | p44_1 | ¿Cuál es tu nivel de conocimiento del euskera?: Le |
| 0.365 | 0.008 | 0.60 | 1000 | p44_2 | ¿Cuál es tu nivel de conocimiento del euskera?: Es |
| 0.353 | 0.006 | 0.59 | 1000 | p44_3 | ¿Cuál es tu nivel de conocimiento del euskera?: Co |
| 0.336 | 0.008 | 0.58 | 887 | p26_3 | Indica tu grado de acuerdo con cada una de las sig |
| 0.335 | 0.009 | 0.58 | 976 | p21_9 | ¿En qué medida confías en cada una de las siguient |
| 0.281 | 0.012 | 0.53 | 834 | p26_1 | Indica tu grado de acuerdo con cada una de las sig |
| 0.239 | 0.011 | 0.49 | 805 | p26_2 | Indica tu grado de acuerdo con cada una de las sig |
| 0.199 | 0.010 | 0.45 | 962 | p21_16 | ¿En qué medida confías en cada una de las siguient |
| 0.196 | 0.010 | 0.44 | 979 | p21_2 | ¿En qué medida confías en cada una de las siguient |
| 0.182 | 0.013 | 0.43 | 880 | p39_6 | Y en la misma escala, ¿dónde colocarías a los sigu |
| 0.177 | 0.013 | 0.42 | 979 | p21_3 | ¿En qué medida confías en cada una de las siguient |
| 0.174 | 0.014 | 0.42 | 959 | p21_4 | ¿En qué medida confías en cada una de las siguient |
| 0.171 | 0.014 | 0.41 | 885 | p39_7 | Y en la misma escala, ¿dónde colocarías a los sigu |
| 0.168 | 0.006 | 0.41 | 969 | p21_15 | ¿En qué medida confías en cada una de las siguient |
| 0.165 | 0.009 | 0.41 | 978 | p21_6 | ¿En qué medida confías en cada una de las siguient |
| 0.149 | 0.009 | 0.39 | 800 | p23 | ¿En qué medida consideras necesario un nuevo estat |
| 0.145 | 0.013 | 0.38 | 952 | p6_11 | Indica si en el último mes, y como consecuencia de |
| 0.140 | 0.010 | 0.37 | 977 | p21_13 | ¿En qué medida confías en cada una de las siguient |
| 0.140 | 0.012 | 0.37 | 966 | p21_7 | ¿En qué medida confías en cada una de las siguient |
| 0.134 | 0.011 | 0.37 | 925 | p12_3 | En qué medida estás de acuerdo con cada una de las |
| 0.127 | 0.012 | 0.36 | 978 | p21_1 | ¿En qué medida confías en cada una de las siguient |
| 0.126 | 0.012 | 0.36 | 957 | p20_2 | Si tuvieras que valorar con una nota de 0 a 10 la  |
| 0.118 | 0.016 | 0.34 | 905 | p37_6 | Y en la misma escala, ¿dónde colocarías a los sigu |
| 0.116 | 0.009 | 0.34 | 956 | p18 | ¿Cómo calificarías la situación política general d |
| 0.113 | 0.011 | 0.34 | 932 | p8_11 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.105 | 0.011 | 0.32 | 975 | p21_18 | ¿En qué medida confías en cada una de las siguient |
| 0.102 | 0.011 | 0.32 | 982 | p21_8 | ¿En qué medida confías en cada una de las siguient |
| 0.098 | 0.012 | 0.31 | 966 | p21_14 | ¿En qué medida confías en cada una de las siguient |
| 0.089 | 0.009 | 0.30 | 974 | p21_20 | ¿En qué medida confías en cada una de las siguient |
| 0.088 | 0.010 | 0.30 | 960 | p21_10 | ¿En qué medida confías en cada una de las siguient |
| 0.079 | 0.009 | 0.28 | 981 | p21_19 | ¿En qué medida confías en cada una de las siguient |
| 0.079 | 0.010 | 0.28 | 962 | p8_2 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.076 | 0.014 | 0.28 | 930 | p8_3 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.072 | 0.006 | 0.27 | 962 | p21_5 | ¿En qué medida confías en cada una de las siguient |
| 0.071 | 0.012 | 0.27 | 962 | p6_12 | Indica si en el último mes, y como consecuencia de |
| 0.071 | 0.012 | 0.27 | 886 | p8_14 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.066 | 0.016 | 0.26 | 970 | p6_4 | Indica si en el último mes, y como consecuencia de |
| 0.064 | 0.014 | 0.25 | 941 | p16 | ¿En qué medida crees que el aumento de turistas af |
| 0.063 | 0.014 | 0.25 | 971 | p8_9 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.060 | 0.013 | 0.25 | 985 | p8_8 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.060 | 0.014 | 0.25 | 986 | p8_6 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.058 | 0.010 | 0.24 | 980 | p7_3 | ¿Con qué frecuencia has pasado por los siguientes  |
| 0.057 | 0.016 | 0.24 | 940 | p8_12 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.056 | 0.011 | 0.24 | 970 | p8_10 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.054 | 0.012 | 0.23 | 979 | p7_6 | ¿Con qué frecuencia has pasado por los siguientes  |
| 0.053 | 0.015 | 0.23 | 955 | p8_5 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.053 | 0.013 | 0.23 | 956 | p21_12 | ¿En qué medida confías en cada una de las siguient |
| 0.050 | 0.012 | 0.22 | 958 | p8_7 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.049 | 0.011 | 0.22 | 984 | p7_8 | ¿Con qué frecuencia has pasado por los siguientes  |
| 0.049 | 0.017 | 0.22 | 901 | p37_7 | Y en la misma escala, ¿dónde colocarías a los sigu |
| 0.047 | 0.012 | 0.22 | 939 | p8_16 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.042 | 0.017 | 0.20 | 978 | p7_7 | ¿Con qué frecuencia has pasado por los siguientes  |
| 0.040 | 0.009 | 0.20 | 985 | p7_2 | ¿Con qué frecuencia has pasado por los siguientes  |
| 0.040 | 0.013 | 0.20 | 985 | p2 | ¿Cómo calificarías la situación económica del País |
| 0.038 | 0.012 | 0.19 | 928 | p8_13 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.037 | 0.010 | 0.19 | 981 | p6_1 | Indica si en el último mes, y como consecuencia de |
| 0.035 | 0.016 | 0.19 | 870 | p37_5 | Y en la misma escala, ¿dónde colocarías a los sigu |
| 0.035 | 0.016 | 0.19 | 981 | p7_5 | ¿Con qué frecuencia has pasado por los siguientes  |
| 0.032 | 0.012 | 0.18 | 972 | p8_4 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.029 | 0.017 | 0.17 | 890 | p37_1 | Y en la misma escala, ¿dónde colocarías a los sigu |
| 0.028 | 0.012 | 0.17 | 930 | p19 | ¿Y cómo crees que será la situación política del P |
| 0.028 | 0.013 | 0.17 | 959 | p20_1 | Si tuvieras que valorar con una nota de 0 a 10 la  |
| 0.027 | 0.016 | 0.16 | 881 | p39_1 | Y en la misma escala, ¿dónde colocarías a los sigu |
| 0.026 | 0.012 | 0.16 | 972 | p6_13 | Indica si en el último mes, y como consecuencia de |
| 0.026 | 0.014 | 0.16 | 881 | p37_2 | Y en la misma escala, ¿dónde colocarías a los sigu |
| 0.025 | 0.014 | 0.16 | 931 | p12_1 | En qué medida estás de acuerdo con cada una de las |
| 0.025 | 0.012 | 0.16 | 982 | p21_11 | ¿En qué medida confías en cada una de las siguient |
| 0.025 | 0.012 | 0.16 | 930 | p29_2 | Indica tu grado de acuerdo con cada una de las sig |
| 0.023 | 0.014 | 0.15 | 987 | p7_4 | ¿Con qué frecuencia has pasado por los siguientes  |
| 0.021 | 0.022 | 0.14 | 881 | p37_4 | Y en la misma escala, ¿dónde colocarías a los sigu |
| 0.020 | 0.012 | 0.14 | 941 | p29_1 | Indica tu grado de acuerdo con cada una de las sig |
| 0.020 | 0.016 | 0.14 | 973 | p6_5 | Indica si en el último mes, y como consecuencia de |
| 0.014 | 0.015 | 0.12 | 892 | p37_3 | Y en la misma escala, ¿dónde colocarías a los sigu |
| 0.014 | 0.010 | 0.12 | 990 | p8_1 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.012 | 0.014 | 0.11 | 953 | p8_15 | ¿Qué valoración le das a cada uno de los siguiente |
| 0.011 | 0.015 | 0.10 | 877 | p39_3 | Y en la misma escala, ¿dónde colocarías a los sigu |
| 0.010 | 0.019 | 0.10 | 890 | p26_4 | Indica tu grado de acuerdo con cada una de las sig |
| 0.009 | 0.016 | 0.10 | 592 | p5 | ¿Crees que es probable que en los próximos seis me |
| 0.009 | 0.013 | 0.10 | 1000 | p13 | ¿En qué medida ha aumentado en los últimos años tu |
| 0.009 | 0.015 | 0.09 | 976 | p6_8 | Indica si en el último mes, y como consecuencia de |
| 0.007 | 0.012 | 0.08 | 975 | p21_17 | ¿En qué medida confías en cada una de las siguient |
| 0.006 | 0.015 | 0.08 | 881 | p39_2 | Y en la misma escala, ¿dónde colocarías a los sigu |
| 0.006 | 0.014 | 0.08 | 976 | p6_10 | Indica si en el último mes, y como consecuencia de |
| 0.005 | 0.014 | 0.07 | 920 | p12_2 | En qué medida estás de acuerdo con cada una de las |
| 0.000 | 0.020 | 0.01 | 966 | p6_9 | Indica si en el último mes, y como consecuencia de |
| -0.004 | 0.013 | 0.00 | 977 | p6_6 | Indica si en el último mes, y como consecuencia de |
| -0.007 | 0.011 | 0.00 | 981 | p7_1 | ¿Con qué frecuencia has pasado por los siguientes  |
| -0.009 | 0.011 | 0.00 | 985 | p6_2 | Indica si en el último mes, y como consecuencia de |
| -0.011 | 0.014 | 0.00 | 975 | p6_7 | Indica si en el último mes, y como consecuencia de |
| -0.013 | 0.011 | 0.00 | 1000 | p9_5 | ¿Crees que los inmigrantes que viven en el País Va |
| -0.019 | 0.013 | 0.00 | 1000 | p9_3 | ¿Crees que los inmigrantes que viven en el País Va |
| -0.022 | 0.013 | 0.00 | 1000 | p9_4 | ¿Crees que los inmigrantes que viven en el País Va |
| -0.024 | 0.014 | 0.00 | 1000 | p9_2 | ¿Crees que los inmigrantes que viven en el País Va |
| -0.026 | 0.014 | 0.00 | 1000 | p9_6 | ¿Crees que los inmigrantes que viven en el País Va |
| -0.026 | 0.015 | 0.00 | 1000 | p9_7 | ¿Crees que los inmigrantes que viven en el País Va |
| -0.028 | 0.010 | 0.00 | 956 | p3 | Y dentro de un año, ¿cómo crees que será la situac |
| -0.029 | 0.013 | 0.00 | 978 | p6_3 | Indica si en el último mes, y como consecuencia de |
| -0.034 | 0.015 | 0.00 | 853 | p39_5 | Y en la misma escala, ¿dónde colocarías a los sigu |
| -0.039 | 0.015 | 0.00 | 1000 | p9_1 | ¿Crees que los inmigrantes que viven en el País Va |
| -0.073 | 0.015 | 0.00 | 868 | p39_4 | Y en la misma escala, ¿dónde colocarías a los sigu |