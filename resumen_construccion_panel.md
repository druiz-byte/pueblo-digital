# Pueblo Digital — Cómo hemos construido el panel sintético del País Vasco

## ¿Qué es Pueblo Digital?

Pueblo Digital es un panel sintético de 1.000 Personas que simulan ser la población del País Vasco. Cada Persona es un perfil estadísticamente representativo construido a partir de microdatos reales de encuestas oficiales, y puede ser instanciado como un agente LLM capaz de responder preguntas, expresar opiniones y comportarse de forma coherente con su perfil sociodemográfico, político, mediático y de bienestar.

---

## Fase 1 — Definición del esquema y fuentes de datos

El primer paso fue decidir qué variables caracterizarían a cada Persona y de dónde vendrían los datos.

### Fuentes de datos utilizadas

**Barómetro político de Euskadi (Eustat / Gobierno Vasco)**
El núcleo del panel. Es una encuesta de opinión pública con microdatos individuales que recoge variables sociodemográficas (edad, sexo, estudios, clase social, situación laboral, territorio, nacimiento, religión), lingüísticas (competencia en euskera, lengua preferida), políticas (voto en autonómicas 2024, preferencia territorial, ideología, valoración de la economía y la política vasca, problemas principales) y mediáticas (medio de información principal, redes sociales activas, confianza en medios, interés político).

**Encuesta de Bienestar Personal 2025 (Eustat)**
Encuesta específica sobre bienestar subjetivo que añadimos en una segunda fase mediante emparejamiento estadístico. Recoge salud autopercibida, estado emocional, satisfacción vital, control sobre la propia vida, satisfacción con relaciones sociales y situación económica, actividad física, soledad, contacto social, preocupación por el cambio climático, sentido de pertenencia y presencia de la cultura en la vida cotidiana.

**Resultados electorales de las autonómicas vascas 2024**
Usados para validar y calibrar la distribución de voto en el panel.

### Esquema de la Persona

Cada Persona tiene cuatro bloques de atributos:

- **Perfil sociodemográfico**: id, nombre, apellidos, edad, género, provincia, nivel de estudios, situación laboral, clase social, religión, lugar de nacimiento, euskera
- **Perfil político**: voto en autonómicas 2024, preferencia territorial, ideología (0–10), nacionalismo vasco (0–10), valoración de economía y política, principales preocupaciones
- **Perfil mediático**: medio principal de noticias, redes sociales activas, confianza en TV/radio/redes (0–10), interés político
- **Perfil de bienestar**: salud autopercibida, estado emocional, satisfacción vital (0–10), control de la vida (0–10), satisfacción con relaciones y ahorro, actividad física, frecuencia de soledad, contacto social, transporte habitual, preocupación por el clima, sentido de pertenencia, presencia de la cultura

---

## Fase 2 — Generación de las 1.000 Personas

Las Personas se generaron a partir de los microdatos del Barómetro, respetando las distribuciones reales de la encuesta. El proceso fue:

1. **Muestreo estratificado** por territorio (Álava, Gipuzkoa, Bizkaia), sexo, grupo de edad y competencia en euskera para que el panel reproduzca la estructura demográfica del País Vasco.
2. **Asignación de nombres** aleatorios culturalmente coherentes con el perfil lingüístico de cada Persona (más nombres vascos para los euskaldunes, nombres castellanos para los no vascos, etc.).
3. **Post-estratificación**: se calcularon pesos por territorio × competencia en euskera para corregir posibles desviaciones respecto a la distribución real de la población vasca.

El resultado es un fichero `pv_agentes.json` con las 1.000 Personas en formato JSON.

---

## Fase 3 — Enriquecimiento con datos de bienestar (emparejamiento estadístico)

Los datos de bienestar no estaban en el Barómetro, así que los incorporamos mediante **emparejamiento estadístico (statistical matching)** entre el Barómetro y la Encuesta de Bienestar Personal de Eustat.

### Variables de enlace (linking variables)

Se identificaron cuatro variables comunes a ambas encuestas que sirven como "llave" de emparejamiento:

| Variable | Descripción |
|----------|-------------|
| `lurral` | Territorio (Álava / Gipuzkoa / Bizkaia) |
| `sexo` | Género |
| `edad_g` | Grupo de edad (cuatro tramos) |
| `eus_g` | Competencia en euskera (dos categorías) |

### Método: k-NN por celda

Para cada Persona del panel se busca en la Encuesta de Bienestar la celda exacta que coincide en los cuatro valores (emparejamiento exacto 4-variable). Si no hay coincidencia exacta, se hace emparejamiento parcial con 3, 2 o 1 variable. El resultado fue:

- **100% de Personas con emparejamiento a 4 variables** (tras corregir un bug inicial que usaba el código de grupo de edad pre-codificado en vez de la edad exacta).

Los atributos de bienestar de la celda emparejada se asignan a la Persona, completando su perfil.

---

## Fase 4 — Panel HTML interactivo

Con las 1.000 Personas construidas, se desarrolló un panel HTML interactivo (`panel_pais_vasco.html`) que permite:

- **Explorar** el panel con filtros por provincia, género, edad, voto, euskera, estudios y clase social
- **Ver el perfil completo** de cada Persona en un modal: datos sociodemográficos, políticos, mediáticos y de bienestar
- **Consultar distribuciones** ponderadas de las principales variables del panel
- **Generar el prompt** de simulación de cada Persona con un solo clic (texto listo para usar con un LLM)

El panel es un fichero HTML autocontenido (2,3 MB) que incluye los datos de las 1.000 Personas en JSON inline — no requiere servidor ni base de datos.

---

## Fase 5 — Aplicación de entrevista con avatar

Como herramienta de demostración y exploración cualitativa, se construyó una aplicación web (`entrevista/`) que permite entrevistar a cualquier Persona del panel mediante un avatar animado que habla en tiempo real.

### Arquitectura

```
Navegador  ←→  Servidor Python (stdlib)  ←→  API de Anthropic (Claude)
                                          ←→  API de LiveAvatar (HeyGen)
                                               └→ LiveKit WebRTC (vídeo/audio)
```

- **Servidor**: Python puro (sin dependencias externas), sirve la interfaz y actúa como proxy de las APIs externas.
- **LLM**: Claude (Anthropic) recibe el perfil completo de la Persona como system prompt y genera respuestas en primera persona, en lenguaje oral, breves y coherentes con el perfil.
- **Avatar**: LiveAvatar (producto de HeyGen) proporciona un avatar animado en streaming vía WebRTC (protocolo LiveKit). El avatar habla el texto generado por Claude.
- **Voces**: LiveAvatar permite crear Voice Agents propios con voz clonada, que combinan avatar + voz + contexto en un solo elemento.

### Flujo de una entrevista

1. El usuario selecciona una Persona del panel y un Voice Agent de LiveAvatar.
2. La app crea una sesión de avatar (token → start → conexión LiveKit).
3. El usuario escribe una pregunta. Claude responde como la Persona.
4. La respuesta se envía al avatar via canal de datos LiveKit (`agent-control`), que la verbaliza en tiempo real.
5. La conversación queda transcrita en pantalla.

---

## Ficheros principales del proyecto

| Fichero | Descripción |
|---------|-------------|
| `pv_agentes.json` | Las 1.000 Personas en JSON (datos completos) |
| `panel_pais_vasco.html` | Panel interactivo autocontenido (2,3 MB) |
| `entrevista/server.py` | Servidor Python de la app de entrevista |
| `entrevista/public/index.html` | Interfaz web de la app de entrevista |
| `entrevista/.env` | Claves API (LiveAvatar + Anthropic) |
