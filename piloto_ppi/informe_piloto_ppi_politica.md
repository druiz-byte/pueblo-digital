# Piloto PPI++ — Bloque de política (Deustobarómetro verano 2026)

**Fecha:** 2026-07-15 · **Autor:** David Ruiz (Universidad de Deusto)
**Método:** Prediction-Powered Inference con power-tuning (PPI++), Angelopoulos et al. (2023a, 2023b).

## Qué se ha hecho

Primer piloto que aplica **PPI++** al panel *Pueblo Digital* usando por fin **microdatos individuales reales** del Deustobarómetro verano 2026 (n = 1.000, fichero SPSS). Se combina una muestra real pequeña con las predicciones del panel sintético para estimar magnitudes poblacionales del **Bloque 5 (situación política y calidad de la democracia)** con intervalos de confianza *válidos*, en lugar de sustituir la encuesta por el panel (que es lo que hace la aproximación actual, y que la literatura demuestra sesgada).

- **Gold-standard `Y`:** respuestas reales del Deustobarómetro (`p18`, `p20_2`, `p21_1`, `p21_6`, `p21_13`).
- **Predicción `f`:** respuesta del panel v2. En este piloto se usa un **sustituto sin API**: para cada encuestado real se toma la respuesta del panel emparejada por **voto × ideología × sexo**. La versión limpia (predicción generativa directa, un LLM por encuestado) se deja lista en `generar_predicciones_deusto.py` (requiere API, ver más abajo).
- **Protocolo:** de los 1.000 encuestados se "revela" `Y` en un subconjunto de tamaño *n* (etiquetado) y el resto queda como no etiquetado; PPI++ estima combinando ambos. Se barre *n* ∈ {50…500} y se promedia sobre 40 particiones.

## Resultados

### A. La sustitución ingenua se equivoca gravemente (p18)

Proporción real vs. lo que diría el panel tomado como verdad ("imputación ingenua", el enfoque actual):

| Opción | Real | Panel como verdad | Error |
|---|---:|---:|---:|
| Muy buena | 1,7 % | 3,1 % | 1,4 |
| Buena | 32,5 % | 64,5 % | **32,0** |
| Regular | 43,5 % | 0,1 % | **43,4** |
| Mala | 12,0 % | 20,5 % | 8,5 |
| Muy mala | 5,9 % | 5,2 % | 0,6 |
| NS/NC | 4,4 % | 6,5 % | 2,1 |

El panel colapsa casi todo en "Buena" y **prácticamente nunca dice "Regular"** (0,1 % frente al 43,5 % real). Sustituir la encuesta por el panel daría un retrato radicalmente falso. Este es exactamente el sesgo que PPI++ corrige.

### B. PPI++ es válido y se adapta a la calidad del predictor

Para las escalas 0-10 (media poblacional), reducción del ancho del intervalo de PPI++ frente al clásico (solo datos reales), y correlación individual predicción-realidad:

| Pregunta | Real | Sesgo panel | corr(Y,f) | Reducción IC (n=100) |
|---|---:|---:|---:|---:|
| Confianza Gobierno Vasco (p21_6) | 5,05 | +0,08 | **+0,28** | 4,1 % |
| Democracia Euskadi (p20_2) | 5,80 | −0,09 | **+0,22** | 2,6 % |
| Confianza partidos (p21_13) | 3,10 | −1,92 | +0,07 | 0,6 % |
| Confianza Gobierno Central (p21_1) | 3,80 | −1,82 | −0,00 | 0,3 % |

Dos lecturas clave:

1. **Validez siempre.** La cobertura de los intervalos PPI++ acompaña a la del clásico (~95 %): es estadísticamente válido en todos los casos, a diferencia de la imputación ingenua.
2. **Power-tuning en acción.** Donde el panel *informa* (Gobierno Vasco, democracia Euskadi: correlación 0,22-0,28) PPI++ estrecha el intervalo. Donde el panel está muy sesgado y no correlaciona (Gobierno Central, partidos) PPI++ **se repliega automáticamente al clásico** (reducción ≈ 0): nunca empeora. Esa es la diferencia de PPI++ frente a PPI.

## Interpretación para el proyecto

- **El experimento confirma la tesis de la literatura** (PPI; Wang et al. AAE): el panel *no* debe sustituir a la encuesta (sesgos de decenas de puntos), pero *sí* puede complementarla dentro de un marco con garantías. PPI++ convierte tu DAM en una corrección estadística válida en vez de un simple diagnóstico de error.
- **Las ganancias de eficiencia son todavía modestas (2-5 %)** porque el predictor de este piloto es un *sustituto por emparejamiento demográfico*, que no reproduce la predicción individual del LLM. La correlación individual está topada en ~0,28. Con la **predicción generativa directa** (un LLM por encuestado, con su perfil completo) la correlación —y por tanto el ahorro de datos— debería subir sustancialmente. Ese es el siguiente paso.

## Versión generativa (300 encuestados, emparejamiento 1:1) — ejecutada

Se generó con LLM una predicción `f_i` para cada uno de 300 encuestados reales a partir de **su propio perfil** (sin inyectar las variables objetivo). Resultado frente al sustituto por emparejamiento:

| Pregunta | corr emparejado | corr **generativa** | Reducción IC (n=50) | Ahorro datos (n=50) |
|---|---:|---:|---:|---:|
| Confianza Gobierno Vasco (p21_6) | +0,28 | **+0,42** | 8,6 % | ~17 % (n_efic 60) |
| Confianza partidos (p21_13) | +0,07 | **+0,17** | 1,8 % | — |
| Democracia Euskadi (p20_2) | +0,22 | +0,18 | 2,7 % | — |
| Confianza Gobierno Central (p21_1) | −0,00 | +0,03 | 0,4 % | — |

Conclusiones:

1. **La predicción generativa informa más donde el panel ya ayudaba.** En confianza Gobierno Vasco la correlación individual sube de 0,28 a **0,42** y PPI++ recorta el IC un 8,6 % a n=50 (equivale a que el clásico necesitaría ~20 % más de encuestas reales). Confirma la hipótesis: predecir con el perfil completo de cada encuestado bate al emparejamiento demográfico.
2. **p18 sigue siendo caso de protección, no de ganancia.** Sin la variable inyectada, el LLM ya no colapsa en "Buena" sino en **"Regular" (86 %)** — sigue muy sesgado (40 p.p.) y con 41 % de concordancia individual. PPI++ vuelve a replegarse al clásico: nunca empeora.
3. **Techo por tamaño.** La ganancia de PPI escala con el tamaño del conjunto *no etiquetado* (N ≫ n). Aquí N total = 300, así que la mejora se diluye al crecer n (a n=250 solo quedan 50 no etiquetados). **Generar los 1.000** (o predecir sobre una población sintética grande) ampliaría el margen y haría visibles ahorros mayores.

Figura: `piloto_ppi_generativo.png`. Runner: `true_ppi.py`. Predicciones: `entrevista/predicciones_deusto_bloque5.json`.

## Siguiente paso: ampliar a los 1.000 (más margen de ahorro)

El techo de ahorro depende del tamaño del conjunto no etiquetado. Para ampliarlo, generar los 1.000 (en el ordenador de David, con `ANTHROPIC_API_KEY` en `entrevista/.env`):

```
cd entrevista
python generar_predicciones_deusto.py        # sin --muestra = los 1.000
```

El script lee `predictores_deusto.csv` (ya convertido del `.sav`, sin dependencias SPSS) y **no inyecta en el prompt las variables que se predicen** (evita circularidad). Luego se recalcula con `true_ppi.py`. Con N=1.000 no etiquetados y n pequeño, el ahorro de datos debería crecer respecto al 300 actual.

Otras extensiones útiles: repetir sobre los demás bloques (bienestar, economía) para ver dónde el panel es más informativo; y probar PPI para coeficientes de regresión (no solo medias), que es donde el AAE de Wang et al. muestra sus mayores ventajas.

## Archivos

- `ppi_engine.py` — motor PPI++ (proporciones y medias). Validado con Monte Carlo (`selftest_ppi.py`: cobertura ~95 %, sesgo ~0, imputación sesgada).
- `construir_pred.py` — predictor-sustituto por emparejamiento voto × ideología × sexo.
- `piloto_final.py` — runner del piloto (Partes A y B).
- `figura.py` → `piloto_ppi_politica.png` — figura resumen.
- `resultado_piloto_final.json` — resultados completos.
- `generar_predicciones_deusto.py` — predicción generativa directa (lee `predictores_deusto.csv`, requiere API). Ya ejecutado para 300.
- `true_ppi.py` → `piloto_ppi_generativo.png` — PPI++ con predicción generativa emparejada 1:1.
- `predictores_deusto.csv` (raíz) — perfiles de los 1.000 encuestados extraídos del `.sav`.
- `entrevista/predicciones_deusto_bloque5.json` — predicciones LLM del Bloque 5 para 300 encuestados.

## Referencias

Angelopoulos, A. N., Bates, S., Fannjiang, C., Jordan, M. I., & Zrnic, T. (2023a). Prediction-powered inference. *Science, 382*(6671), 669–674.
Angelopoulos, A. N., Duchi, J. C., & Zrnic, T. (2023b). PPI++: Efficient prediction-powered inference. *arXiv:2311.01453*.
Wang, M., Zhang, D. J., & Zhang, H. (2026). Large language models for market research: A data-augmentation approach. *arXiv:2412.19363*.
