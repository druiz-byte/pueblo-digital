# Pueblo Digital — Literatura académica relacionada

Una revisión de trabajos que convergen con las distintas capas del proyecto: simulación de poblaciones sintéticas con LLMs, predicción de opinión pública, agentes generativos y Personas sintéticas interactivas.

---

## 1. El paper fundacional: "Silicon Sampling"

### Argyle et al. (2023) — *Out of One, Many: Using Language Models to Simulate Human Samples*
**Political Analysis** · Cambridge University Press  
[→ Cambridge Core](https://www.cambridge.org/core/journals/political-analysis/article/out-of-one-many-using-language-models-to-simulate-human-samples/035D7C8A55B237942FB6DBAD7CAA4E49) · [→ ResearchGate PDF](https://www.researchgate.net/publication/368699890_Out_of_One_Many_Using_Language_Models_to_Simulate_Human_Samples)

El trabajo que acuñó el concepto de **"silicon sampling"**: condicionar un LLM con el perfil sociodemográfico de un encuestado real para que genere las respuestas que esa persona daría en una encuesta. Los autores demuestran que GPT-3, al recibir el "backstory" demográfico de un participante de la ANES (American National Election Studies), reproduce distribuciones de opinión política cercanas a las reales.

**Relevancia directa para Pueblo Digital:** es exactamente el fundamento teórico de lo que hacemos cuando instanciamos una Persona del panel como prompt de Claude. La diferencia clave es que Pueblo Digital ancla cada Persona en microdatos reales de encuesta (no en perfiles sintéticos genéricos), y aplica emparejamiento estadístico para enriquecer los atributos.

---

## 2. Simulación de opinión pública con LLMs

### Kim & Peng (2024) — *Random Silicon Sampling: Simulating Human Sub-Population Opinion Using a LLM Based on Group-Level Demographic Information*
**arXiv:2402.18144**  
[→ PDF](https://arxiv.org/pdf/2402.18144)

Extiende el silicon sampling a subpoblaciones definidas por combinaciones de variables demográficas (no solo individuos). El LLM genera distribuciones de opinión para celdas demográficas (ej. "mujeres de 35–44 años con estudios universitarios"). Muy próximo a nuestra lógica de emparejamiento por celdas lurral × sexo × edad_g × eus_g.

---

### Kozlowski et al. (2023/2025) — *AI-Augmented Surveys: Leveraging Large Language Models and Surveys for Opinion Prediction*
**arXiv:2305.09620**  
[→ HTML](https://arxiv.org/html/2305.09620v4)

Propone un marco híbrido: usar datos de encuesta reales para *calibrar* el LLM, y luego el LLM para predecir respuestas no recogidas (retrodiction) o preguntas nunca formuladas (unasked opinion prediction). Fine-tuning sobre el General Social Survey (GSS, 1972–2021). El enfoque es diferente al nuestro (fine-tuning vs. prompting), pero el objetivo es muy similar: rellenar huecos en los datos de encuesta.

---

### Bail et al. (2024) — *Simulating Public Opinion: Comparing Distributional and Individual-Level Predictions from LLMs and Random Forests*
**Entropy (MDPI)** · PMC  
[→ PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12468613/) · [→ DOI](https://doi.org/10.3390/e27090923)

Comparación sistemática entre LLMs y modelos de machine learning clásicos (Random Forests) para predecir opinión a nivel individual y distribucional. Conclusión: los LLMs son mejores para capturar distribuciones agregadas, los RF para predicción individual. Condicionados sobre datos ANES 2020.

---

### Qu et al. (2024) — *Performance and Biases of Large Language Models in Public Opinion Simulation*
**Humanities and Social Sciences Communications** (Nature Portfolio)  
[→ Nature](https://www.nature.com/articles/s41599-024-03609-x)

Evaluación sistemática de sesgos en la simulación de opinión. Identifica que los LLMs sobrerrepresentan la opinión mayoritaria, infrarepresentan minorías y posiciones extremas, y se comportan peor en contextos no anglosajones. Importante para evaluar los límites de Pueblo Digital en un contexto vasco/español.

---

### Bail et al. (2025) — *Do LLMs Track Public Opinion? A Multi-Model Study of Favorability Predictions in the 2024 U.S. Presidential Election*
**arXiv:2602.06302**  
[→ HTML](https://arxiv.org/html/2602.06302v1)

Test de validación externa: ¿pueden los LLMs predecir intención de voto en tiempo real? Resultado: todos los modelos sobrestimaron la favorabilidad de Harris entre un 10–40% respecto a los sondeos reales. Apunta al problema de sesgo político en los modelos base.

---

### Synthesizing Public Opinions with LLMs (2025) — *Role Creation, Impacts, and the Future to eDemocracy*
**arXiv:2504.00241**  
[→ HTML](https://arxiv.org/html/2504.00241)

Explora el uso de LLMs para sintetizar opinión pública con vistas a procesos de democracia digital y participación ciudadana — dimensión de aplicación directamente relevante para Pueblo Digital como herramienta de investigación aplicada.

---

## 3. Agentes generativos y simulación social

### Park et al. (2023) — *Generative Agents: Interactive Simulacra of Human Behavior*
**UIST 2023** · Stanford + Google Research  
[→ PDF arXiv:2304.03442](https://arxiv.org/pdf/2304.03442)

El paper de referencia para agentes LLM socialmente situados. Los autores poblan un entorno sandbox con 25 agentes que planifican su día, forman relaciones, comparten información y coordinan acciones colectivas — todo ello emergiendo del LLM sin programación explícita de esos comportamientos. La arquitectura combina memoria en streaming, reflexión y descomposición recursiva de planes.

**Relevancia:** Pueblo Digital usa una arquitectura más simple (sin memoria persistente entre conversaciones), pero el principio de dotar a cada Persona de un perfil coherente que guíe su comportamiento conversacional es idéntico.

---

### Zhang et al. (2025) — *SocioVerse: A World Model for Social Simulation Powered by LLM Agents and A Pool of 10 Million Real-World Users*
**arXiv:2504.10157** · Fudan University  
[→ arXiv](https://arxiv.org/abs/2504.10157) · [→ GitHub](https://github.com/FudanDISC/SocioVerse)

El trabajo más ambicioso en escala: 10 millones de Personas reales extraídas de redes sociales, con cuatro componentes de alineación (Social Environment, User Engine, Scenario Engine, Behavior Engine). Validado en simulaciones políticas, de noticias y económicas. Es, en cierto modo, la versión a gran escala de lo que Pueblo Digital hace con 1.000 Personas, pero usando datos de redes sociales en lugar de microdatos de encuesta oficial.

---

### Evaluating LLMs as Synthetic Social Agents (2025)
**arXiv:2509.26080**  
[→ PDF](https://arxiv.org/pdf/2509.26080)

Evaluación sistemática de LLMs como agentes sociales sintéticos para investigación en ciencias sociales, con énfasis en coherencia conductual y validez de constructo.

---

## 4. Personas sintéticas interactivas y entrevistas

### Brade et al. (2025) — *PersonaCite: VoC-Grounded Interviewable Agentic Synthetic AI Personas for Verifiable User and Design Research*
**arXiv:2601.22288**  
[→ HTML](https://arxiv.org/html/2601.22288)

El trabajo más próximo a la app de entrevista de Pueblo Digital. Los autores construyen Personas sintéticas entrevistables donde las respuestas del LLM están **ancladas y citadas** en evidencia real (Voice of the Customer data), lo que evita alucinaciones. La Persona solo puede afirmar lo que los datos respaldan.

**Relevancia directa:** aborda exactamente el problema de fidelidad que Pueblo Digital tiene con la app de entrevista — ¿cómo garantizar que Claude, al hablar como una Persona, no inventa más allá del perfil?

---

### Synthetic Founders (2025) — *AI-Generated Social Simulations for Startup Validation Research*
**arXiv:2509.02605**  
[→ HTML](https://arxiv.org/html/2509.02605)

Usa LLMs para generar Personas de potenciales clientes y simular entrevistas de validación de startups. Metodológicamente muy cercano: Persona con perfil demográfico + psicográfico → entrevista con LLM → análisis de respuestas.

---

### PersonaBOT (2025) — *Bringing Customer Personas to Life with LLMs and RAG*
**arXiv:2505.17156**  
[→ HTML](https://arxiv.org/html/2505.17156)

Combina LLM con Retrieval-Augmented Generation para hacer Personas de clientes "entrevistables" en contexto industrial (Volvo). Aproximación complementaria a la nuestra: usa RAG para anclar respuestas en documentos reales sobre el segmento de cliente.

---

## 5. Poblaciones sintéticas para modelos basados en agentes (ABM)

### Synthetic Population Generation with Public Health Characteristics (2024/2025)
**medRxiv / PMC**  
[→ PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11957385/)

Genera poblaciones sintéticas para modelos epidemiológicos de agentes usando encuestas de salud pública y emparejamiento estadístico — la misma técnica que Pueblo Digital usa para incorporar los datos de bienestar. El contexto es salud pública (vacunación COVID en Virginia), pero la metodología de statistical matching entre encuestas es idéntica.

---

## 6. Sesgos y limitaciones (lecturas críticas)

### Santurkar et al. (2025) — *The Threat of Analytic Flexibility in Using LLMs to Simulate Human Data*
**arXiv:2509.13397**  
[→ PDF](https://arxiv.org/pdf/2509.13397)

Advertencia metodológica importante: la flexibilidad en el diseño del prompt puede hacer que los LLMs "confirmen" prácticamente cualquier hipótesis. Los resultados de silicon sampling son muy sensibles a pequeños cambios en la formulación del perfil demográfico.

---

### Guo et al. (2025) — *Mitigating Social Desirability Bias in Random Silicon Sampling*
**arXiv:2512.22725**  
[→ PDF](https://arxiv.org/pdf/2512.22725)

Los LLMs tienden a dar respuestas socialmente deseables (más moderadas, políticamente correctas) que los humanos reales en las mismas preguntas. El paper propone técnicas de mitigación.

---

### The Prompt Makes the Persona (2025)
**arXiv:2507.16076**  
[→ PDF](https://arxiv.org/pdf/2507.16076)

Evaluación sistemática de cómo el prompting sociodemográfico afecta al comportamiento del LLM. Muestra que la misma Persona puede comportarse de forma muy diferente según cómo esté formulado el prompt — relevante para el diseño del system prompt de Pueblo Digital.

---

## 7. Perspectiva de la industria: taxonomías comerciales de investigación sintética

### Qualtrics (2024/2025) — *Understanding the different types of synthetic responses* (eBook / blog)
**Qualtrics** · pieza divulgativa/comercial  
[→ eBook](https://www.qualtrics.com/ebooks-guides/synthetic-responses/)

No es un trabajo académico, sino material de un proveedor comercial de encuestas, pero resulta útil para **posicionar Pueblo Digital frente al mercado** y para el marco del artículo. Clasifica la oferta de respuestas sintéticas en tres tipos: (1) **LLM wrapper** —un modelo genérico (ChatGPT, Claude, etc.) más ingeniería de prompt como IP, alimentado solo de datos públicos—; (2) **modelo ML supervisado** —Decision Trees / XGBoost / Random Forest entrenados sobre respuestas humanas tabulares para extrapolar 300→600—; y (3) **LLM fundacional** —modelo base hidratado con datos propietarios y licenciados para tareas específicas—.

**Dónde encaja Pueblo Digital:** en la mecánica es un **"LLM wrapper"** (Claude Haiku genérico + prompt, sin fine-tuning ni entrenamiento con datos tabulares propios), pero es un wrapper atípico que **neutraliza la debilidad central que el propio artículo atribuye a esta categoría**: la homogeneización y la incapacidad de "trocear por segmento o demografía". Al anclar cada Persona en microdatos reales de encuesta por celda (silicon sampling, cf. Argyle 2023), sí produce granularidad individual —la prueba de 20 dio firmas únicas 20/20 sin homogeneización—. Metodológicamente, por tanto, aspira a la ambición del tipo fundacional (opción 3) sin su coste computacional, mediante una cuarta vía que la taxonomía comercial no contempla: **grounding individuo a individuo**, no hidratación del modelo base.

**Diálogo con el contraste empírico:** el apartado "not as good for" del wrapper (generar datos cuantitativos, Likert, NPS; temas fuera de sus datos) anticipa cualitativamente lo que nuestro contraste mide con precisión —DAM global 16,7 p.p., fidelidad casi perfecta cuando la variable está en el perfil (política 0,4; economía 0,7) y error alto en lo ajeno al perfil y multirrespuesta (hasta 56,9 p.p.)—. La frontera no es el modelo, sino qué contiene el perfil de cada Persona.

**Uso para el artículo:** las seis preguntas de evaluación de proveedores que propone el artículo (tipo de modelo, entrenamiento, actualización, validación, capacidad de generar respuestas nuevas, poblaciones modelables) sirven de checklist de posicionamiento; Pueblo Digital responde con fuerza justo donde los proveedores comerciales son opacos —validación (contraste página a página contra el Deustobarómetro real) y límites poblacionales documentados con datos—.

---

## Mapa de convergencia con Pueblo Digital

| Componente de Pueblo Digital | Papers más relevantes |
|---|---|
| Personas sintéticas ancladas en microdatos de encuesta | Argyle et al. 2023, Kim & Peng 2024 |
| Emparejamiento estadístico entre encuestas | Synthetic Population + Public Health (2024) |
| LLM respondiendo como una Persona con perfil demográfico-político | Argyle 2023, Kozlowski 2023, Bail 2024 |
| Panel de 1.000 Personas representativas de una región | SocioVerse 2025, Random Silicon Sampling 2024 |
| Entrevista interactiva con la Persona | PersonaCite 2025, Synthetic Founders 2025, PersonaBOT 2025 |
| Avatar hablante (app de entrevista) | Sin equivalente directo publicado (novedad del proyecto) |
| Validación de distribuciones frente a datos reales | Bail et al. 2024, Qu et al. 2024 |
| Sesgos y limitaciones | Santurkar 2025, Guo 2025, Qu 2024 |
| Posicionamiento frente al mercado comercial | Qualtrics 2024 (taxonomía wrapper / ML / fundacional) |
