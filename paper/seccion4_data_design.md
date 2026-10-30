# §4 — Data and design

> **Nota de idioma** (misma convención que §3): el texto de manuscrito va en **inglés**; las notas
> editoriales van en español, marcadas con `▸`.
>
> **Borrador 1, 2026-08-24.** Escrita a partir de `resumen_construccion_panel.md`,
> `fuentes_datos_panel.md`, `PASOS_ppi_full.md`, `PASOS_contraste_v1_oficial.md`,
> `preregistro_robustez.md`, `subcorpus_marketing.md` y `glosario.md`. Es la primera vez que este
> material se redacta como prosa continua para el manuscrito.

---

## 4.0 · Two designs, not one

Two distinct data-generating procedures recur under the label "the panel" across the studies below,
and keeping them apart is essential to reading the results correctly.

**Design A — profile-conditioned digital twins.** For each respondent in the primary validation
survey (§4.2) we construct a synthetic respondent whose profile $x_i$ is *that same person's own*
predictor variables, as recorded in the survey, and query the model for an answer to items the
profile does not already contain. Because $x_i$ belongs to an identified real respondent, the
resulting $\hat{y}_i$ can be compared one-to-one against that person's true $y_i$. This design
requires no language model at all for the ceiling itself — Study 1 (§5) regresses real $y$ on real
$x$ — and underlies individual-level fidelity throughout: Study 2 (§6) and the paired
anti-concentration probe (Study 6, §10).

**Design B — a population panel.** A separate panel of 1,000 synthetic personas is built by
stratified sampling from the marginals of an independent political barometer, then enriched with
wellbeing attributes through statistical matching (§4.1). These personas are not anchored to any
identified real respondent. The panel is queried against complete questionnaires and its *aggregate*
response distribution is compared to the real aggregate distribution of an external instrument. This
design underlies the distributional-collapse analysis (Study 3, §7), the enrichment contrast v1/v2
(Study 4, §8) and the three robustness manipulations (Study 5, §9) — all comparisons that, because
the validating instrument in those studies does not release individual microdata, can only be made
in aggregate.

The two designs share the same model, prompting approach and decoding settings (§4.5); they differ
in what the profile is anchored to and, consequently, in what level of fidelity they can test.

▸ *Esta separación no estaba escrita en ningún sitio como tal — la reconstruyo de
`resumen_construccion_panel.md` (panel v1 por muestreo estratificado, no anclado a individuos reales)
frente a `PASOS_ppi_full.md` (predicciones inyectando el perfil de cada encuestado real del
Deustobarómetro, sin las 152 respuestas objetivo, para emparejamiento 1:1). Conviene que la revises
antes de dar la sección por cerrada: en particular, confirmar que Study 4 (enriquecimiento) usa
solo Design B y no mezcla ambos.*

---

## 4.1 · The population panel (Design B)

The panel comprises 1,000 synthetic personas of the Basque Country (País Vasco / Euskadi), built in
two stages.

**Stratified sampling.** Sociodemographic, political and media attributes are drawn from an
independent regional political barometer, stratifying by territory (Álava, Gipuzkoa, Bizkaia), sex,
age group and Basque-language proficiency so that the panel reproduces the demographic structure of
the region; post-stratification weights by territory × language proficiency correct residual
deviation from population marginals. Each persona additionally receives a randomly assigned name
culturally consistent with its linguistic profile.

**Wellbeing enrichment via statistical matching.** Wellbeing attributes are not present in the
barometer and are imported from an independent wellbeing survey through nearest-neighbour matching
on four linking keys common to both instruments — territory, sex, four-band age group, and
two-category Basque proficiency — with exact-cell matching (all four keys) falling back to three,
two or one key when a cell is empty. Full four-key matching was achieved for 100 % of personas.

Two versions of the panel are used:

- **v1** — the panel described above, four linking keys, used as the reference configuration
  throughout Studies 3, 5 and as the baseline of Study 4.
- **v2** — an enriched variant built for the enrichment contrast (Study 4): personas are anchored to
  an identified real respondent and extended with blocks from a national social survey and a
  regional social-capital survey (5–6 linking keys instead of 4), adding canonical predictors of
  attitudes toward immigration (generalised trust, economic insecurity, perceived safety, social
  cohesion) that v1 lacks.

▸ *v2 ancla a un encuestado real ("anchored to an identified real respondent") en lugar de muestrear
de forma estratificada — esto la acerca a Design A en la construcción del perfil, aunque su uso en
Study 4 sigue siendo agregado, no emparejado 1:1. Merece una frase aclaratoria adicional; lo dejo
marcado para revisar contigo.*

---

## 4.2 · Primary validation instrument: Deustobarómetro

The primary source of real microdata is the Deustobarómetro, a political and social opinion survey
fielded by the authors' own institution (Universidad de Deusto) in summer 2026, $n = 1{,}000$,
covering the same population as the panel. We use the full SPSS microdata file, comprising 152
items organised in seven questionnaire blocks — economy, wellbeing, fears, tourism, politics,
geopolitics, and a profile/validation block — plus the respondent-level predictor variables (68
columns) used as $x$ throughout.

Two properties of this instrument make it the anchor of the design. First, item-level microdata are
available at the individual level, which is what permits Design A: for every one of the 152 items,
each real respondent's own answer $y_i$ can be paired with a synthetic answer $\hat{y}_i$ generated
from that respondent's own profile. Second, seven items of the profile/validation block are
themselves predictors injected into $x$ (ideology, Basque nationalism, education, religion, place of
birth, and vote recall in the 2024 and 2020 regional elections); these are **circular items** — the
model is asked to reproduce a variable it was already given — and are excluded from every ceiling
estimate and every individual-accuracy figure reported in this paper (§7 details the correction; an
earlier draft included them by mistake).

▸ *Acceso propio a los microdatos: es una fortaleza metodológica (permite el emparejamiento 1:1 que
la mayoría de la literatura no puede hacer) y también algo que un revisor puede señalar como
potencial conflicto — merece una frase explícita de declaración, no solo mencionarlo de pasada.*

---

## 4.3 · External replication: Ikuspegi

To test whether the results are an artefact of one questionnaire, one research team or one survey
house, we replicate the distributional-collapse analysis (Study 3) and the robustness manipulations
(Study 5) against Ikuspegi 2025, an independent survey on immigration attitudes in the Basque
Autonomous Community (CAE) fielded by a different research group at the University of the Basque
Country (UPV/EHU), $n = 600$. Ikuspegi shares no authors, no questionnaire items and no topic
overlap with the Deustobarómetro beyond the same target population, which is precisely what makes it
a useful check: a failure mode that reproduces across two unrelated instruments, topics and teams is
unlikely to be a property of either questionnaire.

Ikuspegi does not release individual microdata, so the comparison here is aggregate only — the
panel's synthetic marginal distribution against Ikuspegi's published real marginal, item by item, on
the 13 items used across Studies 3 and 5. This is the central limitation of the replication and is
declared as such in §12.5: **the paired individual-level test (Design A) is only possible on the
Deustobarómetro**, because it is the only instrument for which we hold both real microdata and the
right to generate paired predictions.

---

## 4.4 · Marketing subcorpus

A 44-item subcorpus is selected *ex ante*, by construct rather than by outcome, to address a
predictable reviewer objection: that the results above characterise political-opinion prediction,
not marketing research. All 44 items come from the Deustobarómetro (§4.2) and are grouped into four
constructs directly analogous to standard marketing-research tasks:

| Construct | Items | Analogue in marketing practice |
|---|--:|---|
| A · Cost-of-living retrenchment | 13 | category-level spending-intention tracker |
| B · Travel decisions | 5 | purchase intention / abandonment in a high-value category |
| C · Service satisfaction | 16 | multi-provider satisfaction tracker |
| D · Institutional/brand confidence | 10 | brand-trust tracker |
| E · *(contrast)* Political confidence | 10 | — |

A fifth block (E) of 10 political-confidence items, selected by the same *ex ante* procedure, serves
as an in-domain contrast: it lets us ask whether marketing-adjacent constructs behave differently
from the political-attitude items that dominate the rest of the paper, using the same instrument,
the same panel and the same period, so that any difference cannot be attributed to a change in
survey house or fielding date.

▸ **Límite a declarar sin rodeos.** Los 44 ítems miden consumo de medios, satisfacción con servicios
y comportamiento de gasto dentro de un barómetro de opinión pública general — son *marketing-
adyacentes*, no un estudio de consumo dedicado (no hay conjoint, no hay elección de producto
envasado). Un segundo bloque candidato (Sociómetro GV 2025, consumo de medios y confianza en
influencers, ~45 ítems, `subcorpus_marketing.md` §B) habría aportado un dominio de marketing más
puro y una cuarta casa de campo independiente, pero requería una tanda nueva con API y **se decidió
no lanzarla** (2026-08-22, "no se harán más tandas"). Esto va en Limitaciones (§12.5), no aquí, pero
hay que ser explícitos sobre qué se dejó fuera y por qué.

---

## 4.5 · Model, prompting and decoding

All main-text results (Studies 1–4, 6–8) use a single language model, Claude Haiku 4.5, queried
through the Anthropic API; we refer to it in this section as the *baseline model* and reserve the
term *frontier model* (Claude Opus 5) for the model-capability manipulation of Study 5, where it is
the only thing that changes relative to the baseline configuration.

Each synthetic respondent is instantiated by serialising its profile $x_i$ into a natural-language
persona description, which is passed to the model together with the survey item; the model answers
in the format the questionnaire specifies (single choice, multiple choice, or a 0–10 scale), and
responses are parsed against the same coding scheme as the real instrument. No call in the project
fixed the decoding `temperature` explicitly until the robustness experiments of Study 5; every other
result in this paper therefore ran at the Anthropic API's default of $\tau = 1.0$ — the
maximum-variance configuration available, not a decoding choice tuned in either direction. Study 5
(§9, F1) shows this is inconsequential: setting $\tau = 0$ changes every statistic we measure by
less than half a percentage point.

▸ *Pendiente: incluir aquí (o en un apéndice de reproducibilidad) el texto literal de la plantilla de
prompt — hoy solo tengo la descripción funcional, no la cadena exacta que ve el modelo. También
falta decidir si el detalle de concurrencia/reintentos (documentado en `preregistro_robustez.md` a
raíz del incidente del hueco 2) va en apéndice: no cambia ningún resultado, pero un revisor
meticuloso puede preguntar cómo se gestionaron los fallos de API.*

---

## 4.6 · Baselines

Three baselines contextualise every accuracy figure in the paper, none of which uses the language
model:

- **Modal baseline.** Always answer the single most frequent real category for that item. This is
  the baseline against which $\Delta$-vs-mode is computed throughout (Studies 2, 4, 6–8): a positive
  value means the panel beats a respondent who is simply told the most common answer and repeats it;
  a negative value — the outcome in every family of items we test — means it does not.
- **Uniform baseline.** Answer uniformly at random across the item's available options, ignoring
  both the profile and the real marginal. It is systematically worse than the modal baseline (MAD
  19.7 versus 17.0 on the Ikuspegi items) and is reported mainly as a sanity floor.
- **Sampling-noise floor.** The MAD between two independent real subsamples of the same size drawn
  from the same population (0.8 percentage points at $n = 1{,}000$). This is the error a *perfect*
  panel — one that reproduced the population exactly — would still show against a finite reference
  sample, and it is two orders of magnitude below every panel MAD we report.

▸ *El esquema (§4.6) llamaba a la segunda "marginal"; la tabla de referencia en
`preregistro_robustez.md` la llama "uniforme" (MAD 19,7). Son conceptualmente distintas: un baseline
"marginal" propiamente dicho —sortear cada respuesta según las proporciones reales— es la
construcción exacta del Corolario de separabilidad en §3.5 (reproduce el histograma y da correlación
individual cero), y con eso el MAD esperado sería ≈0, no 19,7. Uso "uniforme" aquí porque es la que
está numéricamente documentada; si el "marginal" del esquema se refería a otra cosa, hay que
corregir esa entrada del esquema.*

---

## 4.7 · Metrics

We report two families of metrics, aggregate and individual, because — as the Corollary in §3.5
formalises — they are logically independent and a method can score well on one while failing the
other.

**Aggregate fidelity** — closeness of the synthetic marginal to the real marginal, ignoring who said
what:

- **MAD** (mean absolute deviation): the mean, over an item's response options, of the absolute
  difference in percentage points between the synthetic and real share choosing that option. The
  headline measure of aggregate fit throughout the paper.
- **Modal concentration**: the share of respondents choosing the single most-selected option, real
  and synthetic side by side. The direct operationalisation of the collapse index $\Delta_C$
  (Proposition 2a).
- **Erased mass / recovery ratio**: for a category holding non-trivial real mass, the share of that
  mass the synthetic marginal reproduces (Proposition 2b; §3.3).
- **Effective number of options** (inverse Herfindahl index over the synthetic shares): declared
  explicitly as an *exploratory metric added after the fact*, once the pre-registered "number of
  options used" metric turned out to be mechanically increasing in sample size and therefore
  uninformative about concentration (§9).

**Individual fidelity** — agreement between the synthetic and real answer of the *same* person,
computable only under Design A (§4.0):

- **Pearson correlation**, on the same numeric coding as the ceiling estimate, is the metric compared
  against $\sqrt{R^2_{\max}}$ (§5). We do not use Spearman for this comparison: in items where close
  to 90 % of respondents fall in one category, rank correlation is inflated by tie handling and can
  exceed the Pearson-based ceiling, which is impossible by construction (§3.2, §7).
- **Weighted Cohen's $\kappa$**, exact-match rate and $\pm 1$-category accuracy for ordinal and
  nominal items.
- **MAE** and signed bias, in scale points, for 0–10 items.
- **$\Delta$ vs. mode**: exact-match accuracy of the panel minus exact-match accuracy of the modal
  baseline, item by item. This is the single most load-bearing statistic in the paper: it is negative
  in every item family we test, which is what "no individual result in this project is positive"
  (§6) means operationally.
- **Jaccard index and $F_1$** for multiple-response items, comparing the set of options chosen.
- **Cramér's $V$**, between a profile variable (typically vote) and the synthetic response, used not
  as a fidelity metric but as a falsification check on the hypothesis that the model ignores the
  profile altogether (§7).

---

## Pendientes de esta sección

1. Confirmar la separación Design A / Design B del §4.0, en particular si Study 4 mezcla ambos
   diseños en algún punto (nota en §4.1).
2. Decidir la redacción de "marginal" vs "uniforme" en §4.6 y corregir `esquema_paper_IJRM.md` si
   procede.
3. Añadir la plantilla de *prompt* literal (§4.5), como cita en el texto o como apéndice de
   reproducibilidad.
4. Verificar la cifra de "68 columnas de perfil" citada en §4.2/Study 1 contra el script real
   (`piloto_ppi/techo_v2.py` o `techo_gbm_global.py`), no la he recontado a mano.
5. Decidir si el segundo bloque de marketing (Sociómetro GV, no ejecutado) se menciona en §4.4 con
   este nivel de detalle o se deja solo para Limitaciones (§12.5), para no duplicar.
