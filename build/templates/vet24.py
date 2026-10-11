"""Layout for 24-hour veterinary clinics ("vet24").

Design idea: the visitor arrives with one of two questions, "is this an
emergency?" or "I want an appointment". The hero answers both at once: the
live time in Colombia says the clinic is open right now, and two large panels
split the paths (call for an emergency, WhatsApp for an appointment). The
services read like the clinic's own storefront window, in wide type.

Typeface: Archivo (variable width), expanded for headings, normal for text.
It does not share structure or type with the clinic template.

render(g) receives the build script's globals (SITE, COPY, THEME, helpers).
"""
import base64
from pathlib import Path

FONT = Path(__file__).resolve().parent.parent / "fonts" / "archivo-latin-standard-normal.woff2"


def render(g):
    S, C, T, e, wa = g["SITE"], g["COPY"], g["THEME"], g["e"], g["wa"]
    hero, facade, data_uri = g["hero"], g["facade"], g["data_uri"]
    WA, PH, STAR = g["WA_ICON"], g["PHONE_ICON"], g["STAR"]
    tel, book = g["tel"], g["book"]
    font = base64.b64encode(FONT.read_bytes()).decode()
    topics = S.get("review_topics", [])

    # Services as storefront-window tiles. A service whose name matches one
    # of Google's review topics is marked, because that is what people
    # actually write about this clinic.
    def mentioned(name):
        n = name.lower()
        return any(t[:6] in n or n[:6] in t for t in topics)

    tiles = []
    for group in S["groups"]:
        for item in group["items"]:
            tag = '<span class="tag">De lo más mencionado en sus reseñas</span>' if mentioned(item["name"]) else ""
            tiles.append(
                f'<li class="tile{" tile-hot" if tag else ""}">{tag}<h3>{e(item["name"])}</h3>'
                f'<p>{e(item["text"])}</p>'
                f'<a href="{e(wa("Hola, quiero información sobre " + item["name"].lower() + "."))}" target="_blank" rel="noopener">Preguntar por WhatsApp</a></li>'
            )
    tiles_html = "".join(tiles)

    topics_html = "".join(f"<li>{e(t)}</li>" for t in topics)
    social = g["SOCIAL"]
    insta = social[0] if social else None
    insta_html = ""
    if insta:
        insta_html = f"""
<section class="insta">
  <div class="wrap">
    <p><b>{e(insta.get('note', ''))}</b> siguen a {e(S['name'])} en {e(insta['network'])}. {e(C.get('social_lead', ''))}</p>
    <a class="btn btn-line" href="{e(insta['url'])}" target="_blank" rel="noopener">Ver @{e(insta['handle'])}</a>
  </div>
</section>"""

    return f"""<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{T['ink']}">
<title>{e(S['name'])}: {e(S['tagline'].lower())} 24 horas en {e(S['city'])} (demo)</title>
<meta name="description" content="{e(S['intro'])}">
<style>
@font-face {{
  font-family: "Archivo";
  src: url(data:font/woff2;base64,{font}) format("woff2");
  font-weight: 100 900; font-stretch: 62% 125%; font-display: swap;
}}
:root {{
  --noche: {T['ink']};
  --azul: {T['accent']};
  --azul-claro: {T['accent_light']};
  --pared: {T['sky']};
  --blanco: #fff;
  --texto: #18233f;
  --gris: #54607a;
  --linea: {T['line']};
  --verde: #1f9d55;
  --ancho: 1240px;
}}
*, *::before, *::after {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }}
body {{ margin: 0; font-family: "Archivo", system-ui, sans-serif; font-stretch: 100%; font-size: 1.0625rem; line-height: 1.55; color: var(--texto); background: var(--blanco); }}
h1, h2, h3, p, ul {{ margin: 0; }}
ul {{ list-style: none; padding: 0; }}
img {{ display: block; max-width: 100%; height: auto; }}
a {{ color: inherit; }}
:focus-visible {{ outline: 3px solid var(--azul-claro); outline-offset: 3px; border-radius: 4px; }}
.wrap {{ width: min(100% - 2.5rem, var(--ancho)); margin-inline: auto; }}
.wide {{ font-stretch: 125%; letter-spacing: -.02em; }}

.demo-bar {{ background: #fff4cc; color: #4a3800; font-size: .875rem; text-align: center; padding: .5rem 1rem; border-bottom: 1px solid #ecd98a; }}

.btn {{ display: inline-flex; align-items: center; justify-content: center; gap: .55rem; min-height: 3.1rem; padding: .7rem 1.4rem; border-radius: .6rem; font: inherit; font-weight: 650; text-decoration: none; border: 2px solid transparent; }}
.btn svg {{ width: 1.3rem; height: 1.3rem; flex: none; }}
.btn-line {{ border-color: var(--noche); color: var(--noche); }}
.btn-line:hover {{ background: var(--noche); color: #fff; }}

/* Encabezado: el teléfono de urgencias siempre a la vista */
.top {{ background: var(--noche); color: #fff; }}
.top .wrap {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding-block: 1rem; }}
.logo {{ font-stretch: 125%; font-weight: 800; font-size: 1.5rem; letter-spacing: -.02em; text-decoration: none; }}
.top-call {{ display: inline-flex; align-items: center; gap: .5rem; text-decoration: none; font-weight: 650; font-size: .9375rem; }}
.top-call svg {{ width: 1.1rem; height: 1.1rem; }}
.top-call span {{ opacity: .75; font-weight: 500; }}

/* Portada */
.hero {{ background: var(--noche); color: #fff; padding-bottom: 3rem; overflow: hidden; }}
.hero .wrap {{ display: grid; gap: 2.5rem; }}
.hero .wrap {{ padding-top: 2.2rem; }}
.status {{ display: inline-flex; align-items: center; gap: .55rem; font-weight: 650; font-size: .9375rem; color: #b9f0cf; }}
.status .dot {{ width: .65rem; height: .65rem; border-radius: 50%; background: #3fd17f; animation: pulse 2.4s ease-out infinite; }}
@keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(63,209,127,.55); }} 70%, 100% {{ box-shadow: 0 0 0 .6rem rgba(63,209,127,0); }} }}
.clock {{ margin-top: 1.2rem; font-stretch: 125%; font-weight: 800; letter-spacing: -.035em; line-height: .92; }}
.clock .time {{ display: block; font-size: clamp(3.4rem, 15vw, 7rem); font-variant-numeric: tabular-nums; white-space: nowrap; }}
.clock .rest {{ display: block; margin-top: .4rem; font-size: clamp(1.6rem, 4.2vw, 2.6rem); font-weight: 700; color: #cfdaf5; }}
.hero .intro {{ margin-top: 1.6rem; max-width: 46ch; color: #cfdaf5; }}
.paths {{ display: grid; gap: .9rem; margin-top: 2rem; }}
.path {{ display: grid; gap: .25rem; padding: 1.3rem 1.4rem; border-radius: 1rem; text-decoration: none; }}
.path small {{ font-size: .9375rem; font-weight: 550; }}
.path b {{ display: flex; align-items: center; gap: .6rem; font-stretch: 112%; font-size: 1.45rem; font-weight: 750; letter-spacing: -.01em; }}
.path b svg {{ width: 1.5rem; height: 1.5rem; flex: none; }}
.path-urgent {{ background: #fff; color: var(--noche); }}
.path-urgent small {{ color: #b3261e; }}
.path-book {{ background: var(--azul); color: #fff; }}
.path-book small {{ color: #dbe6ff; }}
.path:hover {{ outline: 3px solid var(--azul-claro); outline-offset: 2px; }}
.hero figure {{ margin: 0; position: relative; }}
.hero figure img {{ width: 100%; aspect-ratio: 4 / 3; object-fit: cover; object-position: {S['hero'].get('position', '50% 50%')}; border-radius: 1rem; }}
.hero figure figcaption {{ margin-top: .7rem; font-size: .875rem; color: #9fb0d8; }}

/* Vitrina de servicios */
.window {{ padding-block: 4.5rem; background: var(--pared); }}
.window h2, .rating h2, .visit h2 {{ font-stretch: 125%; font-weight: 800; letter-spacing: -.03em; line-height: 1; font-size: clamp(2rem, 5.5vw, 3.4rem); color: var(--noche); }}
.window .lead {{ margin-top: .9rem; max-width: 52ch; color: var(--gris); }}
.tiles {{ display: grid; gap: 1px; margin-top: 2.5rem; background: var(--linea); border: 1px solid var(--linea); border-radius: 1rem; overflow: hidden; }}
.tile {{ background: #fff; padding: 1.5rem 1.4rem 1.4rem; display: flex; flex-direction: column; gap: .45rem; }}
.tile h3 {{ font-stretch: 118%; font-weight: 750; font-size: 1.35rem; letter-spacing: -.015em; color: var(--noche); line-height: 1.1; }}
.tile p {{ color: var(--gris); font-size: 1rem; flex: 1; }}
.tile a {{ margin-top: .4rem; font-weight: 650; font-size: .9375rem; color: var(--azul); text-underline-offset: .3em; text-decoration-thickness: 2px; }}
.tile .tag {{ align-self: flex-start; font-size: .8125rem; font-weight: 650; color: #13703f; background: #e3f5ea; padding: .2rem .6rem; border-radius: .4rem; }}
.tile-hot {{ box-shadow: inset 0 4px 0 var(--verde); }}

/* Calificación */
.rating {{ padding-block: 4.5rem; }}
.rating .wrap {{ display: grid; gap: 2rem; align-items: end; }}
.score {{ font-stretch: 125%; font-weight: 800; font-size: clamp(5rem, 16vw, 9rem); line-height: .85; letter-spacing: -.05em; color: var(--noche); }}
.score small {{ font-size: .32em; letter-spacing: -.01em; color: var(--gris); font-weight: 650; }}
.stars {{ display: inline-flex; gap: 2px; color: #f0ab1c; margin-top: 1rem; }}
.stars svg {{ width: 1.5rem; height: 1.5rem; }}
.stars .off {{ opacity: .3; }}
.rating p {{ margin-top: .7rem; color: var(--gris); max-width: 44ch; }}
.topics {{ display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1rem; }}
.topics li {{ font-weight: 600; font-size: .9375rem; padding: .35rem .85rem; border-radius: .5rem; background: var(--pared); color: var(--noche); }}

/* Visita */
.visit {{ padding-block: 4.5rem; background: var(--noche); color: #fff; }}
.visit h2 {{ color: #fff; }}
.visit .wrap {{ display: grid; gap: 2.5rem; }}
.visit address {{ margin-top: 1.2rem; font-style: normal; font-stretch: 112%; font-size: 1.5rem; font-weight: 700; line-height: 1.25; }}
.visit .hint {{ margin-top: .8rem; color: #cfdaf5; max-width: 42ch; }}
.visit .actions {{ display: flex; flex-wrap: wrap; gap: .8rem; margin-top: 1.6rem; }}
.visit .btn-solid {{ background: #fff; color: var(--noche); }}
.visit .btn-ghost {{ border-color: #fff; color: #fff; }}
.visit .btn-ghost:hover {{ background: #fff; color: var(--noche); }}
.visit figure {{ margin: 0; }}
.visit figure img {{ width: 100%; aspect-ratio: 4 / 3; object-fit: cover; object-position: {S['facade'].get('position', '50% 50%')}; border-radius: 1rem; }}
.map {{ margin-top: 1rem; border-radius: 1rem; overflow: hidden; aspect-ratio: 16 / 9; background: #23367a; position: relative; display: grid; place-items: center; }}
.map span {{ color: #cfdaf5; font-size: .9375rem; padding: 1rem; text-align: center; }}
.map iframe {{ position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }}

.insta {{ padding-block: 2.5rem; border-bottom: 1px solid var(--linea); }}
.insta .wrap {{ display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1.2rem; }}
.insta p {{ max-width: 60ch; color: var(--gris); }}
.insta b {{ color: var(--noche); font-stretch: 112%; }}

footer {{ padding-block: 2.5rem 7rem; font-size: .9375rem; color: var(--gris); }}
footer .wrap {{ display: grid; gap: 1.2rem; }}
footer a {{ color: var(--noche); font-weight: 600; text-underline-offset: .25em; }}
footer .note {{ font-size: .8125rem; border-top: 1px solid var(--linea); padding-top: 1.2rem; }}

.bar {{ position: fixed; inset: auto 0 0 0; z-index: 20; display: grid; grid-template-columns: 1fr 1fr; gap: .5rem; padding: .6rem .8rem calc(.6rem + env(safe-area-inset-bottom)); background: rgba(255,255,255,.96); backdrop-filter: blur(8px); border-top: 1px solid var(--linea); }}
.bar[hidden] {{ display: none; }}
.bar a {{ min-height: 3rem; font-size: .9375rem; }}
.bar .b-call {{ background: var(--noche); color: #fff; }}
.bar .b-wa {{ background: var(--azul); color: #fff; }}

@media (min-width: 900px) {{
  body {{ font-size: 1.125rem; }}
  .bar {{ display: none; }}
  footer {{ padding-bottom: 2.5rem; }}
  .hero {{ padding-bottom: 4.5rem; }}
  .hero .wrap {{ grid-template-columns: minmax(0, 1.4fr) minmax(0, .6fr); gap: 3.5rem; align-items: center; padding-top: 3.5rem; }}
  .hero figure img {{ aspect-ratio: 3 / 4; }}
  .paths {{ grid-template-columns: 1fr 1fr; }}
  .tiles {{ grid-template-columns: repeat(4, 1fr); }}
  .window, .rating, .visit {{ padding-block: 6rem; }}
  .rating .wrap {{ grid-template-columns: auto 1fr; gap: 4rem; }}
  .visit .wrap {{ grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 4rem; align-items: start; }}
  footer .wrap {{ grid-template-columns: 1.3fr 1fr 1fr; }}
  footer .note {{ grid-column: 1 / -1; }}
}}
@media (min-width: 600px) and (max-width: 899px) {{
  .tiles {{ grid-template-columns: 1fr 1fr; }}
  .paths {{ grid-template-columns: 1fr 1fr; }}
}}
@media (prefers-reduced-motion: reduce) {{
  html {{ scroll-behavior: auto; }}
  .status .dot {{ animation: none; }}
}}
</style>
</head>
<body>
<div class="demo-bar" role="note"><strong>Página de muestra.</strong> Es una propuesta de diseño, no el sitio oficial de {e(S['name'])}.</div>

<header class="top">
  <div class="wrap">
    <a class="logo" href="#inicio">{e(S['name'])}</a>
    <a class="top-call" href="{tel}">{PH}<span>Urgencias</span> {e(S['phone_display'])}</a>
  </div>
</header>

<main id="inicio">
  <section class="hero">
    <div class="wrap">
      <div>
      <p class="status"><span class="dot" aria-hidden="true"></span>Abierto ahora en {e(S['city'])}</p>
      <h1 class="clock">
        <span class="js-clock" hidden><span class="time"><time class="now"></time></span><span class="rest">y {e(S['name'])} está abierto.</span></span>
        <span class="no-js"><span class="time">24 horas</span><span class="rest">{e(S['name'])} no cierra.</span></span>
      </h1>
        <p class="intro">{e(S['intro'])}</p>
        <div class="paths">
          <a class="path path-urgent" href="{tel}"><small>¿Es una urgencia? Llama ya</small><b>{PH}{e(S['phone_display'])}</b></a>
          <a class="path path-book" href="{book}" target="_blank" rel="noopener"><small>¿Quieres una cita? Escríbenos</small><b>{WA}{e(S['whatsapp_display'])}</b></a>
        </div>
      </div>
      <figure>
        <img src="{data_uri(hero, 80)}" width="{hero.width}" height="{hero.height}" alt="{e(S['hero']['alt'])}">
        <figcaption>La recepción de {e(S['name'])}, en {e(S['area'])}, {e(S['city'])}.</figcaption>
      </figure>
    </div>
  </section>

  <section class="window" id="servicios">
    <div class="wrap">
      <h2>Todo en la misma sede</h2>
      <p class="lead">Lo mismo que anuncia la vitrina de la clínica. Pregunta por cualquier servicio y te responden por WhatsApp.</p>
      <ul class="tiles">{tiles_html}</ul>
    </div>
  </section>

  <section class="rating" id="opiniones">
    <div class="wrap">
      <div>
        <p class="score">{e(S['rating'])}<small> /5</small></p>
        <span class="stars" role="img" aria-label="{e(g['stars_label'])}">{g['stars_html']}</span>
      </div>
      <div>
        <h2>{g['reviews_n']} reseñas en Google</h2>
        <p>Es la calificación promedio que le dan sus {e(C['reviewers'])}, a {e(S['reviews_asof'])}. Lo que más mencionan:</p>
        <ul class="topics">{topics_html}</ul>
        <p><a class="btn btn-line" href="{e(S['maps_url'])}" target="_blank" rel="noopener">Leer las reseñas en Google</a></p>
      </div>
    </div>
  </section>
{insta_html}
  <section class="visit" id="ubicacion">
    <div class="wrap">
      <div>
        <h2>Cómo llegar</h2>
        <address>{e(S['address'])}<br>{e(S['area'])}, {e(S['city'])}</address>
        <p class="hint">{e(S['entrance_hint'])}</p>
        <div class="actions">
          <a class="btn btn-solid" href="{e(S['maps_url'])}" target="_blank" rel="noopener">Abrir en Google Maps</a>
          <a class="btn btn-ghost" href="{e(wa(C['directions_wa']))}" target="_blank" rel="noopener">Pedir indicaciones</a>
        </div>
      </div>
      <div>
        <figure><img src="{data_uri(facade, 80)}" width="{facade.width}" height="{facade.height}" loading="lazy" alt="{e(S['facade']['alt'])}"></figure>
        <div class="map">
          <span>{e(g['full_address'])}</span>
          <iframe title="Mapa de {e(S['name'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={g['quote'](S['maps_embed_q'])}&output=embed"></iframe>
        </div>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <div><a class="logo" href="#inicio" style="color:var(--noche)">{e(S['name'])}</a><br>{e(S['tagline'])}</div>
    <div>{e(S['address'])}<br>{e(S['area'])}, {e(S['city'])}</div>
    <div>
      <a href="{tel}">Teléfono {e(S['phone_display'])}</a><br>
      <a href="{book}" target="_blank" rel="noopener">WhatsApp {e(S['whatsapp_display'])}</a><br>
      {g['social_footer']}
    </div>
    <p class="note">Página de muestra creada como propuesta de diseño; no es el sitio oficial de {e(S['name'])}. {e(C['sources'])}</p>
  </div>
</footer>

<nav class="bar" aria-label="Contacto rápido">
  <a class="btn b-call" href="{tel}">{PH}Llamar</a>
  <a class="btn b-wa" href="{book}" target="_blank" rel="noopener">{WA}WhatsApp</a>
</nav>

<script>
(function () {{
  var bar = document.querySelector('.bar'), paths = document.querySelector('.paths');
  if (!bar || !paths || !('IntersectionObserver' in window)) return;
  new IntersectionObserver(function (en) {{ bar.hidden = en[0].isIntersecting; }}).observe(paths);
}})();
(function () {{
  var t = document.querySelector('.now');
  if (!t || !window.Intl) return;
  var fmt = new Intl.DateTimeFormat('es-CO', {{ hour: 'numeric', minute: '2-digit', hour12: true, timeZone: 'America/Bogota' }});
  function tick() {{ t.textContent = fmt.format(new Date()).replace(/\\u00a0/g, ' '); }}
  tick(); setInterval(tick, 20000);
  document.querySelector('.js-clock').hidden = false;
  document.querySelector('.no-js').hidden = true;
}})();
</script>
</body>
</html>
"""
