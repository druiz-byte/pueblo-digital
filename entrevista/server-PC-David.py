#!/usr/bin/env python3
"""
Pueblo Digital — Entrevistador
Servidor Python · sin dependencias externas (stdlib only)
Uso: python server.py

API: LiveAvatar (api.liveavatar.com) + Anthropic
"""

import json
import os
import re
import time
import threading
import concurrent.futures
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# ── Cargar .env ────────────────────────────────────────────────────────────────
def load_env():
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        print('⚠  No se encontró el fichero .env')
        print('   Copia .env.example como .env y añade tus claves API.')
        return
    for line in env_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, _, v = line.partition('=')
            os.environ.setdefault(k.strip(), v.strip())

load_env()

LIVEAVATAR_API_KEY = os.environ.get('HEYGEN_API_KEY', '')
ANTHROPIC_API_KEY  = os.environ.get('ANTHROPIC_API_KEY', '')
GROQ_API_KEY       = os.environ.get('GROQ_API_KEY', '')
PORT               = int(os.environ.get('PORT', 3000))
PUBLIC_DIR         = Path(__file__).parent / 'public'
RESULTS_DIR        = Path(__file__).parent / 'resultados'   # encuestas guardadas (sincroniza vía OneDrive)
RESULTS_DIR.mkdir(exist_ok=True)

# ── Cargar agentes ─────────────────────────────────────────────────────────────
AGENTS_PATH = Path(__file__).parent.parent / 'pv_agentes.json'
agents = []
try:
    with open(AGENTS_PATH, encoding='utf-8') as f:
        agents = json.load(f)['poblacion']
    print(f'✓ {len(agents)} agentes cargados')
except Exception as e:
    print(f'✗ No se pudo cargar pv_agentes.json: {e}')

def find_agent(agent_id):
    return next((a for a in agents if a['id'] == agent_id), None)

# ── System prompt ──────────────────────────────────────────────────────────────
def build_system_prompt(a):
    ideol = (f' Ideología: {a["ideologia_0_10"]}/10 (1=izq, 10=dcha).'
             if a.get('ideologia_0_10') is not None else '')
    nac   = (f' Sentimiento nacionalista vasco: {a["escala_nacionalismo_0_10"]}/10.'
             if a.get('escala_nacionalismo_0_10') is not None else '')
    probs = ', '.join(a.get('principales_problemas') or []) or 'No especificados'

    p = (
        f"Eres {a['nombre']} {a['apellidos']}, una persona que vive en {a['provincia']} (País Vasco). "
        f"Tienes {a['edad']} años.\n\n"
        f"PERFIL PERSONAL:\n"
        f"- Género: {a['genero']}\n"
        f"- Estudios: {a['nivel_estudios']}\n"
        f"- Situación laboral: {a['situacion_laboral']}\n"
        f"- Clase social: {a['clase_social']}\n"
        f"- Religión: {a['religion']}\n"
        f"- Nacimiento: {a['nacimiento']}\n\n"
        f"PERFIL LINGÜÍSTICO:\n"
        f"- Competencia en euskera: {a['euskera']}\n"
        f"- Idioma preferido: {a['lengua_encuesta']}\n\n"
        f"PERFIL POLÍTICO:\n"
        f"- Voto autonómicas 2024: {a['voto_autonomicas_2024']}\n"
        f"- Preferencia territorial: {a['preferencia_territorial']}{ideol}{nac}\n"
        f"- Valoración de la economía vasca: {a['valoracion_economia_pv']}\n"
        f"- Valoración de la situación política: {a['valoracion_politica_pv']}\n"
        f"- Principales preocupaciones: {probs}"
    )

    m = a.get('perfil_mediatico')
    if m:
        rrss = ', '.join(m.get('rrss_activas') or []) or 'Ninguna'
        cm   = m.get('confianza_medios') or {}
        p += (
            f"\n\nPERFIL MEDIÁTICO:\n"
            f"- Medio principal noticias: {m.get('medio_principal_noticias','N/D')}\n"
            f"- Redes sociales: {rrss}\n"
            f"- Confianza medios (TV/Radio/RRSS): "
            f"{cm.get('television','?')}/{cm.get('radio','?')}/{cm.get('rrss','?')} (0-10)\n"
            f"- Interés política: {m.get('interes_politica','N/D')}"
        )

    b = a.get('perfil_bienestar')
    if b:
        p += (
            f"\n\nPERFIL DE BIENESTAR:\n"
            f"- Salud autopercibida: {b.get('salud_autopercibida','N/D')}\n"
            f"- Estado emocional: {b.get('estado_emocional','N/D')}\n"
            f"- Satisfacción vital (0-10): {b.get('satisfaccion_vida_0_10','N/D')}\n"
            f"- Control de la propia vida (0-10): {b.get('control_vida_0_10','N/D')}\n"
            f"- Satisfacción relaciones (0-10): {b.get('satisfaccion_relaciones_0_10','N/D')}\n"
            f"- Situación económica personal (0-10): {b.get('satisfaccion_ahorro_0_10','N/D')}\n"
            f"- Actividad física: {b.get('actividad_fisica','N/D')}\n"
            f"- Sentimiento de soledad: {b.get('frecuencia_soledad','N/D')}\n"
            f"- Contacto social: {b.get('contacto_social','N/D')}\n"
            f"- Preocupación cambio climático: {b.get('preocupacion_clima','N/D')}\n"
            f"- Sentido de pertenencia: {b.get('sentido_pertenencia','N/D')}\n"
            f"- Cultura presente en su vida: {b.get('cultura_presente_en_vida','N/D')}"
        )

    p += (
        f"\n\nINSTRUCCIONES DE RESPUESTA:\n"
        f"- Responde SIEMPRE en primera persona como {a['nombre']}, con el lenguaje propio de tu perfil.\n"
        f"- Las respuestas son para ser HABLADAS por un avatar. Usa lenguaje oral, sin listas ni formatos.\n"
        f"- Sé BREVE: máximo 3-4 frases por respuesta.\n"
        f"- Muestra matices y posibles contradicciones como una persona real.\n"
        f"- Si la pregunta es en castellano, responde en castellano. Si es en euskera, responde en euskera."
    )
    return p

# ── HTTP helper ────────────────────────────────────────────────────────────────
def http_json(url, method='GET', body=None, headers=None):
    data = json.dumps(body).encode('utf-8') if body is not None else None
    h = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            body_text = e.read().decode('utf-8')
            return e.code, json.loads(body_text)
        except Exception:
            return e.code, {'error': str(e), 'code': e.code}

def la_headers(token=None):
    """LiveAvatar API headers. token = session JWT; otherwise API key auth."""
    h = {'Content-Type': 'application/json'}
    if token:
        h['Authorization'] = f'Bearer {token}'
    else:
        h['X-API-KEY'] = LIVEAVATAR_API_KEY
    return h

# ── Motor de encuesta ─────────────────────────────────────────────────────────
_survey = {
    'running': False, 'done': 0, 'total': 0,
    'results': [], 'error': None, 'definition': None,
}
_survey_lock = threading.Lock()

def _parse_survey_response(text, preguntas):
    """Parsea la respuesta de un LLM en múltiples formatos.
    Respuesta única → "A"; selección múltiple → "A,C,F" (hasta k letras)."""
    resps = {}
    n_q = len(preguntas)
    # Formato "N:X", "N. X", "N) X", "N- X", "N:X,Y,Z"
    for m in re.finditer(r'(\d+)\s*[:.)\-]\s*([A-Za-z]\b(?:\s*[,;/]\s*[A-Za-z]\b)*)', text):
        idx = int(m.group(1)) - 1
        if not (0 <= idx < n_q):
            continue
        q    = preguntas[idx]
        n_op = len(q.get('opciones') or [])
        k    = max(1, int(q.get('multiple') or 1))
        letters = []
        for ch in re.findall(r'[A-Za-z]', m.group(2)):
            ch = ch.upper()
            if (ord(ch) - 65) < n_op and ch not in letters:
                letters.append(ch)
        if letters:
            resps[str(idx)] = ','.join(letters[:k])
    # Fallback para pregunta única de respuesta única: buscar letra sola en el texto
    if not resps and n_q == 1 and int(preguntas[0].get('multiple') or 1) == 1:
        n_op = len(preguntas[0].get('opciones') or [])
        hi_u, hi_l = chr(64 + n_op), chr(96 + n_op)
        m = re.search(rf'^\s*([A-{hi_u}a-{hi_l}])[.)\s\n]', text, re.MULTILINE)
        if not m:
            m = re.search(rf'\b([A-{hi_u}a-{hi_l}])\b', text)
        if m:
            resps['0'] = m.group(1).upper()
    return resps

def _ask_persona(a, preguntas):
    """Envía las preguntas a una Persona. Usa Groq si hay clave, si no Claude Haiku."""
    n = len(preguntas)
    def _ks(p):
        return max(1, int(p.get('multiple') or 1))
    ejemplo = '\n'.join(
        f"{i+1}:{','.join(chr(66 + (i+j) % 4) for j in range(_ks(p)))}"
        for i, p in enumerate(preguntas)
    )
    lines = [
        'Encuesta. Responde como tú mismo/a.',
        f'Escribe SOLO esto (sin texto adicional):',
        ejemplo,
        '(sustituye cada letra por tu elección real)',
        '',
    ]
    for i, p in enumerate(preguntas):
        k = _ks(p)
        extra = f" (elige exactamente {k} opciones)" if k > 1 else ''
        lines.append(f"{i+1}. {p['texto']}{extra}")
        for j, op in enumerate(p['opciones']):
            lines.append(f"   {chr(65+j)}) {op}")
        lines.append('')
    lines.append('Tu respuesta (SOLO letras, formato N:X — o N:X,Y,Z si la pregunta pide varias):')

    user_msg  = '\n'.join(lines)
    max_tok   = max(60, sum(_ks(p) for p in preguntas) * 10)
    text      = ''

    if GROQ_API_KEY:
        # ── Groq (OpenAI-compatible, gratuito) ────────────────────────────────
        payload = {
            'model':      'llama-3.1-8b-instant',
            'max_tokens': max_tok,
            'messages': [
                {'role': 'system', 'content': build_system_prompt(a)},
                {'role': 'user',   'content': user_msg},
            ],
        }
        for attempt in range(8):
            status, data = http_json(
                'https://api.groq.com/openai/v1/chat/completions',
                method='POST', body=payload,
                headers={
                    'Authorization': f'Bearer {GROQ_API_KEY}',
                    'Content-Type':  'application/json',
                }
            )
            if status in (429, 500, 502, 503):   # rate limit / error transitorio → espera exponencial
                time.sleep(min(60, 2 ** attempt))
                continue
            if status == 200:
                text = data['choices'][0]['message']['content'].strip()
            break
    else:
        # ── Claude Haiku (fallback de pago) ────────────────────────────────────
        payload = {
            'model':      'claude-haiku-4-5-20251001',
            'max_tokens': max_tok,
            'system':     build_system_prompt(a),
            'messages':   [{'role': 'user', 'content': user_msg}],
        }
        status, data = http_json(
            'https://api.anthropic.com/v1/messages',
            method='POST', body=payload,
            headers={
                'x-api-key':         ANTHROPIC_API_KEY,
                'anthropic-version': '2023-06-01',
                'content-type':      'application/json',
            }
        )
        if status == 200:
            text = (data.get('content') or [{}])[0].get('text', '').strip()

    return _parse_survey_response(text, preguntas)

def _survey_worker(preguntas, subset=None):
    if subset is None:
        subset = agents
    total = len(subset)
    with _survey_lock:
        _survey.update({'running': True, 'done': 0, 'total': total,
                        'results': [], 'error': None, 'saved_file': None})

    def process(a):
        resps = _ask_persona(a, preguntas)
        return {
            'id':            a['id'],
            'nombre':        f"{a['nombre']} {a['apellidos']}",
            'provincia':     a.get('provincia', ''),
            'genero':        a.get('genero', ''),
            'grupo_edad':    a.get('grupo_edad', ''),
            'edad':          a.get('edad', 0),
            'voto':          a.get('voto_autonomicas_2024', ''),
            'euskera':       a.get('euskera', ''),
            'clase_social':  a.get('clase_social', ''),
            'nivel_estudios':a.get('nivel_estudios', ''),
            'resps':         resps,
        }

    # max_workers bajo: la capa gratuita de Groq limita ~30 req/min;
    # con 20 hilos la mayoría de peticiones caían por rate-limit (429).
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        futs = [ex.submit(process, a) for a in subset]
        for fut in concurrent.futures.as_completed(futs):
            try:
                row = fut.result()
            except Exception as e:
                row = None
                print(f'[encuesta] ⚠ error en una Persona: {e}')
            with _survey_lock:
                if row is not None:
                    _survey['results'].append(row)
                _survey['done'] += 1

    with _survey_lock:
        _survey['running'] = False
        _save_survey_to_disk()
    print(f'[encuesta] completada: {_survey["done"]}/{total} Personas')

def _save_survey_to_disk():
    """Guarda la encuesta terminada en resultados/ (llamar con _survey_lock adquirido)."""
    if not _survey['results']:
        return
    ts = time.strftime('%Y-%m-%d_%H%M%S')
    fname = f'encuesta_{ts}.json'
    data = {
        'fecha':      time.strftime('%Y-%m-%d %H:%M:%S'),
        'modelo':     'groq/llama-3.1-8b-instant' if GROQ_API_KEY else 'claude-haiku-4-5',
        'definition': _survey['definition'],
        'total':      _survey['total'],
        'done':       _survey['done'],
        'results':    _survey['results'],
    }
    try:
        path = RESULTS_DIR / fname
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
        _survey['saved_file'] = fname
        print(f'[encuesta] resultados guardados en resultados/{fname}')
    except Exception as e:
        print(f'[encuesta] ⚠ no se pudieron guardar los resultados: {e}')

_SAFE_FNAME = re.compile(r'^encuesta_[\w\-]+\.json$')

def _list_saved_surveys():
    """Lista las encuestas guardadas en resultados/, la más reciente primero."""
    items = []
    for f in sorted(RESULTS_DIR.glob('encuesta_*.json'), reverse=True):
        try:
            d = json.loads(f.read_text(encoding='utf-8'))
            defn = d.get('definition') or []
            items.append({
                'archivo':    f.name,
                'fecha':      d.get('fecha', ''),
                'modelo':     d.get('modelo', ''),
                'n_personas': len(d.get('results') or []),
                'n_preguntas': len(defn),
                'primera_pregunta': (defn[0].get('texto', '') if defn else '')[:120],
            })
        except Exception:
            continue
    return items

# ── Request handler ────────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_err(self, status, msg):
        self.send_json({'error': msg}, status)

    def read_body(self):
        n = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(n)) if n else {}

    def serve_static(self, filepath, ctype='text/html'):
        full = PUBLIC_DIR / filepath
        if not full.exists():
            return self.send_err(404, 'File not found')
        content = full.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', ctype + '; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, fmt, *args):
        pass  # silencia logs de acceso

    # ── GET ────────────────────────────────────────────────────────────────────
    def do_GET(self):
        p = self.path.split('?')[0]

        if p in ('/', '/index.html'):
            self.serve_static('index.html')

        elif p == '/livekit.js':
            local = PUBLIC_DIR / 'livekit-client.umd.min.js'
            if not local.exists():
                print('Descargando LiveKit SDK...')
                try:
                    req = urllib.request.Request(
                        'https://cdn.jsdelivr.net/npm/livekit-client@2/dist/livekit-client.umd.min.js',
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )
                    with urllib.request.urlopen(req) as r:
                        local.write_bytes(r.read())
                    print(f'LiveKit SDK guardado ({local.stat().st_size//1024} KB)')
                except Exception as e:
                    self.send_err(500, f'No se pudo descargar LiveKit SDK: {e}')
                    return
            content = local.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        elif p == '/api/agentes':
            lite = [{'id': a['id'],
                     'nombre': a['nombre'] + ' ' + a['apellidos'],
                     'edad': a['edad'], 'genero': a['genero'],
                     'provincia': a['provincia'],
                     'voto': a['voto_autonomicas_2024']} for a in agents]
            self.send_json(lite)

        elif p.startswith('/api/agentes/'):
            try:
                aid = int(p.rsplit('/', 1)[-1])
            except ValueError:
                return self.send_err(400, 'ID inválido')
            a = find_agent(aid)
            self.send_json(a) if a else self.send_err(404, 'No encontrado')

        # Debug — muestra clave cargada y test de avatares
        elif p == '/api/debug':
            key = LIVEAVATAR_API_KEY
            key_preview = (key[:6] + '…' + key[-4:]) if len(key) > 10 else f'[{len(key)} chars]'
            status, data = http_json(
                'https://api.liveavatar.com/v1/avatars/public?page_size=3',
                headers=la_headers()
            )
            self.send_json({
                'key_preview': key_preview,
                'key_length': len(key),
                'avatars_status': status,
                'avatars_count': data.get('data', {}).get('count') if status == 200 else None,
                'avatars_error': data if status != 200 else None,
            })

        # LiveAvatar — listar avatares públicos
        elif p == '/api/liveavatar/avatars':
            status, data = http_json(
                'https://api.liveavatar.com/v1/avatars/public?page_size=50',
                headers=la_headers()
            )
            print(f'[avatares] status={status} count={data.get("data",{}).get("count","?")}')
            self.send_json(data, status)

        # Voces disponibles (propias del usuario en LiveAvatar)
        elif p == '/api/liveavatar/voices':
            result = []

            # Voces custom del usuario (las que crea él mismo)
            for vtype in ('custom', 'private', 'user'):
                s, d = http_json(
                    f'https://api.liveavatar.com/v1/voices?voice_type={vtype}&page_size=50',
                    headers=la_headers()
                )
                print(f'[voces type={vtype}] status={s} raw={json.dumps(d)[:200]}')
                if s == 200:
                    items = (d.get('data') or {}).get('results') or []
                    for v in items:
                        result.append({
                            'voice_id': v.get('id') or v.get('voice_id'),
                            'name':     v.get('name', 'Sin nombre'),
                            'gender':   v.get('gender', ''),
                            'provider': 'LiveAvatar (tuya)',
                            'language': v.get('language', ''),
                        })

            # Si no hay voces propias, mostrar todas las públicas sin filtro de idioma
            if not result:
                s, d = http_json(
                    'https://api.liveavatar.com/v1/voices?voice_type=public&page_size=100',
                    headers=la_headers()
                )
                if s == 200:
                    items = (d.get('data') or {}).get('results') or []
                    for v in items:
                        result.append({
                            'voice_id': v.get('id') or v.get('voice_id'),
                            'name':     v.get('name', ''),
                            'gender':   v.get('gender', ''),
                            'provider': 'LiveAvatar',
                            'language': v.get('language', ''),
                        })

            print(f'[voces] total={len(result)}')
            self.send_json({'voices': result, 'total': len(result)})

        # Voice Agents del usuario (avatar + voz + contexto combinados)
        elif p == '/api/liveavatar/myavatars':
            status, data = http_json(
                'https://api.liveavatar.com/v1/voice-agents?page_size=50',
                headers=la_headers()
            )
            print(f'[voice agents] status={status} raw={json.dumps(data)[:400]}')
            self.send_json(data, status)

        # ── Encuesta ──────────────────────────────────────────────────────────
        elif p in ('/encuesta', '/encuesta.html'):
            self.serve_static('encuesta.html')

        elif p == '/api/encuesta/progreso':
            with _survey_lock:
                self.send_json({
                    'running':    _survey['running'],
                    'done':       _survey['done'],
                    'total':      _survey['total'],
                    'definition': _survey['definition'],
                })

        elif p == '/api/encuesta/debug':
            with _survey_lock:
                sample = _survey['results'][:5]
            self.send_json(sample)

        elif p == '/api/encuesta/resultados':
            with _survey_lock:
                self.send_json({
                    'running':    _survey['running'],
                    'done':       _survey['done'],
                    'total':      _survey['total'],
                    'definition': _survey['definition'],
                    'results':    _survey['results'],
                    'saved_file': _survey.get('saved_file'),
                })

        # Historial de encuestas guardadas en resultados/
        elif p == '/api/encuesta/historial':
            self.send_json(_list_saved_surveys())

        elif p.startswith('/api/encuesta/historial/'):
            fname = p.rsplit('/', 1)[-1]
            if not _SAFE_FNAME.match(fname):
                return self.send_err(400, 'Nombre de archivo inválido')
            f = RESULTS_DIR / fname
            if not f.exists():
                return self.send_err(404, 'Encuesta no encontrada')
            try:
                self.send_json(json.loads(f.read_text(encoding='utf-8')))
            except Exception as e:
                self.send_err(500, f'Error leyendo la encuesta: {e}')

        else:
            self.send_err(404, 'Ruta no encontrada')

    # ── POST ───────────────────────────────────────────────────────────────────
    def do_POST(self):
        p    = self.path.split('?')[0]
        body = self.read_body()

        # ── Claude ────────────────────────────────────────────────────────────
        if p == '/api/chat':
            agent = find_agent(body.get('agentId'))
            if not agent:
                return self.send_err(404, 'Agente no encontrado')
            payload = {
                'model':      'claude-opus-4-8',
                'max_tokens': 300,
                'system':     build_system_prompt(agent),
                'messages':   body.get('messages', []),
            }
            status, data = http_json(
                'https://api.anthropic.com/v1/messages',
                method='POST', body=payload,
                headers={
                    'x-api-key':         ANTHROPIC_API_KEY,
                    'anthropic-version': '2023-06-01',
                    'content-type':      'application/json',
                }
            )
            if status == 200:
                text = (data.get('content') or [{}])[0].get('text', '')
                self.send_json({'text': text})
            else:
                self.send_json(data, status)

        # ── LiveAvatar — paso 1: crear token de sesión ────────────────────────
        # Requiere avatar_id (UUID) del avatar elegido
        elif p == '/api/liveavatar/token':
            if body.get('voice_agent_id'):
                # Modo Voice Agent: avatar + voz + contexto definidos en LiveAvatar
                payload = {
                    'mode':        'FULL',
                    'is_sandbox':  False,
                    'voice_agent': {'voice_agent_id': body['voice_agent_id']},
                }
                print(f'[LiveAvatar token] mode=voice_agent  id={body["voice_agent_id"]}')
            else:
                # Modo avatar público con persona
                persona = {'language': 'es'}
                if body.get('voice_id'):
                    persona['voice_id'] = body['voice_id']
                payload = {
                    'mode':           'FULL',
                    'avatar_id':      body.get('avatar_id'),
                    'is_sandbox':     False,
                    'avatar_persona': persona,
                }
                print(f'[LiveAvatar token] mode=avatar  id={body.get("avatar_id")}')
            status, data = http_json(
                'https://api.liveavatar.com/v1/sessions/token',
                method='POST', body=payload, headers=la_headers()
            )
            if status != 200:
                print(f'  response={json.dumps(data)}')
            self.send_json(data, status)

        # ── LiveAvatar — paso 2: iniciar sesión (Bearer = session_token) ──────
        # Devuelve livekit_url + livekit_client_token para conectar desde el browser
        elif p == '/api/liveavatar/session/start':
            status, data = http_json(
                'https://api.liveavatar.com/v1/sessions/start',
                method='POST', body={},
                headers=la_headers(body.get('session_token'))
            )
            print(f'[LiveAvatar start] status={status}')
            if status not in (200, 201):
                print(f'  response={json.dumps(data)}')
            self.send_json(data, status)

        # ── LiveAvatar — detener sesión ───────────────────────────────────────
        elif p == '/api/liveavatar/session/stop':
            session_id   = body.get('session_id')
            sess_token   = body.get('session_token')
            status, data = http_json(
                f'https://api.liveavatar.com/v1/sessions/{session_id}/stop',
                method='POST', body={},
                headers=la_headers(sess_token)
            )
            self.send_json(data, status)

        # ── Encuesta ──────────────────────────────────────────────────────────
        elif p == '/api/encuesta/iniciar':
            preguntas = body.get('preguntas', [])
            if not preguntas:
                return self.send_err(400, 'Sin preguntas')
            with _survey_lock:
                if _survey['running']:
                    return self.send_err(409, 'Encuesta en curso')
                _survey['definition'] = preguntas
            muestra = body.get('muestra')  # None = todas
            import random
            subset = random.sample(agents, min(muestra, len(agents))) if muestra else agents
            threading.Thread(target=_survey_worker, args=(preguntas, subset), daemon=True).start()
            print(f'[encuesta] iniciada: {len(preguntas)} pregunta(s), {len(subset)} Personas')
            self.send_json({'ok': True, 'total': len(subset)})

        else:
            self.send_err(404, 'Ruta no encontrada')

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if not LIVEAVATAR_API_KEY:
        print('⚠  HEYGEN_API_KEY (LiveAvatar) no configurada en .env')
    if not ANTHROPIC_API_KEY:
        print('⚠  ANTHROPIC_API_KEY no configurada en .env')
    if GROQ_API_KEY:
        print('✓  Encuestas usarán Groq (llama-3.1-8b-instant) — gratuito')
    else:
        print('   Encuestas usarán Claude Haiku (sin GROQ_API_KEY en .env)')

    server = HTTPServer(('', PORT), Handler)
    print(f'\n🎙  Pueblo Digital — Entrevistador  (LiveAvatar API)')
    print(f'   Abre en el navegador: http://localhost:{PORT}')
    print(f'   (Ctrl+C para detener)\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServidor detenido.')
