===============================================================
 PUEBLO DIGITAL
 Panel sintetico de 1.000 Personas del Pais Vasco
===============================================================

Autor: David Ruiz — Universidad de Deusto (druiz@deusto.es)


QUE ES
---------------------------------------------------------------
Pueblo Digital es un panel sintetico de 1.000 "Personas"
representativas de la poblacion del Pais Vasco. Cada Persona se
construye a partir de microdatos reales de encuestas oficiales
(Deusto Barometro, Sociometro Vasco, ESS, EUSTAT) y puede
instanciarse como un agente conversacional que responde de forma
coherente con su perfil sociodemografico, politico, mediatico y
de bienestar.

Fundamento metodologico: "silicon sampling" (Argyle et al. 2023).


COMO USARLO
---------------------------------------------------------------
1) EL PANEL (web publica)
   https://druiz-byte.github.io/pueblo-digital/
   Muestra las 1.000 Personas. Permite buscar, filtrar por
   estudios/euskera, ver la ficha completa de cada Persona y
   generar el "prompt" que la define.

2) LA ENTREVISTA (con avatar)
   Desde la ficha de una Persona, el boton "Entrevistar" abre una
   conversacion con avatar: la Persona responde por voz y texto.
   Esta parte esta protegida por contrasena (consume creditos de
   API), asi que no es de acceso libre.


QUE HAY EN ESTE REPOSITORIO
---------------------------------------------------------------
- index.html ................ Panel interactivo (version v2).
- panel_pais_vasco_v2.html .. Panel autocontenido alternativo.
- cuestionario_barometro_digital.html .. Cuestionario.
- pv_agentes_v2.json ........ Las 1.000 Personas (datos sinteticos).
- entrevista/ ............... App de entrevista con avatar (Python).
- *.md ...................... Documentacion y metodologia.


QUE NO HAY (y por que)
---------------------------------------------------------------
Por licencia de los proveedores de datos y por proteccion de
datos, NO se publican los microdatos individuales reales de las
encuestas, los PDFs academicos con copyright ni las claves de API.
El repositorio solo contiene codigo, paneles y el JSON de las
Personas sinteticas (que no son datos personales reales).


TECNOLOGIA
---------------------------------------------------------------
- Panel: HTML/CSS/JavaScript autocontenido (GitHub Pages).
- Entrevista: servidor Python (libreria estandar), avatar de
  HeyGen/LiveAvatar via LiveKit, y Claude Haiku como motor de
  respuesta de la Persona. Desplegado en Render.

Instrucciones de despliegue detalladas en README.md.


LICENCIA Y CONTACTO
---------------------------------------------------------------
Proyecto de investigacion academica. Para usos, citas o
colaboraciones, contactar con David Ruiz (druiz@deusto.es).
