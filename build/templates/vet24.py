"""Layout for 24-hour veterinary clinics ("vet24").

Tone: calm, clean and trustworthy, like a good clinic's reception. Light
backgrounds, one friendly typeface (Figtree), the clinic's blue for actions
and navy for text. The live time is a small detail in the status pill, not
the headline. Urgent care gets its own contained card, not a full-width slab.

Differs from the clinic layout in type (Figtree vs Bricolage), hero
composition, grouped service cards with one action each, the score card and
the visit section with a facade thumbnail next to the map.

render(g) receives the build script's globals (SITE, COPY, THEME, helpers).
"""
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from icons import icon  # noqa: E402

FONT = Path(__file__).resolve().parent.parent / "fonts" / "figtree-latin-wght-normal.woff2"

# Lucide icons for the service groups, in the order they appear.
ICON_NAMES = ["lucide/stethoscope", "lucide/microscope", "lucide/hospital", "lucide/paw-print"]


def render(g):
    S, C, T, e, wa = g["SITE"], g["COPY"], g["THEME"], g["e"], g["wa"]
    hero, facade, data_uri = g["hero"], g["facade"], g["data_uri"]
    WA, PH = g["WA_ICON"], g["PHONE_ICON"]
    tel, book = g["tel"], g["book"]
    font = base64.b64encode(FONT.read_bytes()).decode()

    groups = []
    for i, group in enumerate(S["groups"]):
        items = "".join(f'<li><b>{e(it["name"])}</b><span>{e(it["text"])}</span></li>' for it in group["items"])
        ask = wa(f"Hola, quiero información sobre {group['title'].lower()}.")
        groups.append(
            f'<article class="card"><div class="icon">{icon(ICON_NAMES[i % len(ICON_NAMES)])}</div>'
            f'<h3>{e(group["title"])}</h3><p class="card-lead">{e(group["lead"])}</p><ul>{items}</ul>'
            f'<a class="card-link" href="{e(ask)}" target="_blank" rel="noopener">Preguntar por WhatsApp</a></article>'
        )
    groups_html = "".join(groups)

    topics_html = "".join(f"<li>{e(t)}</li>" for t in S.get("review_topics", []))
    insta = g["SOCIAL"][0] if g["SOCIAL"] else None
    insta_html = ""
    if insta:
        insta_html = f"""
  <section class="insta">
    <div class="wrap">
      <a class="insta-card" href="{e(insta['url'])}" target="_blank" rel="noopener">
        <span class="insta-icon">{icon("brands/instagram")}</span>
        <span><b>@{e(insta['handle'])}</b><small>{e(insta.get('note', ''))} en {e(insta['network'])}. {e(C.get('social_lead', ''))}</small></span>
        <span class="insta-go">Ver perfil</span>
      </a>
    </div>
  </section>"""

    urgent = S.get("urgent", {})

    return f"""<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(S['name'])}: {e(S['tagline'].lower())} 24 horas en {e(S['city'])} (demo)</title>
<meta name="description" content="{e(S['intro'])}">
<style>
@font-face {{
  font-family: "Figtree";
  src: url(data:font/woff2;base64,{font}) format("woff2");
  font-weight: 300 900; font-display: swap;
}}
:root {{
  --navy: {T['ink']};
  --azul: {T['accent']};
  --azul-hover: #1f4f9e;
  --suave: {T['sky']};
  --linea: {T['line']};
  --texto: #1d2742;
  --gris: #5a6683;
  --verde: #1f8a4c;
  --verde-bg: #e4f4ea;
  --radio: 1.25rem;
  --ancho: 1160px;
}}
*, *::before, *::after {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }}
body {{ margin: 0; font-family: "Figtree", system-ui, sans-serif; font-size: 1.0625rem; line-height: 1.6; color: var(--texto); background: #fff; }}
h1, h2, h3, p, ul {{ margin: 0; }}
ul {{ list-style: none; padding: 0; }}
img {{ display: block; max-width: 100%; height: auto; }}
a {{ color: inherit; }}
:focus-visible {{ outline: 3px solid var(--azul); outline-offset: 3px; border-radius: 6px; }}
.wrap {{ width: min(100% - 2.5rem, var(--ancho)); margin-inline: auto; }}
h1, h2 {{ color: var(--navy); font-weight: 750; letter-spacing: -.02em; text-wrap: balance; }}
h2 {{ font-size: clamp(1.9rem, 4vw, 2.6rem); line-height: 1.12; }}
.lead {{ margin-top: .7rem; color: var(--gris); max-width: 52ch; }}

.demo-bar {{ background: #fff4cc; color: #4a3800; font-size: .875rem; text-align: center; padding: .5rem 1rem; border-bottom: 1px solid #ecd98a; }}

.btn {{ display: inline-flex; align-items: center; justify-content: center; gap: .55rem; min-height: 3.1rem; padding: .7rem 1.4rem; border-radius: 999px; font: inherit; font-weight: 650; text-decoration: none; border: 2px solid transparent; transition: background-color .15s, color .15s; }}
.btn svg {{ width: 1.25rem; height: 1.25rem; flex: none; }}
.btn-primary {{ background: var(--azul); color: #fff; }}
.btn-primary:hover {{ background: var(--azul-hover); }}
.btn-outline {{ border-color: var(--linea); color: var(--navy); background: #fff; }}
.btn-outline:hover {{ border-color: var(--navy); }}
.btn-white {{ background: #fff; color: var(--navy); }}

/* Encabezado */
.top {{ border-bottom: 1px solid var(--linea); background: #fff; }}
.top .wrap {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; min-height: 4.5rem; }}
.brand {{ text-decoration: none; line-height: 1.1; }}
.brand b {{ display: block; font-size: 1.45rem; font-weight: 800; color: var(--navy); letter-spacing: -.02em; }}
.brand span {{ font-size: .8125rem; color: var(--gris); }}
.top nav {{ display: flex; align-items: center; gap: 1.6rem; }}
.top nav a:not(.top-call) {{ display: none; text-decoration: none; font-weight: 550; color: var(--texto); }}
.top nav a:not(.top-call):hover {{ color: var(--azul); }}
.top-call {{ display: inline-flex; align-items: center; gap: .45rem; text-decoration: none; font-weight: 650; color: var(--navy); background: var(--suave); padding: .55rem 1rem; border-radius: 999px; font-size: .9375rem; white-space: nowrap; }}
.top-call svg {{ width: 1rem; height: 1rem; color: var(--azul); }}

/* Portada */
.hero {{ padding-block: 2.5rem 3rem; }}
.hero .wrap {{ display: grid; gap: 2.5rem; align-items: center; }}
.status {{ display: inline-flex; align-items: center; gap: .55rem; font-size: .9375rem; font-weight: 600; color: var(--verde); background: var(--verde-bg); padding: .4rem .9rem .4rem .75rem; border-radius: 999px; }}
.status .dot {{ width: .55rem; height: .55rem; border-radius: 50%; background: #2fbf6b; animation: pulse 2.4s ease-out infinite; }}
.status time {{ font-variant-numeric: tabular-nums; }}
@keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(47,191,107,.5); }} 70%, 100% {{ box-shadow: 0 0 0 .5rem rgba(47,191,107,0); }} }}
.hero h1 {{ margin-top: 1.1rem; font-size: clamp(2.3rem, 5.4vw, 3.75rem); line-height: 1.06; }}
.hero .intro {{ margin-top: 1.1rem; color: var(--gris); font-size: 1.125rem; max-width: 46ch; }}
.hero .actions {{ display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 1.8rem; }}
.trust {{ display: flex; align-items: center; gap: .6rem; margin-top: 1.5rem; font-size: .9375rem; color: var(--gris); text-decoration: none; }}
.trust:hover span:last-child {{ text-decoration: underline; text-underline-offset: .25em; }}
.stars {{ display: inline-flex; gap: 1px; color: #f2a516; }}
.stars svg {{ width: 1.05rem; height: 1.05rem; }}
.stars .off {{ opacity: .3; }}
.trust b {{ color: var(--navy); }}
.photo {{ margin: 0; position: relative; }}
.photo img {{ width: 100%; aspect-ratio: 4 / 3; object-fit: cover; object-position: {S['hero'].get('position', '50% 50%')}; border-radius: var(--radio); }}
.photo figcaption {{ position: absolute; left: 1rem; bottom: 1rem; background: rgba(255,255,255,.94); color: var(--navy); font-size: .875rem; font-weight: 600; padding: .45rem .8rem; border-radius: .75rem; }}

/* Urgencias */
.urgent {{ padding-bottom: 1rem; }}
.urgent-card {{ display: grid; gap: 1.2rem; align-items: center; background: var(--navy); color: #fff; border-radius: var(--radio); padding: 1.6rem 1.5rem; }}
.urgent-card h2 {{ color: #fff; font-size: clamp(1.4rem, 3vw, 1.8rem); }}
.urgent-card p {{ margin-top: .3rem; color: #c9d4ee; }}

/* Servicios */
.services {{ padding-block: 4.5rem; }}
.cards {{ display: grid; gap: 1rem; margin-top: 2.2rem; }}
.card {{ display: flex; flex-direction: column; background: #fff; border: 1px solid var(--linea); border-radius: var(--radio); padding: 1.6rem 1.5rem 1.4rem; }}
.icon {{ width: 2.75rem; height: 2.75rem; border-radius: .9rem; background: var(--suave); color: var(--azul); display: grid; place-items: center; }}
.icon svg {{ width: 1.5rem; height: 1.5rem; }}
.card h3 {{ margin-top: 1rem; font-size: 1.3rem; font-weight: 700; color: var(--navy); letter-spacing: -.01em; }}
.card-lead {{ margin-top: .2rem; color: var(--gris); font-size: .9375rem; }}
.card ul {{ margin-top: 1.1rem; display: grid; gap: .85rem; flex: 1; align-content: start; }}
.card li {{ display: grid; gap: .1rem; padding-top: .85rem; border-top: 1px solid var(--linea); }}
.card li b {{ font-weight: 650; color: var(--texto); }}
.card li span {{ color: var(--gris); font-size: .9375rem; line-height: 1.5; }}
.card-link {{ margin-top: 1.3rem; font-weight: 650; color: var(--azul); text-decoration: none; }}
.card-link:hover {{ text-decoration: underline; text-underline-offset: .25em; }}

/* Opiniones */
.reviews {{ background: var(--suave); padding-block: 4.5rem; }}
.reviews .wrap {{ display: grid; gap: 2rem; align-items: center; }}
.score {{ background: #fff; border-radius: var(--radio); padding: 1.8rem; display: grid; gap: .4rem; justify-items: start; }}
.score .num {{ font-size: 4rem; font-weight: 800; line-height: 1; color: var(--navy); letter-spacing: -.03em; }}
.score .num small {{ font-size: 1.25rem; color: var(--gris); font-weight: 600; letter-spacing: 0; }}
.score .stars svg {{ width: 1.35rem; height: 1.35rem; }}
.score p {{ color: var(--gris); font-size: .9375rem; }}
.topics {{ display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1.2rem; }}
.topics li {{ background: #fff; color: var(--navy); font-weight: 600; font-size: .9375rem; padding: .4rem .9rem; border-radius: 999px; border: 1px solid var(--linea); }}
.reviews .btn {{ margin-top: 1.6rem; }}

/* Visita */
.visit {{ padding-block: 4.5rem; }}
.visit .wrap {{ display: grid; gap: 2rem; }}
.visit address {{ margin-top: 1rem; font-style: normal; font-size: 1.3rem; font-weight: 650; color: var(--navy); line-height: 1.35; }}
.entrance {{ display: flex; gap: 1rem; align-items: center; margin-top: 1.4rem; padding: .8rem; border: 1px solid var(--linea); border-radius: 1rem; }}
.entrance img {{ width: 6.5rem; height: 6.5rem; object-fit: cover; object-position: {S['facade'].get('position', '50% 50%')}; border-radius: .7rem; flex: none; }}
.entrance p {{ font-size: .9375rem; color: var(--gris); }}
.visit .actions {{ display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 1.5rem; }}
.map {{ border-radius: var(--radio); overflow: hidden; aspect-ratio: 4 / 3; background: var(--suave); position: relative; display: grid; place-items: center; border: 1px solid var(--linea); }}
.map span {{ color: var(--gris); font-size: .9375rem; padding: 1rem; text-align: center; }}
.map iframe {{ position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }}

/* Instagram */
.insta {{ padding-bottom: 4rem; }}
.insta-card {{ display: flex; align-items: center; gap: 1rem; padding: 1.2rem 1.4rem; border: 1px solid var(--linea); border-radius: var(--radio); text-decoration: none; }}
.insta-card:hover {{ border-color: var(--navy); }}
.insta-icon {{ width: 2.75rem; height: 2.75rem; flex: none; border-radius: .9rem; display: grid; place-items: center; background: var(--suave); color: var(--azul); }}
.insta-icon svg {{ width: 1.5rem; height: 1.5rem; }}
.insta-card b {{ display: block; color: var(--navy); font-size: 1.1rem; }}
.insta-card small {{ display: block; color: var(--gris); font-size: .9375rem; }}
.insta-go {{ margin-left: auto; font-weight: 650; color: var(--azul); white-space: nowrap; }}

footer {{ background: var(--suave); padding-block: 2.5rem 7rem; font-size: .9375rem; color: var(--gris); }}
footer .wrap {{ display: grid; gap: 1.2rem; }}
footer a {{ color: var(--navy); font-weight: 600; text-underline-offset: .25em; }}
footer .fi {{ width: 1rem; height: 1rem; vertical-align: -.15em; margin-right: .4rem; }}
footer .note {{ font-size: .8125rem; border-top: 1px solid var(--linea); padding-top: 1.2rem; }}

.bar {{ position: fixed; inset: auto 0 0 0; z-index: 20; display: grid; grid-template-columns: 1fr 1fr; gap: .5rem; padding: .6rem .8rem calc(.6rem + env(safe-area-inset-bottom)); background: rgba(255,255,255,.96); backdrop-filter: blur(8px); border-top: 1px solid var(--linea); }}
.bar[hidden] {{ display: none; }}
.bar .btn {{ min-height: 3rem; font-size: .9375rem; }}

@media (max-width: 599px) {{
  .hero .actions .btn {{ width: 100%; }}
  .top-call span {{ display: none; }}
  .insta-go {{ display: none; }}
}}
@media (min-width: 760px) {{
  .cards {{ grid-template-columns: repeat(2, 1fr); gap: 1.25rem; }}
  .urgent-card {{ grid-template-columns: 1fr auto; padding: 1.8rem 2.2rem; }}
  .reviews .wrap {{ grid-template-columns: 280px 1fr; gap: 3.5rem; }}
}}
@media (min-width: 960px) {{
  body {{ font-size: 1.125rem; }}
  .bar {{ display: none; }}
  footer {{ padding-bottom: 2.5rem; }}
  .top nav a:not(.top-call) {{ display: inline; }}
  .hero {{ padding-block: 4rem 4.5rem; }}
  .hero .wrap {{ grid-template-columns: minmax(0, 1.05fr) minmax(0, .95fr); gap: 4rem; }}
  .photo img {{ aspect-ratio: 5 / 6; }}
  .services, .reviews, .visit {{ padding-block: 6rem; }}
  .visit .wrap {{ grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: 4rem; align-items: center; }}
  footer .wrap {{ grid-template-columns: 1.3fr 1fr 1fr; }}
  footer .note {{ grid-column: 1 / -1; }}
}}
@media (prefers-reduced-motion: reduce) {{
  html {{ scroll-behavior: auto; }}
  .status .dot {{ animation: none; }}
  .btn {{ transition: none; }}
}}
</style>
</head>
<body>
<div class="demo-bar" role="note"><strong>Página de muestra.</strong> Es una propuesta de diseño, no el sitio oficial de {e(S['name'])}.</div>

<header class="top">
  <div class="wrap">
    <a class="brand" href="#inicio"><b>{e(S['name'])}</b><span>{e(S['tagline'])}</span></a>
    <nav aria-label="Principal">
      <a href="#servicios">Servicios</a>
      <a href="#opiniones">Opiniones</a>
      <a href="#ubicacion">Ubicación</a>
      <a class="top-call" href="{tel}">{PH}<span>Urgencias</span> {e(S['phone_display'])}</a>
    </nav>
  </div>
</header>

<main id="inicio">
  <section class="hero">
    <div class="wrap">
      <div>
        <p class="status"><span class="dot" aria-hidden="true"></span><span class="js-clock" hidden>Abierto ahora, son las <time class="now"></time></span><span class="no-js">Abierto las 24 horas</span></p>
        <h1>Especialistas veterinarios en {e(S['city'])}, abiertos las 24 horas</h1>
        <p class="intro">{e(S['intro'])}</p>
        <div class="actions">
          <a class="btn btn-primary" href="{book}" target="_blank" rel="noopener">{WA}{e(C['book_label'])} por WhatsApp</a>
          <a class="btn btn-outline" href="{tel}">{PH}Llamar al {e(S['phone_display'])}</a>
        </div>
        <a class="trust" href="{e(S['maps_url'])}" target="_blank" rel="noopener"><span class="stars" aria-hidden="true">{g['stars_html']}</span><span><b>{e(S['rating'])}</b> en Google con {g['reviews_n']} reseñas</span></a>
      </div>
      <figure class="photo">
        <img src="{data_uri(hero, 82)}" width="{hero.width}" height="{hero.height}" alt="{e(S['hero']['alt'])}">
        <figcaption>Recepción en {e(S['area'])}</figcaption>
      </figure>
    </div>
  </section>

  <section class="urgent" aria-labelledby="urgent-title">
    <div class="wrap">
      <div class="urgent-card">
        <div>
          <h2 id="urgent-title">{e(urgent.get('title', '¿Tu mascota tiene una urgencia?'))}</h2>
          <p>{e(urgent.get('text', ''))}</p>
        </div>
        <a class="btn btn-white" href="{tel}">{PH}Llamar ahora</a>
      </div>
    </div>
  </section>

  <section class="services" id="servicios">
    <div class="wrap">
      <h2>Servicios</h2>
      <p class="lead">Todo en la misma sede, en {e(S['area'])}. {e(C['services_lead'])}</p>
      <div class="cards">{groups_html}</div>
    </div>
  </section>

  <section class="reviews" id="opiniones">
    <div class="wrap">
      <div class="score">
        <span class="num">{e(S['rating'])}<small> de 5</small></span>
        <span class="stars" role="img" aria-label="{e(g['stars_label'])}">{g['stars_html']}</span>
        <p>{g['reviews_n']} reseñas en Google, a {e(S['reviews_asof'])}</p>
      </div>
      <div>
        <h2>Lo que más mencionan sus {e(C['reviewers'])}</h2>
        <ul class="topics">{topics_html}</ul>
        <a class="btn btn-outline" href="{e(S['maps_url'])}" target="_blank" rel="noopener">Leer las reseñas en Google</a>
      </div>
    </div>
  </section>

  <section class="visit" id="ubicacion">
    <div class="wrap">
      <div>
        <h2>Cómo llegar</h2>
        <address>{e(S['address'])}<br>{e(S['area'])}, {e(S['city'])}</address>
        <div class="entrance">
          <img src="{data_uri(facade, 80)}" width="{facade.width}" height="{facade.height}" alt="{e(S['facade']['alt'])}">
          <p>{e(S['entrance_hint'])}</p>
        </div>
        <div class="actions">
          <a class="btn btn-primary" href="{e(S['maps_url'])}" target="_blank" rel="noopener">Abrir en Google Maps</a>
          <a class="btn btn-outline" href="{e(wa(C['directions_wa']))}" target="_blank" rel="noopener">Pedir indicaciones</a>
        </div>
      </div>
      <div class="map">
        <span>{e(g['full_address'])}</span>
        <iframe title="Mapa de {e(S['name'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={g['quote'](S['maps_embed_q'])}&output=embed"></iframe>
      </div>
    </div>
  </section>
{insta_html}
</main>

<footer>
  <div class="wrap">
    <div><a class="brand" href="#inicio"><b>{e(S['name'])}</b><span>{e(S['tagline'])}</span></a></div>
    <div>{e(S['address'])}<br>{e(S['area'])}, {e(S['city'])}<br>Abierto las 24 horas</div>
    <div>
      <a href="{tel}">{icon("lucide/phone", "fi")}{e(S['phone_display'])}</a><br>
      <a href="{book}" target="_blank" rel="noopener">{icon("brands/whatsapp", "fi")}{e(S['whatsapp_display'])}</a><br>
      {"".join(f'<a href="{e(s["url"])}" target="_blank" rel="noopener">{icon("brands/" + s["network"].lower(), "fi")}@{e(s["handle"])}</a>' for s in g["SOCIAL"])}
    </div>
    <p class="note">Página de muestra creada como propuesta de diseño; no es el sitio oficial de {e(S['name'])}. {e(C['sources'])}</p>
  </div>
</footer>

<nav class="bar" aria-label="Contacto rápido">
  <a class="btn btn-outline" href="{tel}">{PH}Llamar</a>
  <a class="btn btn-primary" href="{book}" target="_blank" rel="noopener">{WA}WhatsApp</a>
</nav>

<script>
(function () {{
  var bar = document.querySelector('.bar'), act = document.querySelector('.hero .actions');
  if (!bar || !act || !('IntersectionObserver' in window)) return;
  new IntersectionObserver(function (en) {{ bar.hidden = en[0].isIntersecting; }}).observe(act);
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
