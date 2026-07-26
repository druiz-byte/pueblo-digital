# -*- coding: utf-8 -*-
"""Construye y VERIFICA el crosswalk 152 preguntas del Barómetro digital ↔
variables del .sav del Deustobarómetro verano 2026 (para el PPI++ completo).

Para cada pregunta de las 7 plantillas `barometro_digital_*.json` determina:
  - tipo: 'cat' (categórica), 'escala' (0-10) o 'multi' (multi-respuesta)
  - la(s) variable(s) del .sav correspondientes (+ códigos de selección en multi)

VERIFICACIÓN AUTOMÁTICA (sin API): reconstruye desde el .sav el % real de cada
opción y lo compara con el campo `datos_reales` que ya trae la plantilla. Si el
crosswalk es correcto, el error medio debe ser ~0. En la última ejecución:
152/152 OK, error medio 0,58 p.p.

Salida:  crosswalk_ppi.json  ·  crosswalk_cobertura.md
Uso:     python build_crosswalk.py     (requiere pyreadstat y el .sav en la raíz)
"""
import json, re, unicodedata
from pathlib import Path
import pyreadstat

RAIZ = Path(__file__).resolve().parent.parent
SAV  = RAIZ / "Datos Deustobarometro verano 2026.sav"
ENC  = RAIZ / "entrevista" / "encuestas"
OUT_JSON = Path(__file__).parent / "crosswalk_ppi.json"
OUT_MD   = Path(__file__).parent / "crosswalk_cobertura.md"

df, meta = pyreadstat.read_sav(str(SAV))
LABELS = meta.column_names_to_labels
VVL    = meta.variable_value_labels
PVARS  = [v for v in df.columns if re.match(r'^p\d', v)]


def norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9ñ ]', ' ', s)


def toks(s):
    return set(w for w in norm(s).split() if len(w) > 2)


VT = {v: toks(LABELS.get(v) or '') for v in PVARS}


def match_var(q, excl=()):
    qt = toks(q); best = (0.0, 0, None)
    for v in PVARS:
        if v in excl or not VT[v]:
            continue
        inter = len(qt & VT[v]); sc = inter / (len(qt | VT[v]) or 1)
        if (sc, inter) > (best[0], best[1]):
            best = (sc, inter, v)
    return best


# grupos de batería binaria: prefijo pN_ cuyos miembros son indicadores
BG = {}
for v in PVARS:
    m = re.match(r'^(p\d+)_\d+$', v); vl = VVL.get(v) or {}
    if m and len(vl) <= 2:
        for code, txt in vl.items():
            BG.setdefault(m.group(1), []).append((v, code, norm(txt)))


def match_multi(ops):
    on = [norm(o) for o in ops]; best = (0, None)
    for pref, mem in BG.items():
        sc = sum(1 for o in on if any(o == t or o in t or t in o for _, _, t in mem))
        if sc > best[0]:
            best = (sc, pref)
    pref = best[1]
    if pref is None:
        return [None] * len(ops), [None] * len(ops)
    mem = BG[pref]; vo = []; co = []
    for o in on:
        h = next(((v, c) for v, c, t in mem if o == t or o in t or t in o), (None, None))
        vo.append(h[0]); co.append(h[1])
    return vo, co


def es_escala(ops):
    return len([o for o in ops if re.fullmatch(r'\d+', o.strip())]) >= 10


def item_de(t):
    return t.split('::')[-1].strip() if '::' in t else None


def pct_cat(var):
    ser = df[var].dropna(); n = len(ser); out = {}
    if not n:
        return out
    for val, cnt in ser.value_counts().items():
        lab = VVL.get(var, {}).get(val)
        if lab is not None:
            out[norm(lab)] = 100.0 * cnt / n
    return out


def mo(op, keys):
    n = norm(op)
    if n in keys:
        return n
    if n.startswith('no lo se') or n in ('ns/nc', 'ns', 'nsnc'):
        for k in keys:
            if k.startswith('no lo se') or k in ('ns/nc', 'ns', 'nsnc'):
                return k
    for k in keys:
        if k and (k in n or n in k):
            return k
    return None


cw = []
for path in sorted(ENC.glob('barometro_digital_*.json')):
    doc = json.loads(path.read_text(encoding='utf-8'))
    for qi, q in enumerate(doc['preguntas']):
        texto = q['texto']; ops = q['opciones']; mult = int(q.get('multiple') or 1)
        dr = q.get('datos_reales') or {}; drn = {norm(k): v for k, v in dr.items()}
        e = {'bloque': path.name, 'qi': qi, 'texto': texto, 'opciones': ops, 'multiple': mult}
        tipo = 'escala' if es_escala(ops) else ('multi' if mult > 1 else 'cat')
        e['tipo'] = tipo; errs = []; estado = 'OK'
        if tipo == 'multi':
            vo, co = match_multi(ops); e['vars'] = vo; e['codigos'] = co
            for op, v, c in zip(ops, vo, co):
                if v is not None:
                    sel = (df[v] == c).mean() * 100.0; k = mo(op, drn.keys())
                    if k is not None:
                        errs.append(abs(sel - drn[k]))
            if any(v is None for v in vo):
                estado = 'REVISAR (opción sin variable)'
        elif tipo == 'escala':
            it = item_de(texto); j, inter, v = match_var(it or texto); e['var'] = v
            ser = df[v].dropna(); ser = ser[ser <= 10]
            if 'media_real' in dr:
                errs.append(abs(ser.mean() - dr['media_real']))
            else:
                rec = pct_cat(v)
                for op in ops:
                    k = mo(op, drn.keys()); kk = mo(op, rec.keys())
                    if k is not None and kk is not None:
                        errs.append(abs(rec[kk] - drn[k]))
            e['match_debil'] = (j < 0.3 or inter < 3)
        else:
            it = item_de(texto); j, inter, v = match_var(it or texto); e['var'] = v
            rec = pct_cat(v)
            for op in ops:
                k = mo(op, drn.keys()); kk = mo(op, rec.keys())
                if k is not None and kk is not None:
                    errs.append(abs(rec[kk] - drn[k]))
            e['match_debil'] = (j < 0.3 or inter < 3)
        err = sum(errs) / len(errs) if errs else None
        if err is not None:
            if err > 5:
                estado = 'REVISAR (error alto)'
        else:
            if e.get('match_debil') or any(x is None for x in e.get('vars', [e.get('var')])):
                estado = 'REVISAR (sin verificación)'
        e['verif_error_pp'] = round(err, 2) if err is not None else None
        e['estado'] = estado
        cw.append(e)

OUT_JSON.write_text(json.dumps(cw, ensure_ascii=False, indent=1), encoding='utf-8')

rep = ['# Crosswalk 152 preguntas ↔ .sav — cobertura y verificación\n',
       'Error = |% reconstruido del .sav − % `datos_reales` del template|, media por pregunta (0 = perfecto).\n',
       '| Bloque | q | Tipo | Variable(s) | Opc. | Error (p.p.) | Estado |',
       '|---|--:|---|---|--:|--:|---|']
for e in cw:
    v = e.get('var') or '+'.join(str(x) for x in e.get('vars', []))
    blk = e['bloque'].split('barometro_digital_')[1].replace('.json', '')[:10]
    err = '—' if e['verif_error_pp'] is None else f"{e['verif_error_pp']:.1f}"
    rep.append(f"| {blk} | {e['qi']} | {e['tipo']} | {v[:38]} | {len(e['opciones'])} | {err} | {e['estado']} |")
errs = [e['verif_error_pp'] for e in cw if e['verif_error_pp'] is not None]
ok = sum(1 for e in cw if e['estado'] == 'OK')
rep += ['\n## Resumen', f"- Preguntas: {len(cw)} · OK: {ok} · a revisar: {len(cw)-ok}",
        f"- Error medio de reconstrucción: {sum(errs)/len(errs):.2f} p.p.",
        f"- Por tipo: cat={sum(1 for e in cw if e['tipo']=='cat')}, "
        f"escala={sum(1 for e in cw if e['tipo']=='escala')}, "
        f"multi={sum(1 for e in cw if e['tipo']=='multi')}"]
OUT_MD.write_text('\n'.join(rep), encoding='utf-8')
print(f"OK {ok}/{len(cw)} · error medio {sum(errs)/len(errs):.2f} p.p. → {OUT_JSON.name}, {OUT_MD.name}")
