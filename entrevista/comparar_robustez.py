# -*- coding: utf-8 -*-
"""Tabla comparativa de las tandas de robustez (huecos 2, 3 y 6).

Recorre `resultados/` buscando tandas lanzadas sobre la plantilla de Ikuspegi y,
para cada una, calcula las cuatro métricas del diagnóstico de la 17ª sesión:

    DAM · concentración de la opción modal · % NS-NC · nº medio de opciones usadas

y las pone al lado de la tanda de referencia y de los baselines. Así se ve de un
vistazo si el modelo frontera o el prompt anti-concentración mueven algo.

Uso:
    python comparar_robustez.py                       → todas las tandas de ≥500 Personas
    python comparar_robustez.py --min-n 30            → incluye las pruebas baratas
    python comparar_robustez.py --out resultados/robustez.md

No requiere API.
"""
import argparse
import glob
import json
from pathlib import Path

from comparar_ikuspegi import norm, real_por_opcion, contar

BASE = Path(__file__).parent
RES = BASE / 'resultados'
PLANTILLA = BASE / 'encuestas' / 'ikuspegi_piloto_2025.json'

# Referencias de la 17ª sesión, para no tener que recalcularlas.
BASELINES = [
    ('Baseline moda',                        17.0, None, None, None),
    ('Baseline uniforme',                    19.7, None, None, None),
    ('Suelo de ruido (panel perfecto)',       0.8, None, None, None),
    ('REAL (Ikuspegi 2025, n=600)',          None, 61.5, 3.4, None),
]


def metricas(data, idx):
    """(DAM, concentración modal, %NS-NC, opciones usadas/pregunta) de una tanda.

    El DAM replica EXACTAMENTE la lógica de `comparar_ikuspegi.py`: aplica
    `colapso` (escalas 1-5 → Acuerdo/Indecisión/Desacuerdo, que es como publica
    Ikuspegi) y excluye las preguntas con `media_real`, de las que el informe
    sólo da la media. Reimplementarlo a mano da 32,8 en vez de 15,7.
    """
    preguntas = data.get('definition') or data.get('preguntas') or []
    resultados = data.get('results') or data.get('resultados') or []
    dams, concs, nsnc, usadas, medias = [], [], [], [], []
    for qi, q in enumerate(preguntas):
        meta = idx.get(norm(q['texto']))
        if not meta:
            continue
        ops = q['opciones']
        counts, n = contar(resultados, qi, len(ops), int(q.get('multiple') or 1))
        if not n:
            continue
        pct = [100.0 * c / n for c in counts]
        reales = meta.get('datos_reales')
        colapso = meta.get('colapso')
        media_real = meta.get('media_real')

        usadas.append(sum(1 for x in pct if x > 0))   # sobre las opciones CRUDAS

        if media_real is not None:
            # 0-10: sólo comparable en media; no entra en DAM ni en concentración
            num = sum(int(op) * counts[j] for j, op in enumerate(ops) if op.isdigit())
            den = sum(counts[j] for j, op in enumerate(ops) if op.isdigit())
            if den:
                medias.append(num / den - media_real)
            continue

        if colapso:
            filas = [(g, sum(pct[j] for j, op in enumerate(ops) if op in miembros),
                      (reales or {}).get(g)) for g, miembros in colapso.items()]
        else:
            filas = [(op, pct[j], real_por_opcion(op, reales)) for j, op in enumerate(ops)]

        pares = [(pv, rv) for _, pv, rv in filas if rv is not None]
        if pares:
            dams.append(sum(abs(pv - rv) for pv, rv in pares) / len(pares))
            concs.append(max(pv for pv, _ in pares))
        for etq, pv, _ in filas:
            if norm(etq).startswith(('ns', 'no lo se', 'no sabe', 'ns/nc')):
                nsnc.append(pv)
    med = lambda v: (sum(v) / len(v)) if v else None
    return med(dams), med(concs), med(nsnc), med(usadas)


def etiqueta(data, fname):
    exp = data.get('experimento')
    if exp:
        partes = [exp.get('exp', '?')]
        if exp.get('modelo'):
            partes.append(exp['modelo'].replace('claude-', ''))
        if exp.get('temperature') is not None:
            partes.append(f"T={exp['temperature']}")
        if exp.get('prompt_anticonc'):
            partes.append('anti-conc')
        return ' · '.join(partes)
    return (data.get('panel') or fname)[:44]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--min-n', type=int, default=500)
    ap.add_argument('--out')
    args = ap.parse_args()

    idx, _ = None, None
    from comparar_ikuspegi import indexar_plantilla
    idx, _doc = indexar_plantilla(PLANTILLA)
    claves = set(idx)

    filas = []
    for p in sorted(glob.glob(str(RES / 'encuesta_*.json'))):
        try:
            data = json.loads(Path(p).read_text(encoding='utf-8'))
        except Exception:
            continue
        preguntas = data.get('definition') or []
        if not preguntas or not any(norm(q.get('texto', '')) in claves for q in preguntas):
            continue                      # no es una tanda de Ikuspegi
        n = len(data.get('results') or [])
        if n < args.min_n:
            continue
        dam, conc, ns, us = metricas(data, idx)
        if dam is None:
            continue
        res = data.get('results') or []
        vac = 100.0 * sum(1 for r in res if not r.get('resps')) / len(res) if res else 100.0
        filas.append((Path(p).name, etiqueta(data, Path(p).name), n, dam, conc, ns, us, vac))

    L = ['# Robustez — modelo frontera, prompt anti-concentración y temperature', '',
         'Cuatro métricas del diagnóstico de la 17ª sesión sobre las mismas 13 preguntas',
         'de Ikuspegi 2025 y el mismo panel v1. **Sólo cambia una cosa por tanda.**', '',
         '| tanda | n | vacías | DAM | concentración | NS-NC % | opciones/preg. | fichero |',
         '|---|--:|--:|--:|--:|--:|--:|---|']
    for f, et, n, dam, conc, ns, us, vac in filas:
        aviso = ' ⛔' if vac > 2.0 else ''
        L.append(f"| {et}{aviso} | {n} | {vac:.0f} % | {dam:.1f} | {conc:.1f} | "
                 f"{ns if ns is None else f'{ns:.1f}'} | {us:.1f} | `{f}` |")
    for et, dam, conc, ns, us in BASELINES:
        L.append(f"| *{et}* | — | — | {'—' if dam is None else f'{dam:.1f}'} | "
                 f"{'—' if conc is None else f'{conc:.1f}'} | "
                 f"{'—' if ns is None else f'{ns:.1f}'} | — | |")
    L += ['', '⛔ = **tanda no válida**: más del 2 % de Personas vacías. Las de referencia',
          'tuvieron 0 %. Casi siempre es límite de tasa de la API; repetir con menos hilos.', '',
          '## Cómo leerla', '',
          '- **DAM**: más bajo es mejor. La referencia v1/Haiku es **15,7**; el baseline tonto',
          '  de la moda es **17,0**. Si una variante no baja de 17,0, no aporta nada.',
          '- **Concentración**: cuota de la opción más elegida. El real es **61,5**; la referencia',
          '  v1/Haiku **83,7**. Es la métrica del colapso de varianza: si el modelo frontera o el',
          '  prompt funcionan, ESTA es la que tiene que bajar.',
          '- **NS-NC**: el real es **3,4 %**; la referencia da **1,4 %**.',
          '- **opciones/pregunta**: cuántas de las disponibles llega a usar el panel. Referencia',
          '  v1 **4,3**, v2 **2,7**.', '',
          '> Contrastar contra `../paper/preregistro_robustez.md`, donde están las predicciones',
          '> registradas **antes** de lanzar.']

    txt = '\n'.join(L)
    print(txt)
    if args.out:
        Path(args.out).write_text(txt, encoding='utf-8')
        print(f'\n→ {args.out}')


if __name__ == '__main__':
    main()
