# -*- coding: utf-8 -*-
"""Lanza un cuestionario SUELTO (un solo archivo de plantilla) al panel.
Pensado para preguntas nuevas fuera del Deustobarómetro.

Uso:  python lanzar_extra.py                         -> extra_lideres_gobierno_2026-07-09.json, 1.000 Personas
      python lanzar_extra.py --muestra 20            -> prueba con 20
      python lanzar_extra.py encuestas/otro.json     -> otra plantilla
"""
import json, sys, threading, time
from pathlib import Path
import server

BASE = Path(__file__).parent
DEFAULT = BASE / 'encuestas' / 'extra_lideres_gobierno_2026-07-09.json'

def main():
    args = sys.argv[1:]
    muestra = None
    if '--muestra' in args:
        i = args.index('--muestra'); muestra = int(args[i+1]); del args[i:i+2]
    path = Path(args[0]) if args else DEFAULT
    if not path.is_absolute(): path = BASE / path

    if not server.ANTHROPIC_API_KEY:
        sys.exit('✗ Falta ANTHROPIC_API_KEY en .env')
    if server.GEMINI_API_KEY or server.GROQ_API_KEY:
        sys.exit('✗ Comenta GEMINI_API_KEY/GROQ_API_KEY en .env para usar Claude Haiku')
    if not server.agents:
        sys.exit('✗ No se cargaron las Personas (pv_agentes.json)')

    doc = json.loads(path.read_text(encoding='utf-8'))
    preguntas = doc['preguntas']
    subset = server.agents
    if muestra:
        import random
        subset = random.sample(server.agents, min(muestra, len(server.agents)))

    print(f"\n══ {doc['titulo']} — {len(preguntas)} preguntas, {len(subset)} Personas ══")
    with server._survey_lock:
        server._survey['definition'] = preguntas

    stop = threading.Event()
    def monitor():
        while not stop.wait(20):
            with server._survey_lock:
                done, total = server._survey['done'], server._survey['total']
                err = server._survey.get('last_error')
            print(f"   … {done}/{total}" + (f"  (último aviso: {err})" if err else ''))
    t = threading.Thread(target=monitor, daemon=True); t.start()

    t0 = time.time()
    server._survey_worker(preguntas, subset)
    stop.set()

    with server._survey_lock:
        fname = server._survey.get('saved_file'); results = server._survey['results']
    vacias = sum(1 for r in results if not r.get('resps'))
    sin_parsear = sum(1 for r in results if r.get('raw_sin_parsear'))
    print(f"   ✔ {len(results)} Personas en {time.time()-t0:.0f}s · vacías: {vacias} · sin parsear: {sin_parsear} · → resultados/{fname}")
    if fname:
        fp = BASE / 'resultados' / fname
        data = json.loads(fp.read_text(encoding='utf-8'))
        data['plantilla'] = path.name; data['titulo'] = doc['titulo']
        fp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')

if __name__ == '__main__':
    main()
