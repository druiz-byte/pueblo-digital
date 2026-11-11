# -*- coding: utf-8 -*-
"""Verifica un fichero de resultados recién descargado contra su plantilla.

Uso:  python paper/experimento_dossier/verificar_tanda.py <encuesta_....json> <plantilla.json>
Ej.:  python paper/experimento_dossier/verificar_tanda.py entrevista/resultados/encuesta_2026-11-11_1530.json entrevista/encuestas/voto_generales_D1_dossier.json

Comprueba: pregunta y opciones idénticas a la plantilla · presencia/ausencia de
contexto según la plantilla · SHA-256 del contexto · modelo · 1.000 Personas ·
0 errores · 0 vacías o sin parsear (umbral del preregistro: 2 %).
"""
import hashlib, json, sys
from pathlib import Path

res = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
tpl = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
ok = True
def check(c, m):
    global ok
    print(('✓ ' if c else '✗ ') + m); ok &= bool(c)

check(res['definition'] == tpl['preguntas'], 'pregunta y opciones idénticas a la plantilla')
ctx_t = (tpl.get('contexto') or '').strip() or None
ctx_r = res.get('contexto')
if ctx_t is None:
    check(ctx_r is None, 'tanda R: el fichero NO lleva contexto')
else:
    check(ctx_r == ctx_t, 'tanda D: contexto idéntico al de la plantilla')
    h = hashlib.sha256(ctx_t.encode('utf-8')).hexdigest()
    check(res.get('contexto_sha256') == h, f'SHA-256 del contexto = {h[:16]}…')
check(res.get('modelo') == 'claude-haiku-4-5-20251001', f"modelo = {res.get('modelo')}")
check(res.get('total') == 1000 and res.get('done') == 1000, f"Personas = {res.get('done')}/{res.get('total')}")
check(not res.get('errores'), f"errores = {res.get('errores') or 0}")
vac = sum(1 for r in res['results'] if not r.get('resps'))
check(vac / max(1, len(res['results'])) <= 0.02, f'vacías o sin parsear = {vac}')
print('\nTANDA VÁLIDA' if ok else '\nTANDA NO VÁLIDA — no analizar; relanzar y declararlo')
sys.exit(0 if ok else 1)
