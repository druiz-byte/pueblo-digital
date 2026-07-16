# Pueblo Digital — Contexto del proyecto

> **Propósito de este archivo:** dar contexto a Claude (Cowork/Claude Code) en cualquier ordenador.
> La carpeta se sincroniza vía OneDrive entre el ordenador de la oficina y el de casa.
> **Mantener actualizado:** al terminar una sesión de trabajo, actualizar la sección "Estado actual y próximos pasos".

## Qué es el proyecto

Pueblo Digital es un **panel sintético de 1.000 Personas** representativas de la población del País Vasco. Cada Persona se construye a partir de microdatos reales de encuestas oficiales (Deusto Barómetro 2026, Barómetro político de Euskadi, Encuesta de Bienestar Personal 2025 de Eustat, ESS de Europa) y puede instanciarse como agente LLM que responde de forma coherente con su perfil sociodemográfico, político, mediático y de bienestar. Fundamento metodológico: "silicon sampling" (Argyle et al. 2023).

Detalle completo de la metodología en `resumen_construccion_panel.md` (muestreo estratificado, post-estratificación, emparejamiento estadístico k-NN por celda lurral × sexo × edad_g × eus_g).

## Estructura de la carpeta

| Ruta | Contenido |
|---|---|
| `pv_agentes.json` | Las 1.000 Personas del panel País Vasco (datos completos) |
| `panel_pais_vasco.html` | Panel interactivo autocontenido (filtros, perfiles, prompts) |
| `resumen_construccion_panel.md` | Documento metodológico: cómo se construyó el panel |
| `literatura_relacionada.md` | Revisión de literatura académica (silicon sampling, agentes generativos, sesgos) |
| `entrevista/` | App web de entrevista con avatar. **Arrancar `server_v2.py`** (sirve el panel v2 `pv_agentes_v2.json` + `build_system_prompt_v2`, sobre el motor de `server.py`) → puerto 3000. `public/` es el frontend. Claude responde como la Persona; LiveAvatar (HeyGen) la verbaliza vía LiveKit. Claves en `entrevista/.env` (no commitear/compartir). El botón "Entrevistar" del panel abre `localhost:3000/?id=NN` en modo enfocado (solo ficha · avatar · conversación) |
| `datos GV/` | Datos fuente del Gobierno Vasco / Eustat (CSV medios 2025, bienestar) |
| `artículos/` | PDFs de la literatura (Argyle et al., datos sintéticos en marketing, etc.) |
| `Informe+Deustobarómetro+verano+2026.pdf` | Referencia Deustobarómetro |
| `Resultado1.spv` | Salida SPSS |

## Estado actual y próximos pasos

**Última actualización: 2026-07-16, novena sesión** (detalle en `bitacora.md`)

Estado (lo más reciente arriba):
- **APP DE ENTREVISTA CONECTADA AL PANEL v2 + VISTA ENFOCADA.** El botón "Entrevistar" del panel raíz (`index.html`, v2) abre `http://localhost:3000/?id=NN` (constante `ENTREVISTA_URL` en `index.html`). **Servidor a usar: `entrevista/server_v2.py`** (no `server.py`): carga `pv_agentes_v2.json` para que los `id` coincidan con el panel v2 (con `server.py`/v1 salía otra Persona). Con `?id=`, `entrevista/public/index.html` entra en **modo enfocado** (`body.focus`): oculta buscador y lista, deja **solo la ficha** de la Persona (izq., enriquecida con campos v2 por secciones) · avatar (centro) · transcripción (dcha.). Sin `?id` sigue funcionando standalone con buscador+lista. Botón de conexión = **`🎙 Hablar con la Persona`**, arriba a la izquierda encima de la ficha. Para acceso remoto (móvil/otro PC): desplegar `server_v2.py` en Render y cambiar `ENTREVISTA_URL`.
- **PILOTO PPI++ SOBRE DATOS REALES (bloque política).** Primer uso de **microdatos individuales del Deustobarómetro verano 2026** (SPSS, n=1.000; convertidos a `predictores_deusto.csv`). Todo en `piloto_ppi/` + informe `piloto_ppi/informe_piloto_ppi_politica.md`. Método: Prediction-Powered Inference con power-tuning (PPI++, Angelopoulos et al. 2023a/b; lib `ppi-python`). Motor `ppi_engine.py` validado con Monte Carlo (`selftest_ppi.py`: cobertura ~95%, sesgo ~0).
  - **Sustitución ingenua (enfoque actual) se equivoca decenas de p.p.:** en p18 el panel diría "Buena" 64% cuando el real es Regular 43,5%/Buena 32,5% (error 43 p.p. en "Regular").
  - **PPI++ es válido siempre y se adapta:** donde el panel informa recorta el IC; donde está sesgado/sin correlación se repliega al clásico (nunca peor).
  - **Versión generativa ejecutada (300 encuestados, API en el PC de David):** `generar_predicciones_deusto.py` crea una Persona con el perfil real de cada encuestado y predice el bloque 5 **sin inyectar las variables objetivo** (anti-circularidad); `true_ppi.py` hace el PPI++ 1:1. Mejora la señal: confianza Gobierno Vasco corr +0,28→**+0,42**, ~9% de reducción de IC a n=50 (~20% ahorro de datos). p18 y Gobierno Central siguen siendo casos de protección (muy sesgados). Sin injección, el LLM colapsa p18 en "Regular" 86%.
  - **Límite:** la ganancia PPI escala con N no etiquetado (N≫n); con solo 300 el margen se agota. PENDIENTE opcional: generar los **1.000** (`python generar_predicciones_deusto.py` sin `--muestra`) y recalcular con `true_ppi.py`.
  - **Nota infra:** la API de Anthropic NO es accesible desde el sandbox de Claude (proxy devuelve 401 text/plain); la generación se lanza en el PC de David. La clave del `.env` es válida ahí.
  - Papers revisados esta sesión (candidatos a literatura/discusión): PPI (Angelopoulos et al. 2301.09633), AAE market research (Wang et al. 2412.19363). PENDIENTE: añadirlos formalmente a `literatura_relacionada.md`.
- **PANEL v2 CONSTRUIDO Y CONTRASTADO (mejora la predicción).** Nuevo enfoque: cada Persona se **ancla en un encuestado real** del Sociómetro Vasco 83 (remuestreo ponderado por `wt`, "opción B") e inyecta los bloques con **más llaves** (5-6 en vez de 4): medios/bienestar del **ESS España** (kNN por sexo×edad×educación×laboral×ideología, 969/1000 a 5 llaves) y confianza/redes/participación de **EUSTAT Capital Social 2022** (kNN por sexo×edad×provincia×clase). Salida en `pv_agentes_v2.json` (esquema compatible + bloque `perfil_social`).
  - **Contraste tanda 1.000 (2026-07-14): DAM global 14,0 p.p.** (143 preg.) frente a 16,7 de la v1. Por bloque (v2 vs v1): B5 política **10,0** vs 11,8 · B2 bienestar/políticas **14,4** vs 17,9 · B1 económica 11,7 vs 10,8 · B3 miedos 18,7 vs 19,6 · B6 geopolítica 23,7 vs 25,8 · B4 turismo 26,9 vs 26,5. Mejoran 4/6 bloques; ganancias donde actúa el rediseño (bienestar +3,5, política +1,8, geopolítica +2,1); turismo plano (ninguna encuesta donante lo cubre); B1 algo peor porque `principales_problemas` quedó vacío (no está en el ancla). Resultados en `entrevista/resultados/encuesta_2026-07-14_1635..1646.json`.
  - **AVISO comparación no 100% limpia:** la v1 (16,7) se midió con plantillas antiguas (91 preg.) y la v2 con las oficiales (143 preg.). Para atribuir la mejora limpiamente al panel, **relanzar el panel v1 con las plantillas oficiales actuales** y contrastar sobre las mismas preguntas. La validación previa sin API ya mostró que la coherencia entre bloques mejora (ideología×interés política ya no sale plana).
  - **Herramientas v2** (todas en la carpeta): `construir_panel_v2.py` (construcción, solo datos), `entrevista/prompt_v2.py` (`build_system_prompt_v2`), `entrevista/lanzar_barometro_v2.py` (lanzador), `entrevista/server_v2.py` (app de entrevista con avatar sobre el panel v2; frontend sin cambios), `panel_pais_vasco_v2.html` (panel interactivo autocontenido con agregados + filtros + fichas + generación de prompt). Voto v2 = recuerdo 2020 (P23) con respaldo intención 2024 (P21).
- **FUENTES DE DATOS NUEVAS analizadas y descargadas** (para pasar de "3 encuestas unidas por 4 llaves" a fuentes con muchas llaves): `fuentes_datos_panel.md` (inventario + matriz de llaves + estrategia de emparejamiento) y `descargar_fuentes.py`. Ficheros en carpetas `Datos ESS/` (ESS España, 21.296×2.747, PV=671), `Datos sociómetro GobEsp/` (SV83, 3.030×80, con codebook en el .sav), `datos capital social 2022/` (ECS 2022, 5.798×57, índices 0-10). EUSTAT relevante: Capital Social, ECV, Bienestar Personal, Sociedad de la Información. Reseña del artículo comercial de Qualtrics en `literatura_relacionada.md` (sección 7).
- **`barometro_preguntas_por_bloques.md`**: las 141 preguntas del barómetro por bloques (texto+opciones+tipo).
- **CUESTIONARIO OFICIAL RECONSTRUIDO** desde el PDF de tablas por educación (46 preguntas p1–p46 = 152 ítems, texto/opciones/% real exactos; validado 1172/1172 opciones con dato real). 7 plantillas nuevas en `entrevista/encuestas/barometro_digital_1..7.json` (Bloque 7 = perfil/validación p40–p46); antiguas en `encuestas/_backup_pre_oficial_2026-07-09/`. `cuestionario_barometro_digital.html` regenerado. **PENDIENTE: relanzar el barómetro completo con estas plantillas y rehacer el contraste.**
- **DAM por pregunta**: `entrevista/resultados/DAM_por_pregunta.md` + Excel `DAM_por_pregunta_Barometro_Digital.xlsx` (raíz).
- **Experimento líderes/Gobierno** (2 preguntas propias): `lanzar_extra.py` + plantillas `extra_lideres_gobierno[_conpartidos]_2026-07-09.json`. Lanzadas a 1.000. Contraste con el real en `resultados/extra_lideres_comparacion_2026-07-09.md` (con partido el "No sé" baja de 64%→24%; sub-reporta NS vs 51% real; pierde el voto transversal de Pradales; sesgo contra Vox/Sumar).
- **Pregunta ABIERTA** "tres problemas": `lanzar_abierta.py` + `codificar_abierta.py`. Lanzada a 1.000. Codificación (≥10%): Vivienda 51,8 · Económicos 47,0 · Sanidad 44,9 · Trabajo 34,8 · Delincuencia 24,1 · Inmigración 19,4. Ranking por subgrupo: `ranking_problemas_por_subgrupo.png`/`.html` (5 categorías, excl. económicos, formato de la imagen real).
- **"Barómetro digital" (versión ANTERIOR, 141 ítems) lanzado y contrastado** el 2026-07-08: `entrevista/resultados/encuesta_2026-07-08_1814..182209.json` (6 bloques). **DAM media global 16,7 p.p.** (91 preguntas). Nota: esta tanda usó las plantillas viejas; conviene rehacerla con las 7 oficiales.
- **Contraste global hecho**: `entrevista/resultados/contraste_bloque1..6.md` + consolidado `contraste_barometro_completo_2026-07-08.md`. **DAM media global 16,7 p.p.** (91 preguntas con dato real). Por bloque: B1 10,8 · B5 11,8 · B2 17,9 · B3 19,6 · B6 25,8 · B4 26,5. Patrón: fidelidad casi perfecta si la variable está en el perfil (política PV 0,4; economía 0,7; territorial 1,4; nacionalismo 1,4); error alto en lo ajeno al perfil y multi-respuesta (peores: Bloque 6 "aliados/enemigos", hasta 56,9 p.p.); exceso de NS/NC en expectativas.
- **PDF comparativo página a página**: `Comparativa_Barometro_Digital_vs_Deustobarometro.pdf` (raíz, 42 págs). Izq = página original del Deustobarómetro; der = resultado del panel (solo nuestros %) replicando el tipo de gráfico. Datos intermedios en `entrevista/resultados/_sintetico_por_pregunta.json`.
- **`panel_pais_vasco.html` retocado**: cabecera limpia renombrada "Barómetro Digital — País Vasco"; subtítulo + fuente en cada cajita; leyenda de voto en % ponderado con 2 decimales. (Fuentes inferidas, pendientes de validar.)
- **Proveedor LLM: Claude Haiku** (`claude-haiku-4-5`, ~1,5-2 $ y ~10 min por tanda de 1.000). Para lanzar: `ANTHROPIC_API_KEY` válida en `.env` y `GEMINI_API_KEY`/`GROQ_API_KEY` comentadas. Debe lanzarse en el ordenador de David (el sandbox de Claude no tiene acceso a la API). Gemini y Groq free descartados.
- **Tanda 1** (5 preguntas): `entrevista/resultados/encuesta_2026-07-08_132943.json` + `contraste_tanda1_2026-07-08.md` (DAM 15,3 p.p.).
- **Herramientas**: `comparar_deustobarometro.py` (lee `datos_reales` de `encuestas/`, vale para cualquier tanda); `server.py` con `"hasta": true` y robustecido (reintento de formato, backoff, 5xx).

Pendiente inmediato (en este orden):
1. **Cerrar el experimento v1 vs v2 de forma limpia:** relanzar el **panel v1** (`pv_agentes.json`) con las **plantillas oficiales actuales** (`lanzar_barometro.py`) y contrastar sobre las mismas 143 preguntas que la v2, para aislar la mejora atribuible al panel (hoy 14,0 vs 16,7 mezcla panel + cambio de plantillas).
2. Añadir `principales_problemas` al ancla v2 (o inyectarlo) para recuperar el bloque B1.
3. Validar las etiquetas de **fuente del panel HTML** (voto/territorial/problemas → Deustobarómetro; edad/euskera → EUSTAT 2021).
2. Posible versión del PDF comparativo con **% real + DAM** al lado (para el artículo) y colores semánticos en las apiladas de impacto (guerra/Trump).
3. Pregunta de intención de voto en generales (mensaje de David quedó cortado: "En las próximas elecciones generales, ¿a q...?").
4. Validación de distribuciones del panel frente a resultados electorales 2024.
5. Redacción del artículo académico (los sesgos del contraste son el material central).

## Convenciones de trabajo

- Idioma de trabajo y documentos: **español**.
- Los individuos sintéticos se llaman **Personas** (con mayúscula), nunca "agentes".
- David es el autor (Universidad de Deusto, druiz@deusto.es).
- Documentación en Markdown en la raíz de la carpeta; datos fuente en `datos GV/`; PDFs académicos en `artículos/`.
- OneDrive puede mantener archivos "solo en la nube": si un script falla al leer un archivo, probablemente no está descargado localmente en ese ordenador.
