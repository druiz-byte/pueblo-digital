# -*- coding: utf-8 -*-
"""Lanza la réplica del Barómetro Ikuspegi 2025 sobre el panel v1
(`pv_agentes.json`, las 1.000 Personas del País Vasco).

Mismo motor que `lanzar_barometro.py`: usa `server.py`, que carga el .env, las
Personas del panel v1 y el worker de encuesta con Claude Haiku.

Uso:
    python lanzar_ikuspegi.py                  → piloto completo, 1.000 Personas
    python lanzar_ikuspegi.py --muestra 30     → prueba barata (30 Personas)
    python lanzar_ikuspegi.py --plantilla encuestas/otra.json

Requisitos: ANTHROPIC_API_KEY válida en .env y GEMINI_API_KEY/GROQ_API_KEY
comentadas. Debe ejecutarse en el PC de David (la API no es accesible desde el
sandbox).

Coste orientativo: ~13 preguntas × 1.000 Personas con Haiku ≈ 0,2-0,3 $ y ~3-5 min.
"""
import json
import sys
import threading
import time
from pathlib import Path

import server  # carga .env, las Personas (panel v1) y el motor de encuesta

BASE = Path(__file__).parent
PLANTILLA_DEF = BASE / 'encuestas' / 'ikuspegi_piloto_2025.json'
PANEL = 'v1 (pv_agentes.json)'   # lanzar_ikuspegi_v2.py lo sobrescribe


def lanzar(path, subset):
    doc = json.loads(path.read_text(encoding='utf-8'))
    preguntas = doc['preguntas']
    print(f"\n══ {doc['titulo']} — {len(preguntas)} preguntas, {len(subset)} Personas ══")

    with server._survey_lock:
        server._survey['definition'] = preguntas

    stop = threading.Event()

    def monitor():
        while not stop.wait(30):
            with server._survey_lock:
                done, total = server._survey['done'], server._survey['total']
                err = server._survey.get('last_error')
            print(f"   … {done}/{total}" + (f"  (último aviso: {err})" if err else ''))

    threading.Thread(target=monitor, daemon=True).start()

    t0 = time.time()
    server._survey_worker(preguntas, subset)   # bloqueante; guarda en resultados/
    stop.set()

    with server._survey_lock:
        fname = server._survey.get('saved_file')
        results = server._survey['results']
    vacias = sum(1 for r in results if not r.get('resps'))
    sin_parsear = sum(1 for r in results if r.get('raw_sin_parsear'))
    print(f"   ✔ {len(results)} Personas en {time.time()-t0:.0f}s · "
          f"vacías: {vacias} · sin parsear: {sin_parsear} · → resultados/{fname}")

    if fname:
        fpath = BASE / 'resultados' / fname
        data = json.loads(fpath.read_text(encoding='utf-8'))
        data['plantilla'] = path.name
        data['titulo'] = doc['titulo']
        data['panel'] = PANEL
        fpath.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
    return fname


def main():
    args = sys.argv[1:]
    muestra = None
    plantilla = PLANTILLA_DEF
    if '--muestra' in args:
        i = args.index('--muestra')
        muestra = int(args[i + 1])
        del args[i:i + 2]
    if '--plantilla' in args:
        i = args.index('--plantilla')
        plantilla = Path(args[i + 1])
        del args[i:i + 2]

    if not server.ANTHROPIC_API_KEY:
        sys.exit('✗ Falta ANTHROPIC_API_KEY en .env')
    if server.GEMINI_API_KEY or server.GROQ_API_KEY:
        sys.exit('✗ Comenta GEMINI_API_KEY/GROQ_API_KEY en .env para usar Claude Haiku')
    if not server.agents:
        sys.exit('✗ No se cargaron las Personas (pv_agentes.json)')
    if not plantilla.exists():
        sys.exit(f'✗ No existe la plantilla {plantilla}')

    subset = server.agents
    if muestra:
        import random
        random.seed(20250311)   # fecha de campo de Ikuspegi: submuestra reproducible
        subset = random.sample(server.agents, min(muestra, len(server.agents)))

    print(f"Réplica Ikuspegi 2025 · panel {PANEL} · {len(subset)} Personas · modelo claude-haiku-4-5")
    fname = lanzar(plantilla, subset)

    print('\n══ Contraste con el dato real ══')
    print(f'  python comparar_ikuspegi.py resultados/{fname} '
          f'> resultados/contraste_ikuspegi_piloto.md')


if __name__ == '__main__':
    main()
