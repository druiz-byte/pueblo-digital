# Preregistro — Experimento «dossier» (D1, D2, D3): ¿la información de campaña cambia la intención de voto en generales 29-N?

**Escrito el 2026-11-11 a las 09:46 (Madrid), ANTES de lanzar D1.** No modificar tras ver los datos: los añadidos van en addendas fechadas. Las addendas de D2 y D3 (texto del dossier y su SHA-256) se escriben y fechan **antes** de lanzar cada una.
Complementa `paper/preregistro_retest_R4_prefijo.md` (serie R1-R4) y la serie R5/R6.

## Calendario y orden de lanzamiento (todo desde la web de Render, de una en una)

| Fecha | Tandas, en este orden | Control de la D |
|---|---|---|
| 11-nov (hoy) | R4b y R4a ya lanzadas (09:17-09:18) → **D1** | R4b (mismo día, mismo texto) |
| 21-nov | **R5a → R5b → D2** | R5b |
| 28-nov | **R6b → R6a → D3** | R6b |

El orden a/b se alterna entre días (R4: b→a; R5: a→b; R6: b→a). La D va siempre la última.

## Qué es una tanda D

- **Pregunta y opciones:** las de R4b, sin prefijo «P1.», copiadas literalmente (comprobado por el test). Se elige la versión sin prefijo para que el contraste D vs Rb aísle el dossier.
- **Dossier:** se envía en el campo `contexto` (nuevo, 11-nov). El servidor lo antepone al bloque de la encuesta con una cabecera fija: «Antes de responder, lee esta información publicada en los medios estos días:». **El system prompt (perfil de la Persona) no cambia.**
- **Constantes:** `claude-haiku-4-5-20251001`, 1.000 Personas, panel de Render (`server_anam.py` → **panel v2**, `pv_agentes_v2.json`, ver nota), sin `SURVEY_TEMPERATURE`, letra de ejemplo por defecto.
- **Acumulativo:** D2 = D1 literal + sección «Novedades del 12 al 21 de noviembre». D3 = D2 literal + «Novedades del 22 al 27 de noviembre». Mismo estilo: hechos atribuidos, sin adjetivos valorativos, cifras con fuente y fecha.
- **Límite legal para D3:** la LOREG prohíbe publicar sondeos en los cinco días anteriores a la votación, así que D3 solo puede citar encuestas publicadas hasta el 23-nov.

## Salvaguardas contra la contaminación (verificadas)

1. El dossier viaja **en la petición** de cada tanda; no es variable global ni de entorno. Sin `contexto`, el cuerpo de la petición es idéntico al de antes.
2. `test_no_contaminacion.py` (ejecutado el 11-nov, **todo OK**): con el código de R1-R4 (commit `7f0ec08`) y el nuevo, las 1.000 peticiones de R4a, R4b, R5a, R5b, R6a y R6b son **idénticas byte a byte**, en panel v1 y v2. En D1, system prompt, modelo y `max_tokens` son idénticos y el bloque de la encuesta es el sufijo exacto; lo único añadido es cabecera + dossier. Una R lanzada justo después de una D no hereda nada.
3. La web: al cargar cualquier plantilla se sobrescribe la caja de contexto (las R la dejan **vacía**); con dossier, aviso en amarillo y confirmación antes de lanzar.
4. El fichero de resultados de una D guarda `contexto`, `contexto_cabecera` y `contexto_sha256`; las R no llevan esos campos (esquema de siempre).
5. Tras cada tanda: `verificar_tanda.py <resultado> <plantilla>` (pregunta, contexto/hash, modelo, 1.000/1.000, 0 errores, ≤ 2 % vacías). Si falla, se relanza y se declara.

## D1

- **Fichero:** `D1_dossier_2026-11-11.txt` · plantilla `entrevista/encuestas/voto_generales_D1_dossier.json`
- **SHA-256:** `3c58928018c4bdcb3e5512a89be378d8330504f1e545a6e74a1ec4097e035d5e` · 3.204 caracteres · 578 palabras
- **Contenido:** motivo del adelanto, calendario, candidatos, temas de campaña, encuestas estatales (PolitPro, CIS, 40dB), resultados de 2023 en Euskadi, Sociómetro del GV (20-23 oct), GAD3 (10-nov), posición de cada partido vasco y cabezas de lista.
- **Fuentes:** RankiaPro/Ostrum (11-nov), Moncloa.com (2 y 9-nov), Emol (5-oct), Yahoo/Europa Press (22-oct), Crónica Vasca (24-oct), Orain (30-oct), Demócrata (10-nov), Público (resultados 2023).

### ⚠ Circularidad con la validación frente al GV

D1 incluye la estimación del Sociómetro del GV (EH Bildu 29,1 · PSE-EE 24,7 · PNV 21,9 · PP 12,6…), que es **el mismo dato** contra el que se valida el panel. **Las tandas D no se usan para el contraste de precisión frente al GV.** Si se acercan al GV, se reporta como efecto de anclaje en la cifra publicada, no como mejor predicción.

## Hipótesis (D1 vs R4b, emparejado por Persona)

- **H1 (efecto de la información):** el dossier cambia la distribución de respuesta.
- **H0:** D1 y R4b son la misma distribución (variación de remuestreo a temperatura 1).

Referencia de ruido: mismo texto en días distintos, estabilidad 92-93 % y Stuart-Maxwell p ≥ 0,085 (4 pares). Solo prefijo: 88,3 % y p < 0,001.

### Predicciones (marginales, %)

| Opción | R4b (observado) | D1 predicho | Rango 95 % | Razonamiento |
|---|--:|--:|--:|---|
| Indeciso | 34,0 | 27,0 | 22,0–32,0 | La información reduce la indecisión |
| No votaré | 22,8 | 21,5 | 19,0–24,0 | Movilización leve |
| EH Bildu | 19,3 | 21,0 | 19,0–23,0 | Arrastre: «primera fuerza en Euskadi» |
| PNV/EAJ | 10,7 | 11,5 | 9,0–14,0 | Fuerzas opuestas (caída vs. «suelo sólido»); sin cambio neto claro |
| PSE | 6,5 | 9,0 | 7,0–11,0 | Voto útil frente a una mayoría PP+Vox |
| PP | 4,7 | 5,5 | 4,0–7,0 | |
| Elkarrekin Podemos | 1,9 | 1,5 | 0,8–2,5 | |
| Sumar + VOX | 0,1 | 1,0 | 0,0–2,0 | El dossier les da visibilidad (Frente Amplio, Vox 18,7 %) |

### Predicciones estructurales

1. **Estabilidad D1–R4b ≤ 87 %** (por debajo del 88,3 % del efecto prefijo) y kappa ≤ 0,84.
2. **Stuart-Maxwell D1 vs R4b p < 0,001.** McNemar en «Indeciso»: flujo neto hacia fuera, p < 0,01.
3. **Localización:** lealtad del recuerdo EH Bildu, PSE-EE y PP ≥ 95 % (el dossier no mueve a los grupos que el perfil determina). El cambio se concentra en recuerdo PNV, Elkarrekin Podemos y quienes no votaron o no recuerdan.
4. **Indecisos que deciden:** de los indecisos en R4b que cambian en D1, la mayoría (> 50 %) va a EH Bildu + PSE.

### Regla de decisión

- **Se confirma H1** si Stuart-Maxwell D1 vs R4b p < 0,01 **y** estabilidad D1–R4b < 89,5 %.
- **Se refuta H1 (H0)** si Stuart-Maxwell p ≥ 0,05 **y** estabilidad ≥ 91 %.
- Cualquier otro patrón → **no concluyente**.

## D2 y D3 (diseño fijado hoy; el texto se registra antes de cada lanzamiento)

- **Efecto de la información en cada fecha:** D2 vs R5b; D3 vs R6b (misma regla de decisión).
- **Efecto del tiempo sin información:** R5b vs R4b y R6b vs R5b (se espera p ≥ 0,05, como en la serie R).
- **Efecto incremental de la información acumulada:** D2 vs D1 y D3 vs D2. Como D2 contiene D1, la diferencia D2 − D1 mezcla información nueva y tiempo; el componente de tiempo se descuenta con R5b − R4b (diferencia en diferencias, por Persona).
- **Limitación declarada:** el dossier acumulativo crece en longitud; no se puede separar «más información» de «más texto».

## Nota de corrección (serie R)

Los preregistros de R4 y R3 dicen «panel v1 (`pv_agentes.json`)», pero Render ejecuta `server_anam.py`, que carga el **panel v2**. Lo confirma el n del recuerdo PNV en las addendas (176 = v2; en v1 serían 194). La serie R y D es coherente entre sí (todas en v2); hay que corregir la descripción en el paper.

---

## Addenda — resultados de D1 (escrita el 2026-11-11, después de ver los datos)

**Fichero:** `entrevista/resultados/encuesta_2026-11-11_090050.json` (10:00 en Madrid, después de este preregistro, 09:46). `verificar_tanda.py`: **tanda válida**. Pregunta y opciones idénticas a R4b, SHA-256 del contexto = preregistrado, `claude-haiku-4-5-20251001`, 1.000/1.000, 0 errores, 0 vacías. Control: R4b (`encuesta_2026-11-11_081714.json`, 09:17).

### Marginales (%)

| Opción | R4b | R4a | **D1** | Δ D1−R4b | Predicción D1 (rango) |
|---|--:|--:|--:|--:|--:|
| PNV/EAJ | 10,7 | 7,8 | **18,0** | **+7,3** | 9,0–14,0 ✗ |
| EH Bildu | 19,3 | 20,6 | **17,5** | −1,8 | 19,0–23,0 ✗ |
| PSE | 6,5 | 9,0 | **6,1** | −0,4 | 7,0–11,0 ✗ |
| PP | 4,7 | 4,9 | **2,6** | −2,1 | 4,0–7,0 ✗ |
| Elkarrekin Podemos | 1,9 | 2,2 | **2,9** | +1,0 | 0,8–2,5 ✗ |
| Sumar + VOX | 0,1 | 0,2 | **0,5** | +0,4 | 0,0–2,0 ✓ |
| Indeciso | 34,0 | 32,3 | **34,5** | +0,5 | 22,0–32,0 ✗ |
| No votaré | 22,8 | 23,0 | **17,9** | **−4,9** | 19,0–24,0 ✗ |

### Acuerdo individual

| Par | Estabilidad | Kappa | Stuart-Maxwell | PNV sale/entra | No votaré sale/entra | Indeciso sale/entra |
|---|--:|--:|--:|--:|--:|--:|
| **R4b → D1** | **81,5 %** | 0,764 | χ²=111,1, gl 7, **p<0,001** | 7/80, p<0,001 | 56/7, p<0,001 | 67/72, p=0,73 |
| R4a → D1 | 78,8 % | 0,732 | χ²=148,5, gl 8, p<0,001 | 4/106 | 59/8 | 55/77 |

Referencia: mismo texto 92-93 %; solo prefijo 88,3 %. El dossier mueve el doble que el prefijo.

### Por recuerdo de voto (R4b → D1)

| Recuerdo | n | Cambio principal |
|---|--:|---|
| PNV/EAJ | 176 | **vota PNV 57 → 100 %** (indeciso 23 → 0; EH Bildu 9 → 0; PP 8 → 0) |
| Elkarrekin Podemos | 36 | vota Elkarrekin Podemos 53 → 81 % |
| Vox | 4 | PP 100 → 0; VOX 0 → 100 % |
| EH Bildu · PSE-EE · PP | 151 · 60 · 26 | 100 % · 98 → 100 % · 100 % |
| Abstención | 256 | no votaré 79 → 64; indeciso 17 → 32 |
| No sabe / No contesta | 244 | indeciso 94 → 95 (sin cambio) |
| Nulo · blanco | 25 · 14 | de «no votaré» a «indeciso» |

Indecisos de R4b (n=340): 273 siguen indecisos; de los 67 que deciden, 45 van al PNV (67 %) y solo 6 a EH Bildu + PSE (9 %).

### Contraste con lo preregistrado

- **Regla de decisión:** Stuart-Maxwell p<0,01 ✓ y estabilidad 81,5 % < 89,5 ✓ → **se confirma H1: el dossier cambia la respuesta.**
- **Dirección: refutada casi entera.** Marginales: 1 de 8 dentro de rango. Estructurales: 1 ✓ (81,5 ≤ 87; kappa 0,764 ≤ 0,84) · 2 parcial (SM ✓; indecisos sin flujo neto, p=0,73 ✗) · 3 ✓ (lealtades ≥ 95 %; cambio concentrado en recuerdo PNV, Podemos y abstención) · 4 ✗ (9 % a EH Bildu + PSE, no > 50 %).
- **No hubo anclaje en el Sociómetro:** DAM sobre válidos frente al GV empeora de 5,9 (R4b) a 7,8 (D1); el PNV sube a 37,8 % sobre válidos frente al 21,9 % publicado.

### Lectura (posterior a los datos, se declara como tal)

1. **El dossier no informa, alinea.** No mueve a los indecisos ni produce arrastre hacia quien lidera las encuestas. Hace que cada Persona vote al partido que figura en su perfil como voto en autonómicas 2024: el recuerdo PNV pasa al 100 % de lealtad, el de Podemos sube, los 4 de Vox pasan de PP a VOX. Es el patrón de copia del atributo del perfil (`project_ancla_sin_regular`), activado por un texto que nombra los partidos.
2. **Movilización sin decisión:** parte de los abstencionistas pasa de «no votaré» a «indeciso».
3. **Lo que el dossier dice del PNV (cae, perdería grupo) no lo penaliza;** al contrario. Compatible con una respuesta de lealtad o «rally», pero también con el simple efecto de saliencia del nombre del partido.
4. **No se puede separar contenido de forma:** un texto largo delante de la pregunta, por sí solo, podría producir la misma alineación. **Recomendación (no preregistrada):** una tanda placebo con texto de la misma longitud y estructura, pero sin contenido electoral, para aislar el efecto del contenido.

---

## Addenda — réplica exacta de D1 (D1r) · escrita el 2026-11-11 ANTES de lanzarla

**Añadida después de ver D1** (se declara así). Objetivo: medir la variación entre dos tandas con el mismo dossier, para tener la referencia de ruido con la que comparar D1b (dossier nuevo de David, sin nombres de candidatos).

- **Qué se lanza:** la misma plantilla `voto_generales_D1_dossier.json`, sin cambiar nada (SHA-256 `3c589280…`). Se identifica como D1r por la hora del fichero.
- **Predicciones:** estabilidad D1–D1r **≥ 90 %**; Stuart-Maxwell D1 vs D1r **p ≥ 0,05**; lealtad del recuerdo PNV en D1r **≥ 95 %**; PNV/EAJ en D1r entre **16 y 20 %**.
- **Lectura:** si se cumple, el efecto de D1 es estable y el ruido con dossier es como mínimo tan bajo como sin él. Si D1–D1r < 88 % o la lealtad PNV < 80 %, el resultado de D1 se trata como inestable y se reporta así.

### Resultado de D1r (escrito después de ver los datos)

**Fichero:** `encuesta_2026-11-11_092840.json` (10:28 en Madrid). Tanda válida: definición idéntica a D1, SHA-256 `3c589280…`, 1.000/1.000, 0 errores, 0 vacías.

| Opción | R4b | D1 | D1r |
|---|--:|--:|--:|
| PNV/EAJ | 10,7 | 18,0 | **17,5** |
| EH Bildu | 19,3 | 17,5 | 17,4 |
| PSE | 6,5 | 6,1 | 5,9 |
| PP | 4,7 | 2,6 | 2,7 |
| Elkarrekin Podemos | 1,9 | 2,9 | 3,3 |
| Sumar + VOX | 0,1 | 0,5 | 0,5 |
| Indeciso | 34,0 | 34,5 | 35,5 |
| No votaré | 22,8 | 17,9 | 17,2 |

| Par | Estabilidad | Kappa | Stuart-Maxwell |
|---|--:|--:|--:|
| **D1 → D1r** | **96,1 %** | 0,950 | χ²=11,1, gl 6, p=0,086 |
| R4b → D1r | 81,3 % | 0,761 | χ²=117,0, gl 7, p<0,001 |

Lealtad del recuerdo PNV en D1r: 174/176 (**98,9 %**).

**Predicciones: 4 de 4 cumplidas** (96,1 ≥ 90 ✓ · p=0,086 ≥ 0,05 ✓ · 98,9 ≥ 95 ✓ · 17,5 en 16–20 ✓). El efecto de D1 es estable. Con dossier, el ruido entre tandas es **menor** que sin él (96,1 % frente a 92-93 %): el texto hace la respuesta más determinista. **Referencia para D1b:** una diferencia con D1 por debajo del 96 % de estabilidad, o con p<0,05, ya no es atribuible al azar.

---

## Addenda — D1b, dossier «placebo» programático · escrita el 2026-11-11 ANTES de lanzarlo

**No preregistrado en el diseño original; se añade después de ver D1 y D1r.** David lo llama «placebo», pero **no es un placebo en sentido estricto**: tiene contenido electoral. Es un dossier **programático**: contexto del adelanto, agenda de temas y posición ideológica de cada partido, **sin encuestas, sin escaños y sin nombres de personas**. Redactado por David y revisado por Claude (se quitaron las dos frases finales que instruían a la Persona y los nombres propios; «campaña» → «precampaña»).

- **Fichero:** `D1b_dossier_programatico_2026-11-11.txt` · plantilla `entrevista/encuestas/voto_generales_D1b_placebo.json`
- **SHA-256:** `f3c6438c829e46d833712a311473d44e1f3d34d7b8b107ba3c6c62d00a98be56` · 3.280 caracteres · 473 palabras (D1: 3.204 · 578)
- **Pregunta, opciones, cabecera y constantes:** idénticas a D1 y R4b.

| | D1 | D1b |
|---|---|---|
| Encuestas, escaños | Sí | No |
| Nombres de candidatos | Sí | No |
| Posición ideológica de cada partido | No | Sí (nacionalismo, izquierda/derecha, territorial) |
| Menciones a partidos | 55 | ≈ 20 (PNV 2, EH Bildu 1) |

### Hipótesis que contrasta

- **Hs (saliencia):** D1 alinea porque nombra mucho a los partidos y da cifras. D1b, con pocas menciones, alinea **menos**.
- **Hp (encaje con el perfil):** D1 alinea porque cualquier texto electoral activa la copia del atributo «voto autonómicas 2024». D1b, que además describe a los partidos en los mismos ejes que el perfil (ideología, nacionalismo, territorio), alinea **igual o más**.

**Predicción de Claude: Hp.**

| Medida | Predicción D1b | Rango 95 % |
|---|--:|--:|
| Lealtad recuerdo PNV → PNV | 97 % | 90–100 |
| Lealtad recuerdo Elkarrekin Podemos → Elkarrekin Podemos | 80 % | 65–95 |
| PNV/EAJ (marginal) | 17,5 | 15,5–19,5 |
| Indeciso | 35,0 | 31,0–39,0 |
| No votaré | 18,5 | 15,5–22,0 |
| Estabilidad D1b–D1 | ≥ 90 % | |
| Estabilidad D1b–R4b | ≤ 85 % | |

### Regla de decisión

- **Hp** si lealtad recuerdo PNV en D1b **≥ 90 %** y Stuart-Maxwell D1b vs R4b **p < 0,01**.
- **Hs** si lealtad recuerdo PNV en D1b **≤ 70 %** (cerca del 57 % de R4b) o Stuart-Maxwell D1b vs R4b **p ≥ 0,05**.
- Entre 70 y 90 % → **mixto**: las dos cosas contribuyen.
- Referencia de ruido con dossier (D1–D1r): 96,1 %. Una estabilidad D1b–D1 < 94 % indica que el contenido cambia la respuesta más allá del azar.
