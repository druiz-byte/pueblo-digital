# Preregistro — prompt anti-concentración sobre encuestados reales

**Escrito el 2026-08-22, ANTES de generar nada.** Este fichero no se edita después de lanzar.

## Qué se contrasta y por qué es el experimento decisivo

Sobre Ikuspegi, el prompt anti-concentración **mejoró la fidelidad agregada**: DAM 15,7 → 14,8 y
concentración 83,7 → 79,4. Pero Ikuspegi no publica microdatos, así que allí fue imposible medir lo
único que de verdad importa: **si repartir la distribución mejora o empeora el acierto persona a
persona.**

El Deustobarómetro sí tiene el microdato individual y permite el emparejamiento 1:1. Es el único
sitio donde se puede poner a prueba la afirmación central del corolario de separabilidad.

**Diseño.** Los **mismos 300 encuestados** (los 300 primeros del fichero, que son exactamente los de
`predicciones_deusto_full.json`), el mismo perfil de 12 predictores, los mismos 7 bloques y 152
preguntas, el mismo modelo. **Lo único que cambia es la instrucción anti-concentración**, con el
texto literal que se usó en Ikuspegi — se importa, no se copia.

## Valores de referencia (tanda por defecto, n=300)

⚠ **Anclajes recalculados el 2026-08-22, antes de lanzar nada.** Los que circulaban incluían los
**ítems circulares** (p36, p38, p40-p46: ideología, nacionalismo, estudios, religión, nacimiento,
voto 2024 y voto 2020), que son **predictores inyectados en el prompt** y dan acuerdo casi perfecto
por construcción. Es el mismo error que ya se corrigió en el techo global
(`correccion_techo_global.md`), aquí repetido en el acuerdo individual.

| métrica | con circulares *(lo publicado)* | **sin circulares** *(correcto)* | ítems |
|---|--:|--:|--:|
| Correlación escalas 0-10 | 0,152 | **0,123** | 52 |
| Acierto exacto escalas | 18,6 % | **17,2 %** | 52 |
| Dentro de ±1 | 47,9 % | **46,1 %** | 52 |
| MAE escalas | 2,04 | **2,10** | 52 |
| Δ vs moda escalas | −5,95 | **−7,53** | 52 |
| Kappa ponderado ordinales | 0,100 | **0,097** | 45 |
| Acierto exacto ordinales | 51,9 % | **52,3 %** | 45 |
| Δ vs moda ordinales | −4,54 | **−4,97** | 45 |
| **Kappa nominales** | 0,231 | **0,139** | 36 |
| Acierto exacto nominales | 51,0 % | **45,5 %** | 36 |
| **Δ vs moda nominales** | **+1,61** | **−5,36** | 36 |
| Concentración modal del panel | — | **66,6 %** | 133 |

### 🔴 Consecuencia: se cae "el único resultado positivo del proyecto"

El Δ vs moda de nominales **+1,61** —descrito repetidamente como *"el primer positivo del proyecto a
nivel individual"*— era **un artefacto de incluir p41, p42, p45 y p46** (religión, lugar de
nacimiento, voto 2024, voto 2020), que se inyectan en el prompt y por tanto dan kappa ≈ 1,00. Sin
ellos, **−5,36**: el panel es peor que responder siempre la moda **también en nominales**.

**Y esto refuerza mucho el argumento del benchmark.** El "+7,5 p.p. del clasificador lineal frente
al +1,6 del LLM" comparaba peras con manzanas: el techo **ya excluía** los circulares y el acuerdo
individual **no**. Con ambos lados limpios:

> imputación clásica **+7,88** vs Persona LLM **−5,36** — trece puntos de diferencia, y el LLM por
> debajo del baseline tonto.

▸ **Pendiente de corregir** en `esquema_paper_IJRM.md` §6, `bitacora.md` (12ª sesión) y `CLAUDE.md`.

## Predicciones de Claude

**Razonamiento.** La Proposición 1 dice que la correlación está acotada por la información del
perfil, y el panel está en 0,137 sobre un techo de 0,271. El prompt no añade información: cambia
cómo se reparte la masa alrededor de la misma media condicional. La extensión (i) de la
Proposición 1 dice que eso es **atenuación estricta**. Por tanto:

*Rangos fijados sobre los anclajes **sin circulares** de la tabla anterior.*

| # | Métrica | Referencia | Predicción | Rango |
|---|---|--:|---|---|
| A1 | Concentración modal | 66,6 | **baja** (replica Ikuspegi) | 61 – 65 |
| A2 | Correlación escalas | 0,123 | **baja o plano** | 0,100 – 0,125 |
| A3 | Acierto exacto escalas | 17,2 % | **baja** | 15 – 17,5 % |
| A4 | MAE escalas | 2,10 | **sube** | 2,12 – 2,32 |
| A5 | Kappa ponderado ordinales | 0,097 | **plano o baja** | 0,075 – 0,100 |
| A6 | Acierto exacto ordinales | 52,3 % | **baja** | 47 – 52 % |
| A7 | Δ vs moda ordinales | −4,97 | **empeora** | −6 a −10 |
| A8 | Kappa nominales | 0,139 | **plano o baja** | 0,10 – 0,145 |
| A9 | Δ vs moda nominales | −5,36 | **empeora** | −6 a −11 |

**Predicción de titular: el agregado mejora y el individual empeora.** Es decir, los dos se mueven
en **direcciones opuestas**.

**Qué falsaría la tesis.** Que el Pearson de escalas suba por encima de **0,16** *y* que el Δ vs
moda mejore en las tres familias. Eso significaría que el reparto es **informativo** —que el prompt
por defecto estaba suprimiendo variación real ligada al perfil— y obligaría a revisar la
Proposición 2(b): el truncamiento del soporte sería corregible por prompting, al menos en parte.
Sería mala noticia para la tesis y buena para el método.

**Resultado nulo también posible.** Que no se mueva nada apreciable. Significaría que el prompt no
transporta del cuestionario de Ikuspegi al Deustobarómetro, probablemente porque las 152 preguntas
tienen distribuciones reales menos dispersas. Habría que reportarlo y no insistir.

## Predicciones de David

**Registradas el 2026-08-22, antes de generar nada.** Literales.

| # | Métrica | Referencia | Predicción de David |
|---|---|--:|--:|
| DA1 | Concentración modal | 66,6 | **60** |
| DA2 | Correlación escalas 0-10 | 0,123 | **0,20** |
| DA3 | Acierto exacto escalas % | 17,2 | **25** |
| DA4 | MAE escalas (puntos) | 2,10 | **1,0** |
| DA5 | Δ vs moda escalas | −7,53 | **−5** |
| DA6 | Kappa ponderado ordinales | 0,097 | *no sé* |
| DA7 | Acierto exacto ordinales % | 52,3 | *no sé* |
| DA8 | Δ vs moda ordinales | −4,97 | *no sé* |
| DA9 | Kappa nominales | 0,139 | *no sé* |
| DA10 | Δ vs moda nominales | −5,36 | *no sé* |

**Criterio de falsación de David:** *"Que la concentración modal disminuya."*

### La discrepancia, que es lo que hace útil el experimento

Las dos posiciones son **incompatibles y ambas comprobables**:

| | Claude | David |
|---|---|---|
| Correlación escalas | 0,100 – 0,125 (**baja o plana**) | **0,20** (sube un 63 %) |
| Acierto exacto escalas | 15 – 17,5 % (**baja**) | **25 %** (sube 8 puntos) |
| MAE escalas | 2,12 – 2,32 (**sube**) | **1,0** (se reduce a menos de la mitad) |
| Interpretación | el reparto extra es **ruido** | el reparto extra es **señal** |

David sostiene que el prompt por defecto estaba suprimiendo variación real ligada al perfil y que
liberarla mejora el acierto individual. Claude sostiene que el prompt no añade información y que
dispersar alrededor de la misma media condicional es atenuación estricta (Proposición 1(i)).
**No pueden tener razón los dos.**

▸ **Observación formulada antes de generar (Claude).** El criterio de falsación de David —"que la
concentración modal disminuya"— **no discrimina entre las dos hipótesis**: la concentración baja es
justo lo que el prompt está diseñado para producir, ya se observó en Ikuspegi (83,7 → 79,4), y es
además lo que el propio David predice en DA1 (66,6 → 60). Es una comprobación de manipulación, no
una prueba de la tesis: bajaría igual tanto si el reparto es señal como si es ruido. Lo que sí
discrimina son DA2, DA3 y DA4, que están fijadas y son netamente distintas de las de Claude. Se
registra tal cual, como pidió David; al evaluar se usarán esas tres.

## ★ RESULTADO (2026-08-22) — nulo, y por una razón que sí interesa

**Tanda válida:** 300 encuestados, 142 preguntas no circulares, 0 bloques vacíos.

**La manipulación SÍ se aplicó.** De las 45.448 respuestas individuales comparables, **cambian
10.841 — el 23,9 %**. El prompt llegó al modelo y le cambió una de cada cuatro respuestas. No es un
fallo técnico.

### Lo que se movió: casi nada

| | por defecto | anti-conc. | Δ |
|---|--:|--:|--:|
| **Concentración modal** | 66,6 | 65,8 | **−0,85** |
| Correlación escalas 0-10 (Pearson) | 0,1229 | 0,1369 | **+0,0140** |
| Acierto exacto escalas % | 17,18 | 17,19 | +0,02 |
| Dentro de ±1 % | 46,14 | 45,98 | −0,16 |
| MAE escalas | 2,100 | 2,114 | +0,014 |
| Δ vs moda escalas | −7,53 | −7,59 | −0,06 |
| Kappa ponderado ordinales | 0,097 | 0,086 | −0,011 |
| Acierto exacto ordinales % | 52,34 | 51,83 | −0,51 |
| Δ vs moda ordinales | −4,97 | −5,48 | −0,51 |
| Kappa nominales | 0,139 | 0,136 | −0,003 |
| Δ vs moda nominales | −5,36 | −5,76 | −0,39 |

**La subida de la correlación no es distinguible de cero.** Contraste pareado sobre los 52 ítems de
escala: diferencia media **+0,0140**, sd 0,057, **t = 1,79**, **IC95 bootstrap [−0,0012, +0,0294]**
(20.000 réplicas). Mejoran 34 de 52 ítems. Es sugerente y va en la dirección de David, pero no
alcanza significación.

### Contraste con lo preregistrado

| # | Claude | David | Observado | |
|---|---|---|--:|---|
| Concentración | 61 – 65 | 60 | **65,8** | ambos ❌ (Claude por 0,8) |
| Correlación escalas | 0,100 – 0,125 | 0,20 | **0,137** | ambos ❌ — sube, contra Claude; muy por debajo de David |
| Acierto exacto escalas | 15 – 17,5 % | 25 % | **17,19** | Claude ✅ · David ❌ |
| MAE escalas | 2,12 – 2,32 | 1,0 | **2,114** | Claude ❌ por 0,006 · David ❌ de largo |
| Δ vs moda escalas | (no fijado) | −5 | **−7,59** | David ❌ |
| Kappa ordinales | 0,075 – 0,100 | — | **0,086** | Claude ✅ |
| Acierto ordinales | 47 – 52 % | — | **51,83** | Claude ✅ |
| Δ vs moda ordinales | −6 a −10 | — | **−5,48** | Claude ❌ por poco |
| Kappa nominales | 0,10 – 0,145 | — | **0,136** | Claude ✅ |
| Δ vs moda nominales | −6 a −11 | — | **−5,76** | Claude ❌ por poco |

**Claude acierta 4 de 9. David falla las 5 que respondió.** Pero la **predicción de titular de
Claude —"el agregado mejora y el individual empeora"— es falsa en los dos términos:** el agregado
apenas se movió y el individual no empeoró de forma clara.

### 🔑 Por qué esto importa: el prompt NO transporta entre instrumentos

En Ikuspegi el mismo prompt movió la concentración **−4,3** puntos (83,7 → 79,4). Aquí, **−0,85**.
La explicación fácil sería "en el Deustobarómetro había menos margen porque partía de 66,6". **Es
falsa**, y la comprobación lo deja claro:

| | ítems | opciones/ítem | por defecto | anti-conc. | Δ |
|---|--:|--:|--:|--:|--:|
| Deustobarómetro · escalas 0-10 | 52 | 11,0 | 53,1 | 52,4 | −0,76 |
| **Deustobarómetro · categóricas** | 81 | **4,7** | **75,3** | 74,4 | **−0,90** |
| **Ikuspegi** | 13 | **4-5** | **83,7** | 79,4 | **−4,3** |

Las categóricas del Deustobarómetro tienen **el mismo número de opciones** que las de Ikuspegi y
parten de una concentración comparable (75,3 vs 83,7). Con margen equivalente, el prompt libera
**0,9 puntos aquí y 4,3 allí**: casi cinco veces menos.

**Interpretación (a declarar como tentativa).** El prompt anti-concentración se diseñó mirando los
fallos de un cuestionario sobre **inmigración**, un dominio donde el modelo tiene incentivos fuertes
a la moderación y donde por tanto hay mucha varianza suprimida que soltar. En un barómetro de temas
generales —economía, bienestar, servicios públicos, política— el modelo no está conteniéndose de la
misma forma, y la instrucción tiene poco sobre lo que actuar. **El efecto del prompt depende del
tema, no es una propiedad general del método.**

### Qué queda sin resolver

**La pregunta de separabilidad sigue abierta.** No se puede comprobar si liberar varianza mejora o
empeora el acierto individual **si no se ha liberado varianza apreciable**. Con Δ de concentración
de −0,85 no hay manipulación suficiente para poner a prueba la hipótesis. Es un experimento
**inconcluyente por manipulación débil**, no una hipótesis refutada, y así hay que reportarlo.

**Vía para cerrarlo, si interesa:** aplicar el prompt únicamente al **subconjunto de ítems del
Deustobarómetro con mayor concentración de partida** (las categóricas con >85 %), donde sí hay
varianza que soltar, y medir el acuerdo individual sólo ahí. Sin API adicional no se puede: exige
una tercera tanda.

---

## Cautelas declaradas de antemano

- **n=300 y no aleatorios:** son los 300 primeros del fichero. Ya declarado en la Fase 1. El
  contraste es pareado, así que el sesgo de selección afecta igual a las dos ramas y no invalida la
  **diferencia**, que es lo que se mide.
- **Ítems circulares excluidos** (p36, p38, p40-p46): son predictores inyectados y su acuerdo es
  artificialmente perfecto.
- **Una sola tanda por rama.** No se puede separar el efecto del ruido de muestreo del LLM. Con 152
  preguntas × 300 encuestados el promedio es estable, pero conviene no interpretar diferencias
  menores de ~0,01 en kappa o ~1 punto en los porcentajes.
- **El prompt se diseñó mirando los fallos de Ikuspegi**, no los del Deustobarómetro. Si funciona
  aquí, es transporte genuino; si no funciona, puede ser sobreajuste al instrumento original y así
  hay que reportarlo.

## Ejecución

```
cd piloto_ppi
python generar_predicciones_anticonc.py --muestra 300     # requiere API, PC de David
python acuerdo_individual.py --pred predicciones_deusto_anticonc.json
python comparar_anticonc.py
```

Coste: el mismo que la tanda de referencia de 300 (152 preguntas × 300 encuestados con Haiku).
El script es **reanudable**: guarda cada 25 encuestados y al relanzarlo continúa donde lo dejó.

| fecha | n | bloques vacíos | resultado | fichero |
|---|--:|--:|---|---|
| | | | | |
