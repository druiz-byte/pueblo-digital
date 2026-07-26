# PPI++ completo — sustitución ingenua vs PPI++ (152 preguntas)

- Predicciones: predicciones_deusto_full.json  ·  n etiquetado titular = 100
- **Sust. ingenua (DAM)** = error del panel usado como verdad (lo que da v2 sola).
- **PPI++ red. IC** = recorte medio del intervalo (eficiencia); estimación válida (cobertura ~95%).
- \* Bloque 7 = perfil inyectado (circular: validación, no ganancia).

| Bloque | Preg | Sust. ingenua DAM | PPI++ red. IC media | cobertura media |
|---|--:|--:|--:|--:|
| 1_situacion_econ | 26 | 13.5 | 0.7% | 87% |
| 2_bienestar_poli | 24 | 13.9 | 0.4% | 91% |
| 3_miedos | 7 | 17.0 | 0.3% | 89% |
| 4_turismo | 2 | 30.4 | 0.5% | 97% |
| 5_politica_democ | 60 | 10.5 | 2.6% | 92% |
| 6_geopolitica | 24 | 28.2 | 0.3% | 90% |
| 7_perfil_validac * | 9 | 14.7 | 18.3% | 86% |
| **GLOBAL** | 152 | **15.1** | **2.4%** | — |


## Detalle por pregunta

| Bloque | q | Tipo | Sust. ingenua (DAM p.p.) | PPI++ red. IC % | cobertura | corr |
|---|--:|---|--:|--:|--:|--:|
| 1_situacio | 0 | multi | 18.7 | 0.1 | 91% | — |
| 1_situacio | 1 | cat | 19.3 | 0.0 | 79% | — |
| 1_situacio | 2 | cat | 14.7 | 0.9 | 88% | — |
| 1_situacio | 3 | cat | 2.5 | 10.3 | 76% | — |
| 1_situacio | 4 | cat | 19.6 | 0.1 | 81% | — |
| 1_situacio | 5 | cat | 18.0 | 0.2 | 90% | — |
| 1_situacio | 6 | cat | 19.3 | 0.3 | 87% | — |
| 1_situacio | 7 | cat | 6.8 | 0.4 | 85% | — |
| 1_situacio | 8 | cat | 6.3 | 0.9 | 82% | — |
| 1_situacio | 9 | cat | 5.7 | 0.8 | 92% | — |
| 1_situacio | 10 | cat | 9.2 | 0.7 | 93% | — |
| 1_situacio | 11 | cat | 12.8 | 0.6 | 88% | — |
| 1_situacio | 12 | cat | 7.3 | 0.0 | 78% | — |
| 1_situacio | 13 | cat | 5.8 | 0.5 | 80% | — |
| 1_situacio | 14 | cat | 10.9 | 0.2 | 93% | — |
| 1_situacio | 15 | cat | 8.9 | 1.5 | 88% | — |
| 1_situacio | 16 | cat | 10.0 | -0.0 | 78% | — |
| 1_situacio | 17 | cat | 16.1 | 0.2 | 97% | — |
| 1_situacio | 18 | cat | 15.7 | 0.3 | 92% | — |
| 1_situacio | 19 | cat | 20.5 | 0.1 | 89% | — |
| 1_situacio | 20 | cat | 25.9 | 0.1 | 93% | — |
| 1_situacio | 21 | cat | 10.8 | 0.4 | 93% | — |
| 1_situacio | 22 | cat | 16.4 | 0.3 | 85% | — |
| 1_situacio | 23 | cat | 24.6 | 0.3 | 91% | — |
| 1_situacio | 24 | cat | 8.9 | 0.2 | 88% | — |
| 1_situacio | 25 | cat | 15.2 | 0.1 | 87% | — |
| 2_bienesta | 0 | escala | 12.9 | 0.1 | 100% | -0.04 |
| 2_bienesta | 1 | escala | 11.2 | 0.5 | 93% | +0.12 |
| 2_bienesta | 2 | escala | 10.5 | 0.4 | 87% | +0.07 |
| 2_bienesta | 3 | escala | 8.2 | 0.3 | 100% | +0.05 |
| 2_bienesta | 4 | escala | 11.9 | 0.1 | 100% | +0.03 |
| 2_bienesta | 5 | escala | 12.9 | 0.5 | 87% | +0.10 |
| 2_bienesta | 6 | escala | 10.8 | 0.5 | 80% | +0.12 |
| 2_bienesta | 7 | escala | 10.0 | 0.2 | 93% | +0.04 |
| 2_bienesta | 8 | escala | 11.3 | 0.1 | 100% | +0.00 |
| 2_bienesta | 9 | escala | 11.2 | 0.2 | 100% | +0.04 |
| 2_bienesta | 10 | escala | 5.6 | 1.8 | 80% | +0.21 |
| 2_bienesta | 11 | escala | 10.6 | 0.8 | 100% | +0.12 |
| 2_bienesta | 12 | escala | 10.9 | 0.6 | 100% | +0.09 |
| 2_bienesta | 13 | escala | 6.8 | 0.5 | 80% | +0.10 |
| 2_bienesta | 14 | escala | 10.3 | 0.1 | 93% | +0.07 |
| 2_bienesta | 15 | escala | 10.8 | 0.3 | 100% | +0.02 |
| 2_bienesta | 16 | cat | 4.0 | 1.1 | 69% | — |
| 2_bienesta | 17 | cat | 22.7 | 0.6 | 84% | — |
| 2_bienesta | 18 | cat | 18.4 | 0.6 | 98% | — |
| 2_bienesta | 19 | cat | 13.9 | 0.3 | 96% | — |
| 2_bienesta | 20 | cat | 22.5 | 0.6 | 93% | — |
| 2_bienesta | 21 | cat | 32.2 | -0.0 | 76% | — |
| 2_bienesta | 22 | cat | 39.2 | 0.3 | 87% | — |
| 2_bienesta | 23 | cat | 15.5 | 0.2 | 96% | — |
| 3_miedos.j | 0 | multi | 19.2 | 0.3 | 87% | — |
| 3_miedos.j | 1 | cat | 19.4 | 0.3 | 84% | — |
| 3_miedos.j | 2 | cat | 22.5 | 0.3 | 99% | — |
| 3_miedos.j | 3 | cat | 18.0 | 0.5 | 95% | — |
| 3_miedos.j | 4 | cat | 14.0 | 0.2 | 91% | — |
| 3_miedos.j | 5 | cat | 6.7 | 0.5 | 80% | — |
| 3_miedos.j | 6 | cat | 19.0 | 0.0 | 86% | — |
| 4_turismo. | 0 | cat | 28.9 | 0.9 | 99% | — |
| 4_turismo. | 1 | multi | 31.9 | 0.2 | 96% | — |
| 5_politica | 0 | cat | 15.8 | 1.3 | 89% | — |
| 5_politica | 1 | cat | 16.8 | 1.3 | 95% | — |
| 5_politica | 2 | escala | 10.4 | 0.3 | 100% | +0.06 |
| 5_politica | 3 | escala | 7.3 | 1.2 | 100% | +0.16 |
| 5_politica | 4 | escala | 12.4 | 0.2 | 100% | +0.01 |
| 5_politica | 5 | escala | 8.1 | 4.2 | 93% | +0.35 |
| 5_politica | 6 | escala | 10.9 | 1.0 | 87% | +0.15 |
| 5_politica | 7 | escala | 5.9 | 2.8 | 100% | +0.27 |
| 5_politica | 8 | escala | 9.6 | 2.1 | 100% | +0.26 |
| 5_politica | 9 | escala | 6.3 | 4.6 | 93% | +0.34 |
| 5_politica | 10 | escala | 7.9 | 1.8 | 100% | +0.25 |
| 5_politica | 11 | escala | 9.8 | 2.6 | 100% | +0.28 |
| 5_politica | 12 | escala | 4.2 | 8.9 | 100% | +0.52 |
| 5_politica | 13 | escala | 8.0 | 0.8 | 87% | +0.13 |
| 5_politica | 14 | escala | 9.6 | 0.6 | 67% | +0.11 |
| 5_politica | 15 | escala | 7.8 | 1.3 | 100% | +0.20 |
| 5_politica | 16 | escala | 11.1 | 1.8 | 100% | +0.23 |
| 5_politica | 17 | escala | 10.3 | 0.2 | 93% | +0.09 |
| 5_politica | 18 | escala | 8.7 | 2.2 | 100% | +0.23 |
| 5_politica | 19 | escala | 11.0 | 1.4 | 93% | +0.21 |
| 5_politica | 20 | escala | 8.7 | 0.7 | 80% | +0.13 |
| 5_politica | 21 | escala | 8.2 | 1.3 | 100% | +0.20 |
| 5_politica | 22 | escala | 13.6 | 0.5 | 100% | +0.11 |
| 5_politica | 23 | escala | 12.0 | 0.7 | 100% | +0.13 |
| 5_politica | 24 | cat | 7.0 | 3.0 | 88% | — |
| 5_politica | 25 | cat | 11.2 | 1.0 | 96% | — |
| 5_politica | 26 | multi | 27.5 | 0.9 | 82% | — |
| 5_politica | 27 | cat | 3.5 | 6.4 | 86% | — |
| 5_politica | 28 | cat | 6.3 | 6.3 | 85% | — |
| 5_politica | 29 | cat | 6.7 | 6.7 | 88% | — |
| 5_politica | 30 | cat | 9.1 | 2.0 | 93% | — |
| 5_politica | 31 | cat | 10.6 | 1.8 | 90% | — |
| 5_politica | 32 | cat | 11.8 | 0.8 | 79% | — |
| 5_politica | 33 | cat | 12.2 | 3.0 | 77% | — |
| 5_politica | 34 | cat | 13.9 | 1.7 | 95% | — |
| 5_politica | 35 | cat | 11.9 | 1.8 | 89% | — |
| 5_politica | 36 | cat | 9.7 | 2.4 | 100% | — |
| 5_politica | 37 | cat | 4.2 | 1.9 | 89% | — |
| 5_politica | 38 | cat | 10.1 | 2.8 | 93% | — |
| 5_politica | 39 | cat | 8.2 | 0.3 | 88% | — |
| 5_politica | 40 | cat | 29.1 | 2.6 | 96% | — |
| 5_politica | 41 | multi | 20.0 | 1.2 | 92% | — |
| 5_politica | 42 | cat | 13.1 | 0.4 | 75% | — |
| 5_politica | 43 | cat | 15.9 | 0.8 | 93% | — |
| 5_politica | 44 | escala | 3.7 | 22.6 | 93% | +0.85 |
| 5_politica | 45 | escala | 12.7 | 0.0 | 100% | -0.10 |
| 5_politica | 46 | escala | 10.3 | 0.2 | 93% | +0.05 |
| 5_politica | 47 | escala | 11.0 | 0.8 | 93% | +0.12 |
| 5_politica | 48 | escala | 11.7 | 0.6 | 87% | +0.09 |
| 5_politica | 49 | escala | 10.6 | 0.7 | 93% | +0.12 |
| 5_politica | 50 | escala | 9.7 | 0.6 | 67% | +0.08 |
| 5_politica | 51 | escala | 6.0 | 0.1 | 87% | +0.00 |
| 5_politica | 52 | escala | 3.7 | 35.5 | 100% | +0.97 |
| 5_politica | 53 | escala | 7.4 | 0.4 | 87% | +0.09 |
| 5_politica | 54 | escala | 10.5 | 0.9 | 100% | +0.09 |
| 5_politica | 55 | escala | 13.1 | 0.0 | 93% | -0.02 |
| 5_politica | 56 | escala | 8.6 | 0.1 | 67% | -0.01 |
| 5_politica | 57 | escala | 12.2 | 0.0 | 87% | -0.01 |
| 5_politica | 58 | escala | 9.3 | 0.5 | 100% | +0.13 |
| 5_politica | 59 | escala | 10.2 | 1.1 | 93% | +0.19 |
| 6_geopolit | 0 | cat | 32.5 | 0.4 | 93% | — |
| 6_geopolit | 1 | cat | 25.2 | 0.2 | 100% | — |
| 6_geopolit | 2 | cat | 24.2 | 2.0 | 100% | — |
| 6_geopolit | 3 | cat | 29.4 | 0.2 | 98% | — |
| 6_geopolit | 4 | cat | 20.9 | 0.3 | 91% | — |
| 6_geopolit | 5 | cat | 37.0 | 0.1 | 98% | — |
| 6_geopolit | 6 | cat | 19.6 | 0.1 | 91% | — |
| 6_geopolit | 7 | cat | 35.3 | -0.0 | 98% | — |
| 6_geopolit | 8 | cat | 20.2 | 0.1 | 96% | — |
| 6_geopolit | 9 | cat | 26.4 | 0.2 | 96% | — |
| 6_geopolit | 10 | cat | 44.3 | 0.0 | 96% | — |
| 6_geopolit | 11 | cat | 7.0 | 1.0 | 98% | — |
| 6_geopolit | 12 | cat | 46.2 | 0.1 | 93% | — |
| 6_geopolit | 13 | cat | 42.5 | 0.1 | 84% | — |
| 6_geopolit | 14 | cat | 16.6 | -0.0 | 80% | — |
| 6_geopolit | 15 | cat | 17.1 | -0.0 | 81% | — |
| 6_geopolit | 16 | cat | 28.1 | 0.1 | 77% | — |
| 6_geopolit | 17 | cat | 32.5 | 0.1 | 89% | — |
| 6_geopolit | 18 | cat | 26.2 | 0.4 | 99% | — |
| 6_geopolit | 19 | cat | 29.5 | 0.0 | 76% | — |
| 6_geopolit | 20 | cat | 30.2 | 0.4 | 80% | — |
| 6_geopolit | 21 | multi | 40.3 | 0.1 | 96% | — |
| 6_geopolit | 22 | multi | 18.9 | 0.2 | 72% | — |
| 6_geopolit | 23 | multi | 27.2 | 0.1 | 81% | — |
| 7_perfil_v * | 0 | cat | 8.7 | 8.7 | 82% | — |
| 7_perfil_v * | 1 | cat | 3.9 | 33.2 | 74% | — |
| 7_perfil_v * | 2 | cat | 2.5 | 40.8 | 100% | — |
| 7_perfil_v * | 3 | multi | 10.1 | 3.2 | 80% | — |
| 7_perfil_v * | 4 | cat | 37.4 | 0.6 | 93% | — |
| 7_perfil_v * | 5 | cat | 34.3 | 0.8 | 89% | — |
| 7_perfil_v * | 6 | cat | 32.8 | 0.9 | 100% | — |
| 7_perfil_v * | 7 | cat | 1.1 | 38.4 | 75% | — |
| 7_perfil_v * | 8 | cat | 1.2 | 38.5 | 82% | — |