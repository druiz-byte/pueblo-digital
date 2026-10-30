# -*- coding: utf-8 -*-
"""Mide cuánta respuesta la pone el EJEMPLO DE FORMATO y cuánta la Persona.

Se usa sobre una tanda lanzada con EJEMPLO_LETRAS_ALEATORIO=1: la letra del ejemplo
se sortea por Persona con semilla determinista, así que aquí se recalcula igual.

    set EJEMPLO_LETRAS_ALEATORIO=1   (Windows)   /   export ... =1  (bash)
    python lanzar_ikuspegi_v2.py --plantilla encuestas/cis_icc_julio2026_A.json
    python analizar_ancla.py resultados/<tanda>.json

Lectura: "sigue al ejemplo" muy por encima del azar (1/n_op) = el formato dicta la
respuesta en ese ítem. Cerca del azar = la respuesta es de la Persona.
"""
import json, sys, random, collections
from pathlib import Path


def letra(pid, i, j, n_op):
    return chr(65 + random.Random(int(pid) * 1009 + i * 31 + j).randrange(max(1, n_op)))


def main(path):
    d = json.loads(Path(path).read_text(encoding='utf-8'))
    print('# Efecto del ejemplo de formato — %s' % Path(path).name)
    print('\nTanda: %s · %d Personas · modelo %s\n' % (d.get('plantilla', '?'), d['done'], d['modelo']))
    print('| ítem | nº opc. | sigue al ejemplo | azar esperado | exceso | moda | ¿moda estable entre condiciones? |')
    print('|---|--:|--:|--:|--:|---|---|')
    for qi, q in enumerate(d['definition']):
        n_op = len(q['opciones'])
        sigue = tot = 0
        por_cond = collections.defaultdict(collections.Counter)
        glob = collections.Counter()
        for r in d['results']:
            v = r['resps'].get(str(qi))
            if not v:
                continue
            L = letra(r.get('id', 0), qi, 0, n_op)
            resp = v[0].upper()
            tot += 1
            glob[resp] += 1
            por_cond[L][resp] += 1
            if resp == L:
                sigue += 1
        if not tot:
            continue
        pct = 100.0 * sigue / tot
        azar = 100.0 / n_op
        modas = {L: c.most_common(1)[0][0] for L, c in por_cond.items() if c}
        estable = 'sí' if len(set(modas.values())) == 1 else 'NO (%s)' % ', '.join(
            '%s→%s' % (k, v) for k, v in sorted(modas.items()))
        print('| %s | %d | **%.1f %%** | %.1f %% | %+.1f | %s %.1f %% | %s |'
              % (q['id'], n_op, pct, azar, pct - azar,
                 glob.most_common(1)[0][0], 100.0 * glob.most_common(1)[0][1] / tot, estable))
    print('\nLa última columna es la prueba directa: si la moda del ítem cambia según la')
    print('letra que le tocó a la Persona, la respuesta la está poniendo el formato.')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    main(sys.argv[1])
