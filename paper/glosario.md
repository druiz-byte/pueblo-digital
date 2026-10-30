# Glosario de variables y conceptos — Obaba-s

**Propósito:** reunir en un solo sitio las definiciones de las variables, parámetros y métricas
usadas en el paper (Acto I: techo de información · Acto II: colapso de varianza), a partir de las
preguntas de concepto planteadas a lo largo de las sesiones (covarianza, temperature, R², kappa,
DAM, etc.) y de las definiciones ya fijadas en `paper/seccion3_marco_teorico.md`,
`paper/esquema_paper_IJRM.md`, `paper/preregistro_robustez.md`, `paper/correccion_techo_global.md`
y `piloto_ppi/acuerdo_individual.md`.

**Convención de nombres:** los individuos sintéticos del panel se llaman siempre **Personas**, no
"agentes" (ver `CLAUDE.md`).

---

## 1 · Notación formal del marco teórico (§3)

Esta es la notación de `seccion3_marco_teorico.md`, la base de las Proposiciones 1 y 2.

| Símbolo | Nombre | Definición |
|---|---|---|
| $i = 1,\dots,N$ | Índice de respondente | Cada persona (real o sintética) de la población objetivo. |
| $x_i \in \mathcal{X}$ | Perfil | Vector de atributos disponibles para construir la Persona (demografía, geografía, lengua, educación, ocupación, anclas actitudinales inyectadas). |
| $y_i \in \mathcal{Y}_q$ | Respuesta real | Respuesta del respondente $i$ al ítem $q$ de la encuesta (escala, categoría ordenada o no ordenada). |
| $\hat{y}_i$ | Respuesta sintética | Respuesta de la Persona $i$, generada como $\hat{y}_i \sim \pi(\cdot \mid x_i,\rho,M)$. |
| $\rho$ | Plantilla de *prompt* | El texto que instancia a la Persona a partir de $x_i$. |
| $M$ | Modelo de lenguaje | El LLM y sus parámetros de decodificación (incluye `temperature`). |
| $\pi(\cdot \mid x_i,\rho,M)$ | Mapa estocástico | La Persona sintética: una distribución de probabilidad sobre respuestas, condicionada **solo** a $x_i$ (no conoce a $i$ más que a través de su perfil) y **genuinamente aleatoria** (la misma consulta dos veces no tiene por qué devolver la misma respuesta). |
| $f(x) = \mathbb{E}[\hat{y} \mid x]$ | Media condicional sintética | Lo que "en promedio" respondería la Persona con perfil $x$. |
| $\mu(x) = \mathbb{E}[y \mid x]$ | Media condicional real | Lo que "en promedio" responde la población real con perfil $x$. |
| $g(x)$ | Predictor genérico | Cualquier estimador de $y$ que dependa de $i$ solo a través de $x_i$ (incluye a $f$, pero también a un modelo estadístico clásico: imputación, $k$-NN, regresión). |

### Varianza, covarianza y correlación

Estos son los tres operadores estadísticos que sostienen la Proposición 1 — el bloque de
"covarianza" preguntado en las sesiones:

- $\operatorname{Var}(\cdot)$ — **varianza**: dispersión de una variable respecto a su media,
  $\operatorname{Var}(Z) = \mathbb{E}[(Z-\mathbb{E}[Z])^2]$.
- $\operatorname{Cov}(\cdot,\cdot)$ — **covarianza**: cómo varían conjuntamente dos variables,
  $\operatorname{Cov}(A,B) = \mathbb{E}[(A-\mathbb{E}[A])(B-\mathbb{E}[B])]$. En la demostración de
  la Proposición 1 se usa la propiedad de la torre para mostrar que
  $\operatorname{Cov}(g(x),y) = \operatorname{Cov}(g(x),\mu(x))$ — es decir, la covarianza de
  cualquier predictor con la respuesta real es igual a su covarianza con la media condicional
  real, porque $g$ solo "ve" a $y$ a través de $x$.
- $\operatorname{corr}(\cdot,\cdot)$ — **correlación de Pearson**: covarianza normalizada por las
  desviaciones típicas, $\operatorname{corr}(A,B) = \operatorname{Cov}(A,B)/(\sigma_A\,\sigma_B)$,
  acotada en $[-1,1]$. Es la métrica que acota la Proposición 1 (por Cauchy–Schwarz).

### El techo de información — Proposición 1

$$\operatorname{corr}\big(g(x), y\big) \;\le\; \sqrt{R^2_{\max}}, \qquad
R^2_{\max} \;=\; \frac{\operatorname{Var}\big(\mu(x)\big)}{\operatorname{Var}(y)}$$

| Símbolo | Nombre | Qué significa |
|---|---|---|
| $R^2_{\max}$ | Techo de información | Proporción de la varianza de $y$ que el perfil $x$ es capaz de explicar como máximo. Es una propiedad de los **datos** (la distribución conjunta de $x$ e $y$), no del método: ningún modelo, generativo o estadístico, puede superarla. |
| $\sqrt{R^2_{\max}}$ | Correlación máxima alcanzable ($corr_{\max}$) | La cota superior de correlación individual que *cualquier* predictor condicionado a $x$ puede lograr con $y$. Es el diagnóstico *ex ante* propuesto como primera contribución del paper. |

La demostración añade dos extensiones:

1. **La aleatoriedad solo puede bajar la cota.** Descomponiendo
   $\operatorname{Var}(\hat y) = \operatorname{Var}(f(x)) + \mathbb{E}[\operatorname{Var}(\hat y \mid x)]$,
   el ruido de muestreo (controlado por `temperature`, ver §3) atenúa la correlación observable
   pero nunca la mejora — la cota $\sqrt{R^2_{\max}}$ sigue rigiendo para cualquier ajuste de
   `temperature`.
2. **La cota no depende del modelo.** Ni del LLM, ni del *prompt*, ni del número de Personas
   generadas: es la cantidad de información que el perfil lleva sobre la respuesta.

**Estimación:** $R^2_{\max}$ no se observa directamente; se estima con microdatos reales
regresando $y$ sobre una función flexible de $x$ y tomando el $R^2$ **fuera de muestra**
(*out-of-sample*, OOS). Ver §3 de este glosario ("Techo de información — estimación práctica").

---

## 2 · Colapso de varianza — Proposición 2

| Símbolo | Nombre | Definición |
|---|---|---|
| $C(P) = \mathbb{E}_x\big[\max_k P(y=k\mid x)\big]$ | Concentración modal condicional | Probabilidad media (sobre los perfiles $x$) de que la respuesta caiga en la categoría más frecuente condicionada a ese perfil. |
| $\bar{C}(P) = \max_k P(y=k)$ | Concentración modal marginal | Lo mismo pero sobre la distribución agregada (sin condicionar en $x$). Es la que se reporta en la práctica como **"concentración de la opción modal"**. |
| $\Delta_C = \bar{C}(\hat P) - \bar{C}(P)$ | Índice de colapso | Diferencia entre la concentración modal del panel sintético y la real. $\Delta_C > 0$ es la operacionalización directa de la Proposición 2: el modelo comprime la distribución hacia la moda más de lo que hace la población real. |

La proposición dice que un modelo puede acertar el **primer momento** ($\mu(x) \approx f(x)$,
la media condicional) y aun así fallar en el **segundo momento**
($\operatorname{Var}(\hat y\mid x) \ll \operatorname{Var}(y\mid x)$): los dos no están ligados
lógicamente. Mecanismo propuesto (conjetura, no demostración): el entrenamiento por máxima
verosimilitud + RLHF empuja al modelo hacia la respuesta *típica* de un perfil (un estereotipo,
que es un punto) en vez de un sorteo de la distribución dentro de ese perfil.

---

## 3 · Techo de información — estimación práctica

| Término | Definición |
|---|---|
| **Techo lineal** | Estimación de $R^2_{\max}$ con un estimador lineal regularizado (ridge). Referencia conservadora: solo recupera $\operatorname{Var}(\mu(x))$ si $\mu$ es lineal en la matriz de diseño; si no, **infraestima** el techo. |
| **Techo GBM** | Estimación de $R^2_{\max}$ con *gradient boosting* (no lineal). Cota más exigente; el paper reporta **la mayor de las dos** como cota operativa (`techo_gbm.py`, `techo_gbm_global.py`). |
| **OOS (*out-of-sample*)** | El $R^2$ se calcula sobre datos **no usados para entrenar**. Imprescindible: el $R^2$ dentro de muestra está sesgado al alza y infla artificialmente el techo estimado — precisamente en la dirección que favorecería al método. |
| **CV 5-fold repetida (20×)** | Validación cruzada de 5 particiones, repetida 20 veces con semilla distinta por ítem, para promediar el ruido de la propia estimación. La desviación típica del $R^2$ entre repeticiones es **0,013**, del mismo orden que la señal en ítems de techo bajo — de ahí que una sola partición no sea reportable. |
| **Semilla por ítem** | Corrección de reproducibilidad: antes, una única semilla global y secuencial hacía que el resultado de una pregunta dependiera de cuántas preguntas se habían evaluado antes. Cada ítem deriva ahora su semilla de su propio identificador. |
| **Ítem circular** | Pregunta que es, a la vez, uno de los predictores inyectados en el perfil $x$ (p. ej. ideología p36, nacionalismo p38). Da $R^2=1{,}00$ por construcción y se **excluye** del techo y del numerador comparado con él. |

**Cifras de referencia (2026-08-21, corregidas):** techo global 0,225 (lineal) / **0,271** (GBM)
sobre 100 ítems de escala + ordinales; panel alcanzado 0,137 (Pearson) → **51 % del techo GBM**.
Por bloque: economía 0,024 · bienestar 0,034 · miedos 0,059 · turismo 0,085 · política 0,099 ·
perfil 0,371 (control, circular). Detalle y errores corregidos en `correccion_techo_global.md` e
`incidencia_mapeo_idx_real.md`.

---

## 4 · Métricas de acuerdo — nivel individual y agregado

| Métrica | Nivel | Definición |
|---|---|---|
| **DAM** (Desviación Absoluta Media) | Agregado | Diferencia media absoluta entre la distribución marginal (histograma) del panel sintético y la real, en puntos porcentuales. Es la métrica de **fidelidad agregada**: puede ser baja aunque la fidelidad individual sea nula (Corolario de separabilidad). |
| **Spearman** (ρ) | Individual | Correlación de rangos entre la respuesta real y la sintética de la **misma** persona, para ítems de escala. Comparar Spearman directamente con $\sqrt{R^2}$ (que acota Pearson) es **incorrecto** — en ítems muy asimétricos el Spearman puede superar el techo, lo cual es imposible por construcción (ver `correccion_techo_global.md`). |
| **Pearson** (r) | Individual | Correlación lineal entre respuesta real y sintética sobre la misma codificación numérica que usa el techo. Es la métrica correcta para comparar "alcanzado" contra $\sqrt{R^2_{\max}}$ (`pearson_alcanzado.py`). |
| **MAE** | Individual | Error absoluto medio, en puntos de escala, entre respuesta real y sintética por persona. |
| **Sesgo** | Individual | Error medio con signo (real − sintética): dirección sistemática del error, si la hay. |
| **kappa ponderado** ($\kappa_w$) | Individual | Acuerdo entre categorías ordinales/nominales corregido por el acuerdo esperable al azar, ponderando por distancia entre categorías. Referencia (Landis & Koch): <0 nulo · 0–0,20 leve · 0,21–0,40 aceptable · 0,41–0,60 moderado · >0,60 sustancial. |
| **Exacto %** / **±1 %** | Individual | Porcentaje de Personas cuya respuesta sintética coincide exactamente (o difiere como máximo en 1 categoría) con la real. |
| **`delta_vs_moda`** | Individual | Acierto del panel menos el acierto del *baseline* ingenuo "responder siempre la categoría más frecuente". **Si es ≈0 o negativo, el perfil no aporta señal individual** — es la prueba operativa de que fidelidad agregada y fidelidad individual son independientes. |
| **Jaccard** / **F1** | Individual | Para ítems multi-respuesta (elegir varias opciones): solapamiento (Jaccard) y media armónica de precisión/recall (F1) entre el conjunto de opciones real y el sintético. |
| **V de Cramér** | Asociación | Fuerza de asociación entre una variable del perfil (p. ej. voto) y la respuesta sintética. Sirve para comprobar que el modelo **sí usa el perfil** (falsación del diagnóstico ingenuo de "el LLM ignora a la Persona"): media 0,36 con el voto en la réplica de Ikuspegi. |

**Distinción clave:** DAM mide si el panel **acierta la forma de la distribución en conjunto**;
Spearman/Pearson/kappa/`delta_vs_moda` miden si acierta **a cada persona**. El caso ilustrativo del
paper (ítem P26, escala 0–10): media panel 5,15 vs real 5,30 (DAM ≈ excelente) pero 86,4 % de las
Personas se concentran en {5,6} y ninguna elige {8,9,10} (fidelidad individual destruida).

---

## 5 · Concentración, colapso y parámetros del experimento

| Término | Definición |
|---|---|
| **Concentración de la opción modal** | Métrica operativa de $\Delta_C$: porcentaje de Personas que eligen la opción más votada en una pregunta categórica. Métrica principal de los experimentos de robustez (Proposición 2 directamente operacionalizada). Real (Ikuspegi) = 61,5 %; panel v1 = 83,7 %. |
| **NS/NC** | "No sabe / No contesta". Su infrarrepresentación en el panel sintético (1,4 % vs 3,4 % real) es uno de los tres mecanismos de colapso observados. |
| **Opciones usadas por pregunta** | Número de categorías distintas que reciben al menos un voto en una pregunta. Ojo: esta métrica **crece con N** (más Personas, más probable que se toque cada opción), así que no debe leerse como un índice de dispersión "puro" — la alternativa sugerida y no adoptada es el número **efectivo** de opciones (inverso del índice de Herfindahl). |
| **`temperature`** | Parámetro de decodificación del LLM que controla la aleatoriedad del muestreo de tokens (0 = determinista/codicioso, valores más altos = más variabilidad). Ninguna llamada del proyecto lo fijaba explícitamente hasta el hueco 6, así que corría al **1,0 por defecto de la API de Anthropic** — el escenario de **máxima varianza posible**. Esto es relevante porque descarta que el colapso de varianza sea un artefacto de decodificación codiciosa (`temperature=0`): si el colapso ocurre incluso a máxima varianza de muestreo, el problema no es de decodificación. |
| **Hueco 2 · modelo** | Experimento de robustez: repetir con un modelo frontera (Claude Opus) en vez de Haiku, para comprobar si el colapso es dependiente de la capacidad del modelo. |
| **Hueco 3 · prompt anti-concentración** | Experimento de robustez: variante de *prompt* que legitima explícitamente NS/NC y posiciones minoritarias/extremas y prohíbe refugiarse en la opción intermedia, **sin revelar la distribución real** (revelarla invalidaría el experimento). |
| **Hueco 6 · temperature** | Experimento de robustez: fijar `temperature=0.0` explícitamente, para cerrar la objeción de que el colapso es un artefacto de decodificación codiciosa. |
| **PPI / PPI++** | *Prediction-Powered Inference* (Angelopoulos et al. 2023): método estadístico para combinar predicciones imperfectas (del LLM) con una muestra pequeña de datos reales, obteniendo intervalos de confianza válidos. Se usa como ejemplo de uso *híbrido* honesto de encuestados sintéticos: el recorte de IC (~1,1 %) es pequeño porque va con $corr^2$, y $corr\approx0{,}15$. |

---

## 6 · Perfil de la Persona ($x_i$) — variables del panel

Los cuatro bloques de atributos que componen el perfil $x_i$ de cada Persona (ver
`resumen_construccion_panel.md`):

| Bloque | Variables |
|---|---|
| **Sociodemográfico** | id, nombre, apellidos, edad, género, provincia, nivel de estudios, situación laboral, clase social, religión, lugar de nacimiento, euskera |
| **Político** | voto en autonómicas 2024, preferencia territorial, ideología (0–10), nacionalismo vasco (0–10), valoración de economía y política, principales preocupaciones |
| **Mediático** | medio principal de noticias, redes sociales activas, confianza en TV/radio/redes (0–10), interés político |
| **Bienestar** | salud autopercibida, estado emocional, satisfacción vital (0–10), control de la vida (0–10), satisfacción con relaciones y ahorro, actividad física, frecuencia de soledad, contacto social, transporte habitual, preocupación por el clima, sentido de pertenencia, presencia de la cultura |

### Variables de enlace (emparejamiento estadístico Barómetro ↔ Bienestar)

| Variable | Descripción |
|---|---|
| `lurral` | Territorio (Álava / Gipuzkoa / Bizkaia) |
| `sexo` | Género |
| `edad_g` | Grupo de edad (cuatro tramos) |
| `eus_g` | Competencia en euskera (dos categorías) |

Método: **k-NN por celda** — para cada Persona se busca en la Encuesta de Bienestar la celda que
coincide en las cuatro variables (emparejamiento exacto); si no hay coincidencia, se degrada a 3,
2 o 1 variable.

**Perfil enriquecido (v2):** variante que ancla la Persona en un encuestado real y añade bloques
de ESS España y EUSTAT Capital Social (5-6 llaves en vez de 4), con los predictores canónicos de
actitudes hacia la inmigración (confianza generalizada, inseguridad económica, seguridad
percibida, cohesión). Hallazgo central del paper: **enriquecer el perfil empeora el colapso**
(no lo mejora), contradiciendo el supuesto de diseño dominante ("más contexto, mejor Persona").

---

## 7 · Siglas y términos frecuentes

| Sigla / término | Significado |
|---|---|
| **DAM** | Desviación Absoluta Media (fidelidad agregada) |
| **GBM** | *Gradient Boosting Machine* (estimador no lineal del techo) |
| **OOS** | *Out-of-sample* (fuera de muestra) |
| **CV** | Validación cruzada (*cross-validation*) |
| **IC** | Intervalo de confianza |
| **PPI / PPI++** | *Prediction-Powered Inference* |
| **IJRM** | *International Journal of Research in Marketing* (revista destino del paper) |
| **RLHF** | *Reinforcement Learning from Human Feedback*, parte del entrenamiento del LLM que se conjetura empuja hacia la respuesta "típica" (mecanismo del colapso de varianza) |
| **Persona** | Individuo sintético del panel (no "agente" — ver nota de terminología) |
| **Acto I** | Bloque del paper sobre el techo de información (Proposición 1) |
| **Acto II** | Bloque del paper sobre el colapso de varianza (Proposición 2) |

---

*Documento generado a partir de `bitacora.md`, `CLAUDE.md` y los materiales de `paper/` y
`piloto_ppi/`. Si se añaden nuevas métricas o notación en próximas sesiones, actualizar este
glosario en el mismo formato Markdown → exportación a `.docx` con fórmulas nativas
(`pandoc -f markdown+tex_math_dollars -t docx glosario.md -o glosario.docx --standalone`).*
