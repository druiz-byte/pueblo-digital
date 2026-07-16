# -*- coding: utf-8 -*-
"""Compara una encuesta del panel sintético (Pueblo Digital) con los datos
reales del Deustobarómetro verano 2026.

Los datos reales se leen del campo `datos_reales` de las plantillas en
`encuestas/*.json` (las preguntas se emparejan por texto normalizado), por lo
que el script sirve para cualquier tanda sin tocar código.

Uso: python comparar_deustobarometro.py <ruta_resultados_json> [plantilla_json]
     (si no se indica plantilla, se buscan coincidencias en encuestas/*.json)
Genera un informe Markdown por stdout con tablas de contraste y DAM.
"""
import json, sys, unicodedata
from pathlib import Path

BASE = Path(__file__).parent


def norm(s):
    """Normaliza texto: sin acentos, minúsculas, espacios colapsados."""
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return ' '.join(s.lower().split())


def cargar_datos_reales(preguntas, plantilla=None):
    """Devuelve una lista paralela a `preguntas` con el dict datos_reales
    (o None) de la plantilla correspondiente, emparejando por texto."""
    if plantilla:
        fuentes = [json.loads(Path(plantilla).read_text(encoding='utf-8'))]
    else:
        fuentes = [json.loads(p.read_text(encoding='utf-8'))
                   for p in sorted((BASE / 'encuestas').glob('*.json'))]
    idx = {}  # texto normalizado -> datos_reales
    for f in fuentes:
        for q in f.get('preguntas', []):
            if q.get('datos_reales'):
                idx[norm(q['texto'])] = q['datos_reales']
    return [idx.get(norm(q['texto'])) for q in preguntas]


def real_por_opcion(op, datos_reales):
    """Busca el % real de una opción por su etiqueta (con tolerancia:
    'NS/NC' empareja con 'No lo sé...', y coincidencias parciales)."""
    if not datos_reales:
        return None
    n_op = norm(op)
    # 1º coincidencia exacta; 2º alias NS/NC; 3º coincidencia parcial
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


def main(path, plantilla=None):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    preguntas = data.get('definition') or data.get('preguntas')
    resultados = data.get('results') or data.get('resultados')
    n_total = len(resultados)
    reales = cargar_datos_reales(preguntas, plantilla)

    out = ['# Contraste panel sintético vs. Deustobarómetro verano 2026\n']
    out.append(f'- Archivo: `{Path(path).name}`')
    out.append(f"- Modelo: {data.get('modelo', '?')}  ·  Personas encuestadas: {n_total}\n")

    resumen_dam = []

    for qi, q in enumerate(preguntas):
        n_op = len(q['opciones'])
        k = int(q.get('multiple') or 1)
        # contar respuestas
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
        pct = [100.0 * c / n_resp if n_resp else 0.0 for c in counts]

        out.append(f'## P{qi+1}. {q["texto"]}\n')
        out.append(f'Respuestas válidas: {n_resp}/{n_total} ({100.0*n_resp/n_total:.1f}%)\n')
        if reales[qi] is None:
            out.append('_Sin datos reales para esta pregunta (no está en ninguna plantilla con `datos_reales`)._\n')
        out.append('| Opción | Panel % | Real % | Dif. (p.p.) |')
        out.append('|---|---:|---:|---:|')

        difs = []
        for j, op in enumerate(q['opciones']):
            rv = real_por_opcion(op, reales[qi])
            if rv is None:
                out.append(f'| {op} | {pct[j]:.1f} | — | — |')
            else:
                d = pct[j] - rv
                difs.append(abs(d))
                out.append(f'| {op} | {pct[j]:.1f} | {rv:.1f} | {d:+.1f} |')
        dam = sum(difs) / len(difs) if difs else None
        resumen_dam.append((qi + 1, dam))
        if dam is not None:
            out.append(f'\n**Desviación absoluta media (sobre opciones con dato real): {dam:.1f} p.p.**\n')
        else:
            out.append('')

    out.append('## Resumen\n')
    out.append('| Pregunta | DAM (p.p.) |')
    out.append('|---|---:|')
    con_dato = [d for _, d in resumen_dam if d is not None]
    for qn, dam in resumen_dam:
        out.append(f'| P{qn} | {dam:.1f} |' if dam is not None else f'| P{qn} | — |')
    if con_dato:
        media = sum(con_dato) / len(con_dato)
        out.append(f'| **Media** | **{media:.1f}** |')

    print('\n'.join(out))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
