# Prompt anti-concentración sobre encuestados reales — contraste pareado

Mismos encuestados, mismas 142 preguntas no circulares, mismo modelo.
**Lo único que cambia es la instrucción anti-concentración en el prompt.**

| | por defecto | anti-conc. | Δ | dirección esperada |
|---|--:|--:|--:|---|
| **AGREGADO** | | | | |
| Concentración modal | 66.618 | 65.772 | -0.846 | ↓ = el prompt funciona |
| **INDIVIDUAL · escalas 0-10** | | | | |
| Acierto exacto % | 17.176 | 17.191 | +0.015 | ↓ si el reparto es ruido |
| Dentro de ±1 % | 46.135 | 45.976 | -0.159 | ↓ si el reparto es ruido |
| MAE (puntos) | 2.100 | 2.114 | +0.014 | ↑ si el reparto es ruido |
| Δ vs moda | -7.533 | -7.590 | -0.057 | ↓ si el reparto es ruido |
| **INDIVIDUAL · ordinales** | | | | |
| Kappa ponderado | 0.097 | 0.086 | -0.011 | ≈ plano o ↓ |
| Acierto exacto % | 52.339 | 51.830 | -0.509 | ↓ |
| Δ vs moda | -4.973 | -5.478 | -0.505 | ↓ (más negativo) |
| **INDIVIDUAL · nominales** | | | | |
| Kappa | 0.139 | 0.136 | -0.003 | ≈ plano o ↓ |
| Δ vs moda | -5.361 | -5.755 | -0.394 | ↓ — pierde el único positivo |

## Lectura

- Si la **concentración baja** y el **acuerdo individual empeora**, los dos límites son
  independientes: repartir la distribución no crea información. Es la confirmación
  directa del corolario de separabilidad, y significa que **optimizar la métrica que
  reporta la industria daña la propiedad que necesitan las aplicaciones.**
- Si la concentración baja y el acuerdo individual **también mejora**, el reparto era
  informativo: el prompt por defecto estaba suprimiendo variación real ligada al perfil.
  Habría que revisar la Proposición 2(b) y sería una buena noticia para el método.
- Si no se mueve nada, el prompt no transporta del cuestionario de Ikuspegi al
  Deustobarómetro y hay que decirlo.

> Predicciones preregistradas en `../paper/preregistro_anticonc_individual.md`.