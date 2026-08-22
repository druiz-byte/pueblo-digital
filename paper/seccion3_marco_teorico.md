# §3 — Marco teórico: dos límites a la fidelidad individual

> **Nota de idioma:** el texto de manuscrito va en **inglés**, porque es lo que se envía a IJRM y
> traducir después introduce deriva. Las notas editoriales, decisiones y pendientes van en español,
> marcados con `▸`. Borrador 1, 2026-08-21.

---

## 3.1 · Setup and notation

Consider a target population of respondents indexed by $i = 1, \dots, N$. Each respondent is
characterised by a **profile** $x_i \in \mathcal{X}$ — the vector of attributes available to the
researcher when constructing a synthetic respondent (demographics, geography, language, education,
occupation, and whatever attitudinal anchors the design injects) — and gives a response $y_i$ to
survey item $q$, taking values in $\mathcal{Y}_q$ (a rating scale, an ordered category, or an
unordered choice).

A **synthetic respondent** is a stochastic map
$$\hat{y}_i \sim \pi(\,\cdot \mid x_i, \rho, M),$$
where $\rho$ is the prompt template and $M$ the language model with its decoding parameters. Two
features of this object matter for what follows. First, $\pi$ depends on $i$ **only through
$x_i$**: whatever the model knows about respondent $i$, it knows it from the profile. Second,
$\pi$ is genuinely stochastic — at the default sampling temperature the same profile queried twice
need not return the same answer.

Write $f(x) = \mathbb{E}[\hat{y} \mid x]$ for the conditional mean of the synthetic response and
$\mu(x) = \mathbb{E}[y \mid x]$ for the conditional mean of the real response.

We evaluate synthetic respondents at two levels, and the distinction is the axis of this paper:

- **Aggregate fidelity** — how close the synthetic marginal $\hat{P}(y = k)$ is to the observed
  marginal $P(y = k)$. This is what published validations almost always report.
- **Individual fidelity** — how well $\hat{y}_i$ tracks $y_i$ for the *same* person $i$. This is
  Argyle et al.'s (2023) most demanding criterion, *pattern correspondence*, and it is what any
  application involving heterogeneity actually requires.

▸ *Aquí conviene una frase que sitúe el paper: la literatura valida sobre todo lo primero y*
*promete lo segundo.*

---

## 3.2 · Proposition 1 — The information ceiling

**Proposition 1.** *Let $g: \mathcal{X} \to \mathbb{R}$ be any predictor of $y$ that depends on $i$
only through $x_i$. Then*
$$\operatorname{corr}\big(g(x), y\big) \;\le\; \sqrt{R^2_{\max}}, \qquad
R^2_{\max} \;=\; \frac{\operatorname{Var}\big(\mu(x)\big)}{\operatorname{Var}(y)},$$
*with equality if and only if $g$ is an affine transformation of $\mu(x)$.*

*Proof.* By the tower property, $\operatorname{Cov}(g(x), y) = \operatorname{Cov}(g(x), \mu(x))$.
Cauchy–Schwarz gives $\operatorname{Cov}(g(x), \mu(x)) \le \sigma_{g} \, \sigma_{\mu}$, so
$\operatorname{corr}(g, y) \le \sigma_{\mu} / \sigma_{y} = \sqrt{R^2_{\max}}$. Equality requires
$g$ and $\mu$ to be perfectly linearly dependent. $\square$

Two extensions matter in practice.

**(i) Stochastic responses can only lower the bound.** A synthetic respondent does not return
$f(x_i)$ but a draw $\hat{y}_i$ around it. Decomposing
$\operatorname{Var}(\hat{y}) = \operatorname{Var}(f(x)) + \mathbb{E}[\operatorname{Var}(\hat{y}\mid x)]$
and noting that the second term contributes nothing to $\operatorname{Cov}(\hat y, y)$,
$$\operatorname{corr}(\hat{y}, y) \;=\; \operatorname{corr}(f(x), y)\cdot
\sqrt{\frac{\operatorname{Var}(f(x))}{\operatorname{Var}(\hat{y})}} \;\le\; \sqrt{R^2_{\max}}.$$
Sampling noise is a strict attenuation. The ceiling therefore binds *a fortiori* for any
temperature setting.

**(ii) The bound is a property of the data, not of the method.** $R^2_{\max}$ is determined by the
joint distribution of $(x, y)$ in the target population. It does not depend on the language model,
the prompt, the number of synthetic respondents generated, or indeed on whether the predictor is
generative at all. A better model cannot cross it; neither can hot-deck imputation, $k$-NN
matching, or a regression. **It is the amount of information the profile carries about the answer.**

### Estimation

$R^2_{\max}$ is unobserved but estimable from a single wave of real microdata: regress $y$ on a
flexible function of $x$ and take the **out-of-sample** $R^2$. Three remarks, each of which we
implement:

1. **Out-of-sample is essential.** With a rich profile the in-sample $R^2$ is upward-biased and
   would inflate the estimated ceiling — precisely the direction that would flatter the method.
2. **The estimate is conservative in the model class.** A linear estimator recovers
   $\operatorname{Var}(\mu(x))$ only if $\mu$ is linear in the design matrix; otherwise it
   understates the ceiling. We therefore report both a regularised linear estimate and a gradient
   boosting estimate, and treat the larger as the operative bound.
3. **Cross-validation noise is not negligible.** In our data the standard deviation of the $R^2$
   estimate across repeated 5-fold partitions is $0.013$, which is of the same order as the signal
   for low-ceiling items. Single-split estimates are not reportable; we average over 20 repetitions
   with an item-specific seed.

▸ *Este punto 3 vino de encontrar que la semilla era global y secuencial. Merece nota al pie: es*
*un fallo de reproducibilidad frecuente y barato de arreglar.*

### Why this is the paper's first contribution

The ceiling is a **pre-commitment diagnostic**. Any organisation contemplating synthetic
respondents typically already holds one wave of real microdata on the same population. Running the
regression above costs minutes and returns the maximum individual-level correlation any method
could achieve on each item, before a single euro is spent on generation. We know of no comparable
*ex ante* test in the marketing literature.

▸ *Cifras a insertar: techo medio 0,22 (lineal) / 0,23 (GBM) sobre 100 ítems; 15 con R² ≤ 0.*
*Por constructo de marketing: consumo 0,13 · viaje 0,14 · satisfacción 0,25 · marca 0,35, frente a*
*contraste político 0,40. Ver `resultados_marketing.md`.*

---

## 3.3 · Proposition 2 — Conditional variance collapse

Proposition 1 bounds what any profile-conditioned method can achieve. It says nothing about
*how* a language model fails when it falls short. The natural hypotheses — that the model ignores
the profile, or that it applies a directional bias — are both refutable, and in our data both are
refuted. What we observe instead is a failure of the **second** moment.

**Definitions.** For a categorical item with support $\{1, \dots, K\}$, define the **conditional
modal concentration** of a response distribution $P$ as
$$C(P) \;=\; \mathbb{E}_x\Big[\max_{k} \; P(y = k \mid x)\Big],$$
and the corresponding marginal quantity $\bar{C}(P) = \max_k P(y = k)$. The **collapse index** is
$$\Delta_C \;=\; \bar{C}(\hat{P}) - \bar{C}(P) .$$

**Proposition 2 (variance collapse).** *A synthetic respondent may reproduce the ordering of
conditional means — $\operatorname{corr}(f(x), \mu(x))$ large and correctly signed — while
systematically compressing the conditional distribution:*
$$\operatorname{Var}(\hat{y} \mid x) \;\ll\; \operatorname{Var}(y \mid x)
\quad\text{for almost every } x, \qquad \Delta_C > 0 .$$

The two moments are logically independent: nothing in matching $\mu$ constrains
$\operatorname{Var}(y \mid x)$. Persona prompting optimises the former and is silent on the latter.

**Mechanism.** We offer a conjecture rather than a proof. Language models are trained to place mass
on likely continuations and are further tuned, through preference optimisation, toward responses a
rater would judge appropriate. Conditioning on a persona description therefore elicits the
*typical* response of that type — a conditional mode — rather than a draw from the within-type
distribution. A persona is a stereotype, and a stereotype is a point, not a distribution. Real
populations contain substantial within-cell heterogeneity that the profile does not explain
(Proposition 1 quantifies exactly how much); a model that emits the conditional mode discards all
of it.

### Testable implications

| | Prediction | Status in our data |
|---|---|---|
| **P2a** | $\Delta_C > 0$, and does not vanish as the number of synthetic respondents grows | Confirmed; $\Delta_C$ **increases** with $N$ (81.7 → 83.7 from $n=30$ to $n=1{,}000$) |
| **P2b** | $\Delta_C$ does not shrink when the profile is enriched | Confirmed and amplified: enrichment **worsens** it (83.7 → 88.8) |
| **P2c** | Direction is preserved — profile effects are correctly signed and non-trivial in size | Confirmed; Cramér's $V$ with vote choice averages 0.36 |
| **P2d** | Extreme categories are systematically under-produced | Confirmed; two options held by 34.2 % and 31.3 % of the real population were chosen by **none** of 1,000 synthetic respondents |

▸ *P2b es el resultado que más va a sorprender al revisor, porque contradice el supuesto de diseño*
*dominante ("más contexto, mejor Persona"). Conviene enunciarlo en la intro, no esconderlo aquí.*

▸ *Falta por decidir si P2a se enuncia sobre $\Delta_C$ marginal o sobre $C$ condicional. El dato*
*que tenemos es marginal; el condicional exigiría celdas con n suficiente. Propongo enunciar en*
*marginal y mencionar el condicional como extensión.*

---

## 3.4 · Corollary — Separability of aggregate and individual fidelity

**Corollary.** *Aggregate fidelity places no lower bound on individual fidelity. For any target
marginal distribution there exist assignments of $\hat{y}$ that reproduce it exactly while attaining
$\operatorname{corr}(\hat{y}, y) = 0$.*

The construction is immediate: permute the observed responses at random across respondents. The
marginal is preserved by construction and the individual correlation is zero in expectation. If
43 % of a population answers "fair", then assigning "fair" to a random 43 % reproduces the histogram
perfectly and identifies no one.

The corollary has an uncomfortable implication for practice. **The validation evidence the industry
reports — agreement between synthetic and observed marginals — is uninformative about the property
that most applications actually need.** A vendor can report low mean absolute deviation on
top-line distributions while the individual-level correlation is indistinguishable from zero, and
there is no contradiction between the two claims.

We document a case that makes the point without any recourse to microdata. On a 0–10 scale, the
synthetic panel returns a mean of 5.15 against an observed 5.30 — an error of 0.15, which any
practitioner would call an excellent result. Yet 86.4 % of synthetic respondents place themselves
at 5 or 6, and **not one** of 1,000 chooses 8, 9 or 10. The first moment is essentially exact; the
distribution is destroyed. *Inspecting the variance is sufficient to detect the failure.*

### From corollary to decision rule

Partition marketing research tasks by whether the quantity of interest is a functional of the
marginal alone, or depends on the conditional distribution:

| Task | Depends on $\operatorname{Var}(y \mid x)$ or tail mass? | Admissible? |
|---|---|---|
| Top-line incidence estimation | No | Yes, subject to validated DAM tolerance |
| Copy or concept pre-testing | Partially | With caution, as a screen |
| Segmentation and profiling | **Yes** | **No** |
| Conjoint / WTP heterogeneity | **Yes** | **No** |
| Targeting, early-adopter identification | **Yes (tails)** | **No** |
| Domains with no donor survey | — | Worst observed performance |

The rule inverts the commercial proposition. Synthetic respondents are marketed for speed and scale
in exactly the tasks — segmentation, heterogeneity, targeting — that the failure mode invalidates,
and are defensible mainly for the one task, top-line estimation, where conventional methods are
already cheapest.

▸ *Esta tabla es el entregable gerencial del paper. Debe repetirse en la Discussion.*

---

## 3.5 · Two ceilings, one diagnosis

The two propositions are independent and compose. Proposition 1 fixes an upper bound $\sqrt{R^2_{\max}}$
that no method can cross. Proposition 2 says that a language model operating below that bound fails
in a specific, measurable way that neither more data nor a richer profile repairs. Together they
explain an otherwise puzzling pattern: aggregate results that look publishable, individual results
that are worthless, and an enrichment strategy that makes matters worse.

▸ *Cierre alternativo, más agresivo, a valorar: "El problema no es que el modelo no sepa lo*
*suficiente sobre la persona; es que sabe justo lo suficiente para producir un estereotipo, y un*
*estereotipo no es una muestra."*

---

## Pendientes de esta sección

1. Insertar las cifras definitivas del techo global una vez recalculado con métricas homogéneas.
2. Decidir si el paper reporta techo lineal, GBM o ambos (recomendación: **ambos**, con el GBM como
   cota operativa y el lineal como referencia conservadora).
3. Formalizar mejor el mecanismo de 3.3 o rebajarlo explícitamente a conjetura. **Riesgo de
   revisión:** si se enuncia como si estuviera demostrado, un revisor lo tumba.
4. Decidir la notación de $\Delta_C$ (marginal vs condicional) — ver nota en 3.3.
5. Referencias a citar en esta sección: Argyle et al. (2023) para los cuatro criterios de fidelidad
   algorítmica; Bisbee et al. (2024) para varianza reducida; Sarstedt et al. (2024) para el puente
   al marketing.
