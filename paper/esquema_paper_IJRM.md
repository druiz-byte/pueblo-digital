# Esquema del paper — International Journal of Research in Marketing

**Autor:** David Ruiz (Universidad de Deusto)
**Destino:** IJRM, vía ordinaria (el special issue "Generative AI, Synthetic Data, and Synthetic
Respondents in Marketing Research", eds. Erdem y Pauwels, cerró el 1-may-2026).
**Estructura:** dos actos — techo de información (Acto I) + colapso de varianza (Acto II).
**Última actualización:** 2026-08-10

---

## 0. La tesis en una frase

Los encuestados sintéticos generados por LLM fallan a nivel individual por **dos causas
independientes y separables**: un límite superior que impone la información contenida en el perfil
(irreducible por cualquier método), y un colapso de la varianza condicional que el modelo añade por
debajo de ese límite — y que **empeora cuando se enriquece el perfil**.

Corolario operativo para el investigador de mercados: la fidelidad agregada y la fidelidad
individual son **estadísticamente independientes**. Se puede clavar la media y no acertar a ninguna
persona. Los casos de uso que motivan comercialmente los paneles sintéticos (segmentación,
heterogeneidad en conjoint, targeting, identificación de early adopters, análisis de colas) son
exactamente los que dependen de la varianza que el modelo destruye.

---

## 1. Título — candidatos

1. **"Two Ceilings: Information Limits and Variance Collapse in LLM-Based Synthetic Respondents"**
   *(el favorito: nombra las dos contribuciones, es memorable, y "ceiling" es vocabulario que un
   editor metodológico reconoce al instante)*
2. "Nailing the Mean, Missing Everyone: The Separability of Aggregate and Individual Fidelity in
   Synthetic Survey Panels"
3. "How Much Can a Synthetic Respondent Know? An Upper Bound on Profile-Conditioned LLM Survey
   Simulation"
4. "Richer Personas, Worse Predictions: Evidence Against the Enrichment Assumption in Synthetic
   Respondent Design"

---

## 2. Abstract (borrador, ~200 palabras)

> Synthetic respondents — large language models prompted to answer surveys as a person with a given
> profile — are being adopted in marketing research as a fast, cheap substitute for human panels.
> We show that their individual-level accuracy is bounded by two distinct and separable mechanisms,
> and we provide a diagnostic for each that researchers can compute before committing to the method.
>
> First, an **information ceiling**: regressing survey items on the full space of variables a
> profile could plausibly contain yields a mean out-of-sample R² of 0.080 across 100 items,
> implying a maximum attainable individual correlation of 0.24; 14% of items are unpredictable from
> any profile. This bound holds for any method, statistical or generative.
>
> Second, **variance collapse**: below that ceiling, the model reproduces the *direction* of profile
> effects correctly but compresses the conditional distribution onto the modal category (83.7%
> modal share versus 61.5% observed). Collapse intensifies with sample size and, critically, with
> profile enrichment — reversing the field's central design assumption.
>
> We validate against 152 items from an official regional barometer and replicate on an independent
> immigration-attitudes survey with 1,000 synthetic respondents. We conclude with a decision rule
> for when synthetic respondents are and are not admissible in marketing practice.

---

## 3. Arquitectura del argumento

```
                    ¿Qué puede saber una Persona sintética?
                                  │
        ┌─────────────────────────┴─────────────────────────┐
        │                                                   │
   ACTO I: TECHO                                    ACTO II: COLAPSO
   (límite de los datos)                            (fallo del modelo)
        │                                                   │
   corr_max = √R²_OOS = 0.24                        conc. 83.7% vs 61.5% real
   14/100 ítems con R² ≤ 0                          0/1000 en opciones del 34.2%
   independiente del LLM                            V(voto)=0.36 → SÍ usa el perfil
   independiente de N                               empeora con N y con enriquecimiento
        │                                                   │
        └─────────────────────────┬─────────────────────────┘
                                  │
                    SEPARABILIDAD AGREGADO / INDIVIDUO
                    P26: media 5.15 vs 5.30 (error 0.15)
                    pero 86.4% en {5,6} y 0% en {8,9,10}
                                  │
                        REGLA DE DECISIÓN PRÁCTICA
```

---

## 4. Estructura de secciones

### 1. Introduction
- Gancho: la promesa comercial (velocidad, coste, escalabilidad) y su adopción acelerada en
  *insights*. El call de IJRM/MSI como evidencia de que la disciplina se toma esto en serio.
- El vacío: la literatura valida sobre todo **distribuciones agregadas**. El criterio más exigente
  de Argyle et al. (2023), la *correspondencia de patrones*, apenas se ha puesto a prueba.
- Tres contribuciones declaradas explícitamente (ver §5).
- Adelanto de resultados y del alcance ("no sustituto, sí instrumento condicional").

### 2. Background
2.1 *Silicon sampling* y fidelidad algorítmica — Argyle et al. (2023) y sus 4 criterios.
2.2 Los *perils* — Bisbee et al. (2024, *Political Analysis*): sesgo y varianza reducida.
2.3 El puente al marketing — Sarstedt et al. (2024, *Psychology & Marketing*): guidelines.
2.4 Encuestados sintéticos en la práctica de insights — Wang et al. (2024, AAE), NIM, evidencia
    de industria.
2.5 **El hueco:** nadie ha separado *cuánto del error es irreducible* de *cuánto lo pone el modelo*.
    Esta distinción es la que decide si el problema es soluble con mejor ingeniería o no.

### 3. Framework: dos límites a la fidelidad individual
*(Sección conceptual corta — es la que hace que esto sea IJRM y no un informe técnico.)*

- Formalización: una Persona sintética es un estimador de $y_i$ condicionado a $x_i$ (el perfil).
- **Proposición 1 (techo).** Para cualquier estimador $\hat{y}(x)$, $\mathrm{corr}(\hat y, y) \le
  \sqrt{R^2_{\max}(y \mid x)}$. El LLM no puede superar la información del perfil; a lo sumo
  la explota óptimamente. Estimable fuera de muestra con microdatos reales.
- **Proposición 2 (colapso).** Un modelo puede respetar $E[y\mid x]$ y aun así fallar en
  $\mathrm{Var}(y \mid x)$. Se define el índice de concentración modal condicional y se argumenta
  por qué el entrenamiento por máxima verosimilitud + RLHF empuja hacia la moda condicional.
- **Corolario (separabilidad).** Fidelidad agregada ⊥ fidelidad individual. Consecuencias directas
  para los casos de uso de marketing.

### 4. Data and design
4.1 El panel: 1.000 Personas del País Vasco; muestreo estratificado, post-estratificación,
    emparejamiento k-NN por celda (lurral × sexo × edad_g × eus_g). Dos versiones (v1, v2) para el
    contraste de enriquecimiento.
4.2 **Validación primaria:** Deustobarómetro verano 2026, microdatos SPSS n=1.000, 152 ítems.
4.3 **Réplica externa:** Barómetro Ikuspegi 2025 (UPV/EHU), n=600, actitudes hacia la inmigración
    en la CAE. Otro equipo, otro tema, otra casa de campo, mismo universo. 13 ítems verificados.
4.4 Modelo, prompting y decodificación. **Declarar temperature = 1.0 (por defecto de la API), es
    decir, el escenario de máxima varianza posible.** El colapso NO es un artefacto de greedy
    decoding.
4.5 Baselines: moda, marginal (uniforme sobre categorías observadas), suelo de ruido de muestreo.
4.6 Métricas: DAM agregado; kappa ponderado, ±1, MAE, Spearman, Jaccard a nivel individual; índice
    de concentración modal; V de Cramér respuesta × perfil.

### 5. Study 1 — El techo de información
- Método: 152 ítems regresados sobre 68 columnas de perfil (sexo, edad+edad², provincia, lengua,
  situación laboral, estudios, religión, nacimiento, voto 2024, voto 2020, ideología 0-10,
  nacionalismo 0-10 + flags NS). R² fuera de muestra, CV 5-fold.
- Resultado: R² medio **0.080** → corr máx **0.24**; mediana 0.052; p90 0.202; máx 0.389.
  **14/100 ítems con R² ≤ 0.**
- Por bloque: economía 0.024 (0.15) · bienestar 0.034 (0.16) · miedos 0.059 (0.21) · turismo 0.085
  (0.29) · política 0.099 (0.28) · perfil 0.371 (0.61, control).
- Control de circularidad: los 2 ítems que *son* predictores dan R² = 1.00 y se excluyen.
- **Lectura:** el margen disponible es estrecho *antes* de que intervenga ningún LLM. Cualquier
  afirmación de "gemelo digital" debe medirse contra este techo, no contra cero.

### 6. Study 2 — Dónde está el panel respecto al techo
- Acuerdo individual 1:1, n=300 encuestados reales emparejados por id.
- Escalas 0-10 (54 ítems): Spearman medio **0.15**, MAE 2.04, ±1 en 48%, delta vs moda **−5.95**.
- Ordinales (48): kappa ponderado **0.100**, acierto 51.9% vs moda 56.5%, delta **−4.54**.
- Nominales (41): kappa **0.231**, delta vs moda **+1.61** (único positivo).
- Multi-respuesta (9): Jaccard 0.37, F1 0.46.
- **El panel alcanza ~51 % del techo (0,137 de 0,271).** ⚠ Cifra corregida el 2026-08-21: la
  anterior (65 % = 0,15 / 0,24) comparaba Spearman con un techo Pearson **e incluía los dos ítems
  circulares** (p36 ideología 0,83 · p38 nacionalismo 0,97). Ver `correccion_techo_global.md`.
  El pipeline no está roto: choca contra el
  límite. Este es el número que desactiva la objeción "es que vuestro panel está mal construido".
- Comparación con imputación estadística clásica: en nominales el clasificador lineal saca **+7.5
  p.p.** sobre la moda frente a **+1.6** del LLM. *Donde el ítem es imputable, la estadística
  clásica gana.*

### 7. Study 3 — Colapso de varianza (réplica externa, Ikuspegi)
- DAM **15.7 p.p.** con 1.000 Personas. Baselines sobre los mismos 13 ítems: moda **17.0**,
  uniforme 19.7, suelo de ruido 0.8. → **gana 1.3 p.p. a un baseline tonto.**
- **El DAM se sostiene entre instrumentos:** 15.7 (Ikuspegi) vs 13.4 (Deustobarómetro). El techo no
  depende del cuestionario.
- **Mecanismo — sobreconcentración:** opción modal 83.7% panel vs 61.5% real (+22 p.p.).
  NS/NC 1.4% vs 3.4%. **Sube con N** (81.7 → 83.7 al pasar de n=30 a n=1.000).
- **Cero de mil:** ninguna Persona elige "permitir la entrada sin obstáculo legal" (real 34.2%) ni
  "acoger sin restricciones" (real 31.3%). En el polo opuesto, misma compresión: "son demasiadas"
  3.0 vs 19.0; "prioridad para las autóctonas" 8.4 vs 29.2. **Borra los dos extremos a la vez** —
  no es sesgo direccional, es compresión.
- **El panel SÍ usa el perfil (falsación del diagnóstico ingenuo).** V de Cramér media: voto 0.36
  (máx 0.47) · euskera 0.19 · estudios 0.16 · clase 0.13 · género 0.11 · edad 0.08 · provincia 0.07.
  La dirección es correcta: acuerdo con expulsión por delito = Vox 90.6% · PP 65.7% · PNV 17.5% ·
  EH Bildu 5.5%. **No ignora a la Persona ni invierte el eje: comprime el rango.**
- **La ilustración limpia (P26, escala 0-10):** media panel 5.15 vs real 5.30 (error 0.15,
  aparentemente excelente), pero **86.4% en {5, 6}** y **cero** en {8, 9, 10}. Fidelidad agregada
  perfecta con validez individual nula, sin necesidad de bajar al microdato.

### 8. Study 4 — El enriquecimiento del perfil empeora el colapso
*(La sección con más potencial de contribución teórica: contradice el supuesto de diseño dominante.)*
- Diseño: v2 = Persona anclada en encuestado real + bloques de ESS España y EUSTAT Capital Social
  (5-6 llaves en vez de 4). Aporta justo los predictores canónicos de actitudes hacia la inmigración
  (confianza generalizada, inseguridad económica, seguridad percibida, cohesión).
- **Predicciones preregistradas antes de lanzar** (sección 7 de `diagnostico_ikuspegi_n1000.md`);
  las 2 que fallan lo hacen en dirección contraria a la falsación. *Esto es un activo enorme ante
  revisores; hay que destacarlo.*
- DAM v2 **18.2** vs v1 15.7 → **peor que el baseline de la moda (17.0)**.
- Concentración **88.8** vs 83.7. Opciones distintas usadas por pregunta: **2.7 (v2) vs 4.3 (v1)**.
- No es artefacto del voto degradado: restringiendo a Personas con partido, v1 14.7 / conc. 81.9 vs
  v2 17.9 / conc. **89.0**.
- Replica y **amplifica** el resultado del Deustobarómetro (Δ +0.4 allí, **Δ +2.5** aquí).
- **Lectura:** dado un perfil que ya ordena bien, enriquecerlo no recupera la varianza. El colapso
  lo pone el modelo, no la pobreza del anclaje. "Más estructura ≠ mejor predicción" pasa de
  anécdota a resultado replicado.
- Cautela a declarar: v2 no es "v1 + campos"; pierde religión, casi todo el perfil mediático y
  `principales_problemas`.

### 9. ¿Dónde aporta el panel? Análisis por tipo de ítem
- A · Política migratoria (5 ítems): DAM v1 18.0 vs moda 24.0 → **Δ +6.0** (4.6× el global).
- B · Valores/identidad (4): **Δ −5.3** (colapsa en la opción *equivocada*: 70-75% "Indecisión"
  cuando el real está de acuerdo 73.7/70.2%).
- C · Percepción factual (3): Δ +2.3.
- **"Donde aporta más" ≠ "donde acierta más":** el DAM del grupo A (18.0) es peor que el global,
  porque son ítems de distribución real dispersa — justo donde la sobreconcentración duele más.
- No se sostiene "a más uso del perfil, más aporta": corr(V(voto), Δ) = +0.10 (v1) / −0.21 (v2),
  frente a corr(concentración real, Δ) = **−0.33**.
- **Declarar el sesgo de selección:** el piloto de 13 ítems no es aleatorio y está sesgado **a
  favor** del panel (5 de 12 son política migratoria, su mejor bloque). **15.7 es probablemente
  optimista.** Declararlo desarma al revisor y refuerza la conclusión.

### 10. Robustness *(PENDIENTE DE EJECUTAR — ver §6 de este documento)*
10.1 Invariancia al modelo: repetir los 13 ítems con un modelo frontera.
10.2 Variante de prompt anti-concentración: legitimar NS/NC y posiciones minoritarias, prohibir el
     refugio en la opción intermedia. Cuantifica cuánta infidelidad es de prompting y cuánta del
     modelo.
10.3 Sensibilidad a temperature (0.0 / 1.0) — cierra la objeción de decodificación.
10.4 Techo no lineal (gradient boosting) para confirmar que 0.24 no es artefacto de linealidad.

### 11. Discussion
11.1 **Regla de decisión para la práctica de marketing** *(el entregable gerencial del paper)*.
     Antes de usar encuestados sintéticos, calcular el techo con los microdatos disponibles. Y luego:

| Tarea de investigación | ¿Depende de la varianza individual? | Veredicto |
|---|---|---|
| Estimación *top-line* de incidencia | No | Admisible con validación |
| Pretest de creatividades / wording | Parcial | Con cautela, como filtro |
| Segmentación y perfilado | **Sí** | **No admisible** |
| Heterogeneidad en conjoint / WTP | **Sí** | **No admisible** |
| Targeting, early adopters, colas | **Sí** | **No admisible** |
| Dominios sin encuesta donante | — | Peor rendimiento (DAM 28-30) |

11.2 Por qué la escalada de capacidad de los modelos no lo arregla: la fidelidad no ha seguido a la
     capacidad (Argyle GPT-3 → *perils* GPT-3.5/4 → Wang/Park GPT-4o → nosotros Haiku 4.5, y los
     sesgos persisten). El techo es informacional, no de modelo. *Turing conversacional ≠ fidelidad
     de panel* (Jones & Bergen 2025, PNAS).
11.3 Consecuencia sustantiva medible: el panel retrata a Euskadi como más tibia ante la inmigración
     de lo que es, **en las dos direcciones**. Los encuestados sintéticos no solo pierden precisión:
     **borran el conflicto**. Si se usan para research de opinión o de marca en temas polarizados,
     producen un consenso que no existe.
11.4 Uso híbrido: PPI++ (Angelopoulos et al. 2023) como forma *válida* de usar predicciones
     imperfectas. Resultado propio: recorte de IC ~1.1% — despreciable, porque el recorte va con
     corr² y corr = 0.15. Honesto y útil: el marco es correcto, la señal no da.
11.5 Limitaciones: región única; dominio de opinión pública más que de consumo; un modelo principal;
     13 ítems en la réplica; v2 no anidada en v1.

### 12. Conclusion
Los paneles sintéticos son admisibles como instrumento condicional, no como sustituto. La condición
es comprobable *ex ante* y la damos hecha.

---

## 5. Las tres contribuciones (declararlas así en la intro)

1. **Un diagnóstico *ex ante*, transportable y barato:** `corr_max = √R²_OOS`. Cualquier equipo con
   una ola previa de microdatos puede calcular su propio techo antes de gastar un euro en Personas
   sintéticas. Es la "methodological innovation in validating synthetic data" que pedía el call.
2. **La caracterización del modo de fallo:** no es indiferencia al perfil ni sesgo direccional, es
   **colapso de varianza condicional**, con un índice medible (concentración modal) que empeora
   monótonamente con N y con el enriquecimiento del perfil.
3. **La separabilidad agregado/individuo, demostrada con un caso limpio** (P26: media correcta,
   distribución destruida), y traducida en una regla de decisión por tipo de tarea de marketing.

---

## 6. Huecos que hay que cerrar antes de enviar a IJRM

Ordenados por riesgo de rechazo si no se hacen.

| # | Hueco | Por qué es crítico | Esfuerzo |
|---|---|---|---|
| 1 | **Ángulo de marketing/consumo** | Un revisor de IJRM preguntará por qué no hay una sola variable de consumo. Hoy la evidencia es de opinión pública. | Alto |
| 2 | **Robustez de modelo (frontera)** | Objeción #1 garantizada: "usasteis Haiku, un modelo pequeño y barato". Sin esto no pasa el primer round. Barato: 13 ítems. | Bajo |
| 3 | **Variante de prompt anti-concentración** | Objeción #2 garantizada: "es un artefacto de prompting". Además, si mueve algo, es contribución. | Medio |
| 4 | **Contribución teórica de la §3** | IJRM no publica benchmarks sin marco. Las dos proposiciones tienen que estar escritas con rigor, no como intuición. | Medio |
| 5 | Microdatos de Ikuspegi (UPV/EHU) | Permitiría calcular el techo en el dominio de la réplica. Sin ellos, "ítem informado" solo se aproxima con la V de Cramér del propio panel, que es circular. | Medio (gestión) |
| 6 | Sensibilidad a temperature | Cierra la objeción de decodificación. Hoy corre a 1.0 por defecto — hay que **verificarlo y declararlo**. | Bajo |
| 7 | Techo no lineal (GBM) | Robustez menor; se espera poco movimiento. | Bajo |
| 8 | Benchmark formal de 3 métodos | Imputación clásica vs Persona LLM vs LLM+PPI, con partición train/test reservada para no contaminar. Elevaría mucho el paper. | Alto |

### Sobre el hueco #1 — cómo resolver el ángulo de marketing

Tres caminos, de menos a más coste:

- **(a) Reencuadre argumental.** Sostener que la variable dependiente es indiferente: lo que se mide
  es una propiedad del *estimador*, no del dominio. Y apoyarse en que la industria vende encuestados
  sintéticos precisamente para las tareas que exigen varianza (segmentación, conjoint, targeting).
  *Barato, pero probablemente insuficiente por sí solo para IJRM.*
- **(b) Explotar los bloques ya existentes de consumo/comportamiento.** El barómetro incluye
  **consumo de medios** (`datos GV/` CSV medios 2025), **turismo** y **frecuencia de conductas**
  (p7). Recalcular techo, acuerdo individual y concentración restringiendo a estos bloques, y
  presentarlos como el caso marketing. *Coste bajo-medio, sin API. Es el camino recomendado.*
- **(c) Réplica en una encuesta de consumo con microdatos públicos.** Sería lo definitivo. Candidatos
  a explorar: paneles de consumo de Eustat/INE, ESS módulos de confianza al consumidor,
  encuestas de hábitos de compra con microdato abierto.

### Aviso: `email_to_jmr_editor.txt` está obsoleto

El borrador de julio presenta el panel como una contribución metodológica **positiva** ("mean
absolute deviation of 14.0 p.p.", "fidelity is highest where profiles are richly specified",
"r² > 0.95 in core domains"). La evidencia posterior lo contradice de plano: el delta vs moda es
≈0 o negativo, y **enriquecer el perfil empeora el resultado**. No enviar ese email. Si se contacta
con un editor, el pitch correcto es el de este esquema.

---

## 7. Referencias a incorporar formalmente

Pendientes de añadir a `literatura_relacionada.md`:

- Angelopoulos, A. N., Bates, S., Fannjiang, C., Jordan, M. I., & Zrnic, T. (2023). Prediction-powered
  inference. *Science*, 382(6671). arXiv:2301.09633.
- Argyle, L. P., Busby, E. C., Fulda, N., Gubler, J. R., Rytting, C., & Wingate, D. (2023). Out of one,
  many: Using language models to simulate human samples. *Political Analysis*, 31(3), 337-351.
- Bisbee, J., Clinton, J. D., Dorff, C., Kenkel, B., & Larson, J. M. (2024). Synthetic replacements for
  human survey data? The perils of large language models. *Political Analysis*, 32(4), 401-416.
- Jones, C. R., & Bergen, B. K. (2025). Large language models pass the Turing test. *PNAS*.
- Sarstedt, M., Adler, S. J., Rau, L., & Schmitt, B. (2024). Using large language models to generate
  silicon samples in consumer and marketing research: Challenges, opportunities, and guidelines.
  *Psychology & Marketing*, 41(6), 1254-1270.
- Wang, Y., et al. (2024). Automated social science / AAE for market research. arXiv:2412.19363.

---

## 8. Próximo paso

Decidir el orden de ataque:

- **Vía rápida:** cerrar huecos 2, 3 y 6 (todos baratos) + camino (b) del hueco 1, y empezar a
  redactar. ~2-3 semanas de trabajo antes del primer borrador completo.
- **Vía completa:** añadir el hueco 8 (benchmark de 3 métodos). Sube mucho la probabilidad en IJRM
  pero añade meses.
