# -*- coding: utf-8 -*-
"""Contraste limpio v1 vs v2 sobre las MISMAS plantillas oficiales.

Calcula el DAM por bloque y global de dos tandas del Barómetro digital
(panel v1 = pv_agentes.json y panel v2 = pv_agentes_v2.json), usando
exactamente la misma lógica de emparejamiento y DAM que
comparar_deustobarometro.py. Así la mejora (14,0 vs 16,7 hoy) se mide
sobre las mismas 143 preguntas y se aísla del cambio de plantillas.

Cada tanda se identifica por la FECHA de sus ficheros de resultados. Para
cada plantilla (bloque) se toma el fichero de esa fecha con la tanda
completa (n>=500 Personas); si hay varios, el más reciente. Así se ignoran
automáticamente las pruebas con --muestra.

Uso:
    python contraste_v1_vs_v2.py --v1 2026-07-16 --v2 2026-07-14
    python contraste_v1_vs_v2.py --v1 2026-07-16 --v2 2026-07-14 --out resultados/contraste_v1_vs_v2.md

Por defecto v2 = 2026-07-14 (la tanda v2 ya lanzada) y escribe el informe
en resultados/contraste_v1_vs_v2.md además de imprimirlo por pantalla.
"""
import argparse
import glob
import json
from pathlib import Path

from comparar_deustobarometro import cargar_datos_reales, real_por_opcion

BASE = Path(__file__).parent
RES = BASE / 'resultados'
MIN_N = 500  # umbral para considerar "tanda completa" (excluye pruebas --muestra)


def dam_pregunta(q, resultados, datos_reales, qi):
    """DAM de una pregunta (media de |panel% - real%| sobre las opciones con
    dato real). Devuelve None si ninguna opción tiene dato real o no hay
    respuestas. Lógica idéntica a comparar_deustobarometro.py."""
    n_op = len(q['opciones'])
    k = int(q.get('multiple') or 1)
    counts = [0] * n_op
    n_resp = 0
    for r in resultados:
        resp = (r.get('resps') or {}).get(str(qi))
        if not resp:
            continue
        letras = [c for c in resp.replace(' ', '').split(',') if c]
        if not letras:
            continue
        n_resp += 1
        for l in letras[:k]:
            j = ord(l.upper()) - 65
            if 0 <= j < n_op:
                counts[j] += 1
    if not n_resp:
        return None
    pct = [100.0 * c / n_resp for c in counts]
    difs = []
    for j, op in enumerate(q['opciones']):
        rv = real_por_opcion(op, datos_reales)
        if rv is not None:
            difs.append(abs(pct[j] - rv))
    return sum(difs) / len(difs) if difs else None


def dam_de_fichero(path):
    """Devuelve (titulo, lista_de_DAM_por_pregunta) de un fichero de resultados."""
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    preguntas = data.get('definition') or data.get('preguntas')
    resultados = data.get('results') or data.get('resultados')
    reales = cargar_datos_reales(preguntas)
    dams = []
    for qi, q in enumerate(preguntas):
        dams.append(dam_pregunta(q, resultados, reales[qi], qi))
    return data.get('titulo') or Path(path).name, dams, len(resultados)


def ficheros_por_bloque(fecha):
    """Para una fecha, devuelve {plantilla: ruta_fichero_completo}."""
    out = {}
    for f in sorted(glob.glob(str(RES / f'encuesta_{fecha}*.json'))):
        try:
            d = json.loads(Path(f).read_text(encoding='utf-8'))
        except Exception:
            continue
        pl = d.get('plantilla')
        n = len(d.get('results') or [])
        if not pl or n < MIN_N:
            continue
        out[pl] = f  # el sorted() deja el más reciente al final
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--v1', required=True, help='fecha de la tanda v1, p.ej. 2026-07-16')
    ap.add_argument('--v2', default='2026-07-14', help='fecha de la tanda v2 (def. 2026-07-14)')
    ap.add_argument('--out', default=str(RES / 'contraste_v1_vs_v2.md'))
    args = ap.parse_args()

    plantillas = sorted(p.name for p in (BASE / 'encuestas').glob('barometro_digital_*.json'))
    f1 = ficheros_por_bloque(args.v1)
    f2 = ficheros_por_bloque(args.v2)

    faltan = []
    for pl in plantillas:
        if pl not in f1:
            faltan.append(f'v1 ({args.v1}): {pl}')
        if pl not in f2:
            faltan.append(f'v2 ({args.v2}): {pl}')
    if faltan:
        print('✗ Faltan tandas completas (n>=%d) para:' % MIN_N)
        for x in faltan:
            print('   -', x)
        print('\nRevisa que la tanda se lanzó completa y que la fecha es correcta.')
        return

    out = ['# Contraste v1 vs v2 — mismas plantillas oficiales\n']
    out.append(f'- Tanda v1 (`pv_agentes.json`): ficheros `encuesta_{args.v1}*`')
    out.append(f'- Tanda v2 (`pv_agentes_v2.json`): ficheros `encuesta_{args.v2}*`')
    out.append(f'- DAM = media de |panel% − real%| sobre opciones con dato real.\n')
    out.append('| Bloque | Preg. | DAM v1 | DAM v2 | Δ (v2−v1) |')
    out.append('|---|---:|---:|---:|---:|')

    pool1, pool2 = [], []
    for pl in plantillas:
        t1, d1, n1 = dam_de_fichero(f1[pl])
        t2, d2, n2 = dam_de_fichero(f2[pl])
        # emparejar por índice de pregunta; contar solo preguntas con DAM en ambas
        b1 = [a for a, b in zip(d1, d2) if a is not None and b is not None]
        b2 = [b for a, b in zip(d1, d2) if a is not None and b is not None]
        pool1 += b1
        pool2 += b2
        m1 = sum(b1) / len(b1) if b1 else None
        m2 = sum(b2) / len(b2) if b2 else None
        titulo = t2.split(':', 1)[-1].strip() if ':' in t2 else t2
        delta = (m2 - m1) if (m1 is not None and m2 is not None) else None
        out.append('| {tit} | {n} | {a} | {b} | {d} |'.format(
            tit=titulo, n=len(b1),
            a=f'{m1:.1f}' if m1 is not None else '—',
            b=f'{m2:.1f}' if m2 is not None else '—',
            d=f'{delta:+.1f}' if delta is not None else '—'))

    g1 = sum(pool1) / len(pool1) if pool1 else 0
    g2 = sum(pool2) / len(pool2) if pool2 else 0
    out.append('| **GLOBAL** | **{n}** | **{a:.1f}** | **{b:.1f}** | **{d:+.1f}** |'.format(
        n=len(pool1), a=g1, b=g2, d=g2 - g1))

    out.append('\n> Δ negativo = la v2 se acerca más al dato real (mejora).')
    txt = '\n'.join(out)
    Path(args.out).write_text(txt, encoding='utf-8')
    print(txt)
    print(f'\n✔ Informe guardado en {args.out}')


if __name__ == '__main__':
    main()
