# Pueblo Digital — Bitácora de sesiones

> Registro cronológico de trabajo (más reciente arriba). Cada sesión con Claude, en cualquier ordenador, debe terminar añadiendo una entrada aquí: fecha, ordenador, qué se hizo y decisiones tomadas. Así ambos ordenadores comparten el mismo contexto.

---

## 2026-07-16 · Novena sesión — App de entrevista: vista enfocada desde el panel + fix de datos v2

**Ordenador:** oficina (Cowork). Entrevista servida en el PC de David.

**Contexto:** David quería que al pulsar "Entrevistar" en el panel (`index.html`, que es el **v2**) la Persona seleccionada se arrastre a la app de entrevista sin volver a elegirla, y que esa página muestre solo esa Persona (ficha · avatar · conversación).

**Hecho:**
- **Configurado el enlace del botón Entrevistar:** en `index.html` (raíz) `ENTREVISTA_URL` pasó del placeholder `https://TU-APP.onrender.com` a `http://localhost:3000` (uso local; para acceso remoto habría que desplegar en Render y cambiar esa línea).
- **Bug de datos detectado y resuelto:** el panel raíz es el **v2** (`id=1` → Julen Otxoa) pero `server.py` carga `pv_agentes.json` (**v1**, `id=1` → Jone Zubizarreta) → con el mismo `id` salía otra Persona. **Solución: arrancar `entrevista/server_v2.py`** (carga `pv_agentes_v2.json` + `build_system_prompt_v2`), así los `id` coinciden y arrastra la Persona correcta. `server_v2.py` reutiliza todo el frontend y el motor de `server.py`.
- **Modo enfocado en `entrevista/public/index.html`:** al llegar con `?id=NN` se añade `body.focus` → se ocultan el buscador y la lista, y a la izquierda queda **solo la ficha** de esa Persona (izquierda) · avatar (centro) · transcripción (derecha). Sin `?id` la app sigue mostrando buscador + lista como antes (funciona standalone).
- **Ficha enriquecida** con los campos v2 agrupados por secciones: Perfil, Política (ideología, nacionalismo, identidad, interés, valoraciones PV), Bienestar (felicidad, satisfacción, salud, contacto, soledad), Confianza y sociedad (perfil_social), Medios. Los campos vacíos se descartan.
- **Botón de conexión** renombrado `▶ Conectar avatar` → **`🎙 Hablar con la Persona`** y movido de abajo del todo a **arriba a la izquierda**, encima de la ficha (nuevo `#connect-bar`, visible al seleccionar Persona).

**Decisiones:**
- El servidor de entrevista a usar de aquí en adelante es **`server_v2.py`** (no `server.py`), para que coincida con el panel v2.
- Cambios acotados al frontend `public/index.html`; sin tocar el backend ni el flujo de LiveAvatar/LiveKit.

---

## 2026-07-15 · Octava sesión — Piloto PPI++ sobre datos reales (bloque política)

**Ordenador:** oficina (sandbox Claude) + generación LLM en el PC de David.

**Contexto:** revisión de tres papers subidos por David (market research/AAE de Wang et al. 2412.19363; una cita sobre ANES con 30 réplicas por encuestado; y PPI de Angelopoulos et al. 2301.09633). Se decidió montar un **piloto de Prediction-Powered Inference (PPI++)** sobre el bloque de política, para pasar de "el panel sustituye la encuesta" (sesgado) a "el panel aumenta la encuesta con garantías".

**Hecho:**
- **Microdatos reales por fin disponibles:** David subió el SPSS del Deustobarómetro verano 2026 (n=1.000, 248 vars). Convertido a `predictores_deusto.csv` (perfiles) y usado como gold-standard `Y`. Copia del `.sav` en la raíz del proyecto.
- **Motor PPI++** `piloto_ppi/ppi_engine.py` (proporciones y medias, lib `ppi-python`, power-tuning con `lam=None`). Validado con Monte Carlo (`selftest_ppi.py`): cobertura ~95%, sesgo ~0, imputación ingenua sesgada.
- **Piloto sustituto (sin API)** `piloto_final.py` + `construir_pred.py`: predicción = panel v2 emparejado por voto×ideología×sexo. Halla que la sustitución ingenua se equivoca hasta 43 p.p. en p18 ("Regular" real 43,5% vs panel 0,1%); PPI++ válido y adaptativo (gana donde el panel informa: Gob Vasco corr +0,28, dem. Euskadi +0,22; se repliega al clásico donde no: Gob Central, partidos).
- **Piloto generativo (con API, PC de David, 300 encuestados)** `generar_predicciones_deusto.py` + `true_ppi.py`: una Persona por encuestado real, **sin inyectar las variables objetivo** (anti-circularidad), emparejada 1:1 con `Y`. Mejora la señal: Gob Vasco corr **+0,42** (vs +0,28), ~9% reducción de IC a n=50 (~20% ahorro de datos). p18 y Gob Central siguen siendo de protección (muy sesgados). Sin injección, el LLM colapsa p18 en "Regular" 86%.
- **Informe + figuras** en `piloto_ppi/` (`informe_piloto_ppi_politica.md`, `piloto_ppi_politica.png`, `piloto_ppi_generativo.png`).

**Decisiones:**
- El proyecto tiene ahora evidencia empírica (datos reales) de las tres tesis: la sustitución ingenua sesga decenas de p.p.; PPI++ da estimaciones válidas siempre; la predicción generativa mejora la eficiencia donde el panel capta señal. Material central para metodología + discusión del artículo.
- Cerrado aquí a petición de David. Pendiente opcional: generar los 1.000 (más N no etiquetado = más ahorro), extender a otros bloques y probar PPI para coeficientes de regresión; añadir PPI/AAE a `literatura_relacionada.md`.

**Infra:** la API de Anthropic NO es accesible desde el sandbox de Claude (proxy → 401 `text/plain` "Unauthorized", sin cabeceras Anthropic). No confundir con clave inválida: la generación se lanza siempre en el PC de David. Además, `generar_predicciones_deusto.py` se reescribió para leer el CSV (sin `pyreadstat`) porque el Python de David no lo tenía.

---

## 2026-07-14 · Séptima sesión — Panel v2: ancla en encuestado real + fuentes nuevas (mejora la predicción)

**Contexto:** partiendo del diagnóstico de que el panel v1 era un "Frankenstein" de 3 encuestas unidas por solo 4 llaves (coherencia rota entre bloques), se rediseñó el panel anclando cada Persona en un encuestado real e inyectando los bloques con más llaves.

**Hecho:**
- **Análisis de fuentes.** Comparadas ESS, Sociómetro Vasco, CIS, Euskobarómetro, EUSTAT (Capital Social, ECV, Bienestar Personal, Sociedad de la Información) → `fuentes_datos_panel.md` (inventario + matriz de llaves verificadas + estrategia de emparejamiento) y `descargar_fuentes.py`. Reseña del artículo comercial de Qualtrics (taxonomía wrapper/ML/fundacional) en `literatura_relacionada.md` §7. Cuestionario del barómetro por bloques en `barometro_preguntas_por_bloques.md`.
- **Microdatos descargados y perfilados:** `Datos ESS/` (España, 21.296×2.747, PV=671; trae los 4 dominios), `Datos sociómetro GobEsp/` (SV83, 3.030×80, codebook en el .sav), `datos capital social 2022/` (ECS 2022, 5.798×57, índices 0-10; sin educación como llave).
- **Panel v2 construido** (`construir_panel_v2.py` → `pv_agentes_v2.json`): ancla = Sociómetro 83 (remuestreo ponderado por `wt`, opción B); inyección ESS (medios+bienestar, kNN 5 llaves, 969/1000) e inyección Capital Social (confianza/redes/participación, kNN 4 llaves, 1000/1000). Voto = recuerdo 2020 (P23) con respaldo intención 2024 (P21). Esquema compatible con el lanzador + bloque nuevo `perfil_social`.
- **Validación previa sin API:** la coherencia entre bloques mejora (ideología×interés política, que en v1 salía plana 34/34/38, en v2 ya diferencia; confianza en políticos y participación gradúan con la ideología).
- **Barómetro v2 lanzado a 1.000** (`lanzar_barometro_v2.py` + `prompt_v2.py`). **Contraste (2026-07-14): DAM global 14,0 p.p.** (143 preg.) vs 16,7 de la v1. Por bloque: B5 política 10,0 (v1 11,8) · B2 bienestar/políticas 14,4 (17,9) · B1 económica 11,7 (10,8) · B3 miedos 18,7 (19,6) · B6 geopolítica 23,7 (25,8) · B4 turismo 26,9 (26,5). Mejoran 4/6 bloques.
- **Panel interactivo v2** `panel_pais_vasco_v2.html` (autocontenido: KPIs + gráficos agregados que se recalculan al filtrar + fichas por Persona + generación de prompt).
- **App de entrevista con avatar v2** `entrevista/server_v2.py` (reutiliza toda la maquinaria LiveAvatar/HeyGen de v1; sirve el panel v2 y usa `build_system_prompt_v2`; frontend sin cambios).

**Decisiones:**
- Ancla = Sociómetro (no el Deustobarómetro propio): usar el propio barómetro como ancla sería **circular** para un test de predicción (las Personas ya llevarían las respuestas). El Sociómetro es fuente independiente.
- Medios/bienestar adaptados a lo que ESS/Capital Social sí miden (el prompt cambia respecto a v1): comparación de *pipeline*, no de un solo factor.
- Voto anclado en recuerdo 2020 (voto realizado, más limpio) en vez de la intención 2024 (52% NS/NC en el SV83).

**Avisos para el artículo:**
- Comparación **no 100% limpia**: v1 (16,7) se midió con plantillas antiguas (91 preg.) y v2 con las oficiales (143 preg.). Falta relanzar el **panel v1 con las plantillas oficiales** para aislar la mejora del panel.
- ESS medios/bienestar se emparejan con toda España (PV=671) → estructura española, no específicamente vasca. Capital Social aporta índices 0-10, no ítems crudos. En v2 `principales_problemas` quedó vacío (no está en el ancla) → penaliza el B1.

**Incidencias:** el mount de OneDrive dio el corte habitual tras editar `construir_panel_v2.py` (bash veía el archivo truncado; disco OK); resuelto reescribiendo el fichero entero.

**Pendiente inmediato:** relanzar el **panel v1 con las plantillas oficiales** (contraste comparable a las mismas 143 preg.); añadir `principales_problemas` al ancla v2.

---

## 2026-07-09 · Sexta sesión — Cuestionario oficial reconstruido + experimentos (líderes, pregunta abierta)

**Hecho:**
- **DAM por pregunta**: tabla detallada (91 preguntas con DAM) → `entrevista/resultados/DAM_por_pregunta.md` y **Excel** `DAM_por_pregunta_Barometro_Digital.xlsx` (raíz; 2 hojas, medias por bloque con fórmulas, DAM coloreada; global 16,7 p.p.).
- **CUESTIONARIO OFICIAL RECONSTRUIDO** desde el PDF de tablas por educación (`Educación+Deustobarómetro+verano+2026 (1).pdf`, 106 págs). David avisó de que las preguntas previas no eran exactas. Extraídas las **46 preguntas (p1–p46) = 152 ítems** con texto, opciones y % real (columna Total) mediante parser línea-a-línea robusto (validado: 0 avisos, 1172/1172 opciones emparejan con su dato real, sumas ~100%). Novedades frente a la versión anterior: **p4 situación laboral** (faltaba), **p29_1 "violencia nunca justificable"**, y **p40–p46 sociodemográficas** como Bloque 7 de validación. Escritas 7 plantillas nuevas en `entrevista/encuestas/barometro_digital_1..7.json` (antiguas en `encuestas/_backup_pre_oficial_2026-07-09/`). `cuestionario_barometro_digital.html` regenerado (51 preguntas/baterías, 152 ítems, 7 bloques). **Pendiente: relanzar el barómetro completo con estas plantillas.**
- **Experimento líderes/Gobierno** (2 preguntas propias, fuera del barómetro): `lanzar_extra.py` + plantillas `extra_lideres_gobierno_2026-07-09.json` (sin partidos) y `..._conpartidos_...` (P1 con partido entre paréntesis). Lanzadas ambas a 1.000. **Hallazgo (comparado con el dato real que pasó David):** sin partido, 64% "No sé"; con partido baja al 24% y el voto predice al líder casi determinista (PNV→Pradales 98, Bildu→Otxandiano 100...). Frente al **real**: nuestro panel (a) **sub-reporta el "No sé"** (24% vs ~51% real), (b) **pierde el atractivo transversal de Pradales** (real: hasta el PSE lo prefiere 28 vs Andueza 18; nosotros hacemos emparejamiento mecánico de partido), y (c) mantiene **sesgo normativo contra Vox y Sumar** (Martínez/Hernández ~0 aun entre sus votantes; real Vox→Martínez 22). Análisis en `entrevista/resultados/extra_lideres_comparacion_2026-07-09.md`.
- **Pregunta ABIERTA** "tres problemas de Euskadi": `lanzar_abierta.py` (texto libre, guarda respuestas) + `codificar_abierta.py` (codificación por palabras clave, multi-respuesta, % de personas por categoría, umbral 10%, con euskera y variantes económicas). Lanzada a 1.000 (0 vacías). Resultado (≥10%): **Vivienda 51,8 · Económicos 47,0 · Sanidad 44,9 · Trabajo 34,8 · Delincuencia 24,1 · Inmigración 19,4** (NS 0, sin codificar 1,5%). En abierto reproduce bien la jerarquía real de la p1 cerrada (vivienda/sanidad/económicos/delincuencia/inmigración encajan) pero **infla empleo y algo sanidad**.
- **Tabla de ranking por subgrupo** (réplica del formato de la imagen del Deustobarómetro): `ranking_problemas_por_subgrupo.png` (figura para el artículo) + `.html` (interactivo con % al pasar el ratón). Filas = 5 problemas (excl. económicos, para igualar la imagen), columnas = Total/Territorio/Sexo/Edad/Situación laboral/Escala izda-dcha/Voto, celdas = 1.º/2.º/3.º. Gradiente ideológico claro (Vox→Inmigración 1º, PP→Delincuencia 1º, jóvenes/parados→Trabajo 1º, ≥65→Vivienda/Sanidad).

**Decisiones:**
- Cuestionario reconstruido en 6 bloques temáticos + 1 de perfil/validación (p40–p46 incluidas para test de consistencia LLM vs. atributo real).
- P1 de líderes: dos versiones (sin/con partido) para aislar el efecto del anclaje.
- Codificación de la abierta por reglas transparentes (no LLM), reproducibles para el método.
- Ranking replicado con 5 categorías (sin "Problemas económicos") para comparabilidad con la imagen real; queda pendiente decidir si se añade económicos como 6.ª fila.

**Observación para el artículo:** homogeneización de **registro lingüístico** en la abierta (casi todas empiezan "Bueno, mira…"): el modelo reproduce mejor *qué* dice la gente que la diversidad de *cómo* lo dice. Anotar como limitación.

**Pendiente inmediato:**
- Relanzar el barómetro completo (7 bloques oficiales) a las 1.000 y rehacer el contraste con `comparar_deustobarometro.py`.
- Decidir versión 5 vs 6 categorías del ranking; opcional tabla de % exactos por subgrupo.

---

## 2026-07-08 · Quinta sesión — Barómetro digital LANZADO (1.000) + contraste + PDF comparativo

**Hecho:**
- **Tanda completa del "Barómetro digital" lanzada** por David en su ordenador (Haiku, `claude-haiku-4-5`). Prueba previa de 20 OK (6 bloques, 20/20, firmas únicas 20/20 → sin colapso por homogeneización). Luego los 6 bloques a las 1.000 Personas, completos: `resultados/encuesta_2026-07-08_1814..182209.json` (uno por bloque, 1.000 cada uno).
- **Contraste vs. Deustobarómetro real** hecho por bloque (`resultados/contraste_bloque1..6.md`) y consolidado en `resultados/contraste_barometro_completo_2026-07-08.md`. **DAM media global 16,7 p.p.** sobre 91 preguntas con dato real (25 con fidelidad alta <10 p.p., 39 media, 27 baja). Por bloque: B1 economía 10,8 · B5 política 11,8 · B2 bienestar 17,9 · B3 miedos 19,6 · B6 geopolítica 25,8 · B4 turismo 26,5.
  - Confirma el patrón de la Tanda 1: fidelidad casi perfecta cuando la variable está en el perfil (situación política PV 0,4; económica 0,7; territorial 1,4; nacionalismo 1,4) y error alto en lo ajeno al perfil y en multi-respuesta (los 6 peores ítems son del Bloque 6, "aliados y enemigos", hasta 56,9 p.p.). Exceso de NS/NC en expectativas.
- **PDF comparativo página a página generado**: `Comparativa_Barometro_Digital_vs_Deustobarometro.pdf` (42 págs: portada + 41). Izquierda = página original del Deustobarómetro (render del PDF que David dejó con solo las preguntas a comparar); derecha = resultado del panel (solo nuestros %) replicando el tipo de gráfico. Datos en `resultados/_sintetico_por_pregunta.json`. Decisión de David: derecha solo con nuestros %, estilo réplica del original.
- **`panel_pais_vasco.html` retocado**: cabecera limpia y renombrada a "Barómetro Digital — País Vasco" (también `<title>`); subtítulo explicativo y fuente en cada una de las 5 cajitas; la leyenda de voto pasa a mostrar % sobre el total ponderado con 2 decimales. (Fuentes inferidas: Deustobarómetro para voto/territorial/problemas, EUSTAT 2021 para edad/euskera — David debe validarlas.)

**Decisiones:**
- Derecha del PDF comparativo: solo nuestros % + réplica del tipo de gráfico original (no se añadió % real ni DAM al lado; versión con DAM queda como opción futura para el artículo).

**Pendiente:**
- Validar las etiquetas de fuente del panel HTML.
- Posible versión del PDF con % real + DAM al lado para el artículo; colores semánticos en apiladas de impacto (guerra/Trump).
- Pregunta de intención de voto en generales; validación frente a resultados electorales 2024; redacción del artículo (los sesgos del contraste son el material central).

---

## 2026-07-08 · Cuarta sesión — "Barómetro digital": réplica completa del Deustobarómetro (lista para lanzar)

**Hecho:**
- **Cuestionario completo extraído del PDF** del Deustobarómetro verano 2026 (59 págs., pypdf + páginas ambiguas verificadas como imagen con pypdfium2): 141 ítems con sus % reales, desplegando todas las baterías. Las páginas 35 (confianza en 20 instituciones), 41 (partido más capacitado, 9 sub-preguntas × 8 partidos), 47 y 48 (escalas nacionalista e ideológica, distribución completa + medias de partidos) se leyeron del render visual porque el texto extraíble era ambiguo.
- **6 plantillas creadas** en `entrevista/encuestas/` (decisión de David: réplica completa, dividida en los 6 bloques del informe): `barometro_digital_1_situacion_economica.json` (25 pregs.), `_2_bienestar_politicas` (25), `_3_miedos` (6), `_4_turismo` (2), `_5_politica_democracia` (59), `_6_geopolitica` (24). Todas con `datos_reales` para el contraste; las baterías de solo-medias llevan `{"media_real": x}` (comparar medias, no distribución) y las preguntas con base condicionada (razón del cambio de viaje, inseguridad laboral) llevan `nota` explicando cómo recalcular.
- **`server.py`: soporte "hasta k"** para preguntas "marca todas las que consideres" (`"hasta": true` + `"multiple": k`): el prompt dice "elige hasta k opciones" y el ejemplo muestra 2 letras para no anclar al máximo. Las preguntas "exactamente k" siguen igual.
- **`entrevista/lanzar_barometro.py` creado**: lanza los 6 bloques en secuencia sin la web (`python lanzar_barometro.py`; `--muestra 50` para prueba; `3` para un solo bloque). Cada bloque se guarda como archivo propio en `resultados/` etiquetado con `plantilla` y `titulo`. Probado de punta a punta con API simulada (parseo, guardado, etiquetado y `comparar_deustobarometro.py` OK, incluidas multi-respuesta y "hasta").
- Validación automática: las claves de `datos_reales` de las 6 plantillas emparejan con sus opciones según la lógica de `comparar_deustobarometro.py` (0 fallos).

**Decisiones:**
- Alcance: réplica completa (~141 ítems desplegados) en 6 bloques; lanzar la tanda entera a las 1.000 Personas con Haiku.
- Las preguntas con base filtrada del informe se hacen a todo el panel añadiendo una opción "no aplica" ("No estoy trabajando actualmente" / "No he descartado ni modificado ningún viaje"); el contraste debe recalcular % excluyéndola.

**Pendiente (no ejecutable desde el sandbox de Claude — la API está bloqueada ahí):**
- **Lanzar en el ordenador de David**: `cd entrevista && python lanzar_barometro.py` (recomendado antes: `python lanzar_barometro.py --muestra 20`). Coste estimado ~15-20 $ y ~30-45 min (141 preguntas × 1.000 Personas ≈ 17M tokens de entrada; más que la Tanda 1 porque el cuestionario es ~30× más largo).
- Tras la tanda: correr `comparar_deustobarometro.py` por bloque (el lanzador imprime los comandos exactos).

---

## 2026-07-08 · Tercera sesión (tarde) — Tanda 1 válida con Haiku

**Hecho:**
- **Gemini descartado**: la clave estaba en un proyecto prepago sin crédito ("Your prepayment credits are depleted"); una clave nueva siguió dando 429 constantes (posiblemente creada en el mismo proyecto). Creado `entrevista/test_gemini.py` (diagnóstico: 1 llamada, muestra el error completo) — sin ejecutar aún.
- **Cambio a Claude Haiku** (`claude-haiku-4-5`): la `ANTHROPIC_API_KEY` del `.env` daba 401 → David creó clave nueva y comentó `GEMINI_API_KEY`/`GROQ_API_KEY`. Prueba de 50: perfecta (50/50, 0 vacías, 0 sin parsear, ~1 min).
- **Tanda 1 completa VÁLIDA**: 1.000 Personas, 5/5 preguntas respondidas por todas, 0 fallos de parseo → `resultados/encuesta_2026-07-08_132943.json`. Coste ~2 $, ~10 min.
- **Mejoras en `server.py`** (`_ask_persona` refactorizada con `_llamada()`):
  - Si la Persona responde en prosa, reintento automático con recordatorio estricto de formato (elimina los "sin parsear").
  - El backoff de 429 reconoce también el `retryDelay` de Gemini.
  - Los errores 5xx ahora se reintentan (antes la Persona se perdía con respuesta vacía).
- **`comparar_deustobarometro.py` generalizado**: ya no tiene datos hardcodeados; lee `datos_reales` de las plantillas `encuestas/*.json` emparejando preguntas por texto normalizado. Sirve para cualquier tanda. Corregido bug de emparejamiento parcial ("Buena" casaba con "Muy buena"); ahora prioridad: exacta > NS/NC > parcial.
- **Contraste Tanda 1 vs. Deustobarómetro** (n=1.000): `resultados/contraste_tanda1_2026-07-08.md`. DAM media 15,3 p.p. Hallazgos:
  - P1 economía: DAM 0,7 — casi perfecto (la variable está en el perfil de la Persona).
  - P2/P4: pesimismo sistemático (Peor 47,4% vs 21,5% real) y exceso de NS/NC (46,1% vs 10,1% en vivienda).
  - P3 (inmigración): evitación del extremo ("Muy de acuerdo" 0,3% vs 19,4%) y refugio en "No lo sé" (+23 p.p.) — deseabilidad social del LLM.
  - P5 miedos: sobreajuste al perfil (precios 99,5% de mención; clima 58,6%) y omisión de guerras (4,7% vs 45,0%). Homogeneización/pérdida de varianza.
- **PDF Deustobarómetro analizado completo** (59 págs., texto extraído): catalogados los 40 ítems del cuestionario con sus % reales. **Dato nuevo: distribución completa de "miedo a viajar"** = Mucho 3,0 / Bastante 17,9 / Poco 37,6 / Nada 28,0 / Nunca he tenido miedo 13,5 → falta volcarla en `deustobarometro_tanda2.json`.

**Decisiones:**
- Proveedor de encuestas: **Claude Haiku** (fiable, ~1,5-2 $ por tanda de 1.000, minutos en vez de horas). Gemini de pago costaría 4-10 $/tanda; no compensa.
- David pidió crear la encuesta **"Barometro digital"**: réplica exacta del cuestionario completo del Deustobarómetro. Quedó pendiente decidir el alcance: réplica completa (~100 ítems desplegando baterías), sin escalas de medias (~60), o solo preguntas simples (~25); y si dividirla en bloques temáticos (recomendado: 6 bloques = 6 plantillas) o una sola plantilla.
- Sesión interrumpida por David ("reiniciar todo") con esa decisión pendiente.

**Pendiente próxima sesión:**
1. **Crear "Barometro digital"**: decidir alcance y estructura (ver arriba) y construir la(s) plantilla(s) JSON en `entrevista/encuestas/` con `datos_reales` extraídos del PDF (texto ya extraíble con pypdf; catálogo de ítems en esta entrada).
2. Completar `deustobarometro_tanda2.json` con los % de miedo a viajar (arriba).
3. Tanda 2 (si sigue interesando tras el Barometro digital).
4. Pregunta de intención de voto en generales (pendiente desde la 2ª sesión).
5. Validación de distribuciones del panel frente a resultados electorales 2024 y redacción del artículo.

---

## 2026-07-08 · Segunda sesión (tarde)

**Hecho:**
- **App de entrevista** (`entrevista/server.py` + `public/index.html`):
  - Audio del avatar corregido (pista de audio LiveKit no se adjuntaba al DOM).
  - LiveKit SDK ahora se descarga y sirve localmente vía ruta `/livekit.js` (evita fallos de CDN).
  - Eliminado checkbox Sandbox (siempre `is_sandbox: false`).
  - Selector de voces en español añadido a la interfaz.
  - **Voice Agents**: el usuario tiene Voice Agents propios en LiveAvatar (Manuel Ibarra, Voz de Jone). Actualizado server.py para llamar a `/v1/voice-agents` y usar `voice_agent: {voice_agent_id}` en el token (modo distinto a `avatar_persona`).
- **Sistema de encuesta** ampliado (segunda implementación completa):
  - Runner paralelo con **Groq** (gratuito, `llama-3.1-8b-instant`).
  - Selector de muestra: 50/200/500/1.000 Personas.
  - Bug crítico de parseo resuelto: Llama no seguía formato `1:A`. Fix: prompt más explícito + parser con regex amplio que acepta `1:A`, `1. A`, `1) A`, letra sola como fallback.
  - Endpoint de debug `/api/encuesta/debug` para inspeccionar respuestas crudas.
- **Terminología fijada definitivamente**: los individuos sintéticos se llaman **Personas** (no "agentes"), guardado en memoria persistente.
- **Documentos nuevos**: `resumen_construccion_panel.md` (metodología) y `literatura_relacionada.md` (12 papers académicos).

**Decisiones:**
- Proveedor LLM para encuestas: Groq free (`llama-3.1-8b-instant`). Límite: 30 RPM y 500K tokens/día.
- El parseo de Groq/Llama estaba produciendo `resps: {}` en ~99% de casos → fix aplicado, pendiente verificar.

**Pendiente próxima sesión:**
1. Verificar parseo con muestra de 50 (lanzar encuesta, revisar `/api/encuesta/debug`).
2. Definir pregunta 2 sobre intención de voto en elecciones generales (el mensaje de David se cortó: "En las próximas elecciones generales, ¿a q...?").
3. Encuesta completa a 1.000 Personas cuando el parseo esté verificado.

---

## 2026-07-08 · Oficina

**Hecho:**
- **Plantillas de encuesta**: nueva carpeta `entrevista/encuestas/` — cualquier JSON ahí aparece en encuesta.html ("📋 Encuestas disponibles") y se carga en el diseñador con un clic. Endpoints nuevos: `GET /api/encuesta/plantillas` y `/api/encuesta/plantillas/<archivo>`.
- Creadas dos plantillas con datos reales de contraste incluidos (`datos_reales` por pregunta, solo documentación):
  - `deustobarometro_tanda1.json` — las 5 preguntas de la validación (economía, expectativa, autóctonos, vivienda, 3 miedos).
  - `deustobarometro_tanda2.json` — nueva tanda (economía a 1 año, autóctonos, ceder libertades por seguridad 5,6/21,6/35,5/29,4/NS 8,0, miedo a viajar). **INCOMPLETA: falta la 1ª pregunta (la imagen no llegó) y los % completos de miedo a viajar (solo Mucho: 3,0).**
- Lanzadas 2 pasadas completas de Tanda 1 (1.000 Personas, Groq free): `resultados/encuesta_2026-07-08_092109.json` y `_103930.json` — **INVÁLIDAS: ~99% de respuestas vacías.**
- **Diagnóstico** (confirmado con prueba de 50 y captura de errores): límites de Groq free — 6.000 tokens/min y 500.000 tokens/día; cada Persona consume ~1.200 tokens. 20 hilos saturaban el TPM y los reintentos se agotaban en silencio. Además, ~400 llamadas sí consumieron tokens pero solo ~23 Personas tienen respuestas → posible problema adicional de parseo de llama-3.1-8b (pendiente confirmar).
- **Arreglos en server.py**: errores de API visibles (`last_error` en `/api/encuesta/progreso` + consola), 4 hilos con Groq (20 con Haiku), reintentos que respetan el "try again in Xs" de la API (hasta 10), y captura del texto crudo cuando el parseo falla (`raw_sin_parsear` en resultados).
- Script de contraste con el Deustobarómetro preparado (aún sin datos válidos que contrastar).

**Decisiones:**
- Validación con **Groq free** (decisión de David). Límite real: ~400 Personas/día → opciones: muestra de 400 en un día, o 1.000 en 3 días (~330/día).
- Cupo diario de Groq agotado el 2026-07-08 → **próxima pasada: 2026-07-09 o después.**

**Ampliación (misma sesión, tarde):**
- `deustobarometro_tanda2.json` **completada** (5 preguntas): 1ª = situación económica actual (3,9/43,0/42,5/6,7/2,5/NS 1,4). Solo faltan los % reales de "miedo a viajar" (se conoce Mucho: 3,0).
- **Cambio de proveedor: Gemini** (decisión de David, tras agotar el cupo diario de Groq). server.py adaptado: endpoint OpenAI-compatible de Google, prioridad GEMINI_API_KEY > GROQ_API_KEY > Anthropic, modelo configurable `GEMINI_MODEL` (defecto `gemini-3.5-flash`), 3 hilos (free = 10 peticiones/min, 1.500/día → pasada completa en ~1h45), `reasoning_effort: low` con reintento sin él si el modelo no lo acepta. Clave añadida al `.env`; el servidor arranca con "✓ Encuestas usarán Gemini".
- Script de contraste copiado a `entrevista/comparar_deustobarometro.py`.

**Pendiente próxima sesión:**
1. **Prueba de 50 con Gemini** (quedó pendiente: la extensión de Chrome perdió la conexión y David reinició el equipo). Verificar en la prueba: que el modelo `gemini-3.5-flash` existe (si no, ajustar `GEMINI_MODEL` en `.env`; el error sale en `last_error` de `/api/encuesta/progreso`), tasa de parseo y campo `raw_sin_parsear`.
2. Si la prueba va bien → lanzar Tanda 1 completa (1.000, ~1h45) y después Tanda 2.
3. Contraste panel vs. Deustobarómetro con `entrevista/comparar_deustobarometro.py` (usa los `datos_reales` de las plantillas; ojo: el script tiene los datos de Tanda 1 hardcodeados, adaptarlo para Tanda 2).
4. Conseguir los % reales completos de "miedo a viajar" del PDF del Deustobarómetro.

---

## 2026-07-07 · Casa

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
