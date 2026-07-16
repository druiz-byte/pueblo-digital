# Contraste Barómetro Digital vs. Deustobarómetro real — Tanda completa (1.000 Personas)

**Fecha:** 2026-07-08 · **Modelo:** claude-haiku-4-5 · **N = 1.000** (6 bloques)

Métrica: **DAM** (desviación absoluta media) = media, en puntos porcentuales (p.p.),
de la diferencia entre el % de cada opción en el panel sintético y el % real del
Deustobarómetro verano 2026. Menor = más cerca del real.

## Resultado global

- **DAM media global: 16,7 p.p.** sobre **91 preguntas** con dato real.
- Fidelidad alta (<10 p.p.): **25** preguntas · media (10–20): **39** · baja (≥20): **27**.

## Por bloque (de más cerca a más lejos)

| Bloque | Preguntas c/ dato real | DAM media | Rango (min–max) |
|---|---|---|---|
| 1 · Situación económica | 25 | 10,8 p.p. | 0,7 – 22,7 |
| 5 · Situación política y calidad de la democracia | 25 | 11,8 p.p. | 0,4 – 29,4 |
| 2 · Estado de bienestar y políticas públicas | 9 | 17,9 p.p. | 7,7 – 30,1 |
| 3 · Los miedos de la era de la inseguridad | 6 | 19,6 p.p. | 2,9 – 29,7 |
| 6 · Geopolítica, guerras y Donald Trump | 24 | 25,8 p.p. | 3,3 – 56,9 |
| 4 · El impacto social del turismo | 2 | 26,5 p.p. | 23,6 – 29,3 |

## Preguntas mejor ajustadas (más cerca del real)

| Bloque | DAM | Pregunta |
|---|---|---|
| 5 | 0,4 | ¿Cómo calificarías la situación política general del País Vasco? |
| 1 | 0,7 | ¿Cómo calificarías la situación económica del País Vasco? |
| 5 | 1,4 | Formas de organización territorial |
| 5 | 1,4 | Sentimiento nacionalista vasco (autoubicación) |
| 3 | 2,9 | ¿En qué medida ha aumentado tu miedo a viajar? |
| 6 | 3,3 | Impacto de la guerra en Oriente Medio |

## Preguntas peor ajustadas (más lejos)

| Bloque | DAM | Pregunta |
|---|---|---|
| 6 | 36,8 | Aliados y enemigos de Europa (P12) |
| 6 | 37,5 | Principales amenazas comunes (P22) |
| 6 | 38,8 | Medidas geopolíticas a utilizar (P24) |
| 6 | 42,3 | Aliados y enemigos de Europa (P13) |
| 6 | 46,4 | Aliados y enemigos de Europa (P10) |
| 6 | 56,9 | Aliados y enemigos de Europa (P8) |

## Interpretación

Confirma el patrón detectado en la Tanda 1:

1. **Fidelidad casi perfecta cuando la variable está en el perfil de la Persona**
   (valoración económica y política del PV, preferencia territorial, nacionalismo):
   DAM < 1,5 p.p. El panel reproduce con precisión lo que ya "sabe" de sí mismo.
2. **Error alto en temas ajenos al perfil sociodemográfico** (geopolítica: aliados/
   enemigos, amenazas, medidas). Las Personas carecen de anclaje y sobre-concentran
   respuestas; los 6 peores ítems son todos del Bloque 6.
3. **Multi-respuesta ("hasta k opciones")**: tiende a homogeneizar y sobre-mencionar
   la opción modal, subestimando las minoritarias.

## Archivos de detalle (por bloque)

`contraste_bloque1.md` … `contraste_bloque6.md` en esta misma carpeta, con las
tablas opción-a-opción de cada pregunta.
