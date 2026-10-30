# -*- coding: utf-8 -*-
"""Contraste de las tandas del ICC (CIS 3575) contra el dato real.

Hace de una vez lo que en Ikuspegi eran varios pasos:
  · DAM por ítem contra el País Vasco Y contra España, con baselines moda y uniforme
  · índice de concentración y número de opciones usadas
  · NS/NC del panel frente al real
  · V de Cramér respuesta × perfil (¿usa la Persona su perfil en este dominio?)
  · contraste A vs B: reparto Mejor/Peor con y sin la categoría intermedia ofrecida

Uso:
    python comparar_icc.py resultados/<tanda_A>.json                       > paper/resultados_icc.md
    python comparar_icc.py resultados/<tanda_A>.json resultados/<tanda_B>.json > paper/resultados_icc.md
"""
import json, sys, math, collections
from pathlib import Path

PERFIL = ['voto', 'clase_social', 'nivel_estudios', 'grupo_edad', 'genero', 'euskera', 'provincia']


def carga(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def clave_real(op):
    return 'NS/NC' if op.startswith('No lo sé') or op.startswith('No sé') else op


def distribucion(doc, qi, q):
    c = collections.Counter()
    for r in doc['results']:
        v = r['resps'].get(str(qi))
        if not v:
            continue
        j = ord(v[0].upper()) - 65
        if 0 <= j < len(q['opciones']):
            c[q['opciones'][j]] += 1
    n = sum(c.values())
    return ({k: 100.0 * v / n for k, v in c.items()}, n) if n else ({}, 0)


def dam(panel, real, opciones):
    return sum(abs(panel.get(o, 0.0) - real.get(clave_real(o), 0.0)) for o in opciones) / len(opciones)


def dam_moda(real, opciones):
    mejor = max(opciones, key=lambda o: real.get(clave_real(o), 0.0))
    return dam({mejor: 100.0}, real, opciones)


def dam_unif(real, opciones):
    u = 100.0 / len(opciones)
    return dam({o: u for o in opciones}, real, opciones)


def cramer(doc, qi, q, campo):
    """V de Cramér entre la respuesta y una variable del perfil."""
    tab = collections.Counter()
    fil, col = collections.Counter(), collections.Counter()
    for r in doc['results']:
        v = r['resps'].get(str(qi))
        g = r.get(campo)
        if not v or g is None:
            continue
        j = ord(v[0].upper()) - 65
        if not (0 <= j < len(q['opciones'])):
            continue
        a = q['opciones'][j]
        tab[(a, g)] += 1
        fil[a] += 1
        col[g] += 1
    n = sum(tab.values())
    if n == 0 or len(fil) < 2 or len(col) < 2:
        return 0.0
    chi2 = 0.0
    for a in fil:
        for g in col:
            e = fil[a] * col[g] / n
            chi2 += (tab.get((a, g), 0) - e) ** 2 / e
    return math.sqrt(chi2 / (n * (min(len(fil), len(col)) - 1)))


def informe(A, B=None):
    out = []
    w = out.append
    w('# Contraste ICC (CIS 3575) — panel sintético vs dato real\n')
    w('Tanda A: `%s` · modelo `%s` · %d Personas.' % (A.get('plantilla', '?'), A['modelo'], A['done']))
    if B:
        w('Tanda B: `%s` · %d Personas.' % (B.get('plantilla', '?'), B['done']))
    w('\n`datos_reales` = submuestra País Vasco (n=133, ±8,5 p.p.); '
      '`datos_reales_espana` = muestra nacional (n=3.004, ±1,8 p.p.).\n')

    w('## DAM por ítem\n')
    w('| ítem | DAM vs CAE | moda CAE | unif. | DAM vs ESP | moda ESP | conc. panel | conc. real CAE | opciones |')
    w('|---|--:|--:|--:|--:|--:|--:|--:|--:|')
    cp, cr, filas = [], [], []
    for qi, q in enumerate(A['definition']):
        p, n = distribucion(A, qi, q)
        if not n:
            continue
        rv, re_ = q['datos_reales'], q.get('datos_reales_espana', q['datos_reales'])
        ops = q['opciones']
        d1, d2 = dam(p, rv, ops), dam(p, re_, ops)
        c = max(p.values())
        cp.append(c); cr.append(max(rv.values()))
        filas.append((q['id'], d1, d2, c, len(p), p, rv, ops))
        w('| %s | **%.1f** | %.1f | %.1f | %.1f | %.1f | %.1f | %.1f | %d de %d |'
          % (q['id'], d1, dam_moda(rv, ops), dam_unif(rv, ops), d2, dam_moda(re_, ops),
             c, max(rv.values()), len(p), len(ops)))
    if cp:
        w('\n**Concentración media: panel %.1f · real CAE %.1f (exceso %+.1f p.p.)**\n'
          % (sum(cp) / len(cp), sum(cr) / len(cr), sum(cp) / len(cp) - sum(cr) / len(cr)))

    w('## Distribuciones\n')
    for qid, _, _, _, _, p, rv, ops in filas:
        w('**%s** · panel: %s' % (qid, ' · '.join('%s %.1f' % (k, v) for k, v in sorted(p.items(), key=lambda x: -x[1]))))
        w('   real CAE: %s\n' % ' · '.join('%s %.1f' % (k, v) for k, v in sorted(rv.items(), key=lambda x: -x[1])))

    w('## ¿Usa la Persona su perfil? (V de Cramér respuesta × perfil)\n')
    w('| ítem | ' + ' | '.join(PERFIL) + ' |')
    w('|---' * (len(PERFIL) + 1) + '|')
    for qi, q in enumerate(A['definition']):
        vs = [cramer(A, qi, q, c) for c in PERFIL]
        w('| %s | %s |' % (q['id'], ' | '.join('%.2f' % v for v in vs)))
    w('\nReferencia: en la réplica de Ikuspegi la V media con el voto fue 0,36; '
      'en la pregunta de impuestos fue 0 por varianza nula.\n')

    if B:
        w('## Contraste A vs B — reparto Mejor/Peor (excluidas "Igual" y NS/NC)\n')
        w('| ítem | A: con intermedia | B: sin intermedia | real CAE | Δ A−B | NS/NC en B (real) |')
        w('|---|---|---|---|--:|---|')
        idxB = {q['id']: i for i, q in enumerate(B['definition'])}
        for qi, q in enumerate(A['definition']):
            if q['id'] not in idxB:
                continue
            qb = idxB[q['id']]
            pa, _ = distribucion(A, qi, q)
            pb, _ = distribucion(B, qb, B['definition'][qb])

            def rep(p):
                m, pe = p.get('Mejor', 0.0), p.get('Peor', 0.0)
                t = m + pe
                return (100 * m / t, 100 * pe / t) if t else (0.0, 0.0)

            rv = q['datos_reales']
            t = rv.get('Mejor', 0) + rv.get('Peor', 0)
            ra = (100 * rv.get('Mejor', 0) / t, 100 * rv.get('Peor', 0) / t) if t else (0, 0)
            a, b = rep(pa), rep(pb)
            nsb = sum(v for k, v in pb.items() if k.startswith('No lo sé'))
            w('| %s | Mejor %.1f / Peor %.1f | Mejor %.1f / Peor %.1f | Mejor %.1f / Peor %.1f | **%.1f** | %.1f (real %.1f) |'
              % (q['id'], a[0], a[1], b[0], b[1], ra[0], ra[1], abs(a[0] - b[0]), nsb, rv.get('NS/NC', 0.0)))
    return '\n'.join(out)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    A = carga(sys.argv[1])
    B = carga(sys.argv[2]) if len(sys.argv) > 2 else None
    print(informe(A, B))
