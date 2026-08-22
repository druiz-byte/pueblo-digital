# Incidencia — bug de mapeo en `_idx_real` y su efecto sobre el techo predictivo

**Detectado:** 2026-08-21, al depurar el `R² = nan` de los 13 ítems de p6.
**Alcance:** `piloto_ppi/techo_predictivo.md` y `.json`. **Nada más.**
**Estado:** corregido, con contraste antes/después.

---

## Qué pasaba

`true_ppi_full._idx_real()` traduce la **etiqueta de valor del `.sav`** al **índice de opción de la
plantilla**. Lo hacía aceptando cualquier contención de subcadena:

```python
if nm(op) == nm(lab) or nm(lab) in nm(op) or nm(op) in nm(lab):
    return j
```

Con las opciones de p6 esto es catastrófico:

| Código real | Etiqueta del `.sav` | Iba a | Debía ir a |
|---|---|---|---|
| 1 | Lo he hecho | `Lo he hecho` ✅ | `Lo he hecho` |
| 2 | Lo he pensado hacer, pero no lo he hecho | **`Lo he hecho`** ❌ | `Lo he pensado hacer…` |
| 3 | Ni lo he hecho, ni lo he pensado hacer | **`Lo he hecho`** ❌ | `Ni lo he hecho…` |
| 4 | Prefiero no contestar | `Prefiero no contestar` ✅ | — |

`"lo he hecho"` es subcadena de las otras dos etiquetas, así que **los códigos 1, 2 y 3 colapsaban
en la misma categoría**. Tras eliminar el NS/NC quedaba un vector constante → `y.std() == 0` →
`r2_oos` devolvía `nan`. El `nan` no era el problema: era el **síntoma**.

El mismo patrón afectaba a:

- **p2** (`Buena` ⊂ `Muy buena`, `Mala` ⊂ `Muy mala`)
- **p18** (ídem)
- **p30_1 … p30_14** (`Aliado` ⊂ `Ni aliado ni enemigo`)

**29 de las 89 preguntas categóricas con variable asignada (33 %).**

---

## Qué NO estaba afectado (verificado, no supuesto)

- **`acuerdo_individual.py`** usa `arrays_pregunta()`, que empareja por **igualdad exacta** sobre
  texto normalizado, no por contención. Se reejecutó y **reproduce exactamente** los valores
  publicados (p6_4 83,62 / 87,03 · p6_9 91,41 / 92,44 · p14 65,67 / 71,00 · p15 16,28 / 43,02), con
  n efectivo de 285-298 sobre 300 en los ítems de p6. **Los resultados de acuerdo individual son
  correctos.**
- **`true_ppi_full.py` en producción**: `_idx_real` solo se invoca desde `cargar_predicciones(simular=…)`,
  el **modo simulación**. El PPI++ sobre predicciones reales no lo toca. **`informe_ppi_full.md` es
  correcto.**
- Los ítems de **escala 0-10** (p8, p21, p20, p37, p39…) nunca pasaron por el matcher: se leen con
  `int(val)`. Su techo era correcto ya antes.

---

## El arreglo

```python
def _match_opcion(ops, lab):
    no = [_nm_dur(o) for o in ops]; nl = _nm_dur(lab)
    if nl in no:                       # 1) igualdad exacta (sin acentos ni puntuación)
        return no.index(nl)
    cand = [j for j, o in enumerate(no) if nl and (nl in o or o in nl)]
    return cand[0] if len(cand) == 1 else None   # 2) contención SÓLO si es única
```

Validado sobre las 89 preguntas categóricas: **mapeo total e inyectivo, 0 colapsos, 0 sin mapear.**

### Dos mejoras de reproducibilidad añadidas (`piloto_ppi/techo_v2.py`)

1. **Semilla por ítem.** La versión original compartía un único `default_rng(0)` consumido en
   secuencia, de modo que el R² de una pregunta dependía de **cuántas preguntas se habían evaluado
   antes**. Al reparar p6, todos los ítems posteriores cambiaban de folds. Ahora cada ítem deriva su
   semilla de su propio identificador.
2. **CV 5-fold repetida 20 veces**, reportando la desviación. **La sd media del R² entre
   repeticiones es 0,013**, comparable a la señal en los ítems de techo bajo. Un solo 5-fold no era
   suficiente y un revisor lo habría señalado.

---

## Efecto sobre las cifras publicadas

Contraste limpio: mismo método, semilla por ítem y CV repetida en ambos; **lo único que cambia es el
mapeo**.

| | antes (bug) | después | |
|---|--:|--:|---|
| R² medio OOS (escalas + ordinales) | 0,0789 | **0,0718** | |
| **corr máxima media** | **0,240** | **0,225** | ⬇ el techo es aún más bajo |
| ítems válidos (no `nan`) | 87 | **100** | ⬆ entran los 13 de p6 |
| ítems con R² ≤ 0 | 11 | **15** | ⬆ |
| nominales: acierto | 65,5 % | 56,4 % | |
| nominales: baseline moda | 58,0 % | 48,6 % | |
| **nominales: Δ vs moda** | **+7,53** | **+7,88** | ≈ igual |

### Lectura

- **El titular del paper se mueve de `corr máx 0,24` a `0,22`, y en la dirección que refuerza la
  tesis:** el techo de información es todavía más bajo de lo que decíamos.
- **El argumento de la §6 del esquema aguanta.** El "+7,5 p.p. de la imputación clásica sobre la
  moda frente al +1,6 del LLM" pasa a **+7,9 vs +1,6**. La conclusión —para preguntas imputables la
  estadística clásica gana al LLM— se mantiene y se refuerza levemente.
- **Los 13 ítems de p6 dejan de ser `nan` y entran en el cómputo.** Su techo es muy bajo: R² entre
  −0,029 y 0,145, con **6 de 13 en R² ≤ 0**. Es decir: el perfil sociodemográfico **no informa** sobre
  el retrenchment de consumo. Esto no es un accidente del arreglo, es el resultado sustantivo que
  faltaba, y es central para el ángulo de marketing.
- **Hay que corregir la afirmación "el panel alcanza el 65 % del techo"** que circula en `bitacora.md`
  y en `CLAUDE.md`. Ese 65 % se obtuvo comparando un **Spearman** (0,15) con un techo **Pearson**
  (0,24), que son métricas distintas. Ver la nota siguiente.

---

## Segunda incidencia, metodológica: Spearman vs Pearson

`corr_max = √R²_OOS` es una cota sobre la correlación de **Pearson**. Compararla con el **Spearman**
del panel es incorrecto, y en ítems muy asimétricos produce resultados imposibles: en el bloque de
retrenchment el Spearman medio del panel es **0,447** contra un techo de **0,122** — un 367 % del
techo, que no puede ser. La causa es el tratamiento de empates cuando ~90 % de los casos caen en una
categoría.

**Corrección aplicada:** `paper/pearson_alcanzado.py` calcula la correlación de Pearson panel↔real
sobre la misma codificación numérica que usa el techo. Es la cifra que debe ir al paper.

Con Pearson, el panel alcanza el **59 %** del techo en el subcorpus de marketing (0,127 de 0,216).
La cifra global del proyecto ("65 %") debe recalcularse con este criterio antes de escribir la §6.

---

## Ficheros

| Fichero | Qué es |
|---|---|
| `piloto_ppi/true_ppi_full.py` | **modificado** — `_idx_real` ahora delega en `_match_opcion` |
| `piloto_ppi/techo_v2.py` | **nuevo** — techo con semilla por ítem y CV repetida; `MATCH=orig` reproduce el bug para el contraste |
| `piloto_ppi/techo_v2_fix.json` / `techo_v2_orig.json` | resultados de ambas versiones |
| `piloto_ppi/techo_predictivo_v2.md` | informe del techo corregido |
| `piloto_ppi/techo_predictivo.md` | **obsoleto**, se le añadió cabecera de aviso |
| `paper/pearson_alcanzado.py` | correlación alcanzada en Pearson |

**Pendiente:** decidir si se regenera `techo_predictivo.md` o se deja como registro histórico con el
aviso. De momento se deja, para que la trazabilidad de lo que se afirmó en cada sesión no se pierda.
