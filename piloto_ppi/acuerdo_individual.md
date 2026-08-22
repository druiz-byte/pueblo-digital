# Acuerdo individual — persona real vs persona digital

Fichero de predicciones: `predicciones_deusto_full.json` · **n = 300 encuestados** emparejados 1:1 por `id`.

Mide si coincide **cada persona** con su gemelo digital (criterio 4 de Argyle,
'correspondencia de patrones'), no si coincide la distribución agregada.

`delta_vs_moda` = cuánto supera el panel al baseline de responder siempre la
categoría más frecuente. **Si es ≈0 o negativo, el perfil no aporta señal individual.**
## Resumen

- **Escalas 0-10** (54): Spearman medio **0.15** · MAE 2.04 puntos · dentro de ±1: 48%
  - ⚠ **Ese 0,15 incluye p36 (ideología, 0,83) y p38 (nacionalismo, 0,97), que son predictores
    inyectados en el prompt.** Excluyéndolos: **0,123** sobre 52 ítems. Y para compararlo con el
    techo hay que usar **Pearson**, no Spearman (`corr_max = √R²` acota Pearson): **0,123**.
    Ver `../paper/correccion_techo_global.md`.
- **Cat. ordinales** (48): kappa ponderado medio **0.100** · acierto 52% vs moda 56% (**delta -4.5**)
- **Cat. nominales** (41): kappa medio **0.231** · acierto 51% vs moda 49% (**delta +1.6**)

Referencia de kappa (Landis & Koch): <0 nulo · 0-0,20 leve · 0,21-0,40 aceptable ·
0,41-0,60 moderado · >0,60 sustancial.


## Escalas 0-10  (n=54 preguntas)

| pregunta | var | spearman | exacto_% | pm1_% | MAE | sesgo | kappa_w | base_moda_% | delta_vs_moda |
|---|---|---|---|---|---|---|---|---|---|
| Y en relación con el sentimiento nacionalista  | p38 | 0.97 | 61.65 | 97.37 | 0.43 | -0.30 | 0.96 | 19.92 | 41.73 |
| Cuando se habla de política se utilizan normal | p36 | 0.83 | 51.76 | 88.24 | 0.68 | -0.50 | 0.82 | 23.14 | 28.63 |
| ¿En qué medida confías en cada una de las sigu | p21_9 | 0.52 | 26.55 | 51.38 | 2.05 | -1.38 | 0.43 | 25.17 | 1.38 |
| ¿En qué medida confías en cada una de las sigu | p21_2 | 0.35 | 17.81 | 42.47 | 2.12 | -0.48 | 0.29 | 36.30 | -18.49 |
| ¿En qué medida confías en cada una de las sigu | p21_6 | 0.31 | 19.31 | 51.03 | 1.79 | 0.42 | 0.26 | 20.00 | -0.69 |
| ¿En qué medida confías en cada una de las sigu | p21_8 | 0.27 | 20.21 | 51.71 | 1.90 | 1.17 | 0.13 | 19.18 | 1.03 |
| ¿En qué medida confías en cada una de las sigu | p21_3 | 0.27 | 15.99 | 46.26 | 2.26 | 1.15 | 0.06 | 15.99 | 0.00 |
| ¿En qué medida confías en cada una de las sigu | p21_7 | 0.25 | 18.18 | 48.25 | 1.87 | 0.22 | 0.16 | 23.78 | -5.59 |
| ¿En qué medida confías en cada una de las sigu | p21_13 | 0.24 | 15.75 | 43.49 | 2.13 | -1.30 | 0.13 | 26.03 | -10.27 |
| ¿En qué medida confías en cada una de las sigu | p21_4 | 0.23 | 19.30 | 49.12 | 1.89 | 0.59 | 0.19 | 22.11 | -2.81 |
| ¿Qué valoración le das a cada uno de los sigui | p8_11 | 0.23 | 17.87 | 44.49 | 2.19 | 0.73 | 0.19 | 22.05 | -4.18 |
| ¿En qué medida confías en cada una de las sigu | p21_5 | 0.22 | 15.38 | 48.25 | 2.16 | 1.09 | 0.12 | 20.28 | -4.90 |
| ¿En qué medida confías en cada una de las sigu | p21_12 | 0.21 | 11.58 | 34.39 | 2.43 | -1.25 | 0.15 | 18.60 | -7.02 |
| ¿En qué medida confías en cada una de las sigu | p21_15 | 0.20 | 15.97 | 37.15 | 2.17 | -0.67 | 0.16 | 21.18 | -5.21 |
| Si tuvieras que valorar con una nota de 0 a 10 | p20_2 | 0.17 | 18.31 | 51.41 | 1.79 | 0.22 | 0.11 | 18.66 | -0.35 |
| ¿En qué medida confías en cada una de las sigu | p21_16 | 0.16 | 9.51 | 31.69 | 2.44 | -1.39 | 0.13 | 20.77 | -11.27 |
| Y en la misma escala, ¿dónde colocarías a los  | p37_6 | 0.16 | 22.85 | 60.67 | 1.46 | -0.36 | 0.05 | 26.59 | -3.75 |
| ¿En qué medida confías en cada una de las sigu | p21_20 | 0.16 | 13.84 | 33.91 | 2.66 | 2.14 | 0.04 | 16.96 | -3.11 |
| ¿En qué medida confías en cada una de las sigu | p21_18 | 0.15 | 10.31 | 39.52 | 2.27 | 0.91 | 0.13 | 17.53 | -7.22 |
| ¿Qué valoración le das a cada uno de los sigui | p8_12 | 0.15 | 18.61 | 55.47 | 1.82 | 0.76 | 0.05 | 21.17 | -2.55 |
| Y en la misma escala, ¿dónde colocarías a los  | p37_3 | 0.14 | 16.60 | 48.68 | 1.78 | -1.29 | 0.04 | 27.17 | -10.57 |
| ¿Qué valoración le das a cada uno de los sigui | p8_13 | 0.14 | 20.80 | 54.74 | 1.78 | 0.83 | 0.04 | 21.17 | -0.36 |
| ¿En qué medida confías en cada una de las sigu | p21_14 | 0.13 | 16.26 | 48.44 | 2.16 | 1.35 | 0.03 | 18.34 | -2.08 |
| ¿Qué valoración le das a cada uno de los sigui | p8_9 | 0.12 | 20.55 | 54.45 | 1.83 | 0.91 | 0.00 | 22.60 | -2.05 |
| Y en la misma escala, ¿dónde colocarías a los  | p37_5 | 0.12 | 22.62 | 55.56 | 1.59 | -1.04 | 0.06 | 21.43 | 1.19 |
| ¿En qué medida confías en cada una de las sigu | p21_10 | 0.12 | 21.53 | 57.64 | 1.61 | 0.13 | 0.10 | 24.31 | -2.78 |
| Y en la misma escala, ¿dónde colocarías a los  | p39_7 | 0.11 | 28.41 | 35.23 | 4.76 | 4.27 | 0.09 | 69.32 | -40.91 |
| ¿Qué valoración le das a cada uno de los sigui | p8_14 | 0.11 | 20.08 | 57.83 | 1.60 | -0.02 | 0.06 | 22.09 | -2.01 |
| Y en la misma escala, ¿dónde colocarías a los  | p39_2 | 0.11 | 11.15 | 39.23 | 2.35 | -1.01 | 0.08 | 40.38 | -29.23 |
| ¿Qué valoración le das a cada uno de los sigui | p8_7 | 0.11 | 18.82 | 49.83 | 1.80 | -0.01 | 0.06 | 20.56 | -1.74 |
| ¿Qué valoración le das a cada uno de los sigui | p8_6 | 0.10 | 13.85 | 45.95 | 2.20 | 1.57 | 0.03 | 20.27 | -6.42 |
| ¿En qué medida confías en cada una de las sigu | p21_11 | 0.10 | 11.86 | 44.75 | 1.95 | -0.24 | 0.06 | 20.34 | -8.47 |
| Y en la misma escala, ¿dónde colocarías a los  | p37_4 | 0.10 | 9.69 | 41.47 | 2.17 | -1.88 | 0.02 | 20.93 | -11.24 |
| ¿Qué valoración le das a cada uno de los sigui | p8_15 | 0.09 | 16.61 | 49.47 | 1.94 | 1.33 | 0.03 | 25.44 | -8.83 |
| ¿En qué medida confías en cada una de las sigu | p21_17 | 0.08 | 19.52 | 56.16 | 1.64 | -0.64 | 0.09 | 21.92 | -2.40 |
| Si tuvieras que valorar con una nota de 0 a 10 | p20_1 | 0.08 | 14.34 | 44.06 | 2.06 | 0.59 | 0.03 | 17.13 | -2.80 |
| ¿En qué medida confías en cada una de las sigu | p21_19 | 0.07 | 8.81 | 28.14 | 2.42 | -1.46 | 0.04 | 22.37 | -13.56 |
| Y en la misma escala, ¿dónde colocarías a los  | p37_7 | 0.07 | 44.15 | 83.77 | 1.23 | 0.47 | 0.00 | 73.58 | -29.43 |
| ¿Qué valoración le das a cada uno de los sigui | p8_10 | 0.07 | 17.01 | 44.44 | 1.97 | 0.01 | 0.02 | 18.75 | -1.74 |
| ¿Qué valoración le das a cada uno de los sigui | p8_4 | 0.06 | 19.79 | 49.65 | 1.86 | 0.35 | 0.03 | 21.18 | -1.39 |
| ¿En qué medida confías en cada una de las sigu | p21_1 | 0.06 | 9.59 | 27.74 | 2.66 | -1.44 | 0.01 | 20.21 | -10.62 |
| ¿Qué valoración le das a cada uno de los sigui | p8_2 | 0.06 | 20.42 | 53.98 | 1.81 | 0.79 | 0.04 | 21.45 | -1.04 |
| Y en la misma escala, ¿dónde colocarías a los  | p39_6 | 0.05 | 15.53 | 43.56 | 3.12 | 1.67 | 0.10 | 45.45 | -29.92 |
| Y en la misma escala, ¿dónde colocarías a los  | p39_1 | 0.03 | 15.00 | 44.23 | 2.09 | -1.11 | 0.07 | 26.54 | -11.54 |
| ¿Qué valoración le das a cada uno de los sigui | p8_3 | 0.02 | 22.79 | 56.62 | 1.55 | 0.08 | 0.04 | 24.63 | -1.84 |
| ¿Qué valoración le das a cada uno de los sigui | p8_5 | 0.02 | 16.43 | 40.91 | 2.07 | 0.54 | 0.01 | 18.18 | -1.75 |
| Y en la misma escala, ¿dónde colocarías a los  | p39_4 | 0.02 | 13.18 | 30.23 | 2.89 | -1.40 | -0.01 | 25.19 | -12.02 |
| ¿Qué valoración le das a cada uno de los sigui | p8_8 | 0.01 | 17.29 | 52.54 | 1.70 | -0.15 | 0.03 | 25.76 | -8.47 |
| ¿Qué valoración le das a cada uno de los sigui | p8_16 | 0.01 | 13.38 | 41.26 | 2.05 | -0.52 | 0.01 | 21.56 | -8.18 |
| Y en la misma escala, ¿dónde colocarías a los  | p39_5 | -0.01 | 10.98 | 30.59 | 2.48 | -1.48 | -0.01 | 27.06 | -16.08 |
| ¿Qué valoración le das a cada uno de los sigui | p8_1 | -0.01 | 16.44 | 42.95 | 2.30 | 1.54 | -0.01 | 15.77 | 0.67 |
| Y en la misma escala, ¿dónde colocarías a los  | p37_2 | -0.02 | 16.99 | 56.76 | 1.76 | -1.00 | 0.02 | 23.55 | -6.56 |
| Y en la misma escala, ¿dónde colocarías a los  | p39_3 | -0.05 | 5.73 | 25.19 | 2.64 | -1.86 | -0.01 | 24.81 | -19.08 |
| Y en la misma escala, ¿dónde colocarías a los  | p37_1 | -0.08 | 19.62 | 42.31 | 1.95 | -1.33 | -0.04 | 23.08 | -3.46 |

**Medias:** spearman=0.15 · exacto_%=18.64 · pm1_%=47.86 · MAE=2.04 · sesgo=0.01 · kappa_w=0.11 · base_moda_%=24.59 · delta_vs_moda=-5.95

## Categóricas ORDINALES  (n=48 preguntas)

| pregunta | var | spearman | exacto_% | pm1_% | MAE | sesgo | kappa_w | base_moda_% | delta_vs_moda |
|---|---|---|---|---|---|---|---|---|---|
| Indica si en el último mes, y como consecuenci | p6_9 | 0.86 | 91.41 | 98.28 | 0.10 | 0.08 | 0.11 | 92.44 | -1.03 |
| Indica si en el último mes, y como consecuenci | p6_4 | 0.71 | 83.62 | 93.52 | 0.23 | 0.10 | 0.13 | 87.03 | -3.41 |
| Indica si en el último mes, y como consecuenci | p6_8 | 0.69 | 88.51 | 95.95 | 0.16 | 0.15 | -0.00 | 88.85 | -0.34 |
| Indica si en el último mes, y como consecuenci | p6_3 | 0.68 | 88.59 | 94.97 | 0.16 | 0.15 | 0.08 | 89.26 | -0.67 |
| Indica si en el último mes, y como consecuenci | p6_12 | 0.64 | 87.71 | 92.49 | 0.20 | 0.20 | 0.00 | 87.71 | 0.00 |
| Indica si en el último mes, y como consecuenci | p6_5 | 0.62 | 83.56 | 95.55 | 0.21 | 0.11 | 0.24 | 86.64 | -3.08 |
| Indica si en el último mes, y como consecuenci | p6_11 | 0.57 | 85.26 | 91.23 | 0.24 | 0.21 | 0.17 | 85.61 | -0.35 |
| Indica tu grado de acuerdo con cada una de las | p26_2 | 0.53 | 43.67 | 88.65 | 0.69 | 0.10 | 0.54 | 34.06 | 9.61 |
| Indica tu grado de acuerdo con cada una de las | p26_3 | 0.53 | 39.53 | 81.01 | 0.82 | 0.45 | 0.52 | 32.56 | 6.98 |
| Y dentro de un año, ¿cómo crees que será la si | p3 | 0.45 | 74.77 | 100.00 | 0.25 | -0.05 | 0.03 | 75.23 | -0.45 |
| Indica tu grado de acuerdo con cada una de las | p26_1 | 0.44 | 41.20 | 81.55 | 0.82 | -0.44 | 0.45 | 31.33 | 9.87 |
| Indica si en el último mes, y como consecuenci | p6_10 | 0.39 | 71.96 | 86.15 | 0.42 | 0.32 | 0.05 | 75.00 | -3.04 |
| ¿En qué medida consideras necesario un nuevo e | p23 | 0.37 | 37.44 | 86.78 | 0.76 | -0.06 | 0.39 | 38.33 | -0.88 |
| ¿Y cómo crees que será la situación política d | p19 | 0.28 | 43.31 | 96.06 | 0.61 | 0.44 | 0.01 | 75.98 | -32.68 |
| ¿Crees que los inmigrantes que viven en el Paí | p9_3 | 0.22 | 62.67 | 83.00 | 0.54 | -0.44 | -0.01 | 65.00 | -2.33 |
| ¿Crees que es probable que en los próximos sei | p5 | 0.21 | 47.65 | 90.60 | 0.64 | 0.56 | -0.04 | 49.66 | -2.01 |
| En qué medida estás de acuerdo con cada una de | p12_1 | 0.21 | 27.08 | 69.10 | 1.10 | 0.97 | 0.06 | 37.15 | -10.07 |
| ¿Cuál es tu nivel de conocimiento del euskera? | p44_3 | 0.19 | 47.67 | 83.00 | 0.69 | 0.69 | 0.15 | 45.67 | 2.00 |
| Indica si en el último mes, y como consecuenci | p6_6 | 0.18 | 54.05 | 87.84 | 0.58 | 0.05 | 0.19 | 67.57 | -13.51 |
| En qué medida estás de acuerdo con cada una de | p12_2 | 0.18 | 36.46 | 72.56 | 0.95 | 0.90 | 0.08 | 33.57 | 2.89 |
| ¿Cuál es tu nivel de conocimiento del euskera? | p44_1 | 0.16 | 40.00 | 80.00 | 0.80 | 0.80 | 0.13 | 38.33 | 1.67 |
| ¿Crees que los inmigrantes que viven en el Paí | p9_1 | 0.16 | 60.33 | 99.33 | 0.40 | -0.05 | 0.20 | 57.00 | 3.33 |
| Indica si en el último mes, y como consecuenci | p6_2 | 0.15 | 33.33 | 73.06 | 0.94 | 0.68 | 0.10 | 48.15 | -14.81 |
| Indica si en el último mes, y como consecuenci | p6_13 | 0.14 | 34.13 | 78.84 | 0.87 | -0.33 | 0.08 | 60.07 | -25.94 |
| Indica si en el último mes, y como consecuenci | p6_7 | 0.14 | 62.96 | 77.78 | 0.59 | 0.42 | 0.10 | 64.98 | -2.02 |
| Indica tu grado de acuerdo con cada una de las | p29_2 | 0.13 | 36.88 | 81.21 | 0.84 | -0.52 | 0.08 | 39.01 | -2.13 |
| ¿Cuál es tu nivel de conocimiento del euskera? | p44_2 | 0.13 | 48.33 | 82.00 | 0.70 | 0.69 | 0.13 | 46.33 | 2.00 |
| ¿Con qué frecuencia has pasado por los siguien | p7_5 | 0.12 | 63.27 | 90.82 | 0.49 | 0.49 | 0.04 | 62.93 | 0.34 |
| ¿Con qué frecuencia has pasado por los siguien | p7_7 | 0.12 | 44.07 | 87.46 | 0.73 | 0.20 | 0.06 | 56.61 | -12.54 |
| Indica tu grado de acuerdo con cada una de las | p26_4 | 0.10 | 39.53 | 81.03 | 0.86 | -0.08 | -0.07 | 51.38 | -11.86 |
| ¿En qué medida ha aumentado en los últimos año | p13 | 0.10 | 35.00 | 82.00 | 0.85 | -0.29 | 0.07 | 37.33 | -2.33 |
| ¿Con qué frecuencia has pasado por los siguien | p7_6 | 0.10 | 33.90 | 89.15 | 0.77 | -0.07 | 0.07 | 40.34 | -6.44 |
| ¿Crees que los inmigrantes que viven en el Paí | p9_5 | 0.10 | 47.67 | 94.00 | 0.58 | 0.07 | 0.11 | 66.00 | -18.33 |
| ¿Con qué frecuencia has pasado por los siguien | p7_4 | 0.09 | 39.39 | 86.87 | 0.74 | -0.25 | 0.14 | 43.77 | -4.38 |
| En qué medida estás de acuerdo con cada una de | p12_3 | 0.08 | 26.12 | 64.93 | 1.21 | 1.04 | 0.08 | 37.69 | -11.57 |
| ¿En qué medida crees que el aumento de turista | p16 | 0.07 | 27.05 | 79.00 | 0.94 | -0.75 | 0.02 | 42.35 | -15.30 |
| ¿Con qué frecuencia has pasado por los siguien | p7_8 | 0.04 | 37.25 | 84.56 | 0.78 | 0.00 | 0.01 | 38.26 | -1.01 |
| ¿Con qué frecuencia has pasado por los siguien | p7_2 | 0.04 | 44.11 | 90.57 | 0.65 | 0.03 | 0.09 | 45.12 | -1.01 |
| Indica si en el último mes, y como consecuenci | p6_1 | 0.02 | 61.07 | 74.83 | 0.64 | 0.55 | 0.05 | 61.41 | -0.34 |
| ¿Con qué frecuencia has pasado por los siguien | p7_1 | -0.00 | 45.42 | 90.17 | 0.66 | 0.22 | 0.03 | 48.81 | -3.39 |
| ¿Crees que los inmigrantes que viven en el Paí | p9_6 | -0.01 | 54.33 | 100.00 | 0.46 | 0.41 | 0.00 | 54.33 | 0.00 |
| ¿Cómo calificarías la situación política gener | p18 | -0.01 | 44.19 | 94.76 | 0.61 | 0.26 | 0.09 | 46.07 | -1.87 |
| ¿Cómo calificarías la situación económica del  | p2 | -0.01 | 40.94 | 96.31 | 0.63 | 0.41 | 0.02 | 47.65 | -6.71 |
| ¿Con qué frecuencia has pasado por los siguien | p7_3 | -0.04 | 34.58 | 93.56 | 0.72 | -0.28 | -0.00 | 51.19 | -16.61 |
| ¿Crees que los inmigrantes que viven en el Paí | p9_2 | -0.08 | 59.33 | 86.33 | 0.54 | -0.45 | -0.01 | 59.33 | 0.00 |
| ¿Crees que los inmigrantes que viven en el Paí | p9_7 | -0.09 | 28.00 | 92.33 | 0.80 | -0.22 | -0.03 | 43.33 | -15.33 |
| ¿Crees que los inmigrantes que viven en el Paí | p9_4 | -0.22 | 66.33 | 76.33 | 0.57 | -0.30 | 0.09 | 69.00 | -2.67 |
| Indica tu grado de acuerdo con cada una de las | p29_1 | -0.28 | 67.61 | 83.80 | 0.59 | -0.10 | -0.01 | 73.94 | -6.34 |

**Medias:** spearman=0.21 · exacto_%=51.90 · pm1_%=86.65 · MAE=0.63 · sesgo=0.15 · kappa_w=0.10 · base_moda_%=56.45 · delta_vs_moda=-4.54

## Categóricas NOMINALES  (n=41 preguntas)

| pregunta | var | exacto_% | kappa | base_moda_% | delta_vs_moda |
|---|---|---|---|---|---|
| ¿Cómo te consideras en materia religiosa? | p41 | 100.00 | 1.00 | 42.07 | 57.93 |
| ¿Dónde has nacido? | p42 | 100.00 | 1.00 | 80.33 | 19.67 |
| Pensando en las últimas elecciones autonómicas | p45 | 100.00 | 1.00 | 25.37 | 74.63 |
| ¿Y a qué partido habías votado en las eleccion | p46 | 99.26 | 0.99 | 25.56 | 73.70 |
| ¿En cuál de las siguientes situaciones te encu | p4 | 75.33 | 0.65 | 46.00 | 29.33 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_7 | 69.33 | 0.02 | 69.33 | 0.00 |
| ¿Qué partido es el que está más capacitado par | p25_2 | 69.19 | 0.56 | 45.93 | 23.26 |
| ¿Qué partido es el que está más capacitado par | p25_1 | 68.31 | 0.58 | 33.10 | 35.21 |
| ¿Qué partido es el que está más capacitado par | p25_3 | 67.06 | 0.55 | 37.06 | 30.00 |
| ¿Cómo crees que la guerra en Oriente Medio (en | p31_1 | 65.84 | 0.00 | 65.84 | 0.00 |
| ¿Has descartado o modificado un viaje en los ú | p14 | 65.67 | 0.08 | 71.00 | -5.33 |
| ¿Cómo crees que la guerra en Oriente Medio (en | p31_2 | 64.77 | 0.00 | 64.77 | 0.00 |
| ¿Qué partido es el que está más capacitado par | p25_6 | 64.71 | 0.20 | 62.75 | 1.96 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_12 | 60.41 | 0.19 | 59.04 | 1.37 |
| ¿Qué partido es el que está más capacitado par | p25_9 | 58.33 | 0.28 | 44.27 | 14.06 |
| ¿Qué partido es el que está más capacitado par | p25_7 | 57.67 | 0.33 | 45.40 | 12.27 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_5 | 57.33 | 0.07 | 56.00 | 1.33 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_4 | 55.33 | 0.02 | 54.67 | 0.67 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_3 | 54.33 | 0.17 | 45.00 | 9.33 |
| ¿Qué nivel de estudios has terminado? | p40 | 54.00 | 0.45 | 21.00 | 33.00 |
| Hay distintas formas de organización territori | p22 | 52.73 | 0.30 | 40.62 | 12.11 |
| ¿Qué partido es el que está más capacitado par | p25_5 | 48.54 | 0.26 | 46.78 | 1.75 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_2 | 48.33 | 0.03 | 47.67 | 0.67 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_8 | 47.33 | 0.00 | 47.33 | 0.00 |
| ¿Crees que dentro de 10 años será más fácil ac | p10 | 46.49 | 0.08 | 42.80 | 3.69 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_9 | 45.33 | 0.02 | 51.67 | -6.33 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_10 | 44.00 | 0.04 | 55.00 | -11.00 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_1 | 41.33 | 0.02 | 46.33 | -5.00 |
| ¿Cuál de las siguientes afirmaciones sobre los | p27 | 40.47 | 0.15 | 49.50 | -9.03 |
| ¿Qué partido es el que está más capacitado par | p25_8 | 37.08 | 0.21 | 28.65 | 8.43 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_14 | 36.00 | -0.00 | 59.00 | -23.00 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_11 | 31.33 | -0.02 | 57.67 | -26.33 |
| ¿Qué partido es el que está más capacitado par | p25_4 | 28.68 | 0.15 | 33.82 | -5.15 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_6 | 27.67 | -0.00 | 64.00 | -36.33 |
| Si hoy tuvieras que señalar a los aliados y lo | p30_13 | 27.00 | 0.02 | 66.33 | -39.33 |
| ¿Crees que las medidas que ha tomado o que pue | p32_1 | 21.00 | 0.04 | 26.00 | -5.00 |
| ¿Cuál fue la principal razón? | p15 | 16.28 | 0.00 | 43.02 | -26.74 |
| ¿Cómo crees que la guerra en Oriente Medio (en | p31_4 | 15.69 | 0.00 | 52.19 | -36.50 |
| ¿Cómo crees que la guerra en Oriente Medio (en | p31_3 | 14.23 | 0.01 | 56.58 | -42.35 |
| ¿Crees que las medidas que ha tomado o que pue | p32_3 | 8.33 | -0.02 | 60.00 | -51.67 |
| ¿Crees que las medidas que ha tomado o que pue | p32_2 | 8.00 | -0.01 | 57.33 | -49.33 |

**Medias:** exacto_%=51.04 · kappa=0.23 · base_moda_%=49.43 · delta_vs_moda=1.61

## Multi-respuesta  (n=9 preguntas)

| pregunta | var | jaccard | F1 |
|---|---|---|---|
| ¿Con quién vives en la actualidad? Indica toda | None | 0.64 | 0.69 |
| ¿Qué papel crees que deben tener las potencias | None | 0.52 | 0.62 |
| ¿A cuál de los siguientes partidos no votarías | None | 0.46 | 0.55 |
| ¿Crees que el turismo tiene alguno de los sigu | None | 0.46 | 0.55 |
| Cuál de las siguientes medidas te gustaría que | None | 0.33 | 0.44 |
| ¿De las siguientes medidas cuales crees que se | None | 0.33 | 0.45 |
| ¿Cuáles crees que son las principales amenazas | None | 0.27 | 0.36 |
| Pensando en los problemas globales actuales, i | None | 0.23 | 0.35 |
| En estos momentos, ¿cuáles crees que son los t | None | 0.09 | 0.15 |

**Medias:** jaccard=0.37 · F1=0.46
