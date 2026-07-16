# Pueblo Digital — Bitácora de sesiones

> Registro cronológico de trabajo (más reciente arriba). Cada sesión con Claude, en cualquier ordenador, debe terminar añadiendo una entrada aquí: fecha, ordenador, qué se hizo y decisiones tomadas. Así ambos ordenadores comparten el mismo contexto.

---

## 2026-07-07 · Casa (cierre de sesión — David sigue en la oficina)

**Para continuar en la oficina:** relanzar la encuesta Deustobarómetro con el servidor corregido — pasos exactos en la sección "PRÓXIMO PASO INMEDIATO" de `CLAUDE.md`. Después, pedir a Claude el contraste con la muestra completa.

**Hecho:**
- Encuesta de validación frente al **Deustobarómetro verano 2026** definida (5 preguntas elegidas por David desde el informe PDF): situación económica actual, expectativa a 1 año, priorizar autóctonos en recursos públicos, vivienda a 10 años, y 3 miedos globales (selección múltiple). Guardada en `entrevista/encuesta_deustobarometro.json` con los datos reales de contraste documentados abajo.
- **Motor de encuesta ampliado a selección múltiple**: preguntas con `"multiple": k` (elegir k opciones, hasta 15 opciones por pregunta, formato de respuesta `N:X,Y,Z`). Cambios en `server.py` (prompt + parser, testado) y `encuesta.html` (selector "elegir k" por pregunta, gráficos con % sobre Personas que responden).
- Datos reales Deustobarómetro para el contraste: P1 economía (3,9/43,0/42,5/6,7/2,5/1,4) · P2 en un año (Mejor 7,5/Igual 66,9/Peor 21,5/NS 4,2) · P3 priorizar autóctonos (19,4/33,1/22,1/18,6/NS 6,8) · P4 vivienda 10 años (3,8/15,0/38,1/33,0/NS 10,1) · P5 miedos top: guerras 45,0, precios 36,4, ideas antidemocráticas 33,1, inseguridad 32,8, clima 26,8.
- Configurada la continuidad entre ordenadores: creado `CLAUDE.md` (contexto para Claude) y esta bitácora.
- Añadida **persistencia de encuestas** en `entrevista/server.py`: cada encuesta completada se guarda automáticamente en `entrevista/resultados/encuesta_<fecha>.json` (sincroniza vía OneDrive → los resultados viajan entre ordenadores).
- Nuevos endpoints: `GET /api/encuesta/historial` (lista encuestas guardadas) y `GET /api/encuesta/historial/<archivo>` (carga una).
- `encuesta.html`: nueva sección "📁 Encuestas guardadas" en la vista de diseño; al hacer clic se reabren los resultados con filtros y gráficos. La barra lateral de resultados indica qué encuesta se está viendo.

**Decisiones:**
- Los resultados de encuesta se guardan como JSON legible en `entrevista/resultados/` (no base de datos), para que OneDrive los sincronice sin fricciones.
- Las conversaciones de Claude/Cowork NO se sincronizan entre ordenadores → el contexto compartido vive en `CLAUDE.md` (estado) y `bitacora.md` (historial).

- **Primera pasada de la encuesta de validación lanzada y contrastada** (`contraste_deustobarometro.md`): quedó mermada por el rate-limit de Groq (solo n≈70-92 útiles de 1.000; 20 hilos eran demasiados). Diagnóstico preliminar: dirección de opinión correcta pero mala calibración (evita extremos, sesgo pesimista en expectativas) y fuerte sesgo de saliencia en miedos (clima +48 pp por anclaje al perfil, guerras −43 pp). Servidor corregido: 3 hilos, reintentos hasta 60 s ante 429/5xx. **Pendiente: relanzar la encuesta** (45-90 min) y rehacer el contraste con n≈1.000.

**Limpieza:**
- Eliminados los archivos del prototipo anterior "Arretxea" (`arretxea_agentes.json`, `panel_arretxea.html`, `prompts_arretxea.md`).

**Perdido / pendiente:**
- La encuesta lanzada hoy en la oficina (1.000 Personas vía Groq) se guardó solo en memoria del servidor → no recuperable. Relanzarla si interesa: con la persistencia nueva ya quedará registrada.

---

## 2026-07-07 · Oficina (reconstruida a posteriori)

- Generado el panel de 1.000 Personas (`pv_agentes.json`) con 100% de emparejamiento a 4 variables con la Encuesta de Bienestar.
- Panel HTML interactivo (`panel_pais_vasco.html`).
- App de entrevista con avatar (`entrevista/server.py`, versión Python stdlib; sustituye a `server.js`).
- Página de encuestas (`entrevista/public/encuesta.html`) con Groq (llama-3.1-8b-instant); lanzada una encuesta a 1.000 Personas (resultados no persistidos).
- Revisión de literatura (`literatura_relacionada.md`) y documento metodológico (`resumen_construccion_panel.md`).
