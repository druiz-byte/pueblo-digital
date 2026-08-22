# -*- coding: utf-8 -*-
"""Experimentos de robustez para el paper de IJRM — huecos 2, 3 y 6.

Relanza las MISMAS 13 preguntas de Ikuspegi 2025 sobre el MISMO panel v1
cambiando una sola cosa cada vez, para poder atribuir el efecto:

  hueco 2 · MODELO      ¿el colapso de varianza desaparece con un modelo frontera?
  hueco 3 · PROMPT      ¿desaparece si el prompt legitima las posiciones minoritarias?
  hueco 6 · TEMPERATURE ¿es un artefacto de decodificación?

Todo lo demás (panel, plantilla, motor, parseo) es idéntico a `lanzar_ikuspegi.py`,
así que el contraste es limpio contra la tanda de referencia
`encuesta_2026-08-08_*.json` (v1, Haiku, DAM 15,7 · concentración 83,7).

USO — debe ejecutarse en el PC de David (la API no es accesible desde el sandbox):

    # 0. prueba barata antes de gastar (30 Personas, ~10 s)
    python lanzar_robustez.py --exp modelo --modelo claude-opus-5 --muestra 30

    # hueco 2 · modelo frontera, 1.000 Personas
    python lanzar_robustez.py --exp modelo --modelo claude-opus-5

    # hueco 3 · prompt anti-concentración, 1.000 Personas, mismo Haiku
    python lanzar_robustez.py --exp prompt

    # hueco 6 · temperature explícita (0.0 = decodificación casi codiciosa)
    python lanzar_robustez.py --exp temp --temperature 0.0

    # combinado: frontera + prompt (sólo si los dos por separado mueven algo)
    python lanzar_robustez.py --exp modelo+prompt --modelo claude-opus-5

Cada tanda se guarda en `resultados/` con la etiqueta del experimento y se
contrasta con:

    python comparar_ikuspegi.py resultados/<fichero> > resultados/<informe>.md

⚠ ANTES DE LANZAR: registra tus predicciones en
   `../paper/preregistro_robustez.md`. Funcionó muy bien en la 17ª sesión y es
   material de credibilidad ante revisores.
"""
import argparse
import json
import os
import sys
from pathlib import Path

BASE = Path(__file__).parent

# ─────────────────────────────────────────────────────────────────────────────
# HUECO 3 · Variante de prompt anti-concentración
# ─────────────────────────────────────────────────────────────────────────────
# Diseño: atacar los tres mecanismos observados en la 17ª sesión —
#   (a) la opción modal se lleva 83,7 % frente al 61,5 % real
#   (b) NS/NC infrarrepresentado (1,4 % vs 3,4 %)
#   (c) CERO de mil eligen las opciones extremas, que en el mundo real tienen
#       el 34,2 % y el 31,3 %
# Sin decir NUNCA cuál es la distribución real ni cuántas opciones usar: eso
# sería filtrar la respuesta y el experimento no valdría nada.
PROMPT_ANTICONC = """
Antes de responder, ten en cuenta:
- Contesta lo que TÚ piensas de verdad, aunque sea una postura minoritaria o
  incómoda. Las opiniones tajantes y los extremos de la escala son respuestas
  tan legítimas como las intermedias.
- No elijas la opción intermedia ni la más prudente por descarte. Si tu postura
  es clara, dilo aunque suene rotundo.
- Si de verdad no tienes opinión formada o prefieres no contestar, esa también
  es una respuesta válida: no te fuerces a elegir.
"""

EXPERIMENTOS = {
    'modelo':        dict(prompt=False, etiqueta='modelo'),
    'prompt':        dict(prompt=True,  etiqueta='prompt_anticonc'),
    'temp':          dict(prompt=False, etiqueta='temp'),
    'modelo+prompt': dict(prompt=True,  etiqueta='modelo_y_prompt'),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--exp', required=True, choices=sorted(EXPERIMENTOS),
                    help='qué se cambia respecto a la tanda de referencia')
    ap.add_argument('--modelo', help='p.ej. claude-opus-5 (hueco 2)')
    ap.add_argument('--temperature', help='p.ej. 0.0 (hueco 6). Si se omite, la API usa 1.0')
    ap.add_argument('--muestra', type=int, help='nº de Personas (por defecto, las 1.000)')
    ap.add_argument('--hilos', type=int,
                    help='peticiones en paralelo. Por defecto 20 con Haiku y 4 con un modelo '
                         'frontera (sus límites de tasa son mucho más bajos)')
    ap.add_argument('--plantilla', default='encuestas/ikuspegi_piloto_2025.json')
    args = ap.parse_args()

    cfg = EXPERIMENTOS[args.exp]
    if 'modelo' in args.exp and not args.modelo:
        sys.exit('✗ --exp modelo requiere --modelo (p.ej. --modelo claude-opus-5)')

    # Los knobs se leen al importar server, así que hay que fijarlos ANTES.
    if args.modelo:
        os.environ['ANTHROPIC_MODEL'] = args.modelo
    if args.temperature is not None:
        os.environ['SURVEY_TEMPERATURE'] = args.temperature
    if args.hilos:
        os.environ['SURVEY_WORKERS'] = str(args.hilos)

    import server                       # noqa: E402  (import tardío a propósito)
    if cfg['prompt']:
        server.EXTRA_INSTRUCCIONES = PROMPT_ANTICONC

    if not server.ANTHROPIC_API_KEY:
        sys.exit('✗ Falta ANTHROPIC_API_KEY en .env')
    if server.GEMINI_API_KEY or server.GROQ_API_KEY:
        sys.exit('✗ Comenta GEMINI_API_KEY/GROQ_API_KEY en .env para usar Claude')
    if not server.agents:
        sys.exit('✗ No se cargaron las Personas (pv_agentes.json)')

    plantilla = Path(args.plantilla)
    if not plantilla.is_absolute():
        plantilla = BASE / plantilla
    if not plantilla.exists():
        sys.exit(f'✗ No existe la plantilla {plantilla}')

    subset = server.agents
    if args.muestra:
        import random
        random.seed(20250311)           # misma semilla que lanzar_ikuspegi.py
        subset = random.sample(server.agents, min(args.muestra, len(server.agents)))

    print('══ Experimento de robustez ══')
    print(f'  experimento .. {args.exp}')
    print(f'  modelo ....... {server.ANTHROPIC_MODEL}')
    print(f'  temperature .. {server.SURVEY_TEMPERATURE or "(por defecto de la API = 1.0)"}')
    print(f'  prompt extra . {"SÍ (anti-concentración)" if cfg["prompt"] else "no"}')
    print(f'  Personas ..... {len(subset)}')
    print(f'  plantilla .... {plantilla.name}')
    print('  referencia ... v1/Haiku: DAM 15,7 · concentración 83,7 · NS-NC 1,4 · 4,3 opciones/preg.\n')

    import lanzar_ikuspegi
    lanzar_ikuspegi.PANEL = (f'v1 (pv_agentes.json) · exp={args.exp} · '
                             f'modelo={server.ANTHROPIC_MODEL} · '
                             f'temp={server.SURVEY_TEMPERATURE or "default"}')
    fname = lanzar_ikuspegi.lanzar(plantilla, subset)

    if fname:
        fpath = BASE / 'resultados' / fname
        data = json.loads(fpath.read_text(encoding='utf-8'))
        res = data.get('results') or []
        vacias = sum(1 for r in res if not r.get('resps'))
        pct = 100.0 * vacias / len(res) if res else 100.0
        data['experimento'] = dict(exp=args.exp, modelo=server.ANTHROPIC_MODEL,
                                   temperature=server.SURVEY_TEMPERATURE,
                                   prompt_anticonc=cfg['prompt'], n=len(subset),
                                   vacias=vacias, pct_vacias=round(pct, 1))
        if pct > 2.0:
            print(f'\n  ⛔ TANDA NO VÁLIDA: {vacias}/{len(res)} Personas vacías ({pct:.0f} %).')
            print('     Las tandas de referencia tuvieron 0. Casi siempre es límite de tasa:')
            print('     baja la concurrencia y repite, p.ej. --hilos 2')
            print('     (los reintentos ya son automáticos: 8 con backoff exponencial).')
        elif vacias:
            print(f'\n  ⚠ {vacias}/{len(res)} Personas vacías ({pct:.1f} %) — dentro de lo tolerable.')
        fpath.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
        etq = cfg['etiqueta']
        print('\n══ Contraste con el dato real ══')
        print(f'  python comparar_ikuspegi.py resultados/{fname} '
              f'> resultados/contraste_ikuspegi_{etq}.md')
        print('\n  Luego, para la tabla comparativa de las tandas:')
        print(f'  python comparar_robustez.py')


if __name__ == '__main__':
    main()
