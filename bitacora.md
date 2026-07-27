# Pueblo Digital — Bitácora de sesiones

> Registro cronológico de trabajo (más reciente arriba). Cada sesión con Claude, en cualquier ordenador, debe terminar añadiendo una entrada aquí: fecha, ordenador, qué se hizo y decisiones tomadas. Así ambos ordenadores comparten el mismo contexto.

---

## 2026-07-27 · Decimosexta sesión — Entrevista en euskera: Personas euskaldun responden en euskera (texto + voz nativa Azure)

**Ordenador:** oficina (Cowork). El despliegue y las pruebas con API (Anam/Anthropic/Azure) los hace David en su PC / en Render.

**Contexto:** cerrar la "fase 2" que quedó de la 15ª sesión — que las Personas euskaldun puedan entrevistarse en euskera, no solo en castellano. Petición de David en dos tiempos: primero solo el prompt, luego "hagamos ya todo esta vez" (entrada de voz + salida de voz).

**Decisiones (con David):**
- **Alcance:** ambos niveles euskaldun (`Euskaldun (habla bien)` 262 + `Euskaldun (habla bastante bien)` 141 = **403 Personas**), no solo el que nombró literalmente.
- **Cuándo:** euskera **solo si se les pregunta en euskera** (no siempre). Si preguntan en castellano, responden en castellano.
- **Voz de salida:** Azure TTS (única opción con euskera nativo entre los grandes).

**Hecho — prompt (`entrevista/prompt_v2.py`):** detección por substring (`euskaldun` + `habla bien`/`bastante bien`); las 403 reciben una instrucción lingüística reforzada (responder siempre en euskera con fluidez si preguntan en euskera, sin pasarse al castellano). El resto mantiene la regla original. Verificado el reparto = 262+141=403, sin tocar a las demás. Aplica a los tres flujos que usan `build_system_prompt_v2` (`server_anam.py`, `server_v2.py`, `lanzar_barometro_v2.py`).

**Hecho — frontend (`entrevista/public/anam.html`):**
- **Selector de idioma ES/EU** en el compositor; marca `EU ✓` + tooltip si la Persona es euskaldun. Dirige tanto el micro como la voz de salida del turno.
- **Entrada de voz:** el dictado Web Speech usa `eu-ES` cuando EU está activo (antes fijo `es-ES`). El reconocimiento en euskera lo hace Chrome en servidor, no depende de voces instaladas.
- **Salida de voz — cascada de 3 niveles** en turnos EU: se silencia la voz castellana del avatar (labios siguen moviéndose vía `talk()` mudo) y se locuta por (1) **Azure TTS** `/api/tts` (nativo), (2) `speechSynthesis` del navegador si hay voz `eu-*`, (3) respaldo a la voz del avatar (castellano). Autopresentación siempre en castellano.

**Hecho — Azure TTS (`entrevista/server_anam.py`):** `azure_tts()` + ruta `POST /api/tts` (body `{id, text}`); SSML a `https://<region>.tts.speech.microsoft.com/cognitiveservices/v1`, salida MP3. Voz por género de la Persona: `eu-ES-AinhoaNeural` (mujer) / `eu-ES-GorkaNeural` (hombre). Claves en `.env` (`AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION=westeurope`), documentadas en `.env.example` y `render.yaml` (key `sync:false`, región con valor).

**Investigación (WebSearch/verificación):**
- **Voces del Chrome de David comprobadas en vivo (Claude in Chrome):** 50 voces, **ninguna `eu-*`** → sin Azure, el euskera sonaría en castellano; por eso Azure es necesario, no opcional.
- **Azure Speech:** capa gratuita **F0 = 500K caracteres/mes** (≈1.500 respuestas), voces euskera incluidas. Error al crear el recurso "plan 'payg' can't be purchased using a free subscription" = el formulario se quedó en **S0**; hay que forzar **Free F0**.
- **ElevenLabs NO tiene euskera** (29 idiomas en Multilingual v2, 32 en Flash v2.5; euskera no está). **Google Cloud TTS tampoco.** Azure sí.

**Despliegue (David):** push a `main` (`git add -A` desde la raíz del repo, no desde `entrevista/`), `AZURE_SPEECH_KEY` añadida en Render → Environment (`AZURE_SPEECH_REGION` ya va con valor en el blueprint). Verificado el push en GitHub (backend + frontend correctos). **Confirmado por David: funciona end-to-end en Render** — Persona euskaldun en EU responde en euskera con voz nativa.

**Pendiente / opcional:** replicar `/api/tts` en `server_v2.py` (flujo LiveAvatar) por si se usa; hoy solo está en el flujo Anam, que es el activo.

---

## 2026-07-26 · Decimoquinta sesión — App de entrevista: emparejamiento automático de avatar y migración a Anam

**Ordenador:** oficina (Cowork). Sin API (Anam/Anthropic solo desde el PC de David).

**Contexto:** retomar la app de entrevista con avatares. Dos peticiones de David: (1) que la Persona se empareje sola con un avatar/voz sin tener que elegir a mano entre los perfiles, y (2) alternativas a LiveAvatar que reflejen mejor los perfiles.

**Decisiones (con David):** migrar a **Anam** (anam.ai) por fidelidad —genera avatar desde **una sola foto**, al contrario que LiveAvatar/Tavus que exigen 2-5 min de vídeo— y granularidad de cara **por celda género×edad** (no una cara por Persona).

**Investigación de alternativas (WebSearch):** LiveAvatar (actual, spin-off de HeyGen), Anam, Tavus CVI, D-ID, Simli. Distinción clave: **cara desde foto (Anam, D-ID) vs desde vídeo (LiveAvatar, Tavus)** → solo las primeras escalan a la diversidad del panel. Voz: ElevenLabs es lo mejor en castellano pero **no tiene euskera**; para las 105 Personas en euskera hará falta TTS externo (Azure `eu-ES`, Google, Narakeet) vía audio passthrough (fase 2).

**Arquitectura elegida:** el cerebro sigue siendo Claude (`/api/chat` genera la respuesta de la Persona); Anam solo pone la cara y la **habla** con `talk()`. El servidor mina el token de sesión de Anam con `ANAM_API_KEY` (no sale del navegador). Entrada por teclado (no STT), así que la migración es limpia.

**Hecho (todo en `entrevista/`):**
- **`emparejar.py`** — selector determinista Persona→(cara, voz). Celdas género×edad (bordes 30/50/65), voz idioma×género. Dentro de celda: `id mod nº_caras`. **Probado sobre las 1.000**: reparto correcto en 12 celdas, 0 Personas sin clasificar. Reparto de voz: cas_h 422 · cas_m 463 · cas_x 10 · eus_h 50 · eus_m 53 · eus_x 2.
- **`avatares_catalogo.json`** — celdas→[avatarId] y voces→voiceId (voces provisionales de la galería EN; caras vacías hasta que David las cree).
- **`anam_setup.py`** (PC de David) — subcomandos `voces` / `avatares` / `crear <carpeta>` / `token <id>`. `crear` sube una imagen por celda (nombre `celda__loquesea.png`) a `POST /v1/avatars` y rellena el catálogo. Avisa si Anam devuelve `403 Requires enterprise plan`.
- **`server_anam.py`** — como `server_v2.py` pero con `AnamHandler`: `POST /api/anam/session {id}` empareja y mina el token; sirve `anam.html` en `/anam`.
- **`public/anam.html`** — frontend enfocado (ficha · avatar · chat) con el SDK de Anam (`esm.sh/@anam-ai/js-sdk`): `createClient(token)` → `streamToVideoElement` → `talk(reply)`. Muestra la celda/voz emparejada en un badge.
- **`MIGRACION_ANAM.md`** — guía + checklist para David (cuenta/clave, voces castellano, ~16-24 caras Cara-4, comprobación, arranque, cambiar `ENTREVISTA_URL`).

**Avisos:** (a) crear avatares custom **puede requerir plan superior** en Anam (403); alternativa: galería stock. (b) **euskera** pendiente de fase 2 (audio passthrough con Azure/Google). (c) el emparejamiento es **independiente del proveedor**: sirve también para LiveAvatar rellenando el catálogo con sus IDs.

**PUESTA EN MARCHA — FUNCIONANDO END-TO-END (misma sesión, PC de David):**
- **Caras: galería stock de Anam** (David no tiene plan para crear custom desde foto, de momento). Se listaron con `anam_setup.py avatares` (10 disponibles) y se mapearon a las 8 celdas: Hunter→h_18_30/h_31_50 · Finn→h_31_50 · Gabriel→h_51_65/h_66_plus · Sophie→m_18_30 · Mia/Liv/Bella→m_31_50 · Anne/Julia→m_51_65 · Julia(canas)→m_66_plus. El digital twin de David se deja fuera. Limitación conocida: la galería tira a **adulto profesional 30-55**, poca cara joven/mayor real → motivo para crear caras propias más adelante.
- **Voces: castellano nativo de Anam.** Las 10 voces por defecto eran inglesas (acento americano). David añadió desde el Lab voces en español y pasó sus IDs. Cableadas en el catálogo con **rotación por id** (como las caras): mujeres **Nuria** `8f90e9ac-4fc0-11f1-84b0-52bacf74fa75` + **Blanca** `8f70d6bd-4fc0-11f1-84b0-52bacf74fa75`; hombres **Martin Osborne** `fbe2b6ee-a4df-4d6c-b51a-92be37c9517f` + **Daniel** `2d96e0ff-6667-4d7d-a908-f5e4d6ee0bcd`. Reparto sobre las 1.000: Blanca 266 · Nuria 262 · Martin 243 · Daniel 229. `emparejar.py` ampliado para admitir una **lista** de voces por clave (además de un dict) y rotar.
- **Fix clave del error "Legacy session tokens":** el token de sesión necesita `personaConfig.llmId = "CUSTOMER_CLIENT_V1"` para desactivar el cerebro de Anam y dejar que responda Claude vía `talk()`. Añadido en `server_anam.py` y `anam_setup.py`. El frontend usa el evento `SESSION_READY` y fija el SDK a `@anam-ai/js-sdk@latest`.
- **Incidencia Anthropic:** la `ANTHROPIC_API_KEY` del `.env` daba 401 `authentication_error` (revocada). Se creó `test_anthropic.py` (prueba la clave sin dependencias). David generó clave nueva → chat OK.
- **Estado: la Persona se empareja sola con cara+voz castellana y conversa** (Claude de cerebro, Anam pone cara y voz). Confirmado por David.

**Enlace del panel + despliegue en Render (misma sesión):** el botón "Entrevistar" de `index.html` ahora abre `/anam?id=` (antes `/?id=`). Desplegado en Render: `render.yaml` y el Start Command del panel cambiados a `python server_anam.py`, variable `ANAM_API_KEY` añadida y `ANTHROPIC_API_KEY` actualizada a la clave nueva (la vieja daba 401 también en Render). **Funciona online** en `pueblo-digital.onrender.com/anam?id=NN` (plan free → duerme tras inactividad, primer arranque lento). Nota de flujo: Render no coge el `startCommand` del `render.yaml` si ya hay uno fijado en el panel → cambiarlo en Settings a mano.

**Incidencia git+OneDrive (resuelta):** `git` daba "not a git repository" pese a existir `.git` porque OneDrive tenía su contenido "solo en la nube" y OneDrive no corría. Solución: arrancar OneDrive + "Conservar siempre en este dispositivo". Git for Windows recién instalado → configurar identidad (`user.email`/`user.name`). Push necesitó `git pull --no-rebase --no-edit` (remoto por delante). Anotado en Convenciones del `CLAUDE.md`.

**Interfaz `anam.html` — responsive + pulido (HECHO esta sesión):**
- **Responsive:** móvil = ficha resumida (nombre·edad·provincia) arriba + avatar + chat abajo; escritorio = 3 columnas con **perfil detallado** (personal/lingüístico/político/mediático/bienestar/capital social, con los campos v2 de `/api/agentes/NN`). Gotcha detectado: en el móvil se veían 3 columnas porque Chrome tenía activado "Versión para ordenador" (fuerza viewport ancho); se desactiva en el menú del navegador.
- **Auto-presentación:** al conectar, la Persona se presenta sola (nombre, edad, de dónde es, a qué se dedica) vía `/api/chat` + `talk()`, sin esperar pregunta.
- **Voz:** micrófono con Web Speech API (`es-ES`); en móvil se quita el botón "Enviar" y el micro queda a la derecha; en escritorio se mantiene "Enviar".
- **Favicons:** micrófono azul (SVG inline) en la entrevista; globo azul en `index.html` (panel).
- **Concurrencia:** la sesión de Anam se cierra al salir/cerrar pestaña (`pagehide`/`beforeunload`) y `maxSessionLengthSeconds` para liberar el cupo. Error "Concurrency limit reached" = varias sesiones vivas a la vez; cerrar pestañas y esperar.
- **Fix scroll móvil:** la página tenía altura variable y hacía scroll global al responder (se perdía el avatar). Ahora `.app` con altura fija a la pantalla (`100dvh - head`) y `overflow:hidden`; **solo el chat** (`#transcript`) tiene scroll interno (con `min-height:0` en los flex). El avatar queda fijo.

**Plan de Anam contratado: Starter** ($12/mes, uso comercial): **50 min/mes gratis** (luego $0,16/min), **límite 5 min/conversación** (→ `maxSessionLengthSeconds=300` en `server_anam.py`), **2 avatares custom**. Cada prueba consume minutos del cupo.

**Pendiente:** (a) **euskera** fase 2 (audio passthrough con Azure `eu-ES`; ahora las 105 Personas usan voz castellana provisional). (b) **caras propias**: el plan Starter permite 2 avatares custom desde foto (insuficiente para las 8 celdas → se sigue con galería stock; reservar los 2 custom para casos concretos). (c) menor: la ficha resumida móvil solo lleva nombre·edad·provincia (David quería añadir campos pero el mensaje quedó cortado). (d) opcional: persona/avatar de David mismo (se le pasó un borrador de perfil en inglés; su "digital twin" ya está en la galería de Anam).

---

## 2026-07-20 · Decimocuarta sesión — El frente PPI++ se CIERRA: el perfil enriquecido no mueve la aguja y sabemos por qué (techo predictivo)

**Ordenador:** oficina (Cowork). Generación de las predicciones en el PC de David; todo el análisis en Cowork (sin API).

**Contexto:** ejecutar por fin el pendiente nº1 (tanda de 300 con perfil enriquecido) y medir si sube la correlación individual, que era el cuello de botella del PPI++.

**Hecho:**
- **Tanda de 300 relanzada y completada** (prueba de 3 → 300). `predicciones_deusto_full.json`: 300 encuestados, 285 con las 152 preguntas completas, 0 sin parsear. Verificado que `generar_predicciones_full.py` **guarda incrementalmente** (línea 122, tras cada bloque de cada encuestado) y es reanudable — el corte del 16-jul no se puede repetir.
- **Herramienta nueva `piloto_ppi/acuerdo_individual.py`** — mide el acuerdo a nivel de MICRODATO (persona real vs su gemelo digital), que hasta ahora solo existía para las escalas 0-10. Métrica según tipo, porque la distancia importa (un 7 real vs 8 predicho no es el mismo error que 7 vs 1): escalas 0-10 → exacto/±1/MAE/Spearman/kappa cuadrático; **cat ORDINAL** (48) → kappa ponderado + ±1; **cat NOMINAL** (41) → kappa de Cohen; multi (9) → Jaccard/F1. Dos decisiones críticas: (a) **baseline "predecir siempre la moda"** en todas —sin él, un 51% de acierto parece bueno cuando la moda sola da 56%—, y (b) **NS/NC excluido** de las métricas de distancia (en las 54 escalas es la opción L = índice 11; tratarlo como número metería un "11" en una escala 0-10). Reutiliza `arrays_pregunta` de `true_ppi_full.py`; stub de `ppi_py` para no exigir la librería.
- **Herramienta nueva `piloto_ppi/techo_predictivo.py`** — calcula el **TECHO de información**: regresa cada una de las 152 preguntas del `.sav` REAL sobre las variables que un perfil podría contener (sexo, edad, provincia, lengua, situación laboral, estudios, religión, nacimiento, voto 2024, voto 2020, ideología, nacionalismo; 68 columnas). R² **fuera de muestra**, validación cruzada 5-fold, ridge suave. `corr_max = sqrt(R²)` es el límite de CUALQUIER panel digital. No toca el panel: es una propiedad de los datos reales.

**RESULTADOS — los tres números que cierran el frente:**
1. **Techo (`techo_predictivo.md`): R² medio fuera de muestra 0,080 → corr máxima media 0,24.** Mediana 0,052; **14/100 preguntas con R² ≤ 0** (el perfil no predice NADA). Por bloque: economía 0,024 (corr máx 0,15) · bienestar 0,034 (0,16) · miedos 0,059 (0,21) · turismo 0,085 (0,29) · **política 0,099 (0,28, el mejor)** · perfil 0,371 (0,61, control). Nominales: un clasificador lineal saca +7,5 p.p. sobre la moda; multi solo +1,1.
2. **Tanda enriquecida vs perfil pobre — resultado NULO en lo esencial.** Umbrales fijados ANTES de mirar (éxito: corr ≥ 0,22, recorte IC ≥ 4%, delta vs moda ≥ 0):

   | métrica | perfil pobre | enriquecido | veredicto |
   |---|--:|--:|---|
   | Spearman escalas (54) | 0,15 | **0,15** | sin cambio |
   | kappa ordinales (48) | 0,101 | **0,100** | sin cambio |
   | kappa nominales (41) | 0,161 | **0,231** | mejora |
   | delta vs moda, nominales | −3,3 | **+1,6** | **cumple** |
   | delta vs moda, ordinales | −5,2 | −4,5 | sigue negativo |
   | recorte IC limpio (bloques 1-6) | 1,1% | **1,4%** | falla |
   | DAM global | 15,8 | **15,1** | marginal |
3. **El panel alcanza ~65% del techo.** Spearman 0,15 sobre un máximo de 0,24 → **el pipeline no está roto, choca contra un límite de información.** Aunque se construyera la Persona perfecta, el recorte del PPI sería corr² ≈ 6%, no el 30-40% que haría el método interesante.

**Diagnóstico:** los 3 campos nuevos aportan **solo donde son mecánicamente relevantes** y nada donde no. El caso ilustrativo: la correlación no circular más alta sube de 0,31 a **0,52** y es `p21_9 = confianza en la Iglesia Católica` — sube porque ahora se inyecta la religión. Señal real (por debajo del techo, no es bug) pero casi **tautológica**: el perfil predice bien lo que es una reformulación del propio perfil. Igual con voto 2020 → preguntas de partido (nominales, que son las que mejoran). El margen 0,17→0,24 existía sobre el papel pero requería variables con señal transversal, y estas no la tienen.

**Decisiones:**
- **NO escalar a los 1.000.** No es cuestión de dinero (~19 $): con corr 0,15 la ganancia del PPI va con corr² y el techo de recorte es ~2% **independientemente del N**. Solo tendría sentido si la correlación hubiera subido.
- **Frente PPI++/panel CERRADO.** El artículo pasa a tener una tesis explicada, no solo un resultado negativo: *la correlación máxima alcanzable desde un perfil sociodemográfico es 0,24 y nuestro panel alcanza el 65% de ese techo* — el límite es de información, no de modelo (ni de prompt, ni de encuestas donantes, ni de LLM frontera).
- **Distinción central para el paper** (fuente de toda la confusión previa): se puede clavar la distribución agregada sin acertar a **ninguna** persona. Si el 43% dice "Regular", repartir las respuestas al azar reproduce el histograma perfecto con acierto individual nulo. Por eso el DAM parecía razonable (economía 13,5) mientras el delta vs moda salía negativo. Son ejes ortogonales.

**Diseño propuesto para el artículo (discutido con David, "empezar de cero"):** benchmark de 3 métodos sobre las mismas 152 preguntas — imputación estadística clásica (hot-deck/kNN), Persona LLM, y LLM+PPI — contra 2 baselines tontos (moda y marginal). Evidencia a favor: en nominales el clasificador lineal saca +7,5 y el LLM +1,6 → **para preguntas imputables la estadística clásica gana al LLM**; el LLM solo debería reservarse para lo que ninguna encuesta donante cubre (turismo, geopolítica), que es justo donde peor sale (DAM 30,4 y 28,2). Cautela metodológica acordada: partir el fichero (mitad para selección de variables, mitad reservada como test) para no contaminar la validación.

**Limitación reconocida:** el techo se calcula con un modelo **lineal**; uno no lineal podría arañar algo más. Es cota razonable, no absoluta. Réplica prevista si un revisor lo pregunta: gradient boosting (se espera poco movimiento — 14 preguntas con R² ≤ 0 no es un problema de forma funcional).

**Infra:** el sandbox de Cowork corta los comandos a 45 s → los análisis largos se lanzan con `setsid nohup … > /tmp/log 2>&1 & disown` y se consultan después (el log **fuera** del mount de OneDrive; dentro del mount, nohup no escribe). Reaparece el desfase del mount: bash listó `predicciones_deusto_full.json` con tamaño y fecha obsoletos cuando el fichero ya había sido borrado; se contrasta con la herramienta de lectura/Glob, que ven el disco real. Ficheros solo-nube (`ppi_engine.py`, `.git/*`) dan `Invalid argument` en bash hasta que se leen una vez con la herramienta de lectura. Instalado `ppi-python` en el sandbox (ahora `true_ppi_full.py` corre en Cowork sin API).

**Ficheros nuevos:** `piloto_ppi/{acuerdo_individual.py, acuerdo_individual.md, acuerdo_individual.json, techo_predictivo.py, techo_predictivo.md, techo_predictivo.json}`. Regenerados: `predicciones_deusto_full.json` (300, perfil enriquecido) e `informe_ppi_full.md`.

**Pendiente:** `.sav` en formato ANCHO para SPSS (una fila por persona con `var_real` y `var_panel` en columnas, para crosstabs y kappa; la bandera `--sav` de `acuerdo_individual.py` está documentada pero **sin implementar** — el `comparacion_real_vs_panel.sav` actual está apilado y NO sirve para acuerdo individual).

---

## 2026-07-17 · Decimotercera sesión — Analítica web (GA4), rediseño de la app de encuestas y entrevista a Haiku

**Ordenador:** oficina (Cowork). Los `git push` y el arranque de la API los hizo David en su PC (el sandbox de Cowork no puede escribir en git; ver "Infra").

**Contexto:** mejorar la analítica de la web pública (`https://druiz-byte.github.io/pueblo-digital/`), rediseñar la página de diseño de encuestas y arreglar el error del chat de la entrevista.

**Analítica web (Google Analytics 4):**
- **Diagnóstico de la cuenta.** La web ya tenía GA4 (`G-4GQ86YD4FM`) y los eventos personalizados pegados por David (`abrir_persona`, `entrevistar_persona`, `lanzar_encuesta`, `generar_prompt`, `usar_filtro`, `limpiar_filtros`). El ID **no** estaba en la cuenta de Google con la que estaba abierto Chrome (esa solo tiene la propiedad "International Weeks", stream `G-TK9Y4XRVBP`, + la cuenta **demo** de GA con tráfico ficticio). El `G-4GQ86YD4FM` vive en **otra cuenta de Google de David** (propiedad "Pueblo Digital", `a6838353p545874210`, `authuser=1`).
- **Informe creado (Explorar → Formato libre):** filas = **País** anidado con **Nombre del evento**, valores = **Usuarios activos** + **Recuento de eventos**. En Tiempo real ya entran los eventos personalizados; en las Exploraciones tardan 24-48 h en procesarse, así que el informe se llena solo. Guardado en la propiedad Pueblo Digital.
- **Limpieza de `index.html`:** eliminado el bloque `<noscript>` de **Google Tag Manager (`GTM-K6Z7RF7G`)** que estaba a medias (sin el script de cabecera → no cargaba nada) y encima mal colocado dentro del `<style>`. GA4 intacto.

**Rediseño de la app de encuestas (`entrevista/public/encuesta.html`):**
- Vista de diseño reorganizada en **3 columnas**: izq. **"Diseña nueva encuesta"** (empieza con **una pregunta en blanco**, no el ejemplo de economía; incluye tamaño de muestra + Lanzar), centro **"Encuestas disponibles"** (plantillas), dcha. **"Resultados encuestas"** (antes "Encuestas guardadas"). Columnas siempre visibles (mensaje de vacío en vez de ocultarse); se apilan <900px.
- **Tema claro** replicando la paleta de `index.html` (`--verde:#00754a`, `--claro:#f4f7f6`, cabecera verde degradada, tarjetas blancas con sombra). Corregidos los colores de los ejes de Chart.js (el eje Y era casi blanco → invisible en claro).
- Quitado el botón **"🎙 Entrevista"** del header; añadido botón **"← Volver"** en la vista de resultados.
- No se tocó la lógica de lanzar/progreso/gráficos.

**Cabecera de `index.html`:** título **"Pueblo digital"** y subtítulo **"Analiza y revisa las personas que componen el pueblo digital"** (misma cabecera verde compartida con la app de encuestas). Botón "Lanzar encuesta" intacto.

**Entrevista con avatar — error del chat resuelto:**
- Síntoma: al preguntar, la Persona respondía `[Error: [object Object]]`. Doble causa: (1) el frontend hacía `throw new Error(objeto)` → aplastaba el error real; (2) el handler `/api/chat` usaba el modelo caro **`claude-opus-4-8`** (el resto del proyecto usa Haiku).
- Arreglos (en `entrevista/public/index.html` y `entrevista/server.py`): el frontend ahora **muestra el mensaje real** de Anthropic; el modelo del chat pasa a **`claude-haiku-4-5-20251001`**. (Quedan restos de Opus en `server.js` y `server-PC-David.py`, que NO se usan en Render.)
- Con el mensaje ya legible, el error real era el **límite de gasto de Anthropic**: *"You have reached your specified API usage limits. You will regain access on 2026-08-01 at 00:00 UTC."* Es el mismo tope que bloqueaba la generación PPI. **David amplió el límite a 200 USD en la consola → la entrevista ya funciona.**

**Push a GitHub (2 commits, hechos por David desde su PC):** `ec06825` "Cabecera Pueblo digital + rediseño encuesta (3 columnas, tema claro)" y `48806c8` "Entrevista: usar Haiku y mostrar el error real del chat". `index.html` lo publica GitHub Pages; `encuesta.html`/`server.py` los sirve Render (autoDeploy).

**Recordatorio de acceso:** la clave de las entrevistas es la variable `SITE_PASSWORD` (Basic Auth, `sync:false` en `render.yaml`) → se cambia en Render → Environment (online) o en `entrevista/.env` (local).

**Infra (importante para futuras sesiones):** el sandbox de Cowork, montado sobre OneDrive, **no puede escribir en git** — falla al crear/borrar `.git/index.lock` ("Operation not permitted"), así que **todos los `git push` los lanza David en su PC**. Técnica usada para subir limpio pese a ir "behind": `git reset --mixed origin/main` (apunta la rama a GitHub sin tocar los ficheros) y luego `add`/`commit`/`push`. Si aparece un `index.lock` huérfano (se sincroniza por OneDrive), borrarlo en el PC (`rm -f .git/index.lock`).

---

## 2026-07-16 · Duodécima sesión — PPI++: perfil de generación enriquecido (preparado para lanzar)

**Ordenador:** oficina (Cowork). La generación con API la lanzará David en su PC.

**Contexto:** cerrar el pendiente nº1 de la sesión anterior — subir la correlación individual del panel (~0,17, el cuello de botella del PPI) reenriqueciendo el perfil de generación con campos REALES del propio Deustobarómetro que no se usaban.

**Hecho (todo sin API, en Cowork):**
- **Decodificados 3 campos del `.sav`** (que no traen etiquetas de valor): **p41 religión**, **p42 nacimiento** (+`ccaa_otra`/`pais_otra` para el lugar concreto) y **p46 voto autonómicas 2020**. Códigos mapeados por posición a las opciones de `barometro_digital_7` y **verificados**: las frecuencias del `.sav` alinean 1:1 con los `datos_reales`, y el join por `id` se validó contra la columna `voto_autonomicas_2024` ya existente (p45 decodificado → 1000/1000 coinciden).
- **`predictores_deusto.csv` enriquecido** con las 3 columnas nuevas vía `piloto_ppi/enriquecer_predictores.py` (backup en `predictores_deusto_backup_pre_enriq.csv`). Cobertura: nacimiento 100%, religión 93,6% (resto NS/NC→N/D), voto 2020 100%. **David no necesita pyreadstat**: el CSV ya viaja por OneDrive.
- **`generar_predicciones_full.py`** ahora inyecta los 3 campos: `persona()` los lee del CSV y el wrapper `build_prompt_enriquecido` añade religión y voto 2020 al prompt (el nacimiento ya lo renderiza `build_system_prompt_v2`). No toca `prompt_v2.py` (compartido con la app de entrevista). **No circular para B1-B6**: solo el Bloque 7 pregunta por estos campos, y ese ya se trataba como validación. Smoke-test OK (el N/D de religión se omite; el detalle de CCAA aparece).
- **Predicciones viejas archivadas** en `predicciones_deusto_full_v1perfilpobre.json` para que la regeneración arranque limpia y poder comparar antes/después.

**Pendiente (David, con API):** `cd piloto_ppi && python generar_predicciones_full.py --muestra 300` → `python true_ppi_full.py`. Comparar la correlación del `informe_ppi_full.md` nuevo con el ~0,17 previo. Si sube (≈0,35+), plantear los 1.000; si no, reencuadrar el artículo con el resultado negativo. Pasos en `PASOS_ppi_full.md`.

**Herramientas nuevas para comparar en SPSS:**
- **`equivalencia_preguntas_panel_barometro.md`** (raíz): tabla de las 152 preguntas con el texto de la plantilla (lo que ve la Persona) junto a la variable + etiqueta del `.sav` original y el error de verificación por opción. Demuestra que se pregunta y codifica exactamente lo mismo (**152/152, error medio 0,58 p.p., máx 1,9**).
- **`piloto_ppi/predicciones_a_sav.py`**: convierte `predicciones_deusto_full.json` en dos `.sav` con el MISMO esquema, códigos y etiquetas que el original (reutiliza el crosswalk): `panel_predicho_<N>.sav` (solo panel) y `comparacion_real_vs_panel.sav` (2N filas con variable `fuente` 1=real / 2=panel, para segmentar en SPSS). Validado de punta a punta.

**Incidencia API + entregable parcial:** David lanzó los 300 pero la cuenta de Anthropic **tocó el límite de gasto de la organización** (400: "reached your API usage limits", se reabre el **1-ago-2026 00:00 UTC**). La generación se cortó y el JSON quedó truncado; se recuperaron **24 encuestados completos** (`piloto_ppi/predicciones_recuperadas_parcial.json`, recuperación por escaneo de llaves). Con ellos se generó **`piloto_ppi/doublecheck.sav`** (48 filas = 24 reales + 24 panel, variable `fuente`, esquema del original) a petición de David para comparar ya en SPSS. Señal preliminar (n=24, no concluyente): el perfil enriquecido **NO** rompe el colapso de p18 en "Regular" (panel 83% vs real 58%). Para completar: David metió una **clave API nueva** en `.env`; pasos de reinicio limpio dados (borrar el JSON corrupto → prueba `--muestra 3` → `--muestra 300`).

**Revisión de literatura — requisitos de un panel digital** (a petición de David, sobre `artículos/`): sintetizados de tres fuentes. (1) **Argyle et al., 4 criterios de fidelidad algorítmica**: Test de Turing social, continuidad hacia atrás (el perfil se infiere de las respuestas), continuidad hacia delante, y **correspondencia de patrones** (mantener las correlaciones internas, no solo la media) — este último es el más exigente y el cuello de botella del panel. (2) **Perils of LLMs**: el perfil DEBE incluir la variable política (omitirla dispara el error), el panel produce menos varianza y falla en relaciones condicionales individuales, y debe ser reproducible. (3) **MRS/AIA Council**: complemento no sustituto, explicabilidad, transparencia de procedencia, estándares de calidad y validación contra datos reales. Discutido con David por qué la política es el predictor de mayor densidad de señal — y la tensión con la circularidad (ideología/nacionalismo inyectados dan corr 0,82-0,96 pero no cuentan).

**Storyline del artículo enriquecido (David prepara el paper):**
- **Mov. 1 — explosión de la IA (cifras defendibles):** *AI Index 2025* → 149 modelos fundacionales en 2023 (2× 2022), ~90% de industria en 2024; cómputo de entrenamiento se duplica cada ~5 meses; coste 2,4×/año. Frontera: GPT-4 (23) → GPT-4o (24) → GPT-5/DeepSeek-R1 (25).
- **Qué modelo usó cada paper del corpus** (`artículos/`): Argyle=GPT-3; *perils*=GPT-3.5 Turbo (+GPT-4.0/Falcon40B robustez); Wang AAE=GPT-4o afinado; Park self-reports=GPT-4o; Yin *Synthetic but Not Infinite*=GPT-4o-mini; nosotros=Claude Haiku 4.5. (`2311.01453`=PPI++ sin LLM; `sjme`=bibliométrico.)
- **"Mejora" con modelos actuales — cálculo honesto:** salto bruto de capacidad grande (MMLU: GPT-3 ~44%, GPT-3.5 ~70% vs frontera ~91-92%), PERO la fidelidad NO sigue a la capacidad: el propio *perils* replicó con GPT-4.0 y los sesgos **persistieron** ("similar results"); el cuello de botella (corr ~0,17) es de anclaje/perfil, no de potencia. Conclusión para el paper: cambiar de modelo movería poco el DAM → propuesta de robustez: re-lanzar un subconjunto (p.ej. 100 del bloque político) con un modelo frontera y enseñar la **invariancia al modelo** del techo de fidelidad.
- **Test de Turing (Mov. 2):** Jones & Bergen — 2023 *Does GPT-4 pass…* (~50%), 2024 *People cannot distinguish GPT-4…* (54%), **2025 *LLMs Pass the Turing Test* (PNAS): GPT-4.5 con persona juzgado humano 73%** en test de 3 partes (primer sistema que lo pasa). Matiz clave para el artículo: pasar el Turing **conversacional** (parecer *un* humano, y solo con persona) ≠ fidelidad de panel (simular a *este* humano / la distribución) = criterios 2-4 de Argyle; nuestra corr ~0,17 lo demuestra.
- PENDIENTE: revisar los 2 PDFs sin abrir del todo, redactar Mov. 2 con las citas de Turing y añadirlas a `literatura_relacionada.md`; opcional, volcar el storyline a `draft_paper.docx`.

**Infra:** reaparece el corte del mount de OneDrive tras Edit/Write (bash ve `generar_predicciones_full.py` truncado en la línea 102, pero el disco está íntegro y correcto — verificado con la herramienta de lectura). No afecta a la ejecución en el PC de David. Los `.sav`/PDF solo-nube se descargan leyéndolos una vez con la herramienta de lectura; luego bash (pyreadstat/pdftotext) ya los ve.

---

## 2026-07-16 · Undécima sesión — PPI++ completo (152 preguntas): piloto con 300

**Ordenador:** oficina (Cowork) + generación LLM en el PC de David.

**Contexto:** extender el piloto PPI++ (que solo cubría 5 variables del bloque 5) a las **152 preguntas** de los 7 bloques, para tener por bloque "sustitución ingenua (DAM)" vs "PPI++ (recorte de IC / ahorro de datos)".

**Hecho:**
- **Crosswalk 152 preguntas ↔ variables del `.sav`** construido y **autoverificado sin API**: `piloto_ppi/build_crosswalk.py` → `crosswalk_ppi.json` + `crosswalk_cobertura.md`. Cada pregunta mapea a su variable (tipo cat/escala/multi, con las baterías resueltas: problemas→p1_1..p1_24, "no votarías"→p28_1..p28_8). Reconstruye el % real desde el `.sav` y lo compara con el `datos_reales` del template: **152/152, error medio 0,58 p.p.**
- **Generador ampliado** `piloto_ppi/generar_predicciones_full.py`: predice las 152 por cada encuestado real con SU perfil (solo 12 predictores, anti-circularidad), reanudable. **David generó los 300** → `predicciones_deusto_full.json` (300×152).
- **Evaluador PPI++ generalizado** `piloto_ppi/true_ppi_full.py` (motor `ppi_engine.py`): por pregunta calcula DAM ingenua (distribución, p.p.), recorte de IC, cobertura y correlación (escalas); agrega por bloque. Modo `--simular` para probar sin API. Informe → `informe_ppi_full.md`. **Bug corregido:** en escalas 0-10 la DAM ingenua se calculaba sobre la media (unidades 0-10) y se multiplicaba ×100 → inflaba bloques 2 y 5; ahora es DAM de distribución, comparable en p.p.

**Resultados (300, n etiquetado=100, 20 semillas) — informe en `piloto_ppi/informe_ppi_full.md`:**
- **Sustitución ingenua DAM global ~15,7 p.p.** (política 11,2 · bienestar 13,8 · economía 14,0 · miedos 16,9 · geopolítica 27,7 · turismo 30,8). Confirma de nuevo que el panel no sirve como sustituto.
- **PPI++ válido pero ganancia despreciable:** recorte de IC ~1,1% global limpio (~2% de ahorro de datos). Solo política asoma (recorte 1,9%).
- **Correlación individual muy baja:** ~0,17 incluso en el mejor grupo (las 20 escalas de "confianza en instituciones"). Como el recorte va con corr², el **techo es bajo aunque se amplíe a 1.000** — el problema no es el tamaño, es la correlación.
- **Las únicas correlaciones altas (0,82-0,96) son circulares:** ideología y nacionalismo, que se inyectan en el prompt. Validan que el motor PPI está bien (cuando el panel sabe, corr→1, recorte→34%), pero no cuentan.
- **Cobertura ~90%**, algo baja; probable artefacto de que los 300 son los primeros del fichero (no submuestra aleatoria) contrastados contra la "verdad" de los 1.000. Con los 1.000 desaparece.

**Decisiones / diagnóstico:** la palanca real es la **correlación**, no el N. La generación usó un perfil pobre (12 predictores, resto N/D). **Siguiente paso acordado:** reenriquecer el perfil con campos REALES del propio Deustobarómetro no usados aún — **p42 lugar de nacimiento** (+`ccaa_otra`/`pais_otra`), **p41 religión**, **p46 voto 2020** (David señaló que el lugar de nacimiento sí está en los datos; se confirmó: está en el `.sav`, no hay que imputarlo). Luego remedir con los 300 y ver si sube la correlación antes de decidir sobre los 1.000. Opcional posterior: bloques imputados medios/bienestar/social evitando los campos circulares (confianza institucional, soledad, seguridad, bienestar-objetivo).

**Ficheros nuevos:** `piloto_ppi/{build_crosswalk.py, crosswalk_ppi.json, crosswalk_cobertura.md, generar_predicciones_full.py, true_ppi_full.py, predicciones_deusto_full.json, informe_ppi_full.md}` y `PASOS_ppi_full.md` (raíz).

**Infra:** persiste el corte del mount de OneDrive tras Edit/Write (bash ve el `.py` truncado aunque el disco está bien); se resolvió ejecutando la lógica por heredoc. La generación LLM se lanza siempre en el PC de David (API bloqueada en el sandbox).

---

## 2026-07-16 · Décima sesión — Contraste limpio v1 vs v2: la mejora era de las plantillas, no del panel

**Ordenador:** oficina (Cowork) + tanda lanzada en el PC de David.

**Contexto:** cerrar el pendiente nº1. Hasta ahora la "mejora v2" (16,7 → 14,0) mezclaba dos cambios: el rediseño del panel **y** el cambio de plantillas (91 preg. viejas → 143/152 oficiales). Había que relanzar el **panel v1 con las mismas plantillas oficiales** que usó la v2 para aislar el efecto del panel.

**Hecho:**
- **Preparación:** verificado que `lanzar_barometro.py` ya carga el panel v1 (`pv_agentes.json`) + las 7 plantillas oficiales `barometro_digital_1..7` (152 preguntas, las mismas que la v2 del 14-jul). Escrito el agregador **`entrevista/contraste_v1_vs_v2.py`**: calcula DAM por bloque y global de dos tandas identificadas por fecha, con la **misma lógica** que `comparar_deustobarometro.py` (tomando por bloque la tanda completa n≥500 de cada fecha; ignora pruebas `--muestra`). Validado con autocontraste v2 vs v2 (Δ=0, reproduce los DAM por bloque documentados). Instrucciones en `PASOS_contraste_v1_oficial.md`.
- **Tanda v1 lanzada por David** (Haiku, 1.000 Personas, 7 bloques): `resultados/encuesta_2026-07-16_1200..1209.json`. Prueba previa de 20 OK; tanda completa con **0 vacías, 0 sin parsear** (huecos sueltos <1%: B5 242/60.000, B6 163/24.000). Confirmado que corrió sobre v1 (id 363 = *Eider*, no *Nahia* de v2).
- **Contraste (`resultados/contraste_v1_vs_v2.md`): DAM v1 = 13,4 vs v2 = 13,9 (Δ +0,4) sobre 152 preguntas.** Excluyendo el B7 de perfil: v1 = 13,8 vs v2 = 14,0. Por bloque (Δ = v2−v1): economía +0,3 · bienestar +1,4 · miedos +3,9 · turismo −3,5 (2 preg.) · política −0,1 · geopolítica −0,9 · perfil +3,3.

**Conclusión (importante para el artículo):**
- **La mejora 16,7 → 14,0 era el cambio de plantillas, no el panel.** Sobre las mismas preguntas la v1 es incluso marginalmente mejor que la v2. El ancla en encuestado real + más llaves (ESS España, Capital Social) **no reduce el DAM** frente al Deustobarómetro: el barómetro está dominado por variables políticas/económicas que la v1 ya capturaba (B5 política idéntico, 10,1), y la v2 empeora bienestar/miedos/perfil. La mejor coherencia interna de la v2 (validación sin API) no se traduce en mejor predicción.
- Es un hallazgo metodológico limpio: un confound de instrumento (plantillas) y la lección de que "más estructura ≠ mejor predicción" en este caso.

**Decisiones / pendiente:** decidir con David el rumbo del frente "panel" (mejorar v2 con ancla vasca real para medios/bienestar y `principales_problemas`; volver a v1 como base; o congelar el panel y centrar el artículo en PPI++ como método). Documentación (`CLAUDE.md`, esta bitácora) actualizada.

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
