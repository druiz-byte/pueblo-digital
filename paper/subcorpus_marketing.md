# Subcorpus de marketing para el paper de IJRM (hueco nº 1)

**Objetivo:** desactivar la objeción "esto no es marketing, es opinión pública" sin generar datos nuevos
ni depender de encuestas externas.
**Fecha:** 2026-08-21

---

## Resumen ejecutivo

Hay **dos fuentes** utilizables, y la segunda es un hallazgo de esta sesión:

| Fuente | Qué es | ¿Microdato? | ¿Requiere API? | Ítems de marketing |
|---|---|:--:|:--:|--:|
| **A. Deustobarómetro verano 2026** | Ya validado, panel ya lanzado | ✅ n=1.000 | ❌ **No** | **~50** |
| **B. Sociómetro GV — Consumo y confianza en medios 2025** | Encuesta de consumo de medios, RRSS e influencers | ✅ **n=1.223 + pesos** | ✅ Sí (tanda nueva) | **~45** |

**Lo importante de B:** `datos sociometro GV/Consumo y confianza en medios...2025.csv` **no es una tabla
agregada, es microdato individual** (1.223 filas × 65 variables, con `wt`). El fichero
`25tef1_gal.pdf` es el **cuestionario completo** (Gizaker para el Gobierno Vasco, campo marzo 2025).

Consecuencias:
1. Es un **dominio inequívocamente de marketing**: dieta de medios, uso de plataformas, seguimiento
   de influencers, elección de canal principal, confianza por marca de canal, atributos de imagen.
2. Al haber microdato, se puede calcular el **techo de información** en el dominio de marketing
   — cosa que con Ikuspegi no podemos (hueco nº 5).
3. Sería el **tercer instrumento independiente** (Deustobarómetro → Ikuspegi → Sociómetro), de una
   **cuarta casa de campo** (Gizaker), reforzando el argumento de que el hallazgo no depende del
   cuestionario.
4. Trae las variables de perfil que necesita el panel: territorio, sexo, edad, situación laboral,
   euskera, estudios, clase social, ideología 0-10, interés político, provincia de nacimiento.

---

## A. Deustobarómetro — ítems de marketing ya disponibles

**Ventaja decisiva: todo esto se puede reanalizar SIN API.** Ya existen (a) el microdato real
(`Datos Deustobarómetro verano 2026.sav`), (b) las predicciones individuales de 300 encuestados
(`piloto_ppi/predicciones_deusto_full.json`) y (c) las tandas agregadas de 1.000 Personas
(`entrevista/resultados/encuesta_2026-07-16_*`). Solo hay que **filtrar por ítem y recalcular**.

### A.1 · Retrenchment de consumo — p6, 13 ítems ⭐ *el bloque más valioso*

> "Indica si en el último mes, y **como consecuencia de tu situación económica**, has hecho o has
> pensado hacer la siguiente acción…"
> Escala: *Lo he hecho* / *Lo he pensado, pero no lo he hecho* / *Ni lo he hecho ni lo he pensado*.

| Var | Acción | Categoría de gasto |
|---|---|---|
| p6_1 | Reducir los gastos en **ocio** | Ocio y entretenimiento |
| p6_2 | Renunciar a **irme de vacaciones** este verano | Turismo / viajes |
| p6_3 | Reducir el consumo de **carne o pescado** | Alimentación (trade-down) |
| p6_4 | Reducir los gastos en **alimentación** | Alimentación (gasto total) |
| p6_5 | No comprar **ropa o calzado** que realmente necesito | Moda / textil |
| p6_6 | Dejar de ir al **dentista** | Salud privada |
| p6_7 | Renunciar a **independizarme** | Vivienda |
| p6_8 | Volver a vivir en casa de mis familiares | Vivienda |
| p6_9 | Pedir **ayuda económica** a familiares/amigos | Crédito informal |
| p6_10 | **Retrasar algún pago** (recibos, hipoteca…) | Estrés financiero |
| p6_11 | No comprar alguna **medicación** | Salud / farmacia |
| p6_12 | Pedir **ropa** | Ayuda en especie |
| p6_13 | Pedir **alimentos** | Ayuda en especie |

**Constructo de marketing:** *cost-of-living trade-down / category-level spending intentions*.
Es exactamente lo que mide un tracker de confianza del consumidor con desglose por categoría —
el caso de uso nº 1 que la industria promete resolver con encuestados sintéticos.

**Lo que ya sabemos de estos ítems** (de `acuerdo_individual.md`, n=300): kappa ponderado entre
**−0,00 y 0,24**, y `delta_vs_moda` **negativo en 9 de 13**. El caso de manual es p6_9: acierto
**91,4 %** — parece excelente — pero la moda acierta **92,4 %**, luego **Δ = −1,03**. Ilustra la tesis
del paper sin necesidad de explicación adicional: *la métrica que reporta la industria (hit rate)
puede ser altísima mientras el aporte real es negativo*.

⚠ **Incidencia a resolver:** en `techo_predictivo.md` los 13 ítems de p6 salen con **R² = nan**.
Hay que depurarlo antes de usarlos en el paper (probable causa: varianza casi nula en algún fold
por la fuerte asimetría de la distribución, o codificación de "Prefiero no contestar"). Es el
primer trabajo técnico del bloque A.

### A.2 · Decisión de viaje — p13, p14, p15 + Bloque 4 (5 ítems)

| Var | Ítem | Constructo |
|---|---|---|
| p13 | ¿En qué medida ha aumentado tu **miedo a viajar**? | Barrera percibida a la compra |
| p14 | ¿Has **descartado o modificado un viaje** en los últimos dos años? | Abandono de compra |
| p15 | ¿Cuál fue la **principal razón**? (precio, inseguridad, guerras, conflicto político, trabajo, sanitaria) | Driver de abandono |
| p16 | ¿El aumento de turistas afecta a la pérdida de tradición e identidad? | Actitud hacia la categoría |
| (multi) | Efectos del turismo en el acceso a la vivienda | Externalidades percibidas |

**Constructo:** *travel purchase intention, trip abandonment and its drivers*. Decisión de compra
en una categoría de alto valor.

**Lo que ya sabemos:** p15 (razón del abandono) tiene `delta_vs_moda` = **−26,74** y kappa **0,00**;
p14, Δ = **−5,33**. Turismo es además el bloque con **peor DAM agregado (26,5-26,9 p.p.)** porque
ninguna encuesta donante lo cubre. Es la ilustración más dura: *la categoría donde el panel sintético
sería comercialmente más atractivo (no hay dato disponible) es donde peor funciona.*

### A.3 · Satisfacción con servicios — p8, 16 ítems (escala 0-10)

Transporte público, universidades públicas, I+D, carreteras, escuelas, protección social,
políticas de vivienda, servicios sociales, atención sanitaria, pensiones, política fiscal,
política industrial, seguridad ciudadana, servicio postal, Administración, políticas de igualdad.

**Constructo:** *service quality / satisfaction ratings multi-proveedor*, formalmente idéntico a un
tracker de satisfacción con marcas de servicio. Techo bajísimo (R² 0,007-0,104) y Spearman
individual 0,01-0,23 → material directo para el Study 1 y el Study 2 en clave de marketing.

### A.4 · Confianza institucional — p21, 20 ítems (escala 0-10)

**Constructo:** *brand trust tracker multi-marca*. Es el bloque con más ítems homogéneos del
barómetro y donde se ve mejor el colapso: Spearman individual entre −0,00 y 0,52, con `delta_vs_moda`
negativo en 16 de 20.

### A.5 · Valoración de figuras públicas — p37 (7) y p39 (7), escala 0-10

**Constructo:** *spokesperson / endorser evaluation*. Analogía razonable con la evaluación de
embajadores de marca. Techo muy bajo (varios R² ≤ 0) y Spearman ≈ 0.

**Total bloque A: ~50 ítems** con microdato real, predicciones individuales ya generadas y tandas
agregadas ya lanzadas.

---

## B. Sociómetro GV 2025 — "Consumo y confianza en medios, contenidos digitales y redes sociales"

**Ficha:** Gizaker para el Gobierno Vasco · campo marzo 2025 · **n = 1.223** · CAE 18+ · telefónica
(fijo y móvil) · ponderador `wt` incluido · euskera/castellano a elección.
**Ficheros:** `datos sociometro GV/Consumo y confianza en medios…2025.csv` (microdato) ·
`25tef1_gal.pdf` (cuestionario) · `P07_etiketak.csv` (etiquetas de P07).

### B.1 · Dieta de medios — P05, 7 ítems

Frecuencia (todos los días → nunca) de: **televisión** · **plataformas de streaming (Netflix,
HBO/Max, Prime Video, Filmin…)** · **radio** · **podcasts** · **prensa en papel** · **prensa en
internet** · **redes sociales**.

**Constructo:** *media diet — reach & frequency por canal*. Es el input básico de la planificación
de medios. Un panel sintético que no reproduzca esto no sirve para nada en agencia.

### B.2 · Uso de plataformas — P06, 6 ítems

Frecuencia en los últimos 7 días de **Facebook · WhatsApp · Instagram · YouTube · Twitter/X ·
TikTok**.

**Constructo:** *platform usage / share of attention*. Medición de audiencia por plataforma, marca
a marca.

### B.3 · Influencer marketing — P07, P08, P09 ⭐

| Var | Ítem | Constructo |
|---|---|---|
| P07 | Motivo principal de uso de RRSS (entretenerse / relacionarse / informarse / compartir aficiones / conocer gente) | *Usage motivations (U&G)* |
| **P08** | **¿Sigue la cuenta de algún o alguna influencer?** | **Exposición a influencer marketing** |
| P09 | Nombre del influencer que más sigue (abierta) | *Unaided recall* |

**Dato real:** 345 sí · 751 no · 10 Ns/Nc · 117 no usan RRSS. **P08 es el ítem más "marketing" de todo
el corpus** y tiene una distribución sana (≈31 % de los usuarios de RRSS), no degenerada — justo el
tipo de ítem donde el colapso de varianza se ve bien.

⚠ **P09 llega codificada (97 = menciona a alguien · 98 = resto · 99 = Ns-Nc), no con el nombre
literal.** Se pierde el test de recuerdo espontáneo de marca, que habría sido espectacular. Queda
utilizable solo como binaria "menciona/no menciona" (297 menciones).

### B.4 · Consumo de noticias por canal — P12, P13 (8 ítems), P14

- P12: nivel de interés en noticias de actualidad.
- P13: frecuencia de seguimiento de noticias en **TV · radio · periódicos papel · periódicos
  internet · RRSS · podcasts informativos · agregadores (Google News) · WhatsApp**.
- **P14: ¿cuál es el medio PRINCIPAL?** — elección única entre 8 canales.
  Dato real: TV 450 · radio 285 · prensa internet 191 · RRSS 130 · prensa papel 85 · agregadores 19 ·
  podcasts 11 · WhatsApp 7 · Ns-Nc 45.

**Constructo de P14:** *discrete brand/channel choice*. Es el análogo más limpio a una pregunta de
elección de marca que hay en todo el material disponible, y con **8 alternativas y una cola larga**
— el escenario donde el colapso de varianza es letal (predecimos que el panel dará ~TV a casi todo
el mundo y borrará podcasts, agregadores y WhatsApp, que juntos son el 3 % real).

### B.5 · Confianza por marca de canal — P15, P16 (7 ítems), escala 0-10

P15: confianza general en los medios. P16: confianza en **televisión · radio · prensa papel · prensa
internet · información por RRSS · agregadores · WhatsApp**.

**Constructo:** *brand trust tracker*, siete "marcas" en la misma escala 0-10. Comparable ítem a ítem
con el p21 del Deustobarómetro → permite un chequeo de consistencia entre instrumentos.

### B.6 · Atributos de imagen — P17, 3 ítems

Los medios vascos ofrecen: **información fiable** · **pluralidad de puntos de vista** ·
**información libre de presiones políticas o comerciales**.

**Constructo:** *brand image attribute ratings*. Batería de atributos clásica de un estudio de imagen.

### B.7 · Percepción de desinformación y alfabetización — P18, P19 (5), P20, P21, P22

Trade-off libertad/control · desinformación percibida por canal (RRSS, TV, radio, prensa, WhatsApp) ·
autoeficacia para detectar contenido falso · frecuencia de verificación · frecuencia de conexión a
internet.

**Constructo:** *perceived channel risk & media literacy*. Relevante para *brand safety* — dónde una
marca quiere o no quiere aparecer.

### B.8 · Perfil disponible para construir la Persona

`lurral` (territorio) · `p01` sexo · `p02` edad (18-94, media 52,5) · `p03` situación laboral ·
`p04` nivel de euskera · `p23` ideología 0-10 · `p24` interés político · `p25` estudios ·
`p26` clase social · `p27` provincia de nacimiento · `wt` ponderador.

Es **el mismo conjunto de llaves** que usa el panel actual → el emparejamiento no requiere método
nuevo.

**Total bloque B: ~45 ítems**, todos de dominio marketing/medios.

---

## Qué análisis permite cada bloque

| Análisis del paper | Bloque A (sin API) | Bloque B (con API) |
|---|:--:|:--:|
| Study 1 — techo de información | ✅ recalcular sobre ~50 ítems | ✅ **nuevo dominio**, resuelve también el hueco 5 |
| Study 2 — posición respecto al techo | ✅ ya hay 300 predicciones | ✅ requiere tanda nueva |
| Study 3 — colapso de varianza | ✅ ya hay tanda de 1.000 | ✅ requiere tanda nueva |
| Study 4 — enriquecimiento (v1 vs v2) | ✅ ambas tandas existen | ⬜ opcional |
| Tercer instrumento independiente | ❌ | ✅ **cuarta casa de campo** |
| Elección discreta tipo *brand choice* | ⬜ débil | ✅ P14, 8 alternativas |

---

## Plan recomendado

**Fase 1 — sin API, empezar ya (bloque A).**
1. Depurar el `R² = nan` de los 13 ítems de p6 en `techo_predictivo.py`.
2. Crear `paper/marketing_items.json`: la lista de ~50 ítems con su etiqueta de constructo de
   marketing (retrenchment · viaje · satisfacción de servicio · confianza de marca · endorser).
3. Recalcular, restringiendo a ese subconjunto: techo (`techo_predictivo.py`), acuerdo individual
   (`acuerdo_individual.py`) y DAM + concentración modal sobre la tanda de 1.000.
4. Producir la tabla que irá al paper: **techo · alcanzado · Δ vs moda · concentración**, por
   constructo de marketing.

**Fase 2 — con API, en el PC de David (bloque B).**
5. Construir el panel para el Sociómetro de medios (mismas llaves, `wt` como peso) y una plantilla
   de encuesta con los ~45 ítems.
6. Lanzar 1.223 Personas (coste esperado del orden de la tanda de Ikuspegi).
7. Techo + acuerdo individual + colapso en el dominio de medios.

Si la Fase 1 ya da una tabla presentable, la Fase 2 pasa de "necesaria" a "la que convierte el paper
en publicable en IJRM": tercer instrumento, dominio de marketing puro y techo calculable.

---

## Cautelas a declarar en el paper

- **Consumo de medios es marketing-*adyacente*.** Cubre planificación de medios, audiencias,
  influencer marketing y confianza de marca de canal, pero **no** compra de producto envasado ni
  conjoint. Un revisor exigente puede seguir presionando; la defensa es que p6 (gasto por categoría)
  y el bloque de viaje sí son decisión de compra.
- **P09 viene codificada**, no con el nombre del influencer → se pierde el recuerdo espontáneo.
- **Los ítems de p6 tienen distribuciones muy asimétricas** (hasta 92 % en la moda). Hay que reportar
  siempre el baseline de moda al lado, o el hit rate engaña. Esto no es un defecto: es precisamente
  el argumento del paper.
- El Sociómetro es de **marzo 2025** y el Deustobarómetro de **junio 2026** → no mezclar olas en una
  misma métrica sin declararlo.
