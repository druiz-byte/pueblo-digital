# Guía: mejorar la analítica de Pueblo Digital

Sitio: https://druiz-byte.github.io/pueblo-digital/ · GA4: `G-BQH2YG2XRG`

## Qué tienes ya (sin tocar nada)

GA4 está bien instalado y **ya mide "quién llega"** de forma automática:

- **Fuente / medio**: buscador, redes, enlace directo, referencias (Informes → Adquisición).
- **País y ciudad**, idioma, dispositivo (móvil/escritorio), navegador.
- **Visitas, usuarios, sesiones y tiempo de interacción**.

Eso no requiere código extra. Lo verás en GA4 → *Informes → Adquisición* y *→ Datos demográficos / Tecnología*.

## Qué faltaba (y añade este cambio)

GA no mide solo los clics dentro de la página. Para entender **qué hacen** hay que mandar
eventos. El bloque `analytics_eventos_GA4.html` añade estos eventos:

| Evento GA4 | Se dispara cuando… | Parámetros |
|---|---|---|
| `abrir_persona` | abren la ficha de una Persona | `persona_id` |
| `entrevistar_persona` | pulsan 🎙 Entrevistar | `persona_id` |
| `lanzar_encuesta` | pulsan 📋 Lanzar encuesta | — |
| `generar_prompt` | pulsan "Generar prompt" | `persona_id` |
| `usar_filtro` | cambian un filtro | `filtro`, `valor` |
| `limpiar_filtros` | pulsan "Limpiar" | — |

El bloque **no modifica** tus funciones: las envuelve, así que no puede romper la web.

## Cómo desplegarlo (GitHub web, como hiciste con GA)

1. Abre `index.html` en https://github.com/druiz-byte/pueblo-digital → botón editar (lápiz).
2. Baja del todo hasta `</body>`.
3. Pega justo **antes** de `</body>` el contenido de `analytics_eventos_GA4.html`.
4. Commit → *Update index.html*. GitHub Pages redepliega en 1–2 min.

## Cómo verificar que funciona

1. En GA4 → **Administrar → DebugView**, o abre la web y ve a **Informes → Tiempo real**.
2. Navega tu propia web: abre una ficha, pulsa Entrevistar, cambia un filtro.
3. En 10–30 s deben aparecer `abrir_persona`, `usar_filtro`, etc. en Tiempo real.

## Un paso más (recomendado, en GA4, sin código)

- **Marcar eventos clave**: GA4 → *Administrar → Eventos* → activa "Marcar como evento clave"
  en `entrevistar_persona` y `lanzar_encuesta`. Así GA los trata como conversiones y puedes
  medir el % de visitantes que llegan a interactuar de verdad.
- **Dimensiones personalizadas**: para segmentar por `filtro`/`valor`/`persona_id` en los
  informes, GA4 → *Administrar → Definiciones personalizadas → Crear dimensión personalizada*
  (ámbito Evento) para cada parámetro que quieras cruzar. Sin esto los ves en Tiempo real y en
  Exploraciones, pero no en los informes estándar.

## Limpieza pendiente (opcional)

En el `<head>` hay un `<noscript>` de **Google Tag Manager (`GTM-K6Z7RF7G`)** pero **falta el
script de cabecera de GTM**, así que ese contenedor no carga nada: es código muerto. Como mides
con gtag directo, puedes borrar esas 3 líneas del `<noscript>` de GTM sin efecto alguno.

## Nota sobre consentimiento (CookieHub)

Tienes CookieHub instalado, pero GA (`gtag config`) se carga antes del consentimiento. Si quieres
cumplir RGPD de forma estricta, el siguiente paso sería enlazar CookieHub con *Consent Mode v2*
(cargar GA solo tras aceptar). No es necesario para que la analítica funcione, pero es lo correcto
para una web pública en la UE.
