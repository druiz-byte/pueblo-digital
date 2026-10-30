# Campos del panel de 1.000 Personas y su procedencia

Panel `pv_agentes_v2.json` (el que usa la app), construido con `construir_panel_v2.py`.

**Método:** cada Persona se **ancla en un encuestado real** del Sociómetro Vasco 83
(remuestreo ponderado por `wt`) y se le **injertan** bloques de otras encuestas por
emparejamiento estadístico (kNN por celdas de perfil, 5-6 llaves).

## Bloque base — ancla: Sociómetro Vasco 83 (Gob. Vasco / GPS)

| Campo | De dónde viene | Variable origen |
|---|---|---|
| id | Generado (índice 1-1000) | — |
| nombre, apellidos | Generados por reglas (según género y si es euskaldun) | — |
| género | Sociómetro 83 | P37 (resp. P01) |
| edad, grupo_edad | Sociómetro 83 | P02 |
| provincia | Sociómetro 83 | lurral |
| hábitat | Sociómetro 83 | P0B |
| lugar de nacimiento | Sociómetro 83 | P35 |
| nivel de estudios | Sociómetro 83 | P33 |
| situación laboral | Sociómetro 83 | P03 |
| clase social | Sociómetro 83 | P34 |
| idioma de la entrevista | Sociómetro 83 | P0A |
| competencia en euskera | Sociómetro 83 | P32 |
| ideología 0-10 | Sociómetro 83 | P28 |
| escala nacionalismo 0-10 | Sociómetro 83 | P29 |
| identidad (vasco/español) | Sociómetro 83 | P30 |
| preferencia territorial | Sociómetro 83 | P31 |
| voto autonómicas | Sociómetro 83: recuerdo 2020 (P23), respaldo intención 2024 (P21) | P23 / P21 |
| valoración economía PV | Sociómetro 83 | P08 |
| valoración política PV | Sociómetro 83 | P06 |
| problemas para llegar a fin de mes | Sociómetro 83 | P11 |
| salud (ancla) | Sociómetro 83 | P04 |
| seguridad percibida | Sociómetro 83 | P05 |
| interés por la política | Sociómetro 83 | P17 |
| religión | Constante "No especificada" (no se imputa en v2) | — |
| principales problemas | Vacío `[]` (no está en el ancla) | — |

## Bloques `perfil_mediatico` y `perfil_bienestar` — donante: ESS España (European Social Survey)

Imputado por kNN con llaves sexo × edad × educación × situación laboral × ideología.

| Campo | Variable ESS |
|---|---|
| consumo de noticias (min/día) | nwspol |
| uso de internet | netusoft |
| consumo de TV | tvtot |
| confianza en políticos 0-10 | trstplt |
| confianza en el parlamento 0-10 | trstprl |
| felicidad 0-10 | happy |
| satisfacción con la vida 0-10 | stflife |
| salud autopercibida | health |
| contacto social | sclmeet |
| sentimiento de soledad | fltlnl |

## Bloque `perfil_social` — donante: EUSTAT, Encuesta de Capital Social 2022

Imputado por kNN con llaves sexo × edad × provincia × clase.

| Campo | Variable ECS22 |
|---|---|
| confianza general en personas | CONGEN |
| confianza en instituciones | CONINS |
| confianza en profesiones | CONPRO |
| red social amplia / próxima | REDAMP / REDPRO |
| apoyo emocional | AYUEMO |
| interés político | INTPOL |
| participación social | PARSOC |
| pertenencia a asociaciones | ASOPER |
| voluntariado | ASOVOL |
| cohesión social | COHSOC |
| sentimiento de proximidad | PROXIM |
| seguridad | SEGURI |
| percepción de corrupción | CORRUP |
| satisfacción con ingresos | SATISF |
| felicidad/salud | FELSAL |

## Notas

- **Nombre y apellidos son inventados** (por reglas, no de datos).
- La **religión es constante** ("No especificada") en este panel. Sí se añadió como
  dato real, pero solo en el experimento PPI (predictores de los encuestados reales
  del Deustobarómetro), que es un conjunto distinto de este panel.

**Fuentes:** Sociómetro Vasco 83 (Gabinete de Prospección Sociológica, Gobierno Vasco) ·
ESS – European Social Survey (muestra de España) · EUSTAT, Encuesta de Capital Social 2022.
