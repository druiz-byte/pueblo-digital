# Migración de la app de entrevista a Anam + emparejamiento automático

Objetivo doble de esta sesión:
1. **Que no haya que elegir el avatar a mano**: la cara y la voz se asignan solas al perfil de la Persona.
2. **Que la cara refleje mejor el perfil**: se pasa de LiveAvatar (galería fija, caras poco representativas) a **Anam**, que genera un avatar desde **una sola foto**.

## Cómo funciona el emparejamiento (sin API, ya probado sobre las 1.000)

`emparejar.py` mapea cada Persona a una **celda demográfica** (género × franja de edad) y a una **voz** (idioma × género). Es determinista: dentro de una celda con varias caras, la Persona recibe siempre la misma (`id mod nº_caras`), así no salen todas idénticas pero es reproducible.

Franjas de edad: **18-30 · 31-50 · 51-65 · 66+**. Géneros: **h / m / x** (No binario). Idiomas: **cas / eus** (según `lengua_encuesta`).

Reparto real del panel (probado con `python emparejar.py`):

| Celda | Personas | | Voz | Personas |
|---|--:|---|---|--:|
| h_18_30 | 114 | | cas_h | 422 |
| h_31_50 | 137 | | cas_m | 463 |
| h_51_65 | 122 | | cas_x | 10 |
| h_66_plus | 99 | | eus_h | 50 |
| m_18_30 | 83 | | eus_m | 53 |
| m_31_50 | 148 | | eus_x | 2 |
| m_51_65 | 158 | | | |
| m_66_plus | 127 | | | |
| x_* (No binario) | 12 | | | |

Las celdas `x_*` (solo 12 Personas) caen a la celda `m_*` de la misma edad si no tienen cara propia.

## Arquitectura (lo que cambia y lo que no)

- **El cerebro sigue siendo Claude.** El entrevistador escribe la pregunta → `/api/chat` genera la respuesta de la Persona (igual que ahora). Anam solo pone la cara y **habla** el texto con `anamClient.talk(reply)`. No se toca la lógica de la Persona ni el prompt v2.
- **El servidor mina el token de Anam.** `server_anam.py` expone `POST /api/anam/session {id}`: empareja la Persona, pide a Anam un *session token* efímero con `avatarId`+`voiceId` de esa celda y lo devuelve al navegador. La clave `ANAM_API_KEY` no sale del servidor.
- **Frontend nuevo y enfocado:** `public/anam.html` (ficha · avatar · chat). Se abre en `http://localhost:3000/anam?id=NN`. Sustituye el flujo LiveKit por el SDK de Anam (`https://esm.sh/@anam-ai/js-sdk`).

## Ficheros añadidos esta sesión

| Fichero | Qué es | Dónde corre |
|---|---|---|
| `emparejar.py` | Selector determinista Persona→cara+voz | Cualquiera (sin API) |
| `avatares_catalogo.json` | Celdas→avatarId y voces→voiceId | — |
| `anam_setup.py` | Crea avatares en Anam y rellena el catálogo | **PC de David** (necesita clave) |
| `server_anam.py` | Servidor v2 con `/api/anam/session` | PC de David |
| `public/anam.html` | Frontend de entrevista con Anam | Navegador |

## Checklist para David (en tu PC)

1. **Cuenta y clave.** Regístrate en https://anam.ai, crea una API key en el Lab y añádela a `entrevista/.env`:
   ```
   ANAM_API_KEY=...
   ```
   (Deja `ANTHROPIC_API_KEY` como está; ya no hace falta `HEYGEN_API_KEY`.)

2. **Voces.** `python anam_setup.py voces` lista las voces de tu organización. Elige voces **en castellano** (masc./fem.) en el Anam Lab —hay voces localizadas más allá de la galería inglesa por defecto— y pega sus `voiceId` en `avatares_catalogo.json → voces` (`cas_h`, `cas_m`). Los valores actuales son provisionales de la galería inglesa.

3. **Caras.** Prepara ~2-3 imágenes por celda (16-24 en total) siguiendo las specs de Cara 4: **cuadradas ≥1152×1152, fondo liso, expresión neutra, boca cerrada, cabeza+hombros, sin manos, <4.5 MB**. Nómbralas con el prefijo de la celda:
   ```
   m_66_plus__ana.png    h_18_30__jon.png    ...
   ```
   Luego: `python anam_setup.py crear <carpeta>` → sube cada cara a Anam y escribe los `avatarId` en el catálogo.
   *De dónde salen las caras:* generador de imágenes (rostros sintéticos, evita personas reales), fotos de stock con licencia, o —si prefieres no crear caras— usa la **galería stock** de Anam (`python anam_setup.py avatares`) y pega esos IDs a mano en las celdas.

4. **Comprobación.** `python emparejar.py` debe decir «Catálogo completo: todas las Personas tienen cara». Prueba una sesión real: `python anam_setup.py token 1`.

5. **Arranca.** `python server_anam.py` y abre `http://localhost:3000/anam?id=1`. El botón «Hablar con la Persona» conecta el avatar ya emparejado; escribe una pregunta y la Persona responde y la verbaliza.

6. **Enlace desde el panel.** En `index.html` (v2), cambia `ENTREVISTA_URL` para que apunte a `/anam?id=` en vez de `/?id=`.

## Avisos importantes

- **Crear avatares custom puede requerir plan de pago superior en Anam** (la API devuelve `403 Requires enterprise plan` en algunos planes). Si te pasa, `anam_setup.py crear` te avisa. Alternativa sin coste extra: usar la **galería stock** de Anam, que ya es diversa en edad/género, y mapearla a las celdas. Confirma tu plan antes de generar las 20 caras.
- **Euskera (105 Personas):** Anam probablemente no tiene voz nativa en euskera. De momento el catálogo enruta esas Personas a una voz provisional y marca `tts_externo` (p.ej. `azure:eu-ES-AinhoaNeural`). **Fase 2**: usar el modo *audio passthrough* de Anam (generación de cara con audio pregenerado) alimentado por Azure/Google TTS en euskera. Requiere sintetizar el audio en el servidor antes de enviarlo; no está implementado aún.
- **La API de Anam no es accesible desde el sandbox de Claude** (igual que Anthropic): todo lo que llama a `api.anam.ai` se ejecuta en tu PC.
- **Coste orientativo Anam:** desde ~12 $/mes + ~0,12 $/min de sesión (verifica en su web, cambia).

## Si quieres quedarte en LiveAvatar

El emparejamiento (`emparejar.py` + `avatares_catalogo.json`) es **independiente del proveedor**. Poniendo en el catálogo `avatarId`/`voiceId` de LiveAvatar en vez de Anam, la misma lógica auto-selecciona sin cambiar de proveedor. Lo montamos sobre Anam porque era la opción que elegiste por fidelidad de las caras.
