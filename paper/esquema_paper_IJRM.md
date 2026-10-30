# Esquema del paper — International Journal of Research in Marketing

**Autor:** David Ruiz (Universidad de Deusto)
**Destino:** IJRM, vía ordinaria (el special issue *"Generative AI, Synthetic Data, and Synthetic
Respondents in Marketing Research"*, eds. Erdem y Pauwels, cerró el 1-may-2026).
**Última actualización:** 2026-08-24, redactada §4 (data and design).

> **Estado de la evidencia: completa.** Se decide **no hacer más tandas** y redactar con lo que hay.
> Todos los números de este documento están verificados y las cifras erróneas anteriores, purgadas.

---

## 0. La tesis en una frase

Los encuestados sintéticos generados por LLM fallan a nivel individual por **dos límites
independientes**: un techo que impone la información contenida en el perfil —irreducible por
cualquier método— y un fallo distribucional que el modelo añade por debajo de ese techo. Ese
segundo límite **se desdobla en dos componentes que se comportan de forma distinta**: la compresión
de varianza cede parcialmente ante modelos mejores, y la borradura de las categorías polares no.

Corolario operativo: la fidelidad agregada y la individual son **lógicamente independientes**. Se
puede clavar la media sin acertar a nadie. Las tareas que motivan comercialmente los paneles
sintéticos —segmentación, heterogeneidad en conjoint, targeting, colas— son exactamente las que
dependen de lo que el modelo destruye.

---

## 1. Título — candidatos

1. **"Two Ceilings: Information Limits and Distributional Collapse in LLM-Based Synthetic
   Respondents"** *(favorito)*
2. "Nailing the Mean, Missing Everyone: The Separability of Aggregate and Individual Fidelity in
   Synthetic Survey Panels"
3. "The Poles Are Missing: What Frontier Models Fix and What They Don't in Synthetic Survey Data"
4. "Richer Personas, Worse Predictions: Evidence Against the Enrichment Assumption"

---

## 2. Abstract (borrador 2, ~220 palabras)

> Synthetic respondents — large language models prompted to answer surveys as a person with a given
> profile — are being adopted in marketing research as a fast, cheap substitute for human panels.
> We show that their individual-level accuracy is bounded by two distinct mechanisms and provide a
> diagnostic for each.
>
> First, an **information ceiling**. Regressing survey items on the full space of variables a
> profile could plausibly contain yields a mean out-of-sample R² of 0.072 across 100 items,
> implying a maximum attainable individual correlation of 0.27; 15 % of items are unpredictable
> from any profile. The bound holds for any method, generative or statistical. Our panel attains
> 0.137 — roughly half the ceiling.
>
> Second, **distributional collapse**, which decomposes into two components. The modal share is
> 83.7 % against 61.5 % observed, and this compression is partly reversible: a frontier model
> lowers it to 75.0 % and improves aggregate fit beyond a modal baseline. But options held by
> 34.2 % and 31.3 % of the population are chosen by **none** of 1,000 synthetic respondents, and
> remain at 3.0 % and 7.8 % with the frontier model. Neither an explicit anti-concentration
> instruction nor a change in decoding temperature moves them at all.
>
> We validate on 152 items from an official regional barometer, replicate on an independent
> immigration survey, and report a marketing subcorpus where the ceiling is **lower** than for
> political attitudes. We close with a decision rule by research task.

▸ *Pendiente: recortar a 200 palabras para el límite de IJRM.*

---

## 3. Arquitectura del argumento

```
                    ¿Qué puede saber una Persona sintética?
                                  │
        ┌─────────────────────────┴─────────────────────────┐
   ACTO I: TECHO                                    ACTO II: COLAPSO
   (límite de los datos)                            (fallo del modelo)
        │                                                   │
   corr máx 0,225 lin / 0,271 GBM              (a) concentración 83,7 vs 61,5
   15/100 ítems con R² ≤ 0                         → CEDE con mejor modelo (75,0)
   invariante al modelo, al prompt,             (b) borradura de los polos
   a la temperature y a N                           → NO cede: 0,0 % en opciones
   el panel alcanza el 51 %                            del 34,2 % y el 31,3 %
        │                                                   │
        └─────────────────────────┬─────────────────────────┘
                    SEPARABILIDAD AGREGADO / INDIVIDUO
                    P26: media 5,15 vs 5,30 (error 0,15)
                    pero 86,4 % en {5,6} y 0 % en {8,9,10}
                                  │
                        REGLA DE DECISIÓN POR TAREA
```

---

## 4. Estructura de secciones

### 1. Introduction
Gancho comercial y adopción en *insights*. El vacío: la literatura valida **distribuciones
agregadas**; el criterio más exigente de Argyle et al. (2023), la *correspondencia de patrones*,
apenas se ha puesto a prueba. Tres contribuciones (§5). Adelanto de resultados.

### 2. Background
2.1 *Silicon sampling* y los 4 criterios de fidelidad algorítmica — Argyle et al. (2023).
2.2 Los *perils* — Bisbee et al. (2024, *Political Analysis*): sesgo y varianza reducida.
2.3 El puente al marketing — Sarstedt et al. (2024, *Psychology & Marketing*).
2.4 Práctica de industria — Wang et al. (2024), NIM.
2.5 **El hueco:** nadie separa *cuánto del error es irreducible* de *cuánto lo pone el modelo*.

### 3. Framework *(escrita — `seccion3_marco_teorico.md`)*
Proposición 1 con demostración y dos extensiones. Proposición 2 desdoblada en concentración y
truncamiento del soporte. Corolario de separabilidad. Tabla de implicaciones contrastables P2a-P2g.

### 4. Data and design
4.1 Panel de 1.000 Personas del País Vasco; dos versiones (v1, v2) para el contraste de
    enriquecimiento.
4.2 **Validación primaria:** Deustobarómetro verano 2026, microdatos SPSS n=1.000, 152 ítems.
4.3 **Réplica externa:** Ikuspegi 2025 (UPV/EHU), n=600, inmigración en la CAE. Otro equipo, otro
    tema, otra casa de campo.
4.4 **Subcorpus de marketing:** 44 ítems seleccionados *ex ante* por constructo + 10 de contraste
    político.
4.5 Modelo, prompting y decodificación. Declarar temperature por defecto = 1,0.
4.6 Baselines: moda, marginal, suelo de ruido muestral (0,8 p.p. con n=1.000).
4.7 Métricas: DAM; correlación de Pearson, kappa ponderado, ±1, MAE, Δ vs moda; concentración
    modal; masa borrada; V de Cramér.

### 5. Study 1 — El techo de información
- 152 ítems regresados sobre 68 columnas de perfil. R² **fuera de muestra**, CV 5-fold **repetida
  20 veces** con semilla por ítem (sd del R² = 0,013, comparable a la señal).
- **R² medio 0,072 → corr máx 0,225 lineal · 0,271 GBM.** 15/100 ítems con R² ≤ 0.
- Por bloque: economía 0,024 · bienestar 0,034 · miedos 0,059 · turismo 0,085 · **política 0,099**.
- Control de circularidad: los ítems que *son* predictores se excluyen.
- **Se reportan los dos techos, con el GBM como cota operativa** (es el más exigente con nosotros).

### 6. Study 2 — Dónde está el panel respecto al techo
- Acuerdo individual 1:1, n=300 emparejados, **excluidos los 10 ítems circulares**.
- Escalas 0-10 (52): Pearson **0,123** · MAE 2,10 · ±1 en 46,1 % · **Δ vs moda −7,53**.
- Ordinales (45): kappa ponderado **0,097** · acierto 52,3 % · **Δ vs moda −4,97**.
- Nominales (36): kappa **0,139** · **Δ vs moda −5,36**.
- Multi-respuesta (9): Jaccard 0,37 · F1 0,46.
- **El panel alcanza el 51 % del techo (0,137 de 0,271).** No está roto: choca contra un límite que
  además es bajísimo.
- **No hay ningún resultado individual positivo en el proyecto.** El Δ vs moda es negativo en las
  tres familias.
- **Comparación con imputación clásica:** en nominales el clasificador lineal saca **+7,88 p.p.**
  sobre la moda y la Persona LLM **−5,36**. Trece puntos, y el LLM por debajo del baseline tonto.
  *Donde el ítem es imputable, la estadística clásica gana con holgura.*

### 7. Study 3 — Colapso distribucional y réplica externa
- Ikuspegi, 1.000 Personas: **DAM 15,7** vs moda 17,0 · uniforme 19,7 · suelo de ruido 0,8.
- **El DAM se sostiene entre instrumentos** (15,7 vs 13,4 en el Deustobarómetro) → no depende del
  cuestionario.
- **Concentración 83,7 vs 61,5 real** (+22,2), y **sube con N** (81,7 → 83,7).
- **Cero de mil** en dos opciones que tienen el **34,2 %** y el **31,3 %** reales. En el polo
  opuesto, misma compresión.
- **El panel SÍ usa el perfil:** V de Cramér con voto **0,36**; dirección correcta (expulsión por
  delito: Vox 91 % · PP 66 % · PNV 18 % · EH Bildu 6 %). No ignora a la Persona: **comprime el
  rango**.
- **P26, la ilustración limpia:** media 5,15 vs 5,30 real (error 0,15) pero **86,4 % en {5,6}** y
  **cero** en {8,9,10}. Fidelidad agregada excelente, distribución destruida.

### 8. Study 4 — Enriquecer el perfil empeora
- Panel v2 con 5-6 llaves y predictores canónicos de actitudes migratorias.
- **Predicciones preregistradas antes de lanzar**; las que fallan lo hacen **en dirección contraria
  a la falsación**.
- **DAM 18,2** (peor que el baseline de la moda) · concentración **88,8** · opciones usadas 2,7 vs
  4,3.
- No es artefacto del voto degradado: restringiendo a Personas con partido, v1 14,7 / conc. 81,9 vs
  v2 17,9 / conc. **89,0**.
- **"Más estructura ≠ mejor predicción" pasa de anécdota a resultado replicado.**

### 9. Study 5 — Robustez: modelo, prompt y temperature ⭐ *nuevo*
Tres manipulaciones independientes, 1.000 Personas cada una, mismos ítems, **con predicciones
preregistradas por dos autores por separado** (`preregistro_robustez.md`).

| | Δ_C | NS/NC | soporte | nº efectivo | P11 · P13 | DAM |
|---|--:|--:|--:|--:|--:|--:|
| Base (Haiku, τ por defecto) | 22,2 | 1,4 % | 4,3 | 1,66 | **0,0 · 0,0** | 15,7 |
| + prompt anti-concentración | **17,9** | 2,0 % | 4,5 | 1,73 | **0,0 · 0,0** | 14,8 |
| + temperature 0,0 | 22,6 | 1,1 % | 4,2 | 1,64 | **0,0 · 0,0** | 15,8 |
| + modelo frontera | **13,5** | 0,0 % | **3,6** | 2,03 | **3,0 · 7,8** | **11,8** |
| *real* | — | 3,4 % | — | — | 34,2 · 31,3 | — |

**F1 · La temperature es irrelevante.** Todas las métricas se mueven menos de medio punto. El
colapso no es un artefacto de decodificación — y no porque τ=0 empeore, sino porque τ **no importa**.

**F2 · El prompt mueve el centro, no los polos.** Se le dice explícitamente que los extremos son
legítimos: redistribuye entre opciones moderadas (P11: 12,1/85,9 → 39,6/58,0) y deja los polos
**exactamente en 0,0 %**. Se le da permiso y no lo usa.

**F3 · El modelo frontera atenúa (a) y apenas toca (b).** Mejor DAM del proyecto (11,8, bate a la
moda por 5,2) y primera vez que los polos reciben masa. Pero recuperan **0,09 y 0,25**: sigue
borrado el **83 %** de la masa polar.

**F4 · Concentración y soporte se mueven en direcciones OPUESTAS.** El frontera está menos
concentrado y usa **menos** categorías (4,3 → 3,6): equilibra las dominantes y **aniquila la cola
más**. Refuta la lectura del colapso como "compresión hacia el centro".

**F5 · El gradiente político se refuerza:** Vox 100 · PP 91 · PNV 41 · EH Bildu 17 · Podemos 3,
frente a 91 · 66 · 18 · 6 · 0 con Haiku. El modelo mejor usa **más** el perfil.

▸ **Honestidad obligada:** preregistramos que el frontera no mejoraría el DAM de forma relevante y
**falló** (15,7 → 11,8). La afirmación de invariancia al modelo se retira y se sustituye por P2g.

### 10. Study 6 — ¿Repartir la varianza mejora el acierto individual? *(inconcluyente)* ⭐ *nuevo*
El prompt anti-concentración aplicado a los **encuestados reales** del Deustobarómetro, para medir
lo que Ikuspegi no permite: el acuerdo persona a persona.

- **La manipulación se aplicó:** cambian **10.841 de 45.448 respuestas (23,9 %)**.
- **Pero apenas mueve nada:** concentración 66,6 → 65,8 (−0,85); correlación de escalas 0,123 →
  0,137, **IC95 bootstrap [−0,001, +0,029]**, no distinguible de cero.
- **El prompt no transporta entre instrumentos.** En Ikuspegi liberó 4,3 puntos de concentración;
  aquí, 0,9 — y **no por falta de margen**: las categóricas del Deustobarómetro tienen el mismo
  número de opciones (4,7 vs 4-5) y parten de 75,3, comparable al 83,7 de Ikuspegi.
- **Interpretación tentativa:** el prompt se diseñó mirando un cuestionario de **inmigración**, un
  dominio donde el modelo se modera mucho y hay varianza suprimida que soltar. En temas generales
  no se está conteniendo igual. **El efecto del prompt depende del tema.**
- **Se reporta como inconcluyente por manipulación débil**, no como hipótesis refutada. Con Δ_C de
  −0,85 no hay manipulación suficiente para poner a prueba la separabilidad.

### 11. Study 7 — El ángulo de marketing
Subcorpus de 44 ítems seleccionados *ex ante* por constructo + 10 de contraste político.

| constructo | ítems | techo GBM | alcanzado | % techo | Δ vs moda | conc. panel / real |
|---|--:|--:|--:|--:|--:|--:|
| Retrenchment de consumo | 13 | 0,134 | 0,149 | — | −5,3 | 84,0 / 70,5 |
| Decisión de viaje | 5 | 0,137 | 0,051 | 38 % | −12,4 | 84,8 / 49,9 |
| Satisfacción de servicio | 16 | 0,254 | 0,072 | 28 % | −3,2 | 54,5 / 21,4 |
| Confianza de marca | 10 | 0,351 | 0,217 | 62 % | −5,7 | 47,3 / 19,8 |
| *(contraste) política* | 10 | 0,399 | 0,202 | 51 % | −5,7 | 45,5 / 21,2 |
| **TOTAL MARKETING** | **44** | **0,234** | **0,127** | **54 %** | **−5,3** | **65,0 / 38,8** |

**🔑 El techo de marketing es MÁS BAJO que el político.** Confianza de marca (0,35) y política
(0,40) van parejas, pero **consumo (0,13)** y **viaje (0,14)** se hunden. El perfil informa *menos*
sobre conducta de consumo que sobre actitud política — al revés de lo que necesita la promesa
comercial y al revés de donde la literatura pone sus benchmarks.

**Cautela obligatoria:** a nivel de ítem, con n≈300 y asimetría del 90 %, las correlaciones
individuales **no son interpretables** (IC bootstrap que incluyen el cero). Sólo lo son los
agregados por constructo.

### 12. Discussion
12.1 **Regla de decisión por tarea de marketing** *(el entregable gerencial)*.

| Tarea | ¿Depende de Var(y\|x) o de las colas? | Veredicto |
|---|---|---|
| Estimación *top-line* de incidencia | No | **Admisible** con tolerancia de DAM validada — y con un modelo frontera, defendible (DAM 11,8 vs moda 17,0) |
| Pretest de creatividades / wording | Parcial | Con cautela, como filtro |
| Segmentación y perfilado | **Sí** | **No admisible** |
| Heterogeneidad en conjoint / WTP | **Sí** | **No admisible** |
| Targeting, early adopters, colas | **Sí** | **No admisible** |
| Dominios sin encuesta donante | — | Peor rendimiento observado |

12.2 Por qué la escalada de capacidad **ayuda pero no resuelve**: el frontera mejora el agregado y
     deja los polos borrados. El techo es informacional.
12.3 Consecuencia sustantiva: el panel **borra el conflicto**. En temas polarizados produce un
     consenso que no existe.
12.4 Uso híbrido y PPI++: marco válido, señal insuficiente (recorte de IC ~1,1 %, porque va con
     corr²).
12.5 Limitaciones: región única; dominio de opinión pública más que de consumo puro; 13 ítems en la
     réplica; v2 no anidada en v1; una sola tanda por manipulación.

### 13. Conclusion
Los paneles sintéticos son un instrumento condicional, no un sustituto. La condición es comprobable
*ex ante* y la damos hecha.

---

## 5. Las tres contribuciones

1. **Diagnóstico *ex ante* transportable:** `corr_max = √R²_OOS`, calculable con una ola previa de
   microdatos antes de gastar un euro. No conocemos equivalente en la literatura de marketing.
2. **Caracterización del modo de fallo en dos componentes** —concentración y truncamiento del
   soporte— que se comportan de forma **opuesta** ante mejoras del modelo. Con índices medibles y
   siete implicaciones contrastables, todas verificadas.
3. **Separabilidad agregado/individuo** demostrada con un caso limpio y traducida en **regla de
   decisión por tarea de marketing**.

---

## 6. Estado de los huecos

| # | Hueco | Estado |
|---|---|---|
| 1 | Ángulo de marketing/consumo | ✅ **cerrado** — subcorpus de 44 ítems, §11 |
| 2 | Robustez con modelo frontera | ✅ **cerrado** — §9, resultado matizado |
| 3 | Prompt anti-concentración | ✅ **cerrado** — §9 (agregado) y §10 (individual, inconcluyente) |
| 4 | Marco teórico con rigor | ✅ **cerrado** — `seccion3_marco_teorico.md` |
| 5 | Microdatos de Ikuspegi | ⬜ no obtenidos; se declara como limitación |
| 6 | Declarar/variar temperature | ✅ **cerrado** — §9, F1 |
| 7 | Techo no lineal (GBM) | ✅ **cerrado** — se reportan los dos |
| 8 | Benchmark formal de 3 métodos | ⬜ **no se hará** — el contraste nominal (+7,88 vs −5,36) cubre lo esencial |

**Decisión (2026-08-22): no se harán más tandas. Se redacta con lo que hay.**

---

## 7. Correcciones aplicadas — leer antes de citar cualquier cifra

Cuatro errores detectados y corregidos. Todos iban en la dirección de **favorecer al panel**.

| # | Error | Efecto | Documento |
|---|---|---|---|
| 1 | Mapeo etiqueta→opción por contención de subcadena; colapsaba 29 de 89 categóricas | techo 0,240 → **0,225** | `incidencia_mapeo_idx_real.md` |
| 2 | Spearman comparado con techo Pearson | ratios inflados, hasta 367 % | `correccion_techo_global.md` |
| 3 | Ítems circulares en el numerador del techo alcanzado | 0,152 → **0,123** | `correccion_techo_global.md` |
| 4 | Ítems circulares en el Δ vs moda de nominales | **+1,61 → −5,36**: se cae "el único positivo del proyecto" | `preregistro_anticonc_individual.md` |

▸ **Al paper:** merece un párrafo de métodos. Cuatro errores independientes, todos favorables al
panel, detectados sólo porque había cifras de referencia con las que contrastar. Es un argumento de
peso a favor de publicar el paquete de replicación.

---

## 8. Ficheros de apoyo

| Fichero | Contenido |
|---|---|
| `seccion3_marco_teorico.md` | §3 redactada (inglés) |
| `seccion4_data_design.md` | §4 redactada (inglés) — *nuevo, 2026-08-24* |
| `resultados_marketing.md` · `marketing_items.json` | subcorpus de marketing, §11 |
| `preregistro_robustez.md` | huecos 2, 3 y 6 — predicciones y resultados, §9 |
| `preregistro_anticonc_individual.md` | anti-concentración individual, §10 + corrección 4 |
| `correccion_techo_global.md` | correcciones 2 y 3 |
| `incidencia_mapeo_idx_real.md` | corrección 1 |
| `subcorpus_marketing.md` | inventario de ítems y fuentes |
| `../piloto_ppi/techo_predictivo_v2.md` | techo corregido |

---

## 9. Referencias a incorporar

- Angelopoulos, A. N., Bates, S., Fannjiang, C., Jordan, M. I., & Zrnic, T. (2023). Prediction-powered
  inference. *Science*, 382(6671).
- Argyle, L. P., et al. (2023). Out of one, many: Using language models to simulate human samples.
  *Political Analysis*, 31(3), 337-351.
- Bisbee, J., et al. (2024). Synthetic replacements for human survey data? The perils of large
  language models. *Political Analysis*, 32(4), 401-416.
- Jones, C. R., & Bergen, B. K. (2025). Large language models pass the Turing test. *PNAS*.
- Sarstedt, M., et al. (2024). Using large language models to generate silicon samples in consumer
  and marketing research. *Psychology & Marketing*, 41(6), 1254-1270.
- Wang, Y., et al. (2024). arXiv:2412.19363.

---

## 10. Próximo paso

**Redactar.** Orden sugerido: ~~§4 (data and design, mecánico)~~ ✅ *borrador 1, 2026-08-24,
`seccion4_data_design.md`, con 5 pendientes marcados con ▸ dentro del fichero — el más importante
es confirmar la distinción Design A (digital twins, emparejados 1:1) / Design B (panel de
población, solo agregado), que no estaba escrita en ningún sitio como tal y la reconstruí a partir
de `resumen_construccion_panel.md` y `PASOS_ppi_full.md`.* → **§5-§8** (studies, los datos ya
están) → §9-§11 → §12 (discussion) → §1-§2 (intro y background, al final, cuando se sepa qué se
está introduciendo) → abstract.
