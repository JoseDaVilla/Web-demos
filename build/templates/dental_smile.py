"""Layout for aesthetic dental practices ("dental_smile").

Tone: bright, fresh and a little elegant, like the practice's own mint wall.
Headlines in Fraunces (a soft serif, italic for the wordmark, echoing the
script logo), text in Outfit. Mint and deep green from the logo, on white.

Composition (different from vet24): a centered headline with the practice's
own slogan, then a wide panoramic photo of the treatment room with the
mountain view; a one-line proof strip with the perfect rating; the signature
treatment featured on its own; the rest of the services as a two-column
list; and the entrance photo next to the directions.

render(g) receives the build script's globals (SITE, COPY, THEME, helpers).
"""
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from icons import icon  # noqa: E402

FONTS = Path(__file__).resolve().parent.parent / "fonts"


def b64(name):
    return base64.b64encode((FONTS / name).read_bytes()).decode()


def render(g):
    S, C, T, e, wa = g["SITE"], g["COPY"], g["THEME"], g["e"], g["wa"]
    hero, facade, data_uri = g["hero"], g["facade"], g["data_uri"]
    WA = g["WA_ICON"]
    book = g["book"]
    serif, serif_i, sans = b64("fraunces-latin-opsz-normal.woff2"), b64("fraunces-latin-opsz-italic.woff2"), b64("outfit-latin-wght-normal.woff2")

    feat = S.get("featured")
    feat_html = ""
    if feat:
        ask = wa(f"Hola, quiero información sobre {feat['name'].lower()}.")
        feat_html = f"""
  <section class="featured">
    <div class="wrap">
      <div class="feat-card">
        <div>
          <p class="kicker">El tratamiento insignia</p>
          <h2>{e(feat['name'])}</h2>
          <p>{e(feat['text'])}</p>
        </div>
        <a class="btn btn-solid" href="{e(ask)}" target="_blank" rel="noopener">{WA}Preguntar por WhatsApp</a>
      </div>
    </div>
  </section>"""

    groups = []
    for group in S["groups"]:
        items = "".join(
            f'<li><span class="n">{e(it["name"])}</span><span class="d">{e(it["text"])}</span></li>'
            for it in group["items"] if not feat or it["name"] != feat["name"]
        )
        groups.append(f'<div class="group"><h3>{e(group["title"])}</h3><ul>{items}</ul></div>')
    groups_html = "".join(groups)

    topics = S.get("review_topics", [])
    topics_txt = ""
    if topics:
        topics_txt = ", ".join(topics[:-1]) + (" y " if len(topics) > 1 else "") + topics[-1]

    insta = g["SOCIAL"][0] if g["SOCIAL"] else None
    insta_line = (f'<a href="{e(insta["url"])}" target="_blank" rel="noopener">{icon("brands/instagram", "fi")}@{e(insta["handle"])}</a>'
                  if insta else "")
    doctor = S.get("doctor")

    return f"""<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(S['name'])}: {e(S['tagline'].lower())} en {e(S['area'])} (demo)</title>
<meta name="description" content="{e(S['intro'])}">
<style>
@font-face {{ font-family: "Fraunces"; src: url(data:font/woff2;base64,{serif}) format("woff2"); font-weight: 100 900; font-style: normal; font-display: swap; }}
@font-face {{ font-family: "Fraunces"; src: url(data:font/woff2;base64,{serif_i}) format("woff2"); font-weight: 100 900; font-style: italic; font-display: swap; }}
@font-face {{ font-family: "Outfit"; src: url(data:font/woff2;base64,{sans}) format("woff2"); font-weight: 100 900; font-display: swap; }}
:root {{
  --verde: {T['ink']};
  --menta: {T['accent']};
  --menta-viva: {T['accent_light']};
  --menta-suave: {T['sky']};
  --linea: {T['line']};
  --texto: #1b2b28;
  --gris: #586b67;
  --ancho: 1120px;
}}
*, *::before, *::after {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }}
body {{ margin: 0; font-family: "Outfit", system-ui, sans-serif; font-size: 1.0625rem; line-height: 1.6; color: var(--texto); background: #fff; }}
h1, h2, h3, p, ul {{ margin: 0; }}
ul {{ list-style: none; padding: 0; }}
img {{ display: block; max-width: 100%; height: auto; }}
a {{ color: inherit; }}
:focus-visible {{ outline: 3px solid var(--menta-viva); outline-offset: 3px; border-radius: 6px; }}
.wrap {{ width: min(100% - 2.5rem, var(--ancho)); margin-inline: auto; }}
h1, h2 {{ font-family: "Fraunces", Georgia, serif; font-weight: 450; color: var(--verde); letter-spacing: -.015em; text-wrap: balance; }}
h2 {{ font-size: clamp(1.9rem, 4.2vw, 2.75rem); line-height: 1.1; }}

.demo-bar {{ background: #fff4cc; color: #4a3800; font-size: .875rem; text-align: center; padding: .5rem 1rem; border-bottom: 1px solid #ecd98a; }}

.btn {{ display: inline-flex; align-items: center; justify-content: center; gap: .55rem; min-height: 3.1rem; padding: .7rem 1.5rem; border-radius: 999px; font: inherit; font-weight: 600; text-decoration: none; border: 2px solid transparent; transition: background-color .15s, color .15s; }}
.btn svg {{ width: 1.25rem; height: 1.25rem; flex: none; }}
.btn-solid {{ background: var(--menta); color: #fff; }}
.btn-solid:hover {{ background: var(--verde); }}
.btn-line {{ border-color: var(--linea); color: var(--verde); }}
.btn-line:hover {{ border-color: var(--verde); }}

/* Encabezado */
.top .wrap {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; min-height: 4.75rem; }}
.mark {{ text-decoration: none; line-height: 1; }}
.mark b {{ display: block; font-family: "Fraunces", Georgia, serif; font-style: italic; font-weight: 600; font-size: 1.75rem; color: var(--verde); letter-spacing: -.01em; }}
.mark span {{ font-size: .8125rem; color: var(--menta); font-weight: 500; letter-spacing: .02em; }}
.top nav {{ display: flex; align-items: center; gap: 1.6rem; }}
.top nav a:not(.btn) {{ display: none; text-decoration: none; font-weight: 500; }}
.top nav a:not(.btn):hover {{ color: var(--menta); }}
.top .btn {{ min-height: 2.6rem; padding: .45rem 1.1rem; font-size: .9375rem; }}

/* Portada */
.hero {{ background: var(--menta-suave); padding-top: 3.5rem; text-align: center; }}
.hero h1 {{ font-size: clamp(2.75rem, 8vw, 5.4rem); line-height: 1; font-weight: 400; }}
.hero .intro {{ margin: 1.3rem auto 0; max-width: 50ch; color: var(--gris); font-size: 1.125rem; }}
.hero .actions {{ display: flex; flex-wrap: wrap; justify-content: center; gap: .75rem; margin-top: 2rem; }}
.rating {{ display: inline-flex; align-items: center; gap: .55rem; margin-top: 1.4rem; font-size: .9375rem; color: var(--gris); text-decoration: none; }}
.rating:hover span:last-child {{ text-decoration: underline; text-underline-offset: .25em; }}
.stars {{ display: inline-flex; gap: 1px; color: #e9a514; }}
.stars svg {{ width: 1.05rem; height: 1.05rem; }}
.stars .off {{ opacity: .3; }}
.rating b {{ color: var(--verde); }}
.pano {{ margin: 3rem auto 0; position: relative; }}
.pano img {{ width: 100%; aspect-ratio: 16 / 9; object-fit: cover; object-position: {S['hero'].get('position', '50% 50%')}; border-radius: 1.5rem 1.5rem 0 0; }}
.pano figcaption {{ position: absolute; right: 1rem; bottom: 1rem; background: rgba(255,255,255,.93); color: var(--verde); font-size: .875rem; font-weight: 500; padding: .45rem .85rem; border-radius: .75rem; }}

/* Prueba */
.proof {{ border-bottom: 1px solid var(--linea); }}
.proof .wrap {{ display: grid; gap: 1.25rem; padding-block: 2.25rem; }}
.proof .score {{ display: flex; align-items: baseline; gap: .6rem; }}
.proof .score b {{ font-family: "Fraunces", Georgia, serif; font-weight: 500; font-size: 3.25rem; line-height: 1; color: var(--verde); }}
.proof .score .stars {{ color: #e9a514; }}
.proof p {{ color: var(--gris); max-width: 58ch; }}
.proof p strong {{ color: var(--verde); font-weight: 600; }}

/* Tratamiento insignia */
.featured {{ padding-block: 4.5rem 0; }}
.feat-card {{ display: grid; gap: 1.6rem; background: var(--verde); color: #fff; border-radius: 1.5rem; padding: 2rem 1.6rem; }}
.feat-card .kicker {{ font-size: .9375rem; color: {T['on_ink']}; font-weight: 500; }}
.feat-card h2 {{ color: #fff; margin-top: .35rem; }}
.feat-card p:not(.kicker) {{ margin-top: .8rem; color: {T['on_ink']}; max-width: 54ch; }}
.feat-card .btn-solid {{ background: var(--menta-viva); color: var(--verde); }}
.feat-card .btn-solid:hover {{ background: #fff; }}

/* Servicios */
.services {{ padding-block: 4.5rem; }}
.services .lead {{ margin-top: .7rem; color: var(--gris); max-width: 54ch; }}
.groups {{ display: grid; gap: 2.25rem 3rem; margin-top: 2.5rem; }}
.group h3 {{ font-size: .9375rem; font-weight: 600; color: var(--menta); padding-bottom: .6rem; border-bottom: 2px solid var(--menta-suave); }}
.group li {{ display: grid; gap: .1rem; padding-block: .85rem; border-bottom: 1px solid var(--linea); }}
.group .n {{ font-weight: 600; font-size: 1.0625rem; color: var(--texto); }}
.group .d {{ color: var(--gris); font-size: .9375rem; line-height: 1.5; }}
.services .more {{ margin-top: 2.25rem; display: flex; flex-wrap: wrap; align-items: center; gap: 1rem; color: var(--gris); }}

/* Doctor */
.doctor {{ background: var(--menta-suave); padding-block: 3.5rem; }}
.doctor .wrap {{ display: grid; gap: 1rem; }}
.doctor p {{ color: var(--gris); max-width: 58ch; }}

/* Visita */
.visit {{ padding-block: 4.5rem; }}
.visit .wrap {{ display: grid; gap: 2.25rem; }}
.visit figure {{ margin: 0; }}
.visit figure img {{ width: 100%; aspect-ratio: 4 / 5; object-fit: cover; object-position: {S['facade'].get('position', '50% 50%')}; border-radius: 1.5rem; }}
.visit address {{ margin-top: 1rem; font-style: normal; font-size: 1.3rem; font-weight: 600; color: var(--verde); line-height: 1.35; }}
.visit .hint {{ margin-top: .7rem; color: var(--gris); max-width: 42ch; }}
.visit .actions {{ display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 1.5rem; }}
.map {{ margin-top: 1.75rem; border-radius: 1.25rem; overflow: hidden; aspect-ratio: 16 / 10; background: var(--menta-suave); position: relative; display: grid; place-items: center; }}
.map span {{ color: var(--gris); font-size: .9375rem; padding: 1rem; text-align: center; }}
.map iframe {{ position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }}

footer {{ background: var(--verde); color: {T['on_ink']}; padding-block: 2.75rem 7rem; font-size: .9375rem; }}
footer .wrap {{ display: grid; gap: 1.2rem; }}
footer a {{ color: #fff; text-underline-offset: .25em; }}
footer .mark b {{ color: #fff; }}
footer .mark span {{ color: {T['on_ink']}; }}
footer .fi {{ width: 1rem; height: 1rem; vertical-align: -.15em; margin-right: .4rem; }}
footer .note {{ font-size: .8125rem; border-top: 1px solid rgba(255,255,255,.18); padding-top: 1.2rem; }}

.bar {{ position: fixed; inset: auto 0 0 0; z-index: 20; padding: .6rem .8rem calc(.6rem + env(safe-area-inset-bottom)); background: rgba(255,255,255,.96); backdrop-filter: blur(8px); border-top: 1px solid var(--linea); }}
.bar[hidden] {{ display: none; }}
.bar .btn {{ width: 100%; }}

@media (max-width: 599px) {{
  .hero .actions .btn {{ width: 100%; }}
  .pano img {{ aspect-ratio: 4 / 3; }}
}}
@media (min-width: 760px) {{
  .groups {{ grid-template-columns: 1fr 1fr; }}
  .feat-card {{ grid-template-columns: 1fr auto; align-items: end; padding: 2.6rem 2.8rem; }}
  .proof .wrap {{ grid-template-columns: auto 1fr; gap: 2.5rem; align-items: center; }}
}}
@media (min-width: 960px) {{
  body {{ font-size: 1.125rem; }}
  .bar {{ display: none; }}
  footer {{ padding-bottom: 2.75rem; }}
  .top nav a:not(.btn) {{ display: inline; }}
  .hero {{ padding-top: 5rem; }}
  .pano img {{ aspect-ratio: 21 / 9; }}
  .services, .visit {{ padding-block: 6rem; }}
  .featured {{ padding-top: 6rem; }}
  .visit .wrap {{ grid-template-columns: minmax(0, .8fr) minmax(0, 1.2fr); gap: 4rem; align-items: start; }}
  footer .wrap {{ grid-template-columns: 1.3fr 1fr 1fr; }}
  footer .note {{ grid-column: 1 / -1; }}
}}
@media (prefers-reduced-motion: reduce) {{
  html {{ scroll-behavior: auto; }}
  .btn {{ transition: none; }}
}}
</style>
</head>
<body>
<div class="demo-bar" role="note"><strong>Página de muestra.</strong> Es una propuesta de diseño, no el sitio oficial de {e(S['name'])}.</div>

<header class="top">
  <div class="wrap">
    <a class="mark" href="#inicio"><b>{e(S['name'])}</b><span>{e(S['tagline'])}</span></a>
    <nav aria-label="Principal">
      <a href="#servicios">Servicios</a>
      <a href="#ubicacion">Ubicación</a>
      <a class="btn btn-solid" href="{book}" target="_blank" rel="noopener">{WA}{e(C['book_label'])}</a>
    </nav>
  </div>
</header>

<main id="inicio">
  <section class="hero">
    <div class="wrap">
      <h1>{e(S['slogan'])}</h1>
      <p class="intro">{e(S['intro'])}</p>
      <div class="actions">
        <a class="btn btn-solid" href="{book}" target="_blank" rel="noopener">{WA}{e(C['book_label'])} por WhatsApp</a>
        <a class="btn btn-line" href="#servicios">Ver tratamientos</a>
      </div>
      <a class="rating" href="{e(S['maps_url'])}" target="_blank" rel="noopener"><span class="stars" aria-hidden="true">{g['stars_html']}</span><span><b>{e(S['rating'])}</b> en Google con {g['reviews_n']} reseñas</span></a>
      <figure class="pano">
        <img src="{data_uri(hero, 82)}" width="{hero.width}" height="{hero.height}" alt="{e(S['hero']['alt'])}">
        <figcaption>{e(S['hero'].get('caption', ''))}</figcaption>
      </figure>
    </div>
  </section>

  <section class="proof" aria-label="Calificación en Google">
    <div class="wrap">
      <div class="score"><b>{e(S['rating'])}</b><span role="img" aria-label="{e(g['stars_label'])}" class="stars">{g['stars_html']}</span></div>
      <p>Es la calificación de sus {g['reviews_n']} reseñas en Google, a {e(S['reviews_asof'])}. Sus {e(C['reviewers'])} destacan sobre todo <strong>{e(topics_txt)}</strong>.</p>
    </div>
  </section>
{feat_html}
  <section class="services" id="servicios">
    <div class="wrap">
      <h2>Todos los tratamientos</h2>
      <p class="lead">Del control de rutina a la rehabilitación completa, en el mismo consultorio.</p>
      <div class="groups">{groups_html}</div>
      <div class="more"><a class="btn btn-solid" href="{book}" target="_blank" rel="noopener">{WA}Preguntar por un tratamiento</a></div>
    </div>
  </section>

  {f'''<section class="doctor"><div class="wrap"><h2>Te atiende el {e(doctor)}</h2><p>Odontólogo con enfoque en estética. Puedes ver sus casos y resultados en el Instagram del consultorio.</p></div></section>''' if doctor else ''}

  <section class="visit" id="ubicacion">
    <div class="wrap">
      <figure><img src="{data_uri(facade, 80)}" width="{facade.width}" height="{facade.height}" loading="lazy" alt="{e(S['facade']['alt'])}"></figure>
      <div>
        <h2>Cómo llegar</h2>
        <address>{e(S['address'])}<br>{e(S['area'])}, {e(S['city'])}</address>
        <p class="hint">{e(S['entrance_hint'])}</p>
        <div class="actions">
          <a class="btn btn-solid" href="{e(S['maps_url'])}" target="_blank" rel="noopener">Abrir en Google Maps</a>
          <a class="btn btn-line" href="{e(wa('Hola, ¿me indican cómo llegar al consultorio?'))}" target="_blank" rel="noopener">Pedir indicaciones</a>
        </div>
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
    <div><a class="mark" href="#inicio"><b>{e(S['name'])}</b><span>{e(S['tagline'])}</span></a></div>
    <div>{e(S['address'])}<br>{e(S['area'])}, {e(S['city'])}</div>
    <div><a href="{book}" target="_blank" rel="noopener">{icon("brands/whatsapp", "fi")}{e(S['whatsapp_display'])}</a><br>{insta_line}</div>
    <p class="note">Página de muestra creada como propuesta de diseño; no es el sitio oficial de {e(S['name'])}. {e(C['sources'])}</p>
  </div>
</footer>

<div class="bar"><a class="btn btn-solid" href="{book}" target="_blank" rel="noopener">{WA}{e(C['book_label'])} por WhatsApp</a></div>
<script>
(function () {{
  var bar = document.querySelector('.bar'), act = document.querySelector('.hero .actions');
  if (!bar || !act || !('IntersectionObserver' in window)) return;
  new IntersectionObserver(function (en) {{ bar.hidden = en[0].isIntersecting; }}).observe(act);
}})();
</script>
</body>
</html>
"""
