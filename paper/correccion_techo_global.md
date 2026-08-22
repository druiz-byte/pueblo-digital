# Corrección del "% del techo" global — cifras definitivas para el paper

**Fecha:** 2026-08-21 · **Sin API.** Sustituye a la afirmación *"el panel alcanza el 65 % del techo"*
que circula en `bitacora.md` y `CLAUDE.md` desde el 20-jul-2026.

---

## La cifra antigua estaba mal por tres motivos acumulados

El 65 % salía de dividir **0,15** (Spearman medio de las escalas 0-10) entre **0,24** (techo).
Los tres errores:

| # | Error | Efecto |
|---|---|---|
| 1 | **Métricas distintas.** `corr_max = √R²` acota la correlación de **Pearson**; el numerador era **Spearman**. | Infla el ratio de forma impredecible; en ítems muy asimétricos, hasta lo absurdo (367 % en el bloque de retrenchment). |
| 2 | **Ítems circulares en el numerador.** Los 54 ítems de escala incluían **p36 (ideología, Spearman 0,83)** y **p38 (nacionalismo, 0,97)**, que son **predictores inyectados en el prompt**. Excluyéndolos, la media cae de **0,152 a 0,123**. | Infla el numerador un 24 %. |
| 3 | **Techo mal estimado.** Bug de mapeo (`incidencia_mapeo_idx_real.md`) y estimador lineal. | 0,240 → **0,225** lineal → **0,271** no lineal. |

▸ El error 2 es el más embarazoso ante un revisor: la propia bitácora dice que los ítems circulares
"validan el motor, no cuentan", pero la media publicada los incluía.

---

## Cifras corregidas

Todo con **Pearson** en numerador y denominador, **excluidos los ítems circulares** (p36, p38,
p40-p46), techo con **CV 5-fold repetida** y semilla por ítem.

| conjunto | ítems | techo lineal | techo GBM | alcanzado (Pearson) | % techo lineal | % techo GBM |
|---|--:|--:|--:|--:|--:|--:|
| **Todas las escalas + ordinales** | 100 | 0,225 | **0,271** | **0,137** | 61 % | **51 %** |
| Sólo escalas 0-10 | 52 | 0,260 | 0,312 | 0,123 | 47 % | 39 % |
| Sólo categóricas ordinales | 48 | 0,187 | 0,226 | 0,154 | 82 % | 68 % |
| *(referencia)* subcorpus de marketing | 44 | 0,216 | 0,234 | 0,127 | 59 % | **54 %** |

### Cifra de titular recomendada

> **El panel alcanza aproximadamente la mitad del techo de información: 0,137 de 0,271 (51 %).**

Es la más defendible: cubre los 100 ítems de escala y ordinales, usa la misma métrica arriba y
abajo, excluye la circularidad y contrasta contra el techo **no lineal**, que es el más exigente
para nuestra propia tesis.

▸ **Ojo con el mensaje.** El 65 % antiguo se usaba para decir *"el pipeline no está roto, choca
contra el límite"*. Ese argumento **se mantiene y hasta se refuerza**: con el techo en 0,27 y lo
alcanzado en 0,14, sigue siendo cierto que aunque el panel fuera perfecto el margen sería mínimo,
porque el techo mismo es bajísimo. Lo que cambia es que ya no podemos decir que el panel "casi
agota" el techo: le queda la mitad, y esa mitad es justo lo que documenta la Proposición 2
(colapso de varianza).

---

## Decisión: ¿qué techo reporta el paper?

**Recomendación: los dos, con el GBM como cota operativa.**

- El **lineal** es la referencia conservadora y el que un lector puede replicar con una regresión
  en cualquier paquete estadístico. Es lo que hace transportable el diagnóstico.
- El **GBM** es el que cierra la objeción "vuestro techo infraestima porque la relación no es
  lineal", que un revisor de IJRM planteará. Y es **más alto**, es decir, más exigente con
  nosotros: reportar sólo el lineal sería quedarnos con el número que nos favorece.

Diferencia global: 0,225 vs 0,271. Por bloque, el GBM sube el techo sobre todo en satisfacción de
servicio (0,228 → 0,254) y confianza institucional (0,326 → 0,351 en marca, 0,354 → 0,399 en
política), y lo baja ligeramente en decisión de viaje (0,175 → 0,137, donde n es pequeño y el GBM
sobreajusta menos que el ridge regularizado).

▸ Redacción propuesta para el paper: *"We report both a regularised linear and a gradient boosting
estimate of the ceiling and treat the larger as the operative bound."* Ya está en `seccion3_marco_teorico.md` §3.2.

---

## Qué hay que corregir en los documentos

| Documento | Dice | Debe decir |
|---|---|---|
| `CLAUDE.md`, estado del 20-jul | "el panel alcanza ~65% del techo (0,15 de 0,24)" | "el panel alcanza ~51 % del techo (0,137 de 0,271)" |
| `bitacora.md`, 12ª sesión | ídem | ídem, con nota de remisión a este fichero |
| `paper/esquema_paper_IJRM.md` §6 | "El panel alcanza ~65% del techo (0,15 de 0,24)" | ídem |
| `piloto_ppi/acuerdo_individual.md` | "Escalas 0-10 (54): Spearman medio 0.15" | añadir que 2 de los 54 son circulares y que sin ellos es 0,123 |

▸ **No** hay que corregir el kappa ponderado de ordinales (0,100): no cambia al excluir circulares.

---

## Reproducibilidad

| Script | Qué hace |
|---|---|
| `piloto_ppi/techo_v2.py` | techo lineal con semilla por ítem y CV repetida 20× |
| `paper/techo_gbm_global.py` | techo no lineal sobre las 100 escalas + ordinales; **reanudable** por tramos |
| `paper/pearson_alcanzado.py` | Pearson panel↔real con la codificación del techo |

`techo_gbm_global.py` guarda cada ítem según lo calcula y se puede relanzar tantas veces como haga
falta: continúa donde lo dejó. Se hizo así porque el cálculo completo excede el tiempo de una
sesión de sandbox.
