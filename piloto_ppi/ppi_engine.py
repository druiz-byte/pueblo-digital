# -*- coding: utf-8 -*-
"""
Motor PPI++ para estimar PROPORCIONES por opción de respuesta.

Idea (Angelopoulos et al. 2023, PPI / PPI++):
  Para una pregunta categórica, cada opción c se trata como una media binaria:
      Y_i^c = 1 si el encuestado REAL i respondió c, 0 si no   (gold-standard)
      f_i^c = 1 si la PREDICCIÓN del panel para i fue c, 0 si no
  Con un conjunto etiquetado pequeño (Y y f emparejados) + un conjunto grande
  no etiquetado (solo f), PPI++ estima la proporción poblacional de c con un
  intervalo de confianza VÁLIDO y normalmente más estrecho que el clásico.
  El "power-tuning" (lam=None / ppi_mean_power) distingue PPI++ de PPI: ajusta
  lambda automáticamente y nunca empeora respecto a usar solo datos reales.

Requiere: ppi-python, numpy.
"""
import numpy as np
from ppi_py import ppi_mean_ci, ppi_mean_pointestimate, classical_mean_ci


def _ind(labels, c):
    return (np.asarray(labels) == c).astype(float)


def estimar_opcion(y_lab, f_lab, f_unlab, c, alpha=0.05):
    """Estima la proporción poblacional de la opción c: PPI++, clásico e imputación ingenua."""
    Y = _ind(y_lab, c); Yh = _ind(f_lab, c); Yhu = _ind(f_unlab, c)

    # lam=None -> PPI++ ajusta lambda (power-tuning) automaticamente
    ppi_pt = float(np.atleast_1d(ppi_mean_pointestimate(Y, Yh, Yhu, lam=None))[0])
    ppi_ci = ppi_mean_ci(Y, Yh, Yhu, alpha=alpha, lam=None)
    ppi_lo, ppi_hi = float(np.atleast_1d(ppi_ci[0])[0]), float(np.atleast_1d(ppi_ci[1])[0])

    cl_pt = float(Y.mean())
    cl_ci = classical_mean_ci(Y, alpha=alpha)
    cl_lo, cl_hi = float(np.atleast_1d(cl_ci[0])[0]), float(np.atleast_1d(cl_ci[1])[0])

    # blindaje: si PPI devuelve NaN (opción degenerada en el etiquetado), replegar al clásico
    import math
    if any(math.isnan(x) for x in (ppi_pt, ppi_lo, ppi_hi)):
        ppi_pt, ppi_lo, ppi_hi = cl_pt, cl_lo, cl_hi

    imp_pt = float(np.concatenate([Yh, Yhu]).mean())

    return {
        "opcion": c,
        "ppi_pt": ppi_pt, "ppi_lo": ppi_lo, "ppi_hi": ppi_hi,
        "ppi_ancho": ppi_hi - ppi_lo,
        "clasico_pt": cl_pt, "clasico_lo": cl_lo, "clasico_hi": cl_hi,
        "clasico_ancho": cl_hi - cl_lo,
        "imputacion_pt": imp_pt,
        "reduccion_ancho_pct": 100.0 * (1 - (ppi_hi - ppi_lo) / (cl_hi - cl_lo)) if (cl_hi - cl_lo) > 0 else 0.0,
    }


def estimar_pregunta(y_lab, f_lab, f_unlab, opciones, alpha=0.05):
    return [estimar_opcion(y_lab, f_lab, f_unlab, c, alpha) for c in opciones]


def estimar_media(y_lab, f_lab, f_unlab, alpha=0.05):
    """Estimando = media poblacional (para escalas 0-10). PPI++ vs clásico vs imputación."""
    import math
    Y = np.asarray(y_lab, float); Yh = np.asarray(f_lab, float); Yhu = np.asarray(f_unlab, float)
    ppi_pt = float(np.atleast_1d(ppi_mean_pointestimate(Y, Yh, Yhu, lam=None))[0])
    ci = ppi_mean_ci(Y, Yh, Yhu, alpha=alpha, lam=None)
    ppi_lo, ppi_hi = float(np.atleast_1d(ci[0])[0]), float(np.atleast_1d(ci[1])[0])
    cl_pt = float(Y.mean())
    cci = classical_mean_ci(Y, alpha=alpha)
    cl_lo, cl_hi = float(np.atleast_1d(cci[0])[0]), float(np.atleast_1d(cci[1])[0])
    if any(math.isnan(x) for x in (ppi_pt, ppi_lo, ppi_hi)):
        ppi_pt, ppi_lo, ppi_hi = cl_pt, cl_lo, cl_hi
    imp_pt = float(np.concatenate([Yh, Yhu]).mean())
    return {'ppi_pt':ppi_pt,'ppi_lo':ppi_lo,'ppi_hi':ppi_hi,'ppi_ancho':ppi_hi-ppi_lo,
            'clasico_pt':cl_pt,'clasico_lo':cl_lo,'clasico_hi':cl_hi,'clasico_ancho':cl_hi-cl_lo,
            'imputacion_pt':imp_pt,
            'reduccion_ancho_pct':100.0*(1-(ppi_hi-ppi_lo)/(cl_hi-cl_lo)) if (cl_hi-cl_lo)>0 else 0.0}
