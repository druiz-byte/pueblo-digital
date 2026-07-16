# Pueblo Digital

Panel sintético de 1.000 **Personas** representativas de la población del País Vasco, construidas a partir de microdatos reales de encuestas oficiales (Deusto Barómetro, Sociómetro Vasco, ESS, EUSTAT). Cada Persona puede instanciarse como agente conversacional que responde de forma coherente con su perfil sociodemográfico, político, mediático y de bienestar (fundamento: *silicon sampling*, Argyle et al. 2023).

Autor: David Ruiz (Universidad de Deusto, druiz@deusto.es).

## Arquitectura online

El proyecto tiene dos piezas que se despliegan por separado:

| Pieza | Qué es | Dónde se aloja |
|---|---|---|
| **Panel** (`index.html`, `panel_pais_vasco_v2.html`, `cuestionario_barometro_digital.html`) | HTML autocontenido con los datos embebidos. Muestra las 1.000 Personas, permite filtrar, ver fichas y abrir la entrevista. | **GitHub Pages** (estático, gratis, público) |
| **Entrevista** (`entrevista/server_v2.py` + `entrevista/public/`) | Backend Python que sirve la ficha, conecta el avatar (HeyGen/LiveAvatar vía LiveKit) y responde como la Persona (Claude Haiku). | **Render** (servicio web, con contraseña) |

El botón **Entrevistar** del panel abre la app de entrevista en modo enfocado (`?id=NN` → solo ficha · avatar · conversación). En local usa `http://localhost:3000`; online usa la URL de Render (constante `ENTREVISTA_RENDER_URL` en `index.html`).

## Datos que NO están en el repositorio

Por licencia de los proveedores y por protección de datos, el `.gitignore` excluye los **microdatos reales** (ESS, `.sav` del Deustobarómetro, Sociómetro, Capital Social), los **PDFs académicos** con copyright y las **claves de API** (`.env`, `.env.txt`). El repo contiene solo código, paneles y el JSON sintético de las Personas (que no es dato personal real).

## Ejecutar en local

```bash
cd entrevista
cp .env.example .env          # y rellena HEYGEN_API_KEY y ANTHROPIC_API_KEY
python server_v2.py           # sirve el panel v2 en http://localhost:3000
```

Abre `index.html` (raíz) y pulsa **Entrevistar** en cualquier ficha. En local `SITE_PASSWORD` puede quedar vacía (acceso libre).

## Poner online

### 1. Subir a GitHub

```bash
# (una vez, en la carpeta del proyecto)
git init
git add .
git commit -m "Pueblo Digital: panel + app de entrevista"
git branch -M main
git remote add origin https://github.com/<tu-usuario>/pueblo-digital.git
git push -u origin main
```

### 2. Publicar el panel (GitHub Pages)

En el repo → **Settings → Pages** → *Build and deployment* → **Deploy from a branch** → rama `main`, carpeta `/ (root)` → *Save*. En un par de minutos el panel estará en `https://<tu-usuario>.github.io/pueblo-digital/`.

### 3. Desplegar la entrevista (Render)

1. En [render.com](https://render.com) → **New → Blueprint** → conecta el repo. Render leerá `render.yaml`.
2. Rellena las tres variables de entorno cuando lo pida:
   - `HEYGEN_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `SITE_PASSWORD` (elige una contraseña; con ella se protege el acceso)
3. Al terminar, Render da una URL tipo `https://pueblo-digital-entrevista.onrender.com`.

### 4. Conectar el panel con la entrevista

En `index.html`, sustituye el placeholder por tu URL de Render:

```js
const ENTREVISTA_RENDER_URL = "https://pueblo-digital-entrevista.onrender.com";
```

Haz `commit` + `push`. Listo: cualquiera puede ver el panel; al pulsar **Entrevistar** el navegador pedirá la contraseña de la app de entrevista.

## Seguridad

- Las claves de API viven solo en `.env` (local) y en las variables de entorno de Render (online). Nunca se suben al repo.
- La app de entrevista está protegida por contraseña (`SITE_PASSWORD`) porque cada entrevista consume créditos de HeyGen y Anthropic.

## Documentación

- `CLAUDE.md` — contexto y estado del proyecto.
- `bitacora.md` — registro cronológico de sesiones.
- `resumen_construccion_panel.md` — metodología de construcción del panel.
- `literatura_relacionada.md` — revisión de literatura.
