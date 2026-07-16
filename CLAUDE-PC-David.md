# Pueblo Digital — Contexto del proyecto

> **Propósito de este archivo:** dar contexto a Claude (Cowork/Claude Code) en cualquier ordenador.
> La carpeta se sincroniza vía OneDrive entre el ordenador de la oficina y el de casa.
> **Mantener actualizado:** al terminar una sesión de trabajo, actualizar la sección "Estado actual y próximos pasos".

## Qué es el proyecto

Pueblo Digital es un **panel sintético de 1.000 Personas** representativas de la población del País Vasco. Cada Persona se construye a partir de microdatos reales de encuestas oficiales (Barómetro político de Euskadi, Encuesta de Bienestar Personal 2025 de Eustat) y puede instanciarse como agente LLM que responde de forma coherente con su perfil sociodemográfico, político, mediático y de bienestar. Fundamento metodológico: "silicon sampling" (Argyle et al. 2023).

Detalle completo de la metodología en `resumen_construccion_panel.md` (muestreo estratificado, post-estratificación, emparejamiento estadístico k-NN por celda lurral × sexo × edad_g × eus_g).

## Estructura de la carpeta

| Ruta | Contenido |
|---|---|
| `pv_agentes.json` | Las 1.000 Personas del panel País Vasco (datos completos) |
| `panel_pais_vasco.html` | Panel interactivo autocontenido (filtros, perfiles, prompts) |
| `resumen_construccion_panel.md` | Documento metodológico: cómo se construyó el panel |
| `literatura_relacionada.md` | Revisión de literatura académica (silicon sampling, agentes generativos, sesgos) |
| `entrevista/` | App web de entrevista con avatar: `server.py` (Python stdlib, versión actual) + `public/`. Claude responde como la Persona; LiveAvatar (HeyGen) la verbaliza vía LiveKit. Claves en `entrevista/.env` (no commitear/compartir) |
| `datos GV/` | Datos fuente del Gobierno Vasco / Eustat (CSV medios 2025, bienestar) |
| `artículos/` | PDFs de la literatura (Argyle et al., datos sintéticos en marketing, etc.) |
| `Informe+Deustobarómetro+verano+2026.pdf` | Referencia Deustobarómetro |
| `Resultado1.spv` | Salida SPSS |

## Estado actual y próximos pasos

**Última actualización: 2026-07-07 noche** (sesión en casa; David continúa en la oficina)

Hecho:
- Panel de 1.000 Personas generado y validado (100% emparejamiento a 4 variables con la Encuesta de Bienestar).
- Panel HTML interactivo funcional (`panel_pais_vasco.html`).
- App de entrevista con avatar operativa (`entrevista/server.py`).
- Revisión de literatura redactada (`literatura_relacionada.md`).
- Persistencia de encuestas: cada encuesta completada se guarda en `entrevista/resultados/` (JSON) y puede reabrirse desde `encuesta.html` ("Encuestas guardadas"). Los resultados sincronizan vía OneDrive.
- Motor de encuesta con selección múltiple (`"multiple": k` en la definición, hasta 15 opciones, respuesta `N:X,Y,Z`).
- Encuesta de validación vs. Deustobarómetro verano 2026 definida (`entrevista/encuesta_deustobarometro.json`, 5 preguntas) y primera pasada contrastada (`contraste_deustobarometro.md`) — preliminar, n≈90 por rate-limit de Groq. Servidor ya corregido (3 hilos, reintentos hasta 60 s).
- `bitacora.md`: registro de sesiones — **añadir una entrada al terminar cada sesión de trabajo**.

**PRÓXIMO PASO INMEDIATO (en cualquier ordenador):**
1. `cd entrevista` y `python server.py` (versión con las correcciones — sincroniza por OneDrive).
2. En otra terminal: `curl -X POST http://localhost:3000/api/encuesta/iniciar -H "Content-Type: application/json" -d @encuesta_deustobarometro.json`
3. Esperar 45-90 min (evitar suspensión del equipo: `powercfg /change standby-timeout-ac 0`). Progreso en `http://localhost:3000/encuesta`.
4. Pedir a Claude que rehaga el contraste con la muestra completa (los datos reales del Deustobarómetro están en `contraste_deustobarometro.md` y en la bitácora).

Líneas pendientes:
- Rehacer contraste Deustobarómetro con n≈1.000; si se confirman los sesgos, repetir con Claude Haiku (quitar GROQ_API_KEY del .env) para separar sesgo del modelo pequeño vs. sesgo del método.
- Validación de distribuciones del panel frente a resultados reales (electorales 2024).
- Evaluación de fidelidad/sesgos (ver Qu 2024, Santurkar 2025, Guo 2025 en la literatura; primeros indicios en `contraste_deustobarometro.md`).
- Redacción de artículo académico a partir de la metodología, la literatura y el contraste.

## Convenciones de trabajo

- Idioma de trabajo y documentos: **español**.
- David es el autor (Universidad de Deusto, druiz@deusto.es).
- Documentación en Markdown en la raíz de la carpeta; datos fuente en `datos GV/`; PDFs académicos en `artículos/`.
- OneDrive puede mantener archivos "solo en la nube": si un script falla al leer un archivo, probablemente no está descargado localmente en ese ordenador.
