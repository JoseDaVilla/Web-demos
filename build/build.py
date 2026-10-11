#!/usr/bin/env python3
"""Build a self-contained demo page for one clinic.

Usage:
    python3 build/build.py sites/<slug>.json <photos_dir>

Writes <slug>/index.html at the repo root. Everything specific to the clinic
lives in the JSON file; the template below is shared by every clinic demo.
Photos and the font are inlined, so the page is a single file.

Rules for the content of a site JSON:
  - Only facts taken from the business's public profile or its own material.
  - No invented testimonials, staff names, prices or opening hours.
  - The page always carries the demo notice and noindex.
"""
import base64
import html
import io
import json
import sys
from pathlib import Path
from urllib.parse import quote

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FONT = Path(__file__).resolve().parent / "fonts" / "bricolage-grotesque-latin-wght-normal.woff2"

site_path, photos = Path(sys.argv[1]), Path(sys.argv[2])
SITE = json.loads(site_path.read_text(encoding="utf-8"))
slug = site_path.stem
e = html.escape


def load_photo(spec: dict, max_size: tuple[int, int]) -> Image.Image:
    img = Image.open(photos / spec["file"])
    if spec.get("crop"):
        img = img.crop(tuple(spec["crop"]))
    img.thumbnail(max_size)
    return img


def data_uri(img: Image.Image, quality: int) -> str:
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def wa(text: str) -> str:
    return f"https://wa.me/{SITE['whatsapp_e164']}?text={quote(text)}"


hero = load_photo(SITE["hero"], (1200, 1200))
facade = load_photo(SITE["facade"], (900, 1000))
font_b64 = base64.b64encode(FONT.read_bytes()).decode()

WA_ICON = ('<svg class="wa" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 1.8a8.2 8.2 0 1 1-4.2 15.3l-.3-.2-2.9.8.8-2.9-.2-.3A8.2 8.2 0 0 1 12 3.8Zm-3 3.9c-.2 0-.5 0-.7.3-.3.3-1 1-1 2.3 0 1.4 1 2.7 1.2 2.9.1.2 2 3.1 4.9 4.3 2.4 1 2.9.8 3.4.7.5 0 1.7-.7 1.9-1.3.2-.7.2-1.2.2-1.3-.1-.2-.3-.2-.6-.4l-1.9-.9c-.3-.1-.5-.2-.7.1l-.9 1.1c-.1.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.8-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.5-.5.3-.5v-.5L9.700 8c-.2-.3-.4-.3-.6-.3Z"/></svg>')
PHONE_ICON = ('<svg class="wa" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1Z"/></svg>')
STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill="currentColor" d="m10 1.6 2.6 5.3 5.8.8-4.2 4.1 1 5.8L10 14.900l-5.2 2.700 1-5.800L1.600 7.700l5.800-.800Z"/></svg>'

groups_html = []
for group in SITE["groups"]:
    rows = "".join(
        f'<li><div><h4>{e(item["name"])}</h4><p>{e(item["text"])}</p></div>'
        f'<a href="{e(wa("Hola, quiero información sobre " + item["name"].lower() + "."))}" target="_blank" rel="noopener" '
        f'aria-label="Preguntar por {e(item["name"].lower())} en WhatsApp">Preguntar</a></li>'
        for item in group["items"]
    )
    groups_html.append(
        f'<div class="group"><div class="group-head"><h3>{e(group["title"])}</h3>'
        f'<p>{e(group["lead"])}</p></div><ul>{rows}</ul></div>'
    )

book = e(wa(f"Hola, quiero agendar una cita en {SITE['name']}."))
full_address = f"{SITE['address']}, {SITE['area']}, {SITE['city']}"

# Colors: each site sets its own palette in "theme"; the defaults are the
# original clinic palette, so older site files still build the same page.
THEME = {
    "ink": "#10294f",          # titles, primary buttons, dark band
    "accent": "#08778f",       # links, tagline, hover
    "accent_light": "#19a9c6", # focus ring
    "sky": "#e2f1f6",          # closing band, map placeholder
    "cloud": "#f5fafc",        # services background
    "line": "#cfe0e8",         # dividers
    "on_ink": "#c3d6e8",       # secondary text on the dark band
    **SITE.get("theme", {}),
}

# Wording that changes by niche. Defaults keep the dental wording.
COPY = {
    "book_label": "Agendar cita",
    "reviewers": "pacientes",
    "directions_wa": "Hola, ¿me indican cómo llegar al consultorio?",
    "services_lead": "Pregunta por el tratamiento que te interesa y te respondemos por WhatsApp.",
    "cta_title": "Agenda tu cita por WhatsApp",
    "cta_text": f"Escríbenos al {SITE['whatsapp_display']} y cuadramos el día y la hora.",
    "sources": "Las fotos, la calificación y los datos de contacto vienen del perfil público del consultorio en Google.",
    **SITE.get("copy", {}),
}

# Optional landline for a "Llamar" button (urgencies, 24-hour places).
phone = SITE.get("phone_e164")
tel = f"tel:+{phone}" if phone else ""
call_btn = (f'<a class="btn btn-ghost" href="{tel}">{PHONE_ICON}Llamar al {e(SITE["phone_display"])}</a>'
            if phone else "")

badges_html = "".join(f"<li>{e(b)}</li>" for b in SITE.get("badges", []))
badges_html = f'<ul class="badges">{badges_html}</ul>' if badges_html else ""

urgent = SITE.get("urgent")
urgent_html = ""
if urgent:
    urgent_html = f"""
  <section class="urgent" aria-labelledby="urgent-title">
    <div class="wrap">
      <div>
        <h2 id="urgent-title">{e(urgent['title'])}</h2>
        <p>{e(urgent['text'])}</p>
      </div>
      <div class="actions">
        {f'<a class="btn btn-light" href="{tel}">{PHONE_ICON}Llamar al {e(SITE["phone_display"])}</a>' if phone else ''}
        <a class="btn btn-light" href="{e(wa(urgent.get('wa_text', 'Hola, tengo una urgencia con mi mascota.')))}" target="_blank" rel="noopener">{WA_ICON}Escribir por WhatsApp</a>
      </div>
    </div>
  </section>"""

tel_footer = f'<a href="{tel}">Teléfono {e(SITE["phone_display"])}</a><br>' if phone else ""
mobile_call = (f'<a class="btn btn-ghost btn-call" href="{tel}" aria-label="Llamar al {e(SITE["phone_display"])}">{PHONE_ICON}</a>'
               if phone else "")

# Stars match the real rating (rounded to the nearest whole star), and the
# review count uses Colombian thousands separators: 1.564, not 1564.
rating_value = float(SITE["rating"].replace(",", "."))
full_stars = int(rating_value + 0.5)
stars_html = STAR * full_stars + STAR.replace("<svg ", '<svg class="off" ', 1) * (5 - full_stars)
stars_label = f"{SITE['rating']} de 5 estrellas"
reviews_n = f"{SITE['reviews']:,}".replace(",", ".")

def note_span(s):
    return f"<span>{e(s['note'])}</span>" if s.get("note") else ""


# Social profiles: a list of {network, handle, url, note}. The older
# "instagram" key still works and becomes a one-item list.
SOCIAL = SITE.get("social") or (
    [{"network": "Instagram", "handle": SITE["instagram"],
      "url": f"https://www.instagram.com/{SITE['instagram']}/"}] if SITE.get("instagram") else [])
social_footer = "<br>".join(
    f'<a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["network"])} @{e(s["handle"])}</a>' for s in SOCIAL)
social_html = ""
if SITE.get("social"):
    cards = "".join(
        f'<a class="social-card" href="{e(s["url"])}" target="_blank" rel="noopener">'
        f'<span class="net">{e(s["network"])}</span><b>@{e(s["handle"])}</b>'
        f'{note_span(s)}</a>'
        for s in SOCIAL)
    social_html = f"""
  <section class="social">
    <div class="wrap">
      <div>
        <h2 class="section-title">{e(COPY.get('social_title', 'Síguenos'))}</h2>
        <p class="section-lead">{e(COPY.get('social_lead', 'Mira lo que publicamos día a día.'))}</p>
      </div>
      <div class="social-cards">{cards}</div>
    </div>
  </section>"""

# Topics Google pulls out of the reviews ("hospitalización", "exámenes"...).
topics = SITE.get("review_topics", [])
topics_html = ""
if topics:
    chips = "".join(f"<li>{e(t)}</li>" for t in topics)
    topics_html = f'<p class="topics-label">Lo que más mencionan en sus reseñas:</p><ul class="topics">{chips}</ul>'

caption = SITE["hero"].get("caption")
caption_html = f"<figcaption>{e(caption)}</figcaption>" if caption else ""

PAGE = f"""<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(SITE['name'])}: {e(SITE['tagline'].lower())} en {e(SITE['area'])} (demo)</title>
<meta name="description" content="{e(SITE['intro'])}">
<style>
@font-face {{
  font-family: "Bricolage Grotesque";
  src: url(data:font/woff2;base64,{font_b64}) format("woff2");
  font-weight: 200 800;
  font-display: swap;
}}
:root {{
  --tinta: {THEME['ink']};
  --turquesa: {THEME['accent']};
  --turquesa-claro: {THEME['accent_light']};
  --cielo: {THEME['sky']};
  --nube: {THEME['cloud']};
  --texto: #1c2c3c;
  --gris: #556779;
  --linea: {THEME['line']};
  --ambar: #f0ab1c;
  --ancho: 1180px;
}}
*, *::before, *::after {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }}
body {{
  margin: 0;
  font-family: "Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  font-size: 1.0625rem;
  line-height: 1.55;
  color: var(--texto);
  background: #fff;
}}
img {{ display: block; max-width: 100%; height: auto; }}
a {{ color: inherit; }}
h1, h2, h3, h4, p, ul {{ margin: 0; }}
ul {{ padding: 0; list-style: none; }}
:focus-visible {{ outline: 3px solid var(--turquesa-claro); outline-offset: 3px; border-radius: 4px; }}
.wrap {{ width: min(100% - 2.5rem, var(--ancho)); margin-inline: auto; }}

/* Aviso de demo */
.demo-bar {{
  position: sticky; top: 0; z-index: 30;
  background: #fff4cc; color: #4a3800;
  font-size: .875rem; line-height: 1.35; text-align: center;
  padding: .5rem 1rem; border-bottom: 1px solid #ecd98a;
}}
.demo-bar strong {{ font-weight: 700; }}

/* Botones */
.btn {{
  display: inline-flex; align-items: center; justify-content: center; gap: .6rem;
  min-height: 3.25rem; padding: .75rem 1.5rem;
  font: inherit; font-weight: 650; text-decoration: none;
  border-radius: 999px; border: 2px solid transparent;
  transition: background-color .15s, color .15s, border-color .15s;
}}
.btn .wa {{ width: 1.35rem; height: 1.35rem; flex: none; }}
.btn-primary {{ background: var(--tinta); color: #fff; }}
.btn-primary:hover {{ background: var(--turquesa); }}
.btn-ghost {{ border-color: var(--tinta); color: var(--tinta); }}
.btn-ghost:hover {{ background: var(--tinta); color: #fff; }}
.btn-light {{ border-color: #fff; color: #fff; }}
.btn-light:hover {{ background: #fff; color: var(--tinta); }}

/* Encabezado */
.top {{ padding-block: 1.1rem; }}
.top .wrap {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; }}
.brand {{ text-decoration: none; line-height: 1.05; }}
.brand b {{ display: block; font-size: 1.6rem; font-weight: 750; letter-spacing: -.02em; color: var(--tinta); }}
.brand span {{ font-size: .875rem; color: var(--turquesa); font-weight: 550; }}
.top nav {{ align-items: center; gap: 1.75rem; }}
.top nav a:not(.btn) {{ text-decoration: none; font-weight: 550; color: var(--tinta); }}
.top nav a:not(.btn):hover {{ text-decoration: underline; text-underline-offset: .3em; }}
.top .btn {{ min-height: 2.75rem; padding: .5rem 1.2rem; }}

/* Portada */
.hero {{ position: relative; overflow: hidden; }}
.hero .wrap {{ display: grid; gap: 2rem; align-items: center; padding-block: 1rem 3.5rem; }}
.hero h1 {{
  font-size: clamp(2.9rem, 9.5vw, 5.6rem);
  font-weight: 750; line-height: .96; letter-spacing: -.035em;
  color: var(--tinta); text-wrap: balance;
}}
.hero .intro {{ margin-top: 1.4rem; max-width: 34ch; font-size: 1.1875rem; color: var(--gris); }}
.hero .actions {{ display: flex; flex-wrap: wrap; gap: .8rem; margin-top: 1.9rem; }}
.rating {{ display: flex; align-items: center; gap: .6rem; margin-top: 1.6rem; font-size: .9375rem; color: var(--gris); text-decoration: none; }}
.rating:hover span {{ text-decoration: underline; text-underline-offset: .25em; }}
.stars {{ display: inline-flex; gap: 1px; color: var(--ambar); }}
.stars .off {{ opacity: .3; }}
.stars svg {{ width: 1.05rem; height: 1.05rem; }}
.hero figure {{ margin: 0; }}
.hero img {{
  width: 100%; aspect-ratio: 4 / 3; object-fit: cover; object-position: {SITE['hero'].get('position', '50% 50%')};
  border-radius: 1.5rem 1.5rem 1.5rem 7rem;
}}
.hero figcaption {{ margin-top: .7rem; font-size: .875rem; color: var(--gris); text-align: right; }}

/* Servicios */
.services {{ background: var(--nube); padding-block: 4.5rem; border-top: 1px solid var(--linea); }}
.section-title {{ font-size: clamp(2rem, 5vw, 3rem); font-weight: 720; line-height: 1.05; letter-spacing: -.03em; color: var(--tinta); }}
.section-lead {{ margin-top: .9rem; max-width: 46ch; color: var(--gris); }}
.groups {{ margin-top: 2.75rem; }}
.group {{ display: grid; gap: 1rem; padding-block: 2rem; border-top: 2px solid var(--tinta); }}
.group-head h3 {{ font-size: 1.5rem; font-weight: 700; letter-spacing: -.02em; color: var(--tinta); }}
.group-head p {{ margin-top: .3rem; color: var(--gris); font-size: 1rem; }}
.group li {{
  display: flex; align-items: center; justify-content: space-between; gap: 1.25rem;
  padding-block: 1rem; border-top: 1px solid var(--linea);
}}
.group li:first-child {{ border-top: 0; padding-top: 0; }}
.group h4 {{ font-size: 1.125rem; font-weight: 650; color: var(--texto); }}
.group li p {{ margin-top: .15rem; color: var(--gris); font-size: 1rem; }}
.group li a {{
  flex: none; font-weight: 650; font-size: .9375rem; color: var(--turquesa);
  text-decoration: underline; text-underline-offset: .3em; text-decoration-thickness: 2px;
  padding: .5rem 0;
}}
.group li a:hover {{ color: var(--tinta); }}

/* Reseñas */
.reviews {{ background: var(--tinta); color: #fff; padding-block: 4rem; }}
.reviews .wrap {{ display: grid; gap: 1.75rem; align-items: center; }}
.reviews .stars svg {{ width: 1.6rem; height: 1.6rem; }}
.reviews h2 {{ margin-top: .9rem; font-size: clamp(2rem, 5.5vw, 3.25rem); font-weight: 720; line-height: 1.05; letter-spacing: -.03em; }}
.reviews p {{ margin-top: .8rem; color: {THEME['on_ink']}; max-width: 44ch; }}

/* Ubicación */
.location {{ padding-block: 4.5rem; }}
.location .wrap {{ display: grid; gap: 2.5rem; }}
.location figure {{ margin: 0; }}
.location figure img {{ width: 100%; aspect-ratio: 5 / 4; object-fit: cover; object-position: {SITE['facade'].get('position', '50% 50%')}; border-radius: 1.5rem; }}
.location address {{ margin-top: 1.25rem; font-style: normal; font-size: 1.375rem; font-weight: 600; line-height: 1.3; color: var(--tinta); }}
.location .hint {{ margin-top: .7rem; color: var(--gris); max-width: 40ch; }}
.location .actions {{ display: flex; flex-wrap: wrap; gap: .8rem; margin-top: 1.6rem; }}
.map {{
  margin-top: 2rem; border-radius: 1.5rem; overflow: hidden; background: var(--cielo);
  aspect-ratio: 16 / 10; display: grid; place-items: center; position: relative;
}}
.map span {{ color: var(--gris); font-size: .9375rem; padding: 1rem; text-align: center; }}
.map iframe {{ position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }}

/* Cierre */
.cta {{ background: var(--cielo); padding-block: 4.5rem; text-align: center; }}
.cta h2 {{ font-size: clamp(2.2rem, 6.5vw, 3.75rem); font-weight: 750; line-height: 1; letter-spacing: -.035em; color: var(--tinta); text-wrap: balance; }}
.cta p {{ margin: 1rem auto 0; max-width: 40ch; color: var(--gris); }}
.cta .btn {{ margin-top: 1.9rem; }}

footer {{ background: #fff; padding-block: 2.5rem 6.5rem; font-size: .9375rem; color: var(--gris); }}
footer .wrap {{ display: grid; gap: 1.5rem; }}
footer a {{ color: var(--tinta); font-weight: 600; text-underline-offset: .25em; }}
footer .note {{ font-size: .8125rem; border-top: 1px solid var(--linea); padding-top: 1.25rem; }}

/* Temas de reseñas */
.topics-label {{ margin-top: 1.4rem !important; font-size: .9375rem; }}
.topics {{ display: flex; flex-wrap: wrap; gap: .5rem; margin-top: .6rem; }}
.topics li {{ font-size: .875rem; font-weight: 600; padding: .3rem .8rem; border-radius: 999px; border: 1px solid rgba(255,255,255,.35); }}

/* Redes */
.social {{ padding-block: 4rem; border-top: 1px solid var(--linea); }}
.social .wrap {{ display: grid; gap: 2rem; align-items: center; }}
.social-cards {{ display: grid; gap: .8rem; }}
.social-card {{
  display: grid; gap: .15rem; text-decoration: none; padding: 1.1rem 1.4rem;
  border: 2px solid var(--tinta); border-radius: 1.25rem; color: var(--tinta);
  transition: background-color .15s, color .15s;
}}
.social-card:hover {{ background: var(--tinta); color: #fff; }}
.social-card .net {{ font-size: .8125rem; font-weight: 650; text-transform: uppercase; letter-spacing: .06em; opacity: .75; }}
.social-card b {{ font-size: 1.375rem; font-weight: 700; letter-spacing: -.01em; }}
.social-card span:last-child:not(.net) {{ font-size: .9375rem; opacity: .8; }}

/* Distintivos */
.badges {{ display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1.4rem; }}
.badges li {{
  font-size: .875rem; font-weight: 650; color: var(--tinta);
  background: var(--cielo); border: 1px solid var(--linea);
  padding: .35rem .8rem; border-radius: 999px;
}}

/* Urgencias */
.urgent {{ background: var(--turquesa); color: #fff; padding-block: 3rem; }}
.urgent .wrap {{ display: grid; gap: 1.5rem; align-items: center; }}
.urgent h2 {{ font-size: clamp(1.75rem, 4.5vw, 2.5rem); font-weight: 720; line-height: 1.05; letter-spacing: -.03em; }}
.urgent p {{ margin-top: .6rem; max-width: 46ch; opacity: .92; }}
.urgent .actions {{ display: flex; flex-wrap: wrap; gap: .8rem; }}

/* Barra fija en celular */
.mobile-cta {{
  position: fixed; inset: auto 0 0 0; z-index: 20;
  padding: .7rem 1rem calc(.7rem + env(safe-area-inset-bottom));
  background: rgba(255, 255, 255, .94); backdrop-filter: blur(8px);
  border-top: 1px solid var(--linea);
}}
.mobile-cta {{ display: flex; gap: .6rem; }}
.mobile-cta .btn {{ flex: 1; }}
.mobile-cta .btn-call {{ flex: none; width: 3.25rem; padding: 0; }}
.mobile-cta .btn-call .wa {{ width: 1.4rem; height: 1.4rem; }}
.mobile-cta[hidden] {{ display: none; }}
.only-desktop {{ display: none; }}

@media (min-width: 860px) {{
  body {{ font-size: 1.125rem; }}
  .only-desktop {{ display: flex; }}
  .mobile-cta {{ display: none; }}
  footer {{ padding-bottom: 2.5rem; }}
  .hero .wrap {{ grid-template-columns: minmax(0, 1fr) minmax(0, 1.12fr); gap: 3rem; padding-block: 2.5rem 5rem; }}
  .hero img {{ aspect-ratio: 6 / 5; border-radius: 2rem 2rem 2rem 9rem; }}
  .services, .location, .cta {{ padding-block: 6.5rem; }}
  .group {{ grid-template-columns: minmax(0, 4fr) minmax(0, 8fr); gap: 3rem; padding-block: 2.5rem; }}
  .reviews {{ padding-block: 5rem; }}
  .social .wrap {{ grid-template-columns: 1fr 1fr; gap: 4rem; }}
  .social {{ padding-block: 5rem; }}
  .urgent .wrap {{ grid-template-columns: 1fr auto; gap: 3rem; }}
  .reviews .wrap {{ grid-template-columns: 1fr auto; gap: 3rem; }}
  .location .wrap {{ grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: 4rem; align-items: start; }}
  footer .wrap {{ grid-template-columns: 1.2fr 1fr 1fr; }}
  footer .note {{ grid-column: 1 / -1; }}
}}
@media (prefers-reduced-motion: reduce) {{
  html {{ scroll-behavior: auto; }}
  .btn {{ transition: none; }}
}}
</style>
</head>
<body>
<div class="demo-bar" role="note"><strong>Página de muestra.</strong> Es una propuesta de diseño, no el sitio oficial de {e(SITE['name'])}.</div>

<header class="top">
  <div class="wrap">
    <a class="brand" href="#inicio" aria-label="{e(SITE['name'])}, inicio"><b>{e(SITE['name'])}</b><span>{e(SITE['tagline'])}</span></a>
    <nav class="only-desktop" aria-label="Principal">
      <a href="#servicios">Servicios</a>
      <a href="#opiniones">Opiniones</a>
      <a href="#ubicacion">Ubicación</a>
      <a class="btn btn-primary" href="{book}" target="_blank" rel="noopener">{WA_ICON}{e(COPY['book_label'])}</a>
    </nav>
  </div>
</header>

<main id="inicio">
  <section class="hero">
    <div class="wrap">
      <div>
        <h1>{e(SITE['slogan'])}</h1>
        <p class="intro">{e(SITE['intro'])}</p>
        {badges_html}
        <div class="actions">
          <a class="btn btn-primary" href="{book}" target="_blank" rel="noopener">{WA_ICON}{e(COPY['book_label'])} por WhatsApp</a>
          {call_btn or '<a class="btn btn-ghost" href="#servicios">Ver servicios</a>'}
        </div>
        <a class="rating" href="{e(SITE['maps_url'])}" target="_blank" rel="noopener">
          <span class="stars" aria-hidden="true">{stars_html}</span>
          <span>{e(SITE['rating'])} de 5 en Google, con {reviews_n} reseñas</span>
        </a>
      </div>
      <figure>
        <img src="{data_uri(hero, 80)}" width="{hero.width}" height="{hero.height}" alt="{e(SITE['hero']['alt'])}">
        {caption_html}
      </figure>
    </div>
  </section>

  <section class="services" id="servicios">
    <div class="wrap">
      <h2 class="section-title">Servicios</h2>
      <p class="section-lead">{e(COPY['services_lead'])}</p>
      <div class="groups">{''.join(groups_html)}</div>
    </div>
  </section>
{urgent_html}

  <section class="reviews" id="opiniones">
    <div class="wrap">
      <div>
        <span class="stars" role="img" aria-label="{e(stars_label)}">{stars_html}</span>
        <h2>{e(SITE['rating'])} de 5 en Google</h2>
        <p>Es el promedio de {reviews_n} reseñas de {e(COPY['reviewers'])}, a {e(SITE['reviews_asof'])}.</p>
        {topics_html}
      </div>
      <a class="btn btn-light" href="{e(SITE['maps_url'])}" target="_blank" rel="noopener">Leer las reseñas en Google</a>
    </div>
  </section>

  <section class="location" id="ubicacion">
    <div class="wrap">
      <figure>
        <img src="{data_uri(facade, 78)}" width="{facade.width}" height="{facade.height}" loading="lazy" alt="{e(SITE['facade']['alt'])}">
      </figure>
      <div>
        <h2 class="section-title">Cómo llegar</h2>
        <address>{e(SITE['address'])}<br>{e(SITE['area'])}, {e(SITE['city'])}</address>
        <p class="hint">{e(SITE['entrance_hint'])}</p>
        <div class="actions">
          <a class="btn btn-primary" href="{e(SITE['maps_url'])}" target="_blank" rel="noopener">Abrir en Google Maps</a>
          <a class="btn btn-ghost" href="{e(wa(COPY['directions_wa']))}" target="_blank" rel="noopener">Pedir indicaciones</a>
        </div>
        <div class="map">
          <span>{e(full_address)}</span>
          <iframe title="Mapa de {e(SITE['name'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
            src="https://www.google.com/maps?q={quote(SITE['maps_embed_q'])}&output=embed"></iframe>
        </div>
      </div>
    </div>
  </section>

{social_html}
  <section class="cta">
    <div class="wrap">
      <h2>{e(COPY['cta_title'])}</h2>
      <p>{e(COPY['cta_text'])}</p>
      <a class="btn btn-primary" href="{book}" target="_blank" rel="noopener">{WA_ICON}Escribir al {e(SITE['whatsapp_display'])}</a>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <div><a class="brand" href="#inicio"><b>{e(SITE['name'])}</b><span>{e(SITE['tagline'])}</span></a></div>
    <div>{e(SITE['address'])}<br>{e(SITE['area'])}, {e(SITE['city'])}</div>
    <div>
      <a href="{book}" target="_blank" rel="noopener">WhatsApp {e(SITE['whatsapp_display'])}</a><br>
      {tel_footer}
      {social_footer}
    </div>
    <p class="note">Página de muestra creada como propuesta de diseño; no es el sitio oficial de {e(SITE['name'])}. {e(COPY['sources'])}</p>
  </div>
</footer>

<div class="mobile-cta"><a class="btn btn-primary" href="{book}" target="_blank" rel="noopener">{WA_ICON}{e(COPY['book_label'])} por WhatsApp</a>{mobile_call}</div>
<script>
(function () {{
  var bar = document.querySelector('.mobile-cta');
  var heroActions = document.querySelector('.hero .actions');
  if (!bar || !heroActions || !('IntersectionObserver' in window)) return;
  bar.hidden = true;
  new IntersectionObserver(function (entries) {{
    bar.hidden = entries[0].isIntersecting;
  }}).observe(heroActions);
}})();
</script>
</body>
</html>
"""

out = ROOT / slug / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(PAGE, encoding="utf-8")
print(f"{out.relative_to(ROOT)}: {len(PAGE) / 1024:.0f} KB")
