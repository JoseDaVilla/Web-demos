# web-demos

Design proposals for local businesses. Each demo is a single self-contained
HTML page, published with GitHub Pages at `/<slug>/`.

## Layout

```
build/build.py        Shared clinic template and build script
build/fonts/          Bricolage Grotesque (SIL Open Font License)
sites/<slug>.json     Content for one demo
<slug>/index.html     Built page (committed, this is what Pages serves)
```

## Build a demo

```bash
pip install pillow
python3 build/build.py sites/oral-life.json /path/to/photos
```

The photos directory holds the image files named in the site JSON (`hero.file`
and `facade.file`). Source photos are not committed; the built page inlines the
resized copies it needs.

## Optional site fields

All of these are optional; a site file without them builds the original clinic page.

- `theme`: colors (`ink`, `accent`, `accent_light`, `sky`, `cloud`, `line`, `on_ink`). Take them from the business's Instagram or its facade.
- `copy`: wording that changes by niche (`book_label`, `reviewers`, `directions_wa`, `services_lead`, `cta_title`, `cta_text`, `sources`, `social_title`, `social_lead`).
- `badges`: short facts shown under the intro, e.g. "Abierto las 24 horas".
- `phone_e164` / `phone_display`: adds "Llamar" buttons.
- `urgent`: `{title, text, wa_text}` band for places that take emergencies.
- `social`: list of `{network, handle, url, note}`; replaces the older `instagram` key.
- `review_topics`: the topics Google shows above the reviews.
- `open_24h`: `true` swaps the headline for the live time in Colombia ("Son las 3:42 p. m. y estamos abiertos"). Only for places Google lists as open 24 hours.

## Content rules

- Use only facts from the business's public profile or its own material.
- Never invent testimonials, staff names, prices or opening hours. Leave out
  anything that is not known.
- Every demo keeps the "Página de muestra" notice and `noindex, nofollow`.
- No forms and no payments. Contact buttons point to the business's own
  WhatsApp, Maps and Instagram.

## Never commit

API keys, tokens or the lead list. Leads live in Notion.
