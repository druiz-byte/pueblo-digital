# Extra — Liderazgo y Gobierno Vasco: sin partidos vs. con partidos

**Fecha:** 2026-07-09 · **Modelo:** claude-haiku-4-5 · **N = 1.000** (dos tandas independientes al mismo panel)

Preguntas propias, fuera del Deustobarómetro (sin % real de referencia). Se lanzó P1 en dos versiones: **sin** el partido junto al nombre del líder y **con** el partido entre paréntesis. P2 idéntica en ambas.

## P1 — ¿Quién sería mejor lehendakari? (global)

| Líder (partido) | Sin partidos | Con partidos | Δ |
|---|---:|---:|---:|
| Imanol Pradales (PNV/EAJ) | 7.6% | 30.8% | +23.2 |
| Pello Otxandiano (EH Bildu) | 24.6% | 28.8% | +4.2 |
| Eneko Andueza (PSE) | 0.4% | 12.8% | +12.4 |
| Amaia Martínez (Vox) | 0.0% | 0.2% | +0.2 |
| Javier de Andrés (PP) | 3.2% | 3.3% | +0.1 |
| Jon Hernández (Sumar) | 0.0% | 0.0% | +0.0 |
| No sé / No contesto | 64.2% | 24.1% | -40.1 |

*Firmas únicas: sin partidos 14/1000 · con partidos 16/1000.*

## P1 por recuerdo de voto (tasa de "No sé" y opción mayoritaria entre quienes responden)

| Voto | n | NS sin | Top sin | NS con | Top con |
|---|---:|---:|---|---:|---|
| PNV/ EAJ | 194 | 16% | Pello Otxandiano 45% | 0% | Imanol Pradales 98% |
| EH Bildu | 163 | 21% | Pello Otxandiano 77% | 0% | Pello Otxandiano 100% |
| PSE | 120 | 82% | Pello Otxandiano 15% | 1% | Eneko Andueza 87% |
| PP | 35 | 66% | Javier de Andrés 23% | 3% | Javier de Andrés 60% |
| Sumar | 32 | 91% | Pello Otxandiano 9% | 6% | Pello Otxandiano 41% |
| Vox | 32 | 28% | Javier de Andrés 72% | 0% | Imanol Pradales 62% |

## P2 — Cualidad que mejor define al Gobierno Vasco (idéntica en ambas)

| Cualidad | Sin partidos | Con partidos |
|---|---:|---:|
| Capacidad | 0.2% | 0.0% |
| Cercanía | 0.1% | 0.5% |
| Iniciativa | 27.5% | 38.6% |
| Honestidad | 0.0% | 0.5% |
| Diagnóstico acertado de los problemas | 0.2% | 0.9% |
| Rapidez de respuesta | 0.0% | 0.0% |
| No sé / No contesto | 72.0% | 59.5% |

## Interpretación

1. **Añadir el partido desploma el "No sé"** en P1: del **64,2% al 24,1%**. Sin la pista de partido las Personas no reconocen los nombres propios y se refugian en "No sé"; con la etiqueta pueden mapear el líder a su propio voto.
2. **Con partido, el voto predice el líder** casi de forma determinista: PNV→Pradales 98%, EH Bildu→Otxandiano 100%, PSE→Andueza 87%, PP→De Andrés 60% (NS ~0% en todos). Sin partido, ni siquiera los votantes del PNV elegían a Pradales (su top era Otxandiano, 45%).
3. **Sesgo residual contra Vox y Sumar**: incluso con el partido, **Amaia Martínez (Vox) 0,2% y Jon Hernández (Sumar) 0,0%**. Los votantes de Vox se pasan a Pradales (62%) y los de Sumar a Otxandiano (41%): el modelo se resiste a señalar a los líderes de Vox y Sumar como "mejor lehendakari" aun para su propio electorado.
4. **Efecto de reconocimiento de nombre**: sin partidos, el nombre más "sonado" (Otxandiano) acaparaba las respuestas no-NS (incluido el electorado del PNV); la etiqueta de partido corrige este sesgo para los partidos grandes.
5. **P2 apenas mejora** (NS 72%→59,5%; sigue dominando "Iniciativa", el resto de cualidades ~0): sin un anclaje al perfil, la pregunta se homogeneiza. Las **firmas siguen bajísimas** (14→16 /1000): el panel responde de forma casi idéntica dentro de cada grupo.

**Conclusión para el artículo:** el experimento aísla dos sesgos del *silicon sampling*: (a) la **dependencia del anclaje** —el mismo panel pasa de 64% de no-respuesta a mapear el voto casi perfectamente solo por añadir el partido al enunciado—, y (b) un **sesgo normativo persistente** que penaliza a los líderes de Vox y Sumar incluso con anclaje y aun entre sus votantes.
