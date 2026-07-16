# Contraste Pueblo Digital vs. Deustobarómetro (verano 2026)

**Encuesta:** `entrevista/resultados/encuesta_2026-07-07_225354.json` · 2026-07-07 22:53 · groq/llama-3.1-8b-instant
**Referencia real:** Informe Deustobarómetro verano 2026 (población del País Vasco).

## ⚠ Advertencia metodológica previa

Esta primera pasada quedó **muy mermada por el rate-limit de la capa gratuita de Groq**: de 1.000 Personas, solo 784 devolvieron fila y de ellas 689 quedaron sin respuesta (peticiones rechazadas con 429). La muestra útil es de **n≈69–92 por pregunta** (62 Personas con las 5 respuestas). Con esa base, los porcentajes tienen márgenes de error de ±10 pp y la submuestra que "sobrevivió" al rate-limit no es necesariamente representativa. **Las cifras siguientes son un diagnóstico preliminar, no un resultado.** El servidor ya está corregido (3 hilos, más reintentos con espera exponencial); hay que relanzar la encuesta para tener el dato definitivo con n≈1.000.

Los que sí respondieron lo hicieron con formato perfecto (P5 siempre con exactamente 3 opciones), es decir, el motor de encuesta y el parser funcionan correctamente.

## Resultados (panel % vs. real %)

### P1. ¿Cómo calificarías la situación económica del País Vasco? (n=69) — MAE 5,2 pp

| Opción | Panel | Real | Dif |
|---|---:|---:|---:|
| Muy buena | 1,4 | 3,9 | −2,5 |
| Buena | 33,3 | 43,0 | −9,7 |
| Regular | 39,1 | 42,5 | −3,4 |
| Mala | 11,6 | 6,7 | +4,9 |
| Muy mala | 10,1 | 2,5 | +7,6 |
| NS/NC | 4,3 | 1,4 | +2,9 |

La mejor de las cinco, como cabía esperar: la valoración económica está anclada en el perfil de las Personas. Aún así el panel se desplaza hacia el pesimismo, señal de que llama-3.1-8b no siempre respeta el atributo del perfil.

### P2. Situación económica dentro de un año (n=86) — MAE 22,1 pp

| Opción | Panel | Real | Dif |
|---|---:|---:|---:|
| Mejor | 7,0 | 7,5 | −0,5 |
| Igual | 23,3 | 66,9 | **−43,6** |
| Peor | 57,0 | 21,5 | **+35,5** |
| NS/NC | 12,8 | 4,2 | +8,6 |

**Fuerte sesgo pesimista.** La población real espera mayoritariamente continuidad ("Igual" 66,9%); el panel se lanza a "Peor". Los LLM tienden a extremizar y a evitar la opción neutral — coherente con la literatura de sesgos (Qu 2024).

### P3. "Priorizar a las personas autóctonas en la redistribución de recursos públicos" (n=92) — MAE 9,2 pp

| Opción | Panel | Real | Dif |
|---|---:|---:|---:|
| Muy de acuerdo | 10,9 | 19,4 | −8,5 |
| Bastante de acuerdo | 51,1 | 33,1 | +18,0 |
| Poco de acuerdo | 27,2 | 22,1 | +5,1 |
| Nada de acuerdo | 8,7 | 18,6 | −9,9 |
| No lo sé | 2,2 | 6,8 | −4,6 |

Acuerdo agregado: panel 62,0% vs. real 52,5%. Dirección correcta pero **aplanada hacia las opciones moderadas** ("Bastante" engorda a costa de "Muy" y "Nada"). Curiosamente no aparece la infrarrepresentación del acuerdo que predeciría el sesgo de deseabilidad social (Guo 2025) — quizá porque el modelo es pequeño y poco "alineado", o porque la muestra superviviente está sesgada.

### P4. ¿Dentro de 10 años será más fácil acceder a una vivienda? (n=86) — MAE 11,0 pp

| Opción | Panel | Real | Dif |
|---|---:|---:|---:|
| Seguro que sí | 1,2 | 3,8 | −2,6 |
| Probablemente sí | 14,0 | 15,0 | −1,0 |
| Probablemente no | 54,7 | 38,1 | +16,6 |
| Seguro que no | 9,3 | 33,0 | **−23,7** |
| NS/NC | 20,9 | 10,1 | +10,8 |

Dirección agregada correcta (no: 64,0% panel vs. 71,1% real) pero **mala calibración de la intensidad**: el panel evita el extremo "Seguro que no" y se refugia en "Probablemente no" y NS/NC. Mismo patrón de moderación que en P3.

### P5. Los 3 problemas globales que más miedo dan (n=89, multirespuesta) — MAE 14,3 pp

| Opción | Panel | Real | Dif |
|---|---:|---:|---:|
| Conflictos internacionales / guerras | 2,2 | 45,0 | **−42,8** |
| Subida brusca de los precios | 18,0 | 36,4 | −18,4 |
| Avance de ideas antidemocráticas | 21,3 | 33,1 | −11,8 |
| Inseguridad ciudadana | 20,2 | 32,8 | −12,6 |
| Cambio climático | 75,3 | 26,8 | **+48,5** |
| Pandemias / crisis sanitarias | 70,8 | 23,8 | **+47,0** |
| Precariedad laboral | 28,1 | 21,0 | +7,1 |
| Migración | 16,9 | 18,4 | −1,5 |
| Desempleo | 5,6 | 17,5 | −11,9 |
| Terrorismo | 9,0 | 9,5 | −0,5 |
| Crisis energética | 14,6 | 9,0 | +5,6 |
| Desarrollos tecnológicos (IA) | 4,5 | 8,8 | −4,3 |
| Ciberataques | 7,9 | 6,7 | +1,2 |
| Desabastecimiento producto básico | 3,4 | 5,2 | −1,8 |
| Ninguno en particular | 2,2 | 2,0 | +0,2 |

La peor con diferencia en las opciones principales. Dos efectos combinados:

1. **Anclaje en el perfil:** el prompt de cada Persona incluye explícitamente "Preocupación cambio climático" (única variable de "miedo" del perfil), lo que dispara "Cambio climático" al 75%.
2. **Sesgo de saliencia del modelo:** "Pandemias" (+47) refleja la prominencia del tema en el corpus de entrenamiento, mientras "guerras" (−42,8), el miedo nº 1 real de los vascos en 2026, apenas aparece — posiblemente porque el corpus del modelo es anterior a la actualidad que motiva ese miedo.

## Lectura general (preliminar)

| | MAE (pp) | Diagnóstico |
|---|---:|---|
| P1 economía actual (anclada al perfil) | 5,2 | Aceptable |
| P2 expectativa a 1 año | 22,1 | Sesgo pesimista fuerte |
| P3 priorizar autóctonos | 9,2 | Dirección bien, intensidad aplanada |
| P4 vivienda 10 años | 11,0 | Dirección bien, evita extremos |
| P5 miedos globales | 14,3 | Anclaje en perfil + saliencia del corpus |

Patrón consistente con la literatura: el panel acierta la **dirección** de la opinión pero falla la **calibración** (evita extremos y opción neutral, infla NS/NC) y arrastra los **temas salientes de su corpus** cuando la pregunta no está anclada en el perfil. Todo ello con la enorme cautela del n.

## Próximos pasos

1. **Relanzar la encuesta** con el servidor corregido (3 hilos, reintentos hasta 60 s) para obtener n≈1.000. Duración estimada: 45–90 min con la capa gratuita de Groq.
2. Repetir el contraste con la muestra completa y, si se confirman los sesgos, probar con un modelo mayor (Claude Haiku como fallback ya implementado) para separar "sesgo del modelo pequeño" de "sesgo del método".
3. Considerar retirar "Preocupación cambio climático" del prompt en preguntas de miedos, o estudiar el efecto anclaje como resultado en sí (interesante para el artículo).
