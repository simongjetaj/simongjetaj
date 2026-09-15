#!/usr/bin/env python3
"""Build original, self-contained SVG artwork. Requires fonttools==4.65.0."""
from pathlib import Path
import html
ROOT = Path(__file__).resolve().parents[1]
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONTS = ROOT / 'design/fonts'
regular = TTFont(FONTS / 'InstrumentSerif-Regular.ttf')
italic = TTFont(FONTS / 'InstrumentSerif-Italic.ttf')


def kern(font, left, right):
    value = 0
    if 'GPOS' not in font:
        return value
    for lookup in font['GPOS'].table.LookupList.Lookup:
        if lookup.LookupType != 2:
            continue
        for sub in lookup.SubTable:
            if left not in sub.Coverage.glyphs:
                continue
            if sub.Format == 1:
                pairset = sub.PairSet[sub.Coverage.glyphs.index(left)]
                for pair in pairset.PairValueRecord:
                    if pair.SecondGlyph == right:
                        value += getattr(pair.Value1, 'XAdvance', 0) if pair.Value1 else 0
                        break
            elif sub.Format == 2:
                c1 = sub.ClassDef1.classDefs.get(left, 0)
                c2 = sub.ClassDef2.classDefs.get(right, 0)
                rec = sub.Class1Record[c1].Class2Record[c2]
                value += getattr(rec.Value1, 'XAdvance', 0) if rec.Value1 else 0
    return value

def lettering(text, font, size, x, baseline, fill, tracking=0):
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font['head'].unitsPerEm
    pen = SVGPathPen(glyphs, ntos=lambda n: f'{n:.2f}'.rstrip('0').rstrip('.') if n else '0')
    names = [cmap[ord(c)] for c in text]
    cursor = x
    for i, name in enumerate(names):
        glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, cursor, baseline)))
        cursor += font['hmtx'][name][0] * scale + tracking
        if i + 1 < len(names):
            cursor += kern(font, name, names[i+1]) * scale
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>', cursor

def svg(body, width, height, title, desc):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title>
<desc id="desc">{html.escape(desc)}</desc>
{body}
</svg>\n'''

PALETTES = {
    'light': {'ink': '#252B32', 'accent': '#A34D2E', 'rule': '#C4BBB1'},
    'dark': {'ink': '#F0EEE8', 'accent': '#E7A385', 'rule': '#605B56'},
}
(ROOT / 'assets').mkdir(exist_ok=True)
for mode, c in PALETTES.items():
    body = []
    # The margin stops before the last word. The word extends beyond it.
    body.append(f'<path d="M886 0V123M886 243V269" fill="none" stroke="{c["rule"]}" stroke-width="1" vector-effect="non-scaling-stroke"/>')
    p, _ = lettering('My work starts where', regular, 114, 0, 90, c['ink'])
    body.append(p)
    p, end = lettering('the playbook ', regular, 114, 235, 218, c['ink'])
    body.append(p)
    p, end = lettering('ends.', italic, 114, end + 2, 218, c['accent'])
    body.append(p)
    print(mode, 'headline right edge', round(end, 2))
    (ROOT / 'assets' / f'masthead-{mode}.svg').write_text(svg('\n'.join(body), 1000, 285,
        'My work starts where the playbook ends.',
        'An editorial typographic signature. The final word steps beyond an interrupted margin.'))
    divider = f'<path d="M0 12H88" fill="none" stroke="{c["rule"]}" stroke-width="1.25"/><path d="M112 12H128" fill="none" stroke="{c["accent"]}" stroke-width="1.75"/>'
    (ROOT / 'assets' / f'divider-{mode}.svg').write_text(svg(divider, 130, 24,
        'Section separator', 'A quiet echo of the interrupted margin in the masthead.'))
