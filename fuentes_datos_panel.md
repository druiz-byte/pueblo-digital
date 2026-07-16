# Fuentes de datos para el rediseño del panel

> Inventario de encuestas con **microdatos** que podrían alimentar la nueva versión de Pueblo Digital.
> Objetivo: pasar de "3 encuestas unidas por 4 llaves" a fuentes con **muchas variables de enlace** (idealmente una sola encuesta que traiga los 4 dominios: sociodemográfico + político + medios + bienestar).
> Llaves de enlace que ya tiene el Deustobarómetro: **sexo, edad, hábitat (tamaño de ciudad), provincia, nivel educativo**.

---

## Resumen

| Fuente | Ámbito | Dominios | Microdatos | Formato | Licencia | Muestra vasca |
|---|---|---|---|---|---|---|
| **Sociómetro Vasco** (GPS, GV) | País Vasco | Política, instituciones, economía, identidad; medios/calidad de vida en monográficos | **Abiertos** | SAV + CSV | CC BY-NC 3.0 | **~3.000/ola** |
| **EUSTAT — Enc. Bienestar Personal (EBP)** | País Vasco | Bienestar (9 indicadores) | **Abiertos** | fichero microdatos | uso científico | Grande |
| **EUSTAT — Soc. de la Información. Familias (ESI)** | País Vasco | TIC / internet / medios digitales | **Abiertos** | fichero microdatos | uso científico | Grande |
| **EUSTAT — Enc. Condiciones de Vida (ECV)** | País Vasco | Renta, exclusión, hábitos y relaciones sociales | **Abiertos** | fichero microdatos | uso científico | Grande |
| **EPDS** (Justicia/GV) | País Vasco | Pobreza y desigualdad, cada 4 años | Bajo petición | SPSS | investigación | Grande |
| **ESS — European Social Survey** | Europa/España | **Los 4 dominios en un cuestionario** | Abiertos (registro) | SPSS/Stata/CSV | uso científico | Pequeña (submuestra ES) |
| **CIS — barómetros** | España | Política (medios/bienestar en monográficos ≠) | **Abiertos** | SPSS/ASCII | reutilización | Pequeña por ola |
| **Euskobarómetro** (UPV/EHU) | País Vasco | Política vasca | Restringido | — | bajo petición | Media |
| **Deustobarómetro** (propio) | País Vasco | **Los 141 ítems objetivo** | Interno UD | — | — | ~1.000 |

---

## Sociómetro Vasco — Gabinete de Prospección Sociológica (Gobierno Vasco)

La mejor combinación de **muestra vasca grande** (~3.000 entrevistas/ola) y **microdato abierto**.

- **Descarga:** catálogo en Open Data Euskadi, un paquete por ola (SAV + CSV + informe PDF + cuestionario).
  - Catálogo: https://opendata.euskadi.eus/catalogo-datos/
  - Última ola localizada: **Sociómetro 89** — https://opendata.euskadi.eus/catalogo/-/informes-estudios/sociometro-89/
  - Ejemplo verificado (SV83, marzo 2024): CSV https://opendata.euskadi.eus/contenidos/ds_informes_estudios/od_24sv83/opendata/24sv83.csv · SAV https://opendata.euskadi.eus/contenidos/ds_informes_estudios/od_24sv83/opendata/24sv83_etik.sav
- **Estructura del fichero (comprobada en SV83):** una fila por entrevistado; columnas `elkar`, `inkes`, `lurral` (territorio histórico), `tfno`, `P0A`, `P0B`, `P01…P39`, y `wt` (peso). **Los nombres de columna son códigos de pregunta**, así que hace falta el **cuestionario/codebook** del PDF de la misma ola para interpretarlos.
- **Avisos metodológicos:** hay que **ponderar por `wt`** para reproducir los resultados publicados; los municipios de <5.000 habitantes se codifican como `999` para anonimizar (esto afecta a la variable *hábitat*).
- **Enlace con el Deustobarómetro:** seguro sexo, edad, euskera, estudios, situación laboral y provincia (`lurral`); **hábitat** presente pero con el tope de anonimización.
- **Ojo:** las olas "de previsión de voto" (como SV83/89) son sobre todo políticas; para máxima cobertura sociodemográfica conviene una ola **monográfica** (medios, calidad de vida) de la serie.

## EUSTAT — portal de microdatos (descarga libre)

EUSTAT publica microdatos anonimizados de descarga libre. Portal: https://www.eustat.eus/prodserv/fich_microdatos_c.html

Encuestas relevantes para el panel:

- **Encuesta de Bienestar Personal (EBP)** — la que **ya usáis** para injertar bienestar. Nueve indicadores: satisfacción con la vida, valor de la vida, satisfacción con el ocio, con la vivienda/entorno, con la economía doméstica, estado de ánimo, relaciones personales, confianza en las personas y confianza en las autoridades. Microdatos: https://es.eustat.eus/estadisticas/tema_632/opt_1/tipo_11/temas.html · Ficha: https://www.eustat.eus/document/ebp_c.html
- **Encuesta sobre la Sociedad de la Información — Familias (ESI)** — **la pieza que hoy falta bien**: equipamiento y uso de TIC e internet en el hogar. Cubre el dominio "medios digitales/consumo" con microdato vasco propio, en vez de injertarlo de la encuesta de medios de Gizaker. Microdatos: https://www.eustat.eus/estadisticas/tema_15/opt_1/tipo_11/ti_encuesta-sobre-la-sociedad-de-la-informacion/temas.html
- **Encuesta de Condiciones de Vida (ECV)** — renta, exclusión social y **hábitos y relaciones sociales** (armonizada con EU-SILC). Útil para bienestar material y capital social. Microdatos: https://www.eustat.eus/estadisticas/tema_76/opt_1/tipo_11/ti_encuesta-de-condiciones-de-vida/temas.html
- **Marginales de población / censo (Eustat)** — imprescindibles para la **post-estratificación**: estructura por territorio × sexo × edad × euskera (Mapa Sociolingüístico) y por hábitat. Ya se usan para calibrar.

## EPDS — Encuesta de Pobreza y Desigualdades Sociales (Dpto. Justicia/GV)

Cuatrienal (última EPDS 2024). Muy fuerte en pobreza, privación y desigualdad. Microdatos bajo petición. Ficha: https://www.euskadi.eus/encuesta-de-pobreza-y-desigualdades-sociales-epds/web01-a2ogaeko/es/

## ESS — European Social Survey (España)

La única que trae **los cuatro dominios en un mismo cuestionario** (medios, política y voto, identidad/inmigración, bienestar personal y social, valores Schwartz) con **el bloque sociodemográfico más completo** de las encuestas comparadas (sexo, edad, educación, región NUTS-2 → ES21 País Vasco, tamaño de hábitat `domicil`, situación laboral, ocupación/clase ISCO, ingresos, hogar, religión, lengua del hogar). Registro gratuito. Portal: https://www.europeansocialsurvey.org/data-portal

- **Uso recomendado:** *donante rico* para importar medios y bienestar emparejando por muchas más llaves que las 4 actuales (añadiendo laboral, clase e ideología). Pega: submuestra vasca pequeña.

## CIS — barómetros (España)

Microdatos **abiertos desde 2009** con un juego de llaves muy completo (sexo, edad, CCAA + provincia + tamaño de municipio, estudios, situación laboral, clase subjetiva, religiosidad, recuerdo de voto, ideología 1–10). Contenido de medios/bienestar en estudios monográficos aparte. Portal: https://www.cis.es

## Euskobarómetro — UPV/EHU

Serie política vasca larga; microdatos de **acceso restringido** (series e indicadores públicos; microdato bajo petición). https://www.ehu.eus/es/web/euskobarometro/home

## Deustobarómetro (fuente propia)

Contiene **exactamente los 141 ítems objetivo**. Si se accede a su microdato (interno de la UD), sería el **ancla ideal**: cada Persona sería un encuestado real con el cuestionario ya respondido → opción B pura para el panel objetivo, sin injerto para el bloque político.

---

## Matriz de llaves de enlace (variables verificadas en los microdatos)

Cotejo de las variables de enlace en las tres fuentes ya descargadas y perfiladas, frente al Deustobarómetro. `✓` = presente y limpia · `~` = derivable/aproximada · `✗` = no está.

| Variable de enlace | Deustobarómetro | Sociómetro 83 (n=3.030) | ESS España (n=21.296; PV=671) | Capital Social 2022 (n=5.798) |
|---|---|---|---|---|
| **Sexo** | ✓ | ✓ `P01` | ✓ `gndr` | ✓ `SEXO` |
| **Edad** | ✓ (exacta) | ✓ `P02` (exacta) | ✓ `agea` (exacta) | ~ `EDADR` (quinquenal) |
| **Provincia / territorio** | ✓ | ✓ `lurral` | ✓ `region` (ES21; solo rondas recientes) | ✓ `TERH` |
| **Hábitat (tamaño municipio)** | ✓ | ~ `P0B` (<5.000 = 999) | ✓ `domicil` (5 categorías) | ✓ `TMUN` (1–3) |
| **Nivel educativo** | ✓ | ✓ `P33` | ✓ `eisced`/`edulvlb` | ✗ |
| Euskera (competencia) | ✓ | ✓ `P32` (5 niveles) | ~ `lnghom` (lengua hogar) | ~ `IDENTR` (idioma entrevista) |
| Clase social | ✓ | ✓ `P34` | ~ `isco08` (ocupación) | ✓ `CLASER` |
| Situación laboral | ✓ | ✓ `P03` | ✓ `mnactic` | ✓ `RELAR` |
| Ideología (0–10) | ✓ | ✓ `P28` | ✓ `lrscale` | ✗ (solo `INTPOL` interés) |
| Recuerdo de voto | ✓ | ✓ `P23` | ✓ `prtvtes` | ✗ |

**Núcleo común a las cuatro:** sexo, edad, provincia y hábitat → 4 llaves universales (con dos armonizaciones pendientes: la edad hay que llevarla a **tramos quinquenales** porque Capital Social solo da grupos; y el hábitat hay que unificar entre `TMUN` 1–3, `domicil` de 5 categorías y el tamaño de municipio del resto).

**Diferencias que condicionan el diseño:**
- **Educación** está en Deusto/Sociómetro/ESS pero **no** en Capital Social → para injertar capital social hay que renunciar a esa llave.
- **Euskera** solo es llave limpia en Sociómetro (y Deustobarómetro). En ESS y Capital Social son proxies débiles → el euskera solo puede usarse como llave si el **ancla** es Sociómetro/Deustobarómetro.
- **Ideología y voto** están en Deusto/Sociómetro/ESS → sirven de llave extra para injertar el ESS, pero no el capital social.

## Estrategia de emparejamiento propuesta

Tres pasos, del ancla hacia los donantes, ampliando las llaves respecto a las 4 actuales:

1. **Ancla — Sociómetro Vasco** (o microdatos propios del Deustobarómetro). Aporta el bloque sociodemográfico + político con las correlaciones reales (voto × ideología × euskera × nacionalismo). Llaves disponibles: sexo, edad, provincia, hábitat, educación, euskera, clase, situación laboral, ideología, voto.

2. **Injerto ESS → medios y bienestar.** Emparejar por **sexo × edad × educación × hábitat × situación laboral** (+ ideología, + provincia si el n lo permite). El euskera no entra (ESS no lo mide). Por los 671 casos vascos, emparejar con **toda la muestra española** asumiendo que la estructura medios/bienestar es española, no específicamente vasca.

3. **Injerto Capital Social → confianza, redes, participación, cohesión, felicidad/salud.** Emparejar por **sexo × edad × provincia × hábitat** (+ clase o relación con la actividad como refuerzo). Sin educación, sin euskera limpio y sin ideología. Ventaja: muestra vasca nativa y grande. Nota: el contenido son **índices 0–10 ya construidos**, así que la Persona recibe *scores* (p. ej. confianza institucional), no ítems.

Método por celda igual que ahora (k-NN exacto sobre la celda de llaves, con retroceso a menos variables si la celda queda vacía), pero con **6–8 llaves** en lugar de 4, lo que reduce la ruptura de correlaciones entre bloques que hoy penaliza el contraste.

---

## Cómo descargar (nota práctica)

Desde este entorno puedo **inspeccionar** los ficheros (he verificado la estructura del CSV del Sociómetro), pero no puedo volcar ficheros grandes completos al disco. Para descargarlos en tu ordenador tienes el script `descargar_fuentes.py` en esta misma carpeta: bájalos ahí y luego los abrimos y perfilamos juntos. Los de EUSTAT requieren un par de clics en su portal (no tienen URL directa estable), así que quedan como enlaces.
