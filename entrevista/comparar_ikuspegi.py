# -*- coding: utf-8 -*-
"""Compara una tanda del panel sintético con los datos reales del
Barómetro Ikuspegi 2025 (Observatorio Vasco de Inmigración, UPV/EHU).

Extiende `comparar_deustobarometro.py` con dos cosas que Ikuspegi necesita:

1. **`colapso`**: el informe publica las baterías de acuerdo/desacuerdo
   agregadas en Acuerdo / Indecisión / Desacuerdo / Ns-Nc. La plantilla
   pregunta la escala de 5 puntos completa y aquí se colapsa antes de comparar.
2. **`media_real`**: preguntas 0-10 de las que el informe solo publica la
   media. Se compara la media de la distribución sintética con la real.

Además emplea el error muestral del dato real (±4,0 p.p. con n=600) como
referencia: una diferencia por debajo de ese umbral no es distinguible de
ruido muestral.

Uso: python comparar_ikuspegi.py <ruta_resultados_json> [plantilla_json]
     (por defecto usa encuestas/ikuspegi_piloto_2025.json)
Genera un informe Markdown por stdout.
"""
import json
import sys
import unicodedata
from pathlib import Path

BASE = Path(__file__).parent
PLANTILLA_DEF = BASE / 'encuestas' / 'ikuspegi_piloto_2025.json'
ERROR_MUESTRAL = 4.0   # ±4,0 p.p. para n=600, 95 %, P=Q=0,5


def norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return ' '.join(s.lower().split())


def indexar_plantilla(plantilla):
    """texto normalizado -> pregunta de la plantilla."""
    doc = json.loads(Path(plantilla).read_text(encoding='utf-8'))
    return {norm(q['texto']): q for q in doc.get('preguntas', [])}, doc


def real_por_opcion(op, datos_reales):
    if not datos_reales:
        return None
    n_op = norm(op)
    for k, v in datos_reales.items():
        if norm(k) == n_op:
            return v
    for k, v in datos_reales.items():
        if norm(k) in ('ns/nc', 'ns', 'nsnc') and n_op.startswith('no lo se'):
            return v
    for k, v in datos_reales.items():
        n_k = norm(k)
        if n_k and (n_k in n_op or n_op in n_k):
            return v
    return None


def contar(resultados, qi, n_op, k):
    """Devuelve (counts, n_resp) para la pregunta qi."""
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
    return counts, n_resp


def tabla(out, filas):
    """filas: lista de (etiqueta, panel_pct, real_pct|None)."""
    out.append('| Opción | Panel % | Real % | Dif. (p.p.) | |')
    out.append('|---|---:|---:|---:|:--|')
    difs = []
    for etiqueta, pv, rv in filas:
        if rv is None:
            out.append(f'| {etiqueta} | {pv:.1f} | — | — | |')
            continue
        d = pv - rv
        difs.append(abs(d))
        marca = '' if abs(d) <= ERROR_MUESTRAL else ('⚠' if abs(d) <= 10 else '❌')
        out.append(f'| {etiqueta} | {pv:.1f} | {rv:.1f} | {d:+.1f} | {marca} |')
    return difs


def main(path, plantilla=None):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    preguntas = data.get('definition') or data.get('preguntas')
    resultados = data.get('results') or data.get('resultados')
    n_total = len(resultados)
    idx, doc = indexar_plantilla(plantilla or PLANTILLA_DEF)

    out = ['# Contraste panel sintético vs. Barómetro Ikuspegi 2025\n']
    out.append(f'- Archivo: `{Path(path).name}`')
    out.append(f"- Panel: {data.get('panel', '?')}  ·  Modelo: {data.get('modelo', '?')}"
               f"  ·  Personas: {n_total}")
    out.append(f"- Dato real: {doc.get('fuente', '?')}")
    out.append(f'- Umbral de ruido: ±{ERROR_MUESTRAL:.1f} p.p. '
               f'(⚠ = {ERROR_MUESTRAL:.0f}-10 p.p. · ❌ = >10 p.p.)\n')

    resumen = []

    for qi, q in enumerate(preguntas):
        meta = idx.get(norm(q['texto']), {})
        qid = meta.get('id') or q.get('id') or f'Q{qi+1}'
        reales = meta.get('datos_reales')
        colapso = meta.get('colapso')
        media_real = meta.get('media_real')

        n_op = len(q['opciones'])
        k = int(q.get('multiple') or 1)
        counts, n_resp = contar(resultados, qi, n_op, k)
        pct = [100.0 * c / n_resp if n_resp else 0.0 for c in counts]

        out.append(f"## {qid}. {q['texto']}\n")
        out.append(f'Respuestas válidas: {n_resp}/{n_total} ({100.0*n_resp/n_total:.1f} %)\n')
        if meta.get('fuente_dato'):
            out.append(f"_Dato real: {meta['fuente_dato']}._\n")

        dam = None

        if media_real is not None:
            # pregunta 0-10: comparar medias (excluyendo NS/NC)
            num = sum(int(op) * counts[j] for j, op in enumerate(q['opciones']) if op.isdigit())
            den = sum(counts[j] for j, op in enumerate(q['opciones']) if op.isdigit())
            media_panel = num / den if den else float('nan')
            ns = 100.0 * (n_resp - den) / n_resp if n_resp else 0.0
            out.append('| Medida | Panel | Real | Dif. |')
            out.append('|---|---:|---:|---:|')
            out.append(f'| Media (0-10) | {media_panel:.2f} | {media_real:.2f} | '
                       f'{media_panel - media_real:+.2f} |')
            out.append(f'\nNS/NC en el panel: {ns:.1f} %\n')
            out.append('Distribución sintética (el informe no la publica): ' +
                       ' · '.join(f'{op}={pct[j]:.1f}' for j, op in enumerate(q['opciones'])) + '\n')
            resumen.append((qid, None, f'media {media_panel - media_real:+.2f}'))
            continue

        if colapso:
            # colapsar la escala de 5 puntos a los grupos que publica Ikuspegi
            filas = []
            for grupo, miembros in colapso.items():
                pv = sum(pct[j] for j, op in enumerate(q['opciones']) if op in miembros)
                rv = reales.get(grupo) if reales else None
                filas.append((grupo, pv, rv))
            difs = tabla(out, filas)
            out.append('\nDetalle sin colapsar: ' +
                       ' · '.join(f'{op}={pct[j]:.1f}' for j, op in enumerate(q['opciones'])) + '\n')
        else:
            filas = [(op, pct[j], real_por_opcion(op, reales)) for j, op in enumerate(q['opciones'])]
            difs = tabla(out, filas)

        if difs:
            dam = sum(difs) / len(difs)
            out.append(f'\n**DAM: {dam:.1f} p.p.**\n')
        else:
            out.append('\n_Sin datos reales para esta pregunta._\n')
        resumen.append((qid, dam, ''))

    out.append('## Resumen\n')
    out.append('| Pregunta | DAM (p.p.) | Nota |')
    out.append('|---|---:|---|')
    con_dato = [d for _, d, _ in resumen if d is not None]
    for qid, dam, nota in resumen:
        out.append(f'| {qid} | {dam:.1f} | {nota} |' if dam is not None
                   else f'| {qid} | — | {nota} |')
    if con_dato:
        media = sum(con_dato) / len(con_dato)
        out.append(f'| **Media** | **{media:.1f}** | |')
        peor = max(resumen, key=lambda t: t[1] if t[1] is not None else -1)
        mejor = min((r for r in resumen if r[1] is not None), key=lambda t: t[1])
        out.append(f'\n- Mejor: **{mejor[0]}** ({mejor[1]:.1f} p.p.)  ·  '
                   f'Peor: **{peor[0]}** ({peor[1]:.1f} p.p.)')
        out.append(f'- Preguntas dentro del ruido muestral (DAM ≤ {ERROR_MUESTRAL:.0f} p.p.): '
                   f'{sum(1 for d in con_dato if d <= ERROR_MUESTRAL)}/{len(con_dato)}')

    print('\n'.join(out))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
