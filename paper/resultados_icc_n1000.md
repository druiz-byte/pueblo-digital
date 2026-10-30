# Contraste ICC (CIS 3575) — panel sintético vs dato real

Tanda A: `cis_icc_julio2026_A.json` · modelo `claude-haiku-4-5-20251001` · 1000 Personas.
Tanda B: `cis_icc_julio2026_B_sin_intermedia.json` · 1000 Personas.

`datos_reales` = submuestra País Vasco (n=133, ±8,5 p.p.); `datos_reales_espana` = muestra nacional (n=3.004, ±1,8 p.p.).

## DAM por ítem

| ítem | DAM vs CAE | moda CAE | unif. | DAM vs ESP | moda ESP | conc. panel | conc. real CAE | opciones |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| P3 | **17.8** | 18.6 | 18.9 | 24.6 | 25.4 | 98.4 | 62.8 | 2 de 4 |
| P12 | **16.6** | 27.8 | 12.8 | 19.3 | 30.4 | 77.7 | 44.4 | 3 de 4 |
| P8 | **16.8** | 29.1 | 11.6 | 14.4 | 24.1 | 50.0 | 41.8 | 3 de 4 |
| P17 | **14.8** | 14.9 | 22.9 | 12.0 | 12.3 | 99.2 | 70.2 | 3 de 4 |
| P18 | **66.1** | 4.0 | 40.4 | 66.1 | 7.8 | 99.7 | 94.0 | 2 de 3 |
| P10 | **19.6** | 15.3 | 22.2 | 12.8 | 21.9 | 52.4 | 69.3 | 2 de 4 |
| P15 | **46.1** | 15.3 | 22.1 | 45.7 | 17.2 | 96.5 | 69.3 | 4 de 4 |

**Concentración media: panel 82.0 · real CAE 64.5 (exceso +17.4 p.p.)**

## Distribuciones

**P3** · panel: Igual 98.4 · Peor 1.6
   real CAE: Igual 62.8 · Peor 20.5 · Mejor 16.0 · NS/NC 0.6

**P12** · panel: Igual 77.7 · Peor 21.3 · Mejor 1.0
   real CAE: Igual 44.4 · Mejor 31.2 · Peor 23.6 · NS/NC 0.8

**P8** · panel: Igual 50.0 · Peor 48.7 · No lo sé / prefiero no contestar 1.3
   real CAE: Peor 41.8 · Mejor 31.4 · Igual 23.3 · NS/NC 3.6

**P17** · panel: Subirá 99.2 · No lo sé / prefiero no contestar 0.7 · Se mantendrá 0.1
   real CAE: Subirá 70.2 · Se mantendrá 25.5 · Bajará 4.3 · NS/NC 0.0

**P18** · panel: No lo sé / prefiero no contestar 99.7 · No 0.3
   real CAE: No 94.0 · Sí 5.4 · NS/NC 0.6

**P10** · panel: Menores 52.4 · Iguales 47.6
   real CAE: Iguales 69.3 · Mayores 15.3 · Menores 13.1 · NS/NC 2.3

**P15** · panel: Menos 96.5 · No lo sé / prefiero no contestar 3.0 · Igual 0.3 · Más 0.2
   real CAE: Más 69.3 · Igual 23.4 · Menos 4.9 · NS/NC 2.4

## ¿Usa la Persona su perfil? (V de Cramér respuesta × perfil)

| ítem | voto | clase_social | nivel_estudios | grupo_edad | genero | euskera | provincia |
|---|---|---|---|---|---|---|---|
| P3 | 0.10 | 0.07 | 0.15 | 0.08 | 0.02 | 0.10 | 0.03 |
| P12 | 0.15 | 0.30 | 0.13 | 0.14 | 0.09 | 0.06 | 0.02 |
| P8 | 0.15 | 0.14 | 0.12 | 0.09 | 0.06 | 0.08 | 0.03 |
| P17 | 0.11 | 0.14 | 0.09 | 0.10 | 0.05 | 0.17 | 0.04 |
| P18 | 0.10 | 0.03 | 0.04 | 0.05 | 0.02 | 0.10 | 0.06 |
| P10 | 0.20 | 0.45 | 0.23 | 0.18 | 0.14 | 0.10 | 0.06 |
| P15 | 0.14 | 0.08 | 0.09 | 0.06 | 0.10 | 0.14 | 0.04 |

Referencia: en la réplica de Ikuspegi la V media con el voto fue 0,36; en la pregunta de impuestos fue 0 por varianza nula.

## Contraste A vs B — reparto Mejor/Peor (excluidas "Igual" y NS/NC)

| ítem | A: con intermedia | B: sin intermedia | real CAE | Δ A−B | NS/NC en B (real) |
|---|---|---|---|--:|---|
| P3 | Mejor 0.0 / Peor 100.0 | Mejor 17.3 / Peor 82.7 | Mejor 43.8 / Peor 56.2 | **17.3** | 50.4 (real 0.6) |
| P12 | Mejor 4.5 / Peor 95.5 | Mejor 66.9 / Peor 33.1 | Mejor 56.9 / Peor 43.1 | **62.5** | 28.0 (real 0.8) |
| P8 | Mejor 0.0 / Peor 100.0 | Mejor 3.1 / Peor 96.9 | Mejor 42.9 / Peor 57.1 | **3.1** | 34.5 (real 3.6) |
