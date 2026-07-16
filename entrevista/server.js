require('dotenv').config();
const express = require('express');
const fetch   = require('node-fetch');
const path    = require('path');
const fs      = require('fs');

const app  = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// ── Load agent data ────────────────────────────────────────────────────────────
const AGENTS_PATH = path.join(__dirname, '..', 'pv_agentes.json');
let agentes = [];
try {
  const raw = fs.readFileSync(AGENTS_PATH, 'utf-8');
  agentes = JSON.parse(raw).poblacion;
  console.log(`✓ ${agentes.length} agentes cargados`);
} catch (e) {
  console.error('✗ No se pudo cargar pv_agentes.json:', e.message);
}

// ── Agent endpoints ────────────────────────────────────────────────────────────
app.get('/api/agentes', (req, res) => {
  const lite = agentes.map(a => ({
    id: a.id,
    nombre: a.nombre + ' ' + a.apellidos,
    edad: a.edad,
    genero: a.genero,
    provincia: a.provincia,
    voto: a.voto_autonomicas_2024,
  }));
  res.json(lite);
});

app.get('/api/agentes/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const a  = agentes.find(x => x.id === id);
  if (!a) return res.status(404).json({ error: 'No encontrado' });
  res.json(a);
});

// ── Build system prompt from agent ────────────────────────────────────────────
function buildSystemPrompt(a) {
  const ideol = a.ideologia_0_10!= null
    ? ` Ideología: ${a.ideologia_0_10}/10 (1=izq, 10=dcha).` : '';
  const nac = a.escala_nacionalismo_0_10 != null
    ? ` Sentimiento nacionalista vasco: ${a.escala_nacionalismo_0_10}/10.` : '';
  const probs = (a.principales_problemas || []).join(', ') || 'No especificados';

  let prompt = `Eres ${a.nombre} ${a.apellidos}, una persona que vive en ${a.provincia} (País Vasco). Tienes ${a.edad} años.

PERFIL PERSONAL:
- Género: ${a.genero}
- Estudios: ${a.nivel_estudios}
- Situación laboral: ${a.situacion_laboral}
- Clase social: ${a.clase_social}
- Religión: ${a.religion}
- Nacimiento: ${a.nacimiento}

PERFIL LINGÜÍSTICO:
- Competencia en euskera: ${a.euskera}
- Idioma preferido: ${a.lengua_encuesta}

PERFIL POLÍTICO:
- Voto autonómicas 2024: ${a.voto_autonomicas_2024}
- Preferencia territorial: ${a.preferencia_territorial}${ideol}${nac}
- Valoración de la economía vasca: ${a.valoracion_economia_pv}
- Valoración de la situación política: ${a.valoracion_politica_pv}
- Principales preocupaciones: ${probs}`;

  if (a.perfil_mediatico) {
    const m = a.perfil_mediatico;
    prompt += `\n\nPERFIL MEDIÁTICO:
- Medio principal noticias: ${m.medio_principal_noticias || 'N/D'}
- Redes sociales: ${(m.rrss_activas || []).join(', ') || 'Ninguna'}
- Confianza medios (TV/Radio/RRSS): ${m.confianza_medios?.television ?? '?'}/${m.confianza_medios?.radio ?? '?'}/${m.confianza_medios?.rrss ?? '?'} (0-10)
- Interés política: ${m.interes_politica || 'N/D'}`;
  }

  if (a.perfil_bienestar) {
    const b = a.perfil_bienestar;
    prompt += `\n\nPERFIL DE BIENESTAR:
- Salud autopercibida: ${b.salud_autopercibida}
- Estado emocional: ${b.estado_emocional}
- Satisfacción vital (0-10): ${b.satisfaccion_vida_0_10 ?? 'N/D'}
- Control de la propia vida (0-10): ${b.control_vida_0_10 ?? 'N/D'}
- Satisfacción relaciones (0-10): ${b.satisfaccion_relaciones_0_10 ?? 'N/D'}
- Situación económica personal (0-10): ${b.satisfaccion_ahorro_0_10 ?? 'N/D'}
- Actividad física: ${b.actividad_fisica}
- Sentimiento de soledad: ${b.frecuencia_soledad}
- Contacto social: ${b.contacto_social}
- Preocupación cambio climático: ${b.preocupacion_clima}
- Sentido de pertenencia: ${b.sentido_pertenencia}
- Cultura presente en su vida: ${b.cultura_presente_en_vida}`;
  }

  prompt += `\n\nINSTRUCCIONES DE RESPUESTA:
- Responde SIEMPRE en primera persona como ${a.nombre}, con el lenguaje propio de tu perfil.
- Las respuestas son para ser HABLADAS por un avatar. Usa lenguaje oral, sin listas ni formatos.
- Sé BREVE: máximo 3-4 frases por respuesta.
- Muestra matices y posibles contradicciones como una persona real.
- Si la pregunta es en castellano, responde en castellano. Si es en euskera, responde en euskera.`;

  return prompt;
}

// ── Claude API proxy ───────────────────────────────────────────────────────────
app.post('/api/chat', async (req, res) => {
  const { agentId, messages } = req.body;
  const agent = agentes.find(a => a.id === agentId);
  if (!agent) return res.status(404).json({ error: 'Agente no encontrado' });

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key':         process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
        'content-type':      'application/json',
      },
      body: JSON.stringify({
        model:      'claude-opus-4-8',
        max_tokens: 300,
        system:     buildSystemPrompt(agent),
        messages:   messages,
      }),
    });
    const data = await response.json();
    if (!response.ok) return res.status(response.status).json(data);
    const text = data.content?.[0]?.text || '';
    res.json({ text });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// ── HeyGen proxy ───────────────────────────────────────────────────────────────
const HG_BASE = 'https://api.heygen.com';

async function hgFetch(path, method, body, token) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  } else {
    headers['x-api-key'] = process.env.HEYGEN_API_KEY;
  }
  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);
  return fetch(`${HG_BASE}${path}`, opts);
}

// Get streaming token
app.post('/api/heygen/token', async (req, res) => {
  try {
    const r    = await hgFetch('/v1/streaming.create_token', 'POST', {});
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// List available avatars
app.get('/api/heygen/avatars', async (req, res) => {
  try {
    const r    = await hgFetch('/v2/avatars', 'GET', null);
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// New streaming session
app.post('/api/heygen/session/new', async (req, res) => {
  const { token, avatar_name, quality } = req.body;
  try {
    const r = await hgFetch('/v1/streaming.new', 'POST', {
      quality:        quality || 'medium',
      avatar_name:    avatar_name || 'Anna_public_3_20240108',
      voice:          { rate: 1.0, emotion: 'Friendly' },
      video_encoding: 'H264',
      version:        'v2',
    }, token);
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// Start session (send WebRTC answer SDP)
app.post('/api/heygen/session/start', async (req, res) => {
  const { token, session_id, sdp } = req.body;
  try {
    const r    = await hgFetch('/v1/streaming.start', 'POST', { session_id, sdp }, token);
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// Send ICE candidate
app.post('/api/heygen/session/ice', async (req, res) => {
  const { token, session_id, candidate } = req.body;
  try {
    const r    = await hgFetch('/v1/streaming.ice', 'POST', { session_id, candidate }, token);
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// Make avatar speak
app.post('/api/heygen/session/task', async (req, res) => {
  const { token, session_id, text } = req.body;
  try {
    const r    = await hgFetch('/v1/streaming.task', 'POST',
      { session_id, text, task_type: 'talk' }, token);
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// Stop session
app.post('/api/heygen/session/stop', async (req, res) => {
  const { token, session_id } = req.body;
  try {
    const r    = await hgFetch('/v1/streaming.stop', 'POST', { session_id }, token);
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// ── Start ──────────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`\n🎙  Pueblo Digital — Entrevistador`);
  console.log(`   http://localhost:${PORT}\n`);
  if (!process.env.HEYGEN_API_KEY)    console.warn('⚠  HEYGEN_API_KEY no configurada');
  if (!process.env.ANTHROPIC_API_KEY) console.warn('⚠  ANTHROPIC_API_KEY no configurada');
});
