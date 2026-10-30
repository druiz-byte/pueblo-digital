# Preregistro — Réplica sobre el ICC de julio (CIS 3575)

**Escrito ANTES de lanzar ninguna tanda.** Fecha: 2026-09-22.

## Instrumento

CIS, Estudio nº 3575 «ICC de julio», julio 2026. Índice de Confianza del Consumidor.
Universo: residentes en España de 16 años y más. n=3.004; submuestra País Vasco n=133.
Entrevista telefónica (CATI), campo 24-29 de julio de 2026, error ±1,8 p.p. nacional.
Microdatos disponibles (`3575.sav`, `3575_num.csv`, `3575_etiq.csv`), cuestionario y ficha técnica.

Por qué este instrumento y no otro:

1. **Es consumo, no política.** Capacidad de ahorro, gasto previsto en bienes duraderos,
   intención de compra de vivienda, expectativas de precios. Es el dominio comercial
   canónico y cubre el hueco 1 del esquema IJRM con un **tercer instrumento y una cuarta
   casa de campo**.
2. **Hay microdato individual** → se puede estimar el techo de información en el dominio,
   que es lo que faltaba en la réplica de Ikuspegi.
3. **Hay submuestra del País Vasco** → el desajuste de universo deja de ser una excusa
   disponible: se contrasta contra la CAE (n=133, ±8,5 p.p.) y contra España (n=3.004).
4. **Cuatro ítems tienen la categoría intermedia marcada (NO LEER)** — no se ofrece al
   entrevistado y aun así la elige la mitad de la muestra. Es el diseño natural para el
   test del satisficing.

## Techo de información en este dominio (calculado antes de lanzar)

Predictores: sexo, edad, estudios, situación laboral, ingresos del hogar, ideología 1-10,
recuerdo de voto 2023, régimen de tenencia de vivienda, tamaño de municipio, CCAA,
personas en el hogar, estado civil. R² fuera de muestra, KFold 5.
`corr_max = sqrt(R²_OOS)`, criterio de `techo_predictivo_v2.py`.

| ítem | corr_max lineal |
|---|--:|
| P2 capacidad de ahorro | 0,483 |
| **P8 economía española (retrospectiva)** | **0,468** |
| P14 economía española (prospectiva) | 0,398 |
| P7 empleo en España | 0,383 |
| **P3 economía del hogar** | **0,353** |
| P9 empleo (prospectiva) | 0,313 |
| P18 intención de compra de vivienda | 0,289 |
| P12 economía del hogar (prospectiva) | 0,280 |
| P10 bienes duraderos | 0,252 |
| P11 capacidad de ahorro (prospectiva) | 0,237 |
| P15 inflación | 0,202 |
| **P16 tipos de interés** | **0,046** |
| **P17 precio de la vivienda** | **0,041** |
| P6 paro en el entorno | 0,015 |
| **media (18 ítems)** | **0,258** |

Cautela declarada: la versión con gradient boosting da R² OOS ≤ 0 en 14 de los 18 ítems
(sobreajuste con n≈2.900 y señal débil), de modo que **aquí la cota fiable es la lineal**,
al revés que en el Deustobarómetro. No se reporta el techo GBM de este instrumento sin
regularizarlo primero.

Lectura: el techo medio (0,258) es del mismo orden que el del Deustobarómetro (0,225 lineal),
en un dominio completamente distinto y con otra casa de campo. **El rango interno es lo
interesante: va de 0,015 a 0,483 dentro de la misma encuesta y la misma escala de respuesta.**
Eso permite un contraste que hasta ahora no teníamos.

## Diseño

Dos plantillas en `entrevista/encuestas/`:

- **`cis_icc_julio2026_A.json`** — 7 ítems, categoría intermedia **ofrecida** en la lista.
- **`cis_icc_julio2026_B_sin_intermedia.json`** — los 3 ítems bipolares, categoría intermedia
  **retirada**, replicando literalmente lo que oye el entrevistado del CIS.

Panel v2, 1.000 Personas, Haiku, temperature por defecto. Ambas tandas con las mismas Personas.

Cuatro pares, cada uno contrasta una hipótesis distinta:

| par | ítems | qué aísla |
|---|---|---|
| A | P3, P12 | satisficing: la categoría central como conducta de respuesta |
| B | P8 vs P17 | techo alto (0,468) vs techo nulo (0,041), misma escala |
| C | P18, P10 | intención de compra: el caso comercial |
| D | P15 | ancla numérica explícita en el enunciado (3,2 %) |

## Predicciones

Escritas antes de ver ningún resultado. Referencia: dato del País Vasco.

- **H1 — el centro se vacía aunque se ofrezca.** En la versión A, "Igual" recibe **< 15 %**
  en P3 (real CAE 62,8 %, España 49,3 %). *Falsación: ≥ 40 %.*
- **H2 — asimetría máxima frente al diseño del instrumento.** Restringiendo a Mejor/Peor,
  las distribuciones de A y de B difieren en **< 8 p.p.**: el panel es insensible a que la
  categoría intermedia se ofrezca o no, mientras que el humano, sin que se le ofrezca, la
  produce espontáneamente en la mitad de los casos. *Falsación: diferencia ≥ 20 p.p.*
- **H3 — el acierto es independiente de la información.** **DAM(P17) < DAM(P8)** pese a que
  el techo de P17 es once veces menor. Es decir, el panel irá mejor justo donde no hay nada
  que saber y el tópico coincide con la moda real. *Falsación: DAM(P8) ≤ DAM(P17).*
- **H4 — intención de compra: colapso hacia el "No".** P18 "No" **≥ 97 %** (real CAE 94,0 %,
  España 88,2 %); "Sí" por debajo del real en ambos universos. *Falsación: "Sí" ≥ 10 %.*
- **H5 — el ancla numérica no se usa.** P15 "Más" **≥ 90 %** (real CAE 69,3 %). El enunciado
  entrega el 3,2 % y la Persona no lo convierte en dispersión. *Falsación: "Más" ≤ 75 %.*
- **H6 — concentración.** Concentración media del panel en los 7 ítems de A **≥ 85 %**,
  frente a **64,5 %** real en la CAE y **60,8 %** en España.
  *Falsación global: si la concentración del panel ≤ real + 5 p.p., la tesis del colapso
  no se sostiene en este instrumento.*

## Confounds declarados de antemano

1. **Submuestra CAE pequeña** (n=133, ±8,5 p.p.). Sirve para descartar el desajuste de
   universo, no como benchmark de precisión. Los dos datos reales van en la plantilla.
2. **Desfase temporal.** El ICC es de julio de 2026 y pregunta por coyuntura concreta
   (inflación del último año, precio de la vivienda, economía española a seis meses). El
   panel no "sabe" la coyuntura de julio de 2026. Afecta sobre todo a P8, P15 y P17, y es
   una razón para no sobreinterpretar el DAM de esos tres ítems por separado. **P3, P12,
   P10 y P18 preguntan por el hogar de la propia Persona y no dependen de conocer la
   coyuntura**, por lo que son los ítems limpios del diseño.
3. **Contaminación del perfil.** Ninguno de los 7 ítems aparece verbatim en los campos que
   inyecta `build_system_prompt_v2`. El más próximo es P3/P12 frente a `problemas_dinero`
   (constructo adyacente, no idéntico): declarar como semicontaminado.
4. **Ancla de formato descartada.** El ejemplo `1:B` de `server.py:247` quedó descartado
   experimentalmente el 2026-09-22 (ver bitácora): al rotar el orden de opciones, la moda
   del panel no siguió a la letra B.

## Qué se reporta pase lo que pase

DAM por ítem contra CAE y contra España; baselines de moda y uniforme; índice de
concentración; número de opciones usadas; NS/NC; V de Cramér respuesta × (ideología,
ingresos, edad, tenencia de vivienda); y la comparación A vs B. Los ítems con falsación
cumplida se reportan como fallo de la hipótesis, no se retiran.
