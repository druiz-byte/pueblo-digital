# -*- coding: utf-8 -*-
"""Lanza el Barómetro digital (141 preguntas, 6 bloques) al panel v2
(pv_agentes_v2.json), usando el prompt adaptado build_system_prompt_v2.

Es idéntico a lanzar_barometro.py pero (1) carga las Personas v2 y (2) sustituye
el generador de prompt. Así se puede comparar la capacidad de predicción del
panel v2 frente al v1 con el mismo motor y las mismas preguntas.

Requiere ANTHROPIC_API_KEY en .env (y GEMINI/GROQ comentadas). Ejecutar en el
ordenador de David; el sandbox de Claude no tiene acceso a la API.

Uso:  python lanzar_barometro_v2.py            → 6 bloques, 1.000 Personas
      python lanzar_barometro_v2.py 3          → solo el bloque 3
      python lanzar_barometro_v2.py --muestra 50
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

# 3) reutilizar toda la maquinaria de lanzamiento del script original
import lanzar_barometro
lanzar_barometro.main()
