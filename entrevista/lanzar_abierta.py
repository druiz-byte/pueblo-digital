# -*- coding: utf-8 -*-
"""Lanza UNA pregunta ABIERTA (texto libre) al panel y guarda las respuestas
espontáneas. La codificación posterior se hace con codificar_abierta.py.

Uso:  python lanzar_abierta.py                 -> 1.000 Personas
      python lanzar_abierta.py --muestra 20    -> prueba
"""
import json, sys, time, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import server

BASE = Path(__file__).parent
PREGUNTA = ("En tu opinión, ¿cuáles son los tres problemas más importantes de "
            "Euskadi (el País Vasco) en este momento?")
USER_MSG = (
    "Te hacemos una única pregunta de una encuesta. Responde como tú mismo/a, "
    "en primera persona y con tus propias palabras.\n\n"
    f"{PREGUNTA}\n\n"
    "Menciona hasta tres problemas concretos, en una o dos frases y de forma "
    "espontánea. No uses numeración ni viñetas."
)

def call_haiku(system, user, max_tok=300):
    payload = {'model':'claude-haiku-4-5-20251001','max_tokens':max_tok,
               'system':system,'messages':[{'role':'user','content':user}]}
    for attempt in range(8):
        status, data = server.http_json(
            'https://api.anthropic.com/v1/messages', method='POST', body=payload,
            headers={'x-api-key':server.ANTHROPIC_API_KEY,
                     'anthropic-version':'2023-06-01','content-type':'application/json'})
        if status == 200:
            return (data.get('content') or [{}])[0].get('text','').strip()
        if status in (429,500,502,503,504):
            time.sleep(min(2**attempt,30)+attempt); continue
        return ''
    return ''

def main():
    args = sys.argv[1:]; muestra=None
    if '--muestra' in args:
        i=args.index('--muestra'); muestra=int(args[i+1]); del args[i:i+2]
    if not server.ANTHROPIC_API_KEY: sys.exit('✗ Falta ANTHROPIC_API_KEY en .env')
    if not server.agents: sys.exit('✗ No se cargaron las Personas (pv_agentes.json)')
    subset = server.agents
    if muestra:
        import random; subset = random.sample(server.agents, min(muestra,len(server.agents)))

    print(f"\n══ Pregunta abierta — {len(subset)} Personas ══\n{PREGUNTA}\n")
    results=[]; done={'n':0}; lock=threading.Lock()
    def process(a):
        txt = call_haiku(server.build_system_prompt(a), USER_MSG)
        row = {'id':a.get('id'),'nombre':(a.get('nombre','')+' '+a.get('apellidos','')).strip(),
               'provincia':a.get('provincia'),'genero':a.get('genero'),
               'grupo_edad':a.get('grupo_edad'),'voto':a.get('voto_autonomicas_2024'),
               'respuesta':txt}
        with lock:
            results.append(row); done['n']+=1
            if done['n']%50==0: print(f"   … {done['n']}/{len(subset)}")
        return row
    t0=time.time()
    with ThreadPoolExecutor(max_workers=20) as ex:
        list(ex.map(process, subset))
    vac=sum(1 for r in results if not r['respuesta'])
    ts=time.strftime('%Y-%m-%d_%H%M%S')
    fname=f"abierta_problemas_{ts}.json"
    out=BASE/'resultados'/fname
    json.dump({'fecha':ts,'modelo':'claude-haiku-4-5','pregunta':PREGUNTA,
               'total':len(results),'vacias':vac,'results':results},
              open(out,'w',encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"\n   ✔ {len(results)} respuestas en {time.time()-t0:.0f}s · vacías: {vac} · → resultados/{fname}")
    print("   Ahora: python codificar_abierta.py resultados/"+fname)

if __name__ == '__main__':
    main()
