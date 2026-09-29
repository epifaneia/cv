# CV · Daniel Martín

**[Español (PDF)](Daniel_Martin_AI_Engineer_ES.pdf) · [English (PDF)](Daniel_Martin_AI_Engineer_EN.pdf)**

AI Engineer · AI solutions for regulated processes · [epifaneia.dev](https://epifaneia.dev)

> AI carries risk. Code bounds it. The standard answers for what remains.
> *La IA tiene riesgos. El código los acota. La norma responde de lo que queda.*

---

## What this repository is

The CV, and the small pipeline that produces it. The content lives as data in `build_cv.py` (two dictionaries, Spanish and English); a template renders it as a self-contained HTML page (the photo is embedded, no external requests) and Microsoft Edge prints it to a one-page A4 PDF. Every build checks the page count: if the content does not fit on one page, the build says so.

```
datos (ES, EN)  →  plantilla HTML  →  Edge headless  →  PDF de una página  →  comprobación
```

## Build

```bash
pip install pymupdf
python build_cv.py        # writes Daniel_Martin_AI_Engineer_ES/EN.html and .pdf next to the script
```

Requires Microsoft Edge (Windows path in the script) and Python 3.11+. To change the content, edit the `ES` and `EN` dictionaries; to change the look, edit the `CSS` block.

## Qué es este repositorio

El CV y el pequeño pipeline que lo produce. El contenido vive como datos en `build_cv.py` (dos diccionarios, español e inglés); una plantilla lo convierte en una página HTML autocontenida (la foto va incrustada, sin peticiones externas) y Microsoft Edge la imprime a un PDF A4 de una página. Cada construcción comprueba el número de páginas: si el contenido no cabe en una, lo dice.

## Credits

The layout follows the [Orbit](https://github.com/xriley/Orbit-Theme) resume theme by Xiaoying Riley (3rd Wave Media), reimplemented from scratch in a single file. Icons are hand-drawn SVG paths in the Feather style.

## Licence

Code (`build_cv.py`) under Apache-2.0. The CV content and the photo are personal data of Daniel Martín: read them, do not reuse them.
