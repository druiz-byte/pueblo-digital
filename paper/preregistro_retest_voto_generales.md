# Preregistro — 3ª ronda test-retest: voto en generales (29-nov-2026)

**Escrito el 2026-10-22, ANTES de lanzar la 3ª ronda (prevista ~1-nov-2026).** No modificar tras ver los datos; los añadidos van en una addenda fechada.

## Diseño
- Rondas previas: R1 `encuesta_2026-10-13_134729.json` (texto sin prefijo) · R2 `encuesta_2026-10-22_172153.json` (texto con «P1.»).
- R3: **texto idéntico a R2**, mismo modelo `claude-haiku-4-5-20251001`, panel v1, 1.000 Personas, sin `SURVEY_TEMPERATURE` (1,0 por defecto), modo de letra de ejemplo por defecto.
- Línea base observada R1→R2: estabilidad individual 89,2 % · kappa 0,86 · PNV sale 34/entra 13 (McNemar p=0,003) · PSE entra 26/sale 5 (p<0,001) · Stuart-Maxwell χ²=23,7, gl 8, p=0,003.

## Hipótesis rivales
- **H0 Ruido puro:** R1 y R2 son la misma distribución y la asimetría fue un falso positivo. R3 cae cerca del punto medio; R3 vs R1 y R3 vs R2 simétricos.
- **H1 Efecto del prefijo «P1.»:** R3 ≈ R2. R3 vs R2 simétrico; R3 vs R1 reproduce la asimetría PNV→PSE.
- **H2 Inestabilidad del sistema (deriva de API):** R3 se separa de R2 de forma asimétrica (Stuart-Maxwell R3 vs R2 p<0,01) o la estabilidad R3–R2 cae por debajo del 85 %.

## Apuestas (marginales, %)
| Opción | R1 | R2 | Si H0 | Si H1 | **Apuesta central** | Rango 95 % |
|---|--:|--:|--:|--:|--:|--:|
| Indeciso | 33,3 | 31,8 | 32,6 | 31,8 | **32,3** | 30,8–33,8 |
| No votaré | 23,4 | 23,8 | 23,6 | 23,8 | **23,7** | 22,7–24,7 |
| EH Bildu | 19,0 | 19,5 | 19,3 | 19,5 | **19,4** | 18,7–20,1 |
| PNV/EAJ | 10,8 | 8,7 | 9,8 | 8,7 | **9,3** | 8,3–10,3 |
| PSE | 7,0 | 9,1 | 8,1 | 9,1 | **8,6** | 7,6–9,6 |
| PP | 4,3 | 5,1 | 4,7 | 5,1 | **4,9** | 4,3–5,5 |
| Elkarrekin Podemos | 2,0 | 1,8 | 1,9 | 1,8 | **1,9** | 1,5–2,3 |
| Sumar | 0,1 | 0,2 | 0,15 | 0,2 | **0,2** | 0,0–0,5 |
| VOX | 0,1 | 0,0 | 0,05 | 0,0 | **0,0** | 0,0–0,3 |

Apuesta central = punto intermedio entre H0 y H1 (no tenemos preferencia fuerte). Rangos: ±2 DE del cambio neto esperado por ruido, estimado del nº de Personas que cruzaron cada opción entre R1 y R2.

## Apuestas estructurales
1. Estabilidad individual R3–R2: **89 %** (87–91). Kappa ≈ 0,86.
2. Lealtad del recuerdo EH Bildu, PSE-EE y PP: **≥ 98 %** (fue 100 % en R1 y R2).
3. La inestabilidad se concentra en el recuerdo PNV: estabilidad de ese grupo **65–75 %**; el resto de grupos ≥ 83 %.
4. Recuerdo PNV que vota PNV en generales: **45–58 %**.
5. VOX + Sumar juntos **≤ 0,5 %**.

## Regla de decisión
- **H1** si Stuart-Maxwell R3 vs R1 p<0,05 **y** R3 vs R2 p≥0,05 **y** estabilidad(R3,R2) − estabilidad(R3,R1) ≥ +2 p.p.
- **H0** si los dos contrastes dan p≥0,05 y PNV ∈ [9,2; 10,3].
- **H2** si Stuart-Maxwell R3 vs R2 p<0,01 o estabilidad(R3,R2) < 85 %.
- Otro patrón → se reporta como no concluyente.

## Apuestas de David (rellenar antes de lanzar)
| Opción | Apuesta | Comentario |
|---|--:|---|
| Indeciso | | |
| No votaré | | |
| EH Bildu | | |
| PNV/EAJ | | |
| PSE | | |
| PP | | |
| Elkarrekin Podemos | | |
| Sumar | | |
| VOX | | |
