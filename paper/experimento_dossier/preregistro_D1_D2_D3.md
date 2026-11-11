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
