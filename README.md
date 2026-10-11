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

## Content rules

- Use only facts from the business's public profile or its own material.
- Never invent testimonials, staff names, prices or opening hours. Leave out
  anything that is not known.
- Every demo keeps the "Página de muestra" notice and `noindex, nofollow`.
- No forms and no payments. Contact buttons point to the business's own
  WhatsApp, Maps and Instagram.

## Never commit

API keys, tokens or the lead list. Leads live in Notion.
