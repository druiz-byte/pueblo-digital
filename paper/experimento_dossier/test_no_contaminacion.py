# -*- coding: utf-8 -*-
"""Test de no contaminación de los prompts (experimento dossier D1-D3, 2026-11-11).

Compara, para las 1.000 Personas, la petición EXACTA que se enviaría a la API
(system + mensajes + max_tokens + modelo) con:
  · el server.py desplegado en R1-R4 (commit 7f0ec08), y
  · el server.py actual (con el campo opcional «contexto»).

Comprueba:
  T1  Tandas R (R4a/R4b/R5a/R5b/R6a/R6b) sin contexto → petición idéntica byte a byte.
  T2  Panel v1 (server.py) y panel v2 (server_anam.py, el de Render): ambos.
  T3  Tanda D: system prompt idéntico; mensaje de usuario = cabecera + dossier + mensaje R (sufijo idéntico).
  T4  Aislamiento: una tanda R lanzada justo después de una D no hereda nada (no hay estado global).
  T5  Las plantillas R no tienen campo «contexto» y la D1 tiene el hash preregistrado.
No llama a la API: intercepta http_json.

Uso (desde la carpeta Pueblo digital):  python paper/experimento_dossier/test_no_contaminacion.py
"""
import hashlib, importlib.util, json, os, subprocess, sys, tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ENT = RAIZ / 'entrevista'
COMMIT_BASE = '7f0ec08'
SHA_D1 = '3c58928018c4bdcb3e5512a89be378d8330504f1e545a6e74a1ec4097e035d5e'

for k in ('GEMINI_API_KEY', 'GROQ_API_KEY', 'EJEMPLO_LETRAS_ALEATORIO', 'EJEMPLO_LETRAS_LEGACY',
          'SURVEY_TEMPERATURE', 'ANTHROPIC_MODEL'):
    os.environ.pop(k, None)

def cargar(nombre, ruta):
    sys.path.insert(0, str(ENT))
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    # el .env local puede traer claves de Gemini/Groq; en Render solo hay Anthropic
    m.GEMINI_API_KEY = ''; m.GROQ_API_KEY = ''; m.ANTHROPIC_API_KEY = 'test'
    m.EXTRA_INSTRUCCIONES = ''
    return m

def capturar(m):
    cap = []
    def fake(url, method='GET', body=None, headers=None):
        cap.append(json.dumps(body, ensure_ascii=False, sort_keys=True))
        return 200, {'content': [{'type': 'text', 'text': '1:A'}]}
    m.http_json = fake
    return cap

base_src = subprocess.run(['git', '-C', str(RAIZ), 'show', f'{COMMIT_BASE}:entrevista/server.py'],
                          capture_output=True, check=True).stdout
tmp = Path(tempfile.mkdtemp()) / 'server_base.py'
tmp.write_bytes(base_src)

viejo = cargar('server_base', tmp)
nuevo = cargar('server_nuevo', ENT / 'server.py')
cv, cn = capturar(viejo), capturar(nuevo)

# panel v2 + prompt v2 (lo que hace server_anam.py en Render)
from prompt_v2 import build_system_prompt_v2
v2 = json.loads((RAIZ / 'pv_agentes_v2.json').read_text(encoding='utf-8'))['poblacion']
v1 = nuevo.agents
paneles = {'v1 (server.py)': (v1, None), 'v2 (server_anam.py / Render)': (v2, build_system_prompt_v2)}

plantillas_R = sorted((ENT / 'encuestas').glob('voto_generales_R*.json'))
d1 = json.loads((ENT / 'encuestas' / 'voto_generales_D1_dossier.json').read_text(encoding='utf-8'))
fallos = 0
def check(cond, msg):
    global fallos
    print(('  ✓ ' if cond else '  ✗ ') + msg)
    if not cond: fallos += 1

print('T5  Plantillas')
for f in plantillas_R:
    check('contexto' not in json.loads(f.read_text(encoding='utf-8')), f'{f.name} sin contexto')
check(hashlib.sha256(d1['contexto'].encode('utf-8')).hexdigest() == SHA_D1, 'D1: SHA-256 = preregistrado')
r4b = json.loads((ENT / 'encuestas' / 'voto_generales_R4b_sin_prefijo.json').read_text(encoding='utf-8'))
check(d1['preguntas'] == r4b['preguntas'], 'D1: pregunta y opciones idénticas a R4b')

for nombre, (agentes, bsp) in paneles.items():
    for m in (viejo, nuevo):
        m.build_system_prompt = bsp or m.build_system_prompt
    print(f'\nPanel {nombre}: {len(agentes)} Personas')
    print('T1  Tandas R sin contexto: código R1-R4 vs código nuevo')
    for f in plantillas_R:
        pr = json.loads(f.read_text(encoding='utf-8'))['preguntas']
        cv.clear(); cn.clear()
        for a in agentes:
            viejo._ask_persona(a, pr); nuevo._ask_persona(a, pr)
        check(cv == cn and len(cn) == len(agentes), f'{f.name}: {len(cn)} peticiones idénticas byte a byte')
    print('T3  Tanda D1')
    ok_sys = ok_suf = ok_pre = True
    pref = nuevo.CONTEXTO_CABECERA + '\n\n' + d1['contexto'].strip() + '\n\n'
    for a in agentes:
        cv.clear(); cn.clear()
        viejo._ask_persona(a, d1['preguntas'])
        nuevo._ask_persona(a, d1['preguntas'], d1['contexto'])
        pv, pn = json.loads(cv[0]), json.loads(cn[0])
        ok_sys &= pv['system'] == pn['system'] and pv['max_tokens'] == pn['max_tokens'] and pv['model'] == pn['model']
        uv, un = pv['messages'][0]['content'], pn['messages'][0]['content']
        ok_suf &= un.endswith(uv)
        ok_pre &= un == pref + uv
    check(ok_sys, 'system prompt, modelo y max_tokens idénticos a la tanda R')
    check(ok_suf, 'el bloque de la encuesta es idéntico (sufijo)')
    check(ok_pre, 'lo único añadido es cabecera + dossier al principio')
    print('T4  Aislamiento: R justo después de D')
    pr = r4b['preguntas']
    cv.clear(); cn.clear()
    for a in agentes[:50]:
        nuevo._ask_persona(a, pr, d1['contexto'])
    cn.clear()
    for a in agentes[:50]:
        viejo._ask_persona(a, pr); nuevo._ask_persona(a, pr)
    check(cv == cn, 'tras una D, la R vuelve a ser idéntica a R1-R4')
    check(all('contexto' not in s for s in cn) and all(nuevo.CONTEXTO_CABECERA not in s for s in cn),
          'ningún rastro del dossier en la R')

print('\nRESULTADO:', 'TODO OK — sin contaminación' if not fallos else f'{fallos} FALLO(S)')
sys.exit(1 if fallos else 0)
