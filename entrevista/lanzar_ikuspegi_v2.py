# -*- coding: utf-8 -*-
"""Lanza la réplica del Barómetro Ikuspegi 2025 sobre el panel v2
(`pv_agentes_v2.json`), usando el prompt adaptado `build_system_prompt_v2`.

Idéntico a `lanzar_ikuspegi.py` salvo por (1) el panel que carga y (2) el
generador de prompt. Mismo motor, mismas 13 preguntas, mismo modelo → el
contraste v1 vs v2 sobre Ikuspegi es limpio.

Uso:  python lanzar_ikuspegi_v2.py                 → 1.000 Personas
      python lanzar_ikuspegi_v2.py --muestra 30
      python lanzar_ikuspegi_v2.py --plantilla encuestas/otra.json

Contraste posterior (el comparador es el mismo, empareja por texto):
      python comparar_ikuspegi.py resultados/<fichero>.json > resultados/contraste_ikuspegi_v2_n1000.md
"""
import json
from pathlib import Path

import server
from prompt_v2 import build_system_prompt_v2

# 1) cargar el panel v2
V2 = Path(__file__).parent.parent / "pv_agentes_v2.json"
server.agents = json.loads(V2.read_text(encoding="utf-8"))["poblacion"]
print(f"Panel v2 cargado: {len(server.agents)} Personas ({V2.name})")

# 2) sustituir el generador de prompt por el adaptado
server.build_system_prompt = build_system_prompt_v2

# 3) reutilizar la maquinaria de lanzamiento del script v1
import lanzar_ikuspegi

lanzar_ikuspegi.PANEL = 'v2 (pv_agentes_v2.json)'

if __name__ == '__main__':
    lanzar_ikuspegi.main()
