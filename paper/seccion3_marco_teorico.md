# §3 — Marco teórico: dos límites a la fidelidad individual

> **Nota de idioma:** el texto de manuscrito va en **inglés**, porque es lo que se envía a IJRM y
> traducir después introduce deriva. Las notas editoriales, decisiones y pendientes van en español,
> marcados con `▸`.
>
> **Borrador 2, 2026-08-22.** Reescrito tras los tres experimentos de robustez con n=1.000
> (`preregistro_robustez.md`). El cambio de fondo respecto al borrador 1: **la Proposición 2 se
> desdobla en dos partes**, porque los datos muestran que la compresión de varianza y la borradura
> del soporte se comportan de forma distinta — y **opuesta** — cuando mejora el modelo.

---

## 3.1 · Setup and notation

Consider a target population of respondents indexed by $i = 1, \dots, N$. Each respondent is
characterised by a **profile** $x_i \in \mathcal{X}$ — the vector of attributes available to the
researcher when constructing a synthetic respondent — and gives a response $y_i$ to survey item
$q$, taking values in a finite set $\mathcal{Y}_q = \{1, \dots, K\}$.

A **synthetic respondent** is a stochastic map
$$\hat{y}_i \sim \pi(\,\cdot \mid x_i, \rho, M, \tau),$$
where $\rho$ is the prompt template, $M$ the language model and $\tau$ the decoding temperature.
Two features matter. First, $\pi$ depends on $i$ **only through $x_i$**. Second, $\pi$ is genuinely
stochastic: at the default temperature the same profile queried twice need not return the same
answer.

Write $f(x) = \mathbb{E}[\hat{y} \mid x]$ and $\mu(x) = \mathbb{E}[y \mid x]$.

We evaluate synthetic respondents at two levels:

- **Aggregate fidelity** — closeness of the synthetic marginal $\hat{P}$ to the observed marginal
  $P$. This is what published validations almost always report.
- **Individual fidelity** — how well $\hat{y}_i$ tracks $y_i$ for the *same* person. This is Argyle
  et al.'s (2023) most demanding criterion, *pattern correspondence*, and what any application
  involving heterogeneity requires.

---

## 3.2 · Proposition 1 — The information ceiling

**Proposition 1.** *Let $g: \mathcal{X} \to \mathbb{R}$ be any predictor of $y$ that depends on $i$
only through $x_i$. Then*
$$\operatorname{corr}\big(g(x), y\big) \;\le\; \sqrt{R^2_{\max}}, \qquad
R^2_{\max} \;=\; \frac{\operatorname{Var}\big(\mu(x)\big)}{\operatorname{Var}(y)},$$
*with equality if and only if $g$ is an affine transformation of $\mu(x)$.*

*Proof.* By the tower property, $\operatorname{Cov}(g(x), y) = \operatorname{Cov}(g(x), \mu(x))$.
Cauchy–Schwarz gives $\operatorname{Cov}(g(x), \mu(x)) \le \sigma_{g}\sigma_{\mu}$, hence
$\operatorname{corr}(g, y) \le \sigma_{\mu}/\sigma_{y} = \sqrt{R^2_{\max}}$. $\square$

**(i) Stochastic responses can only lower the bound.** Decomposing
$\operatorname{Var}(\hat{y}) = \operatorname{Var}(f(x)) + \mathbb{E}[\operatorname{Var}(\hat{y}\mid x)]$,
$$\operatorname{corr}(\hat{y}, y) = \operatorname{corr}(f(x), y)\cdot
\sqrt{\tfrac{\operatorname{Var}(f(x))}{\operatorname{Var}(\hat{y})}} \;\le\; \sqrt{R^2_{\max}}.$$
The bound therefore holds for **any** temperature. This is not merely a theoretical remark: §3.4
reports that varying $\tau$ from its default to $0$ changes every distributional statistic we
measure by less than half a percentage point.

**(ii) The bound is a property of the data, not of the method.** $R^2_{\max}$ is fixed by the joint
distribution of $(x,y)$. No language model, prompt, or sample size crosses it; neither does
hot-deck imputation or $k$-NN matching. **It is the amount of information the profile carries about
the answer.**

### Estimation

$R^2_{\max}$ is estimable from a single wave of real microdata: regress $y$ on a flexible function
of $x$ and take the **out-of-sample** $R^2$. Three implementation points:

1. **Out-of-sample is essential.** In-sample $R^2$ with a rich profile is upward-biased — precisely
   the direction that flatters the method.
2. **The estimate is conservative in the model class.** A linear estimator recovers
   $\operatorname{Var}(\mu(x))$ only if $\mu$ is linear in the design matrix. We report both a
   regularised linear and a gradient boosting estimate and **treat the larger as the operative
   bound**.
3. **Cross-validation noise is not negligible.** The standard deviation of the item-level $R^2$
   across repeated 5-fold partitions is $0.013$, of the same order as the signal for low-ceiling
   items. We average over 20 repetitions with an item-specific seed.

▸ *Cifras: techo medio 0,225 lineal / **0,271 GBM** sobre 100 ítems; 15 con R² ≤ 0. El panel alcanza*
*0,137, es decir **~51 % del techo**. Por constructo de marketing: consumo 0,13 · viaje 0,14 ·*
*satisfacción 0,25 · marca 0,35, frente a contraste político 0,40.*

---

## 3.3 · Proposition 2 — Two distinct distributional failures

Proposition 1 bounds what any profile-conditioned method can achieve. It says nothing about *how*
a language model fails below that bound. The obvious hypotheses — that the model ignores the
profile, or applies a directional bias — are both refutable, and both are refuted in our data.
What we observe is a failure of the response **distribution**, and it decomposes into two
components that behave differently.

### Definitions

For a categorical item with support $\{1,\dots,K\}$ and real marginal $p_k = P(y=k)$, let
$\hat{p}_k$ be the synthetic marginal.

**(a) Concentration.** The modal share $\bar{C}(P) = \max_k p_k$, and the **collapse index**
$$\Delta_C = \bar{C}(\hat{P}) - \bar{C}(P) \;\ge\; 0 .$$
This is a second-moment statistic: how much mass piles onto the single most likely answer.

**(b) Support truncation.** For a tolerance $\varepsilon$, the set of **erased categories**
$$\mathcal{E}_\varepsilon = \{\,k : p_k \ge \delta \ \text{and}\ \hat{p}_k < \varepsilon\,\},$$
and the **erased mass** $\;\mathcal{M} = \sum_{k \in \mathcal{E}_\varepsilon} p_k$. Equivalently,
the **recovery ratio** of a category, $r_k = \hat{p}_k / p_k$.

These are not the same phenomenon. A distribution can become less concentrated while its support
*shrinks*, if the model redistributes mass among the already-dominant categories and abandons the
rare ones. Our data show exactly that.

### Statement

**Proposition 2.** *A synthetic respondent may reproduce the ordering of conditional means —
$\operatorname{corr}(f(x), \mu(x))$ large and correctly signed — while (a) compressing the
conditional distribution, $\Delta_C > 0$, and (b) assigning near-zero probability to categories
that hold substantial mass in the population, $\mathcal{M} \gg 0$. Component (a) attenuates with
model capability; component (b) is far more persistent.*

The two moments are logically independent of $\mu$: nothing in matching the conditional mean
constrains either $\operatorname{Var}(y\mid x)$ or the support of $\hat{P}$. Persona prompting
optimises the first and is silent on the other two.

### Mechanism — stated as a conjecture

Language models place mass on likely continuations and are further tuned, through preference
optimisation, toward responses a rater would judge appropriate. Conditioning on a persona
description elicits the *typical* response of that type rather than a draw from the within-type
distribution: **a persona is a stereotype, and a stereotype is a point, not a distribution.**

The experiments in §3.4 let us sharpen this. Component (b) is **not** a matter of permission: when
the prompt explicitly states that minority and extreme positions are legitimate answers, the model
redistributes mass among moderate options and still assigns **exactly zero** to the poles. Whatever
suppresses polar responses operates upstream of instruction-following.

▸ **Riesgo de revisión.** Este párrafo se declara explícitamente como conjetura. Si se enuncia como
demostrado, un revisor lo tumba — y con razón, porque no tenemos acceso al interior del modelo.

---

## 3.4 · Empirical characterisation: what moves each component

We manipulate three factors independently on the same 1,000 personas and the same 13 items, holding
everything else fixed. Real marginals come from an independent survey of the same population
(Ikuspegi 2025, $n=600$).

| | $\Delta_C$ | NS/DK | support (options with mass) | effective options | recovery $r$: P11 · P13 | MAD |
|---|--:|--:|--:|--:|--:|--:|
| Baseline (small model, $\tau$ default) | **22.2** | 1.4 % | 4.3 | 1.66 | **0.00 · 0.00** | 15.7 |
| + anti-concentration prompt | **17.9** | 2.0 % | 4.5 | 1.73 | **0.00 · 0.00** | 14.8 |
| + temperature $\tau = 0$ | **22.6** | 1.1 % | 4.2 | 1.64 | **0.00 · 0.00** | 15.8 |
| + frontier model | **13.5** | 0.0 % | **3.6** | 2.03 | **0.09 · 0.25** | **11.8** |
| *Observed population* | — | 3.4 % | — | — | 1.00 · 1.00 | — |

*P11 and P13 are the two most permissive options on immigration policy and asylum, held by 34.2 %
and 31.3 % of the population respectively.*

Four findings, each of which constrains the theory:

**F1 · Decoding temperature is irrelevant.** Setting $\tau = 0$ changes $\Delta_C$ by $+0.4$ points
and every other statistic by less. The collapse is not a sampling artefact, and — as Proposition 1(i)
anticipates — the ceiling binds regardless of $\tau$.

**F2 · Instruction moves concentration but not support — and only on some instruments.** The
anti-concentration prompt lowers $\Delta_C$ from 22.2 to 17.9 and raises the don't-know rate,
redistributing mass *among moderate options*. The erased mass is **unchanged at 100 %**. Component
(a) is partly addressable by prompting; component (b) is not.

The effect is, however, **instrument-dependent**. Applied to a second survey covering general
topics — the economy, wellbeing, public services, politics — the same prompt altered **23.9 % of
individual responses** yet moved concentration by only **0.9 points**, against 4.3 on the
immigration instrument. This is not a ceiling artefact: the categorical items of the second survey
have the same number of options (4.7 versus 4–5) and start from a comparable concentration (75.3
versus 83.7). We conjecture that the prompt has purchase where the model is actively moderating —
a socially sensitive domain with substantial suppressed variance — and little elsewhere. **The
prompt is not a general remedy; its effect depends on the topic.**

**F3 · Model capability attenuates (a) and only dents (b).** The frontier model achieves the best
aggregate fit we observe (MAD 11.8, against 17.0 for a modal-response baseline) and lowers
$\Delta_C$ to 13.5. It is also the first configuration in which polar categories receive **any**
mass at all. But recovery remains at 0.09 and 0.25: **roughly 83 % of the polar mass is still
erased.**

**F4 · Concentration and support move in opposite directions.** The frontier model is *less*
concentrated yet uses *fewer* categories (4.3 → 3.6 options with non-zero mass), while its effective
number of options rises (1.66 → 2.03). It balances the dominant alternatives better and
**annihilates the tail more completely**. Any account that treats the failure as a single
"compression toward the middle" is contradicted by this pattern.

▸ *F4 es el hallazgo más nuevo y el que más conviene destacar: obliga a separar los dos componentes*
*y refuta la lectura ingenua del colapso.*

### Testable implications, and their status

| | Prediction | Status |
|---|---|---|
| **P2a** | $\Delta_C > 0$ and does not vanish with sample size | Confirmed; increases from $n=30$ to $n=1{,}000$ |
| **P2b** | $\Delta_C$ does not shrink when the profile is enriched | Confirmed; enrichment **worsens** it (22.2 → 27.3) |
| **P2c** | Direction is preserved and non-trivial | Confirmed; Cramér's $V$ with vote 0.36, and the political gradient **sharpens** with the better model |
| **P2d** | Polar categories are systematically under-produced | Confirmed; $\mathcal{M} = 100\,\%$ for three of four configurations, 83 % for the fourth |
| **P2e** | The failure is invariant to decoding temperature | Confirmed (F1) |
| **P2f** | Explicit instruction does not restore the support | Confirmed (F2) |
| **P2g** | Concentration attenuates with model capability; support truncation persists | Confirmed (F3, F4) |

▸ **Honestidad obligada.** P2g es una **corrección** de lo que este marco afirmaba en su primera
versión. Preregistramos que el modelo frontera no mejoraría el DAM de forma relevante y **falló**:
mejoró de 15,7 a 11,8. La afirmación de invariancia al modelo hay que retirarla y sustituirla por
ésta, más fina y mejor soportada. Que el preregistro esté fechado y sea público es lo que permite
hacer esta corrección sin que parezca oportunismo.

---

## 3.5 · Corollary — Separability of aggregate and individual fidelity

**Corollary.** *Aggregate fidelity places no lower bound on individual fidelity. For any target
marginal there exist assignments of $\hat{y}$ that reproduce it exactly while attaining
$\operatorname{corr}(\hat{y}, y) = 0$.*

The construction is immediate: permute the observed responses at random across respondents. The
marginal is preserved and the individual correlation is zero in expectation. If 43 % of a
population answers "fair", assigning "fair" to a random 43 % reproduces the histogram perfectly and
identifies no one.

The implication for practice is uncomfortable. **The validation evidence the industry reports —
agreement between synthetic and observed marginals — is uninformative about the property most
applications need.** A vendor can report low mean absolute deviation on top-line distributions while
individual-level correlation is indistinguishable from zero, with no contradiction between the two
claims.

One case makes the point without recourse to microdata. On a 0–10 scale the synthetic panel returns
a mean of 5.15 against an observed 5.30 — an error of 0.15, which any practitioner would call
excellent. Yet 86.4 % of synthetic respondents place themselves at 5 or 6, and **not one** of 1,000
chooses 8, 9 or 10. The first moment is essentially exact; the distribution is destroyed.
*Inspecting the variance suffices to detect the failure.*

### From corollary to decision rule

| Task | Depends on $\operatorname{Var}(y \mid x)$ or on tail mass? | Admissible? |
|---|---|---|
| Top-line incidence estimation | No | Yes, subject to a validated MAD tolerance |
| Copy or concept pre-testing | Partially | With caution, as a screen |
| Segmentation and profiling | **Yes** | **No** |
| Conjoint / WTP heterogeneity | **Yes** | **No** |
| Targeting, early-adopter identification | **Yes (tails)** | **No** |
| Domains with no donor survey | — | Worst observed performance |

The rule inverts the commercial proposition. Synthetic respondents are marketed for the tasks —
segmentation, heterogeneity, targeting — that the failure mode invalidates, and are defensible
mainly for the one task where conventional methods are already cheapest.

▸ *Con los resultados nuevos hay un matiz que añadir a la primera fila: con un modelo frontera el*
*DAM baja a 11,8 y bate al baseline de la moda por 5,2 puntos, así que la estimación top-line pasa*
*de "admisible con reservas" a "razonablemente defendible". Las otras cinco filas no cambian.*

---

## 3.6 · An attempted test of separability, and why it is inconclusive

The sharpest prediction the framework makes is that releasing conditional variance should **not**
improve individual accuracy, because variance is not information (Proposition 1(i)). Testing it
requires paired microdata, which the immigration instrument lacks; we therefore applied the
anti-concentration prompt to the 300 matched respondents of the primary survey.

The manipulation reached the model — 23.9 % of individual responses changed — but produced almost
no movement in either direction:

| | default | anti-concentration | Δ |
|---|--:|--:|--:|
| Modal concentration | 66.6 | 65.8 | −0.85 |
| Correlation, 0–10 scales | 0.123 | 0.137 | +0.014 |
| Weighted $\kappa$, ordinal | 0.097 | 0.086 | −0.011 |
| $\Delta$ vs modal baseline, ordinal | −4.97 | −5.48 | −0.51 |

The rise in correlation is **not distinguishable from zero**: paired across 52 items,
$t = 1.79$, bootstrap 95 % CI $[-0.001, +0.029]$.

**We report this as inconclusive by weak manipulation, not as a refuted hypothesis.** One cannot
test whether releasing variance helps individual accuracy without having released appreciable
variance, and a 0.85-point shift in concentration does not qualify. Closing this would require
restricting the manipulation to the most concentrated items, where there is variance to release.

▸ *Honestidad: la predicción preregistrada de Claude era "el agregado mejora y el individual*
*empeora". **Es falsa en los dos términos.** Se reporta como fallo.*

---

## 3.7 · Two ceilings, one diagnosis

The two propositions are independent and compose. Proposition 1 fixes a bound $\sqrt{R^2_{\max}}$
that no method crosses. Proposition 2 says that a model operating below that bound fails in two
measurable ways, of which one yields partially to better models and better prompts and the other
barely yields at all.

Together they explain an otherwise puzzling pattern: aggregate results that look publishable,
individual results that are worthless, an enrichment strategy that makes matters worse, and a
frontier model that improves the headline number while still refusing to voice a third of the
population.

▸ *Cierre alternativo, más agresivo, a valorar: "El problema no es que el modelo no sepa lo*
*suficiente sobre la persona. Es que sabe lo suficiente para producir un estereotipo, y un*
*estereotipo no tiene colas."*

---

## Pendientes de esta sección
2. Formalizar $\mathcal{E}_\varepsilon$ con un $\varepsilon$ y un $\delta$ declarados (propuesta:
   $\varepsilon = 1\,\%$, $\delta = 10\,\%$) en lugar de dejarlos implícitos.
3. Decidir si el nº efectivo de opciones (1/Herfindahl) entra como métrica formal o se queda como
   apoyo. **Declarar que se añadió *a posteriori***, tras los experimentos.
4. Citas a colocar: Argyle et al. (2023) en 3.1; Bisbee et al. (2024) en 3.3 (varianza reducida);
   Sarstedt et al. (2024) en 3.5 (puente al marketing).
5. Comprobar que el ejemplo del 0–10 de 3.5 (P26) usa las cifras de la tanda correcta.
