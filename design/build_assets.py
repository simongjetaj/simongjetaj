#!/usr/bin/env python3
"""Build original, self-contained SVG artwork. Requires fonttools==4.65.0."""
from pathlib import Path
import html
ROOT = Path(__file__).resolve().parents[1]
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONTS = ROOT / 'design/fonts'
def face(filename, optical_size):
    return instantiateVariableFont(TTFont(FONTS / filename), {'wght': 400, 'opsz': optical_size})

regular = face('Newsreader-Regular.ttf', 32)
italic = face('Newsreader-Italic.ttf', 32)
footer_regular = face('Newsreader-Regular.ttf', 16)
footer_italic = face('Newsreader-Italic.ttf', 16)


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
    'light': {'ink': '#252B32', 'accent': '#A34D2E'},
    'dark': {'ink': '#F0EEE8', 'accent': '#E7A385'},
}
(ROOT / 'assets').mkdir(exist_ok=True)
for mode, c in PALETTES.items():
    # Three unequal, tapered strokes suggest directional light in the open margin.
    body = ['<g transform="translate(930 58) scale(.82) translate(-930 -58)">', f'<path d="M886 78C895 53 912 32 935 17C922 40 903 61 886 78Z" fill="{c["accent"]}" opacity=".62"/>',
            f'<path d="M908 82C921 65 939 53 959 49C942 61 926 73 908 82Z" fill="{c["accent"]}" opacity=".82"/>',
            f'<path d="M927 95C943 90 958 90 974 93C958 97 943 98 927 95Z" fill="{c["accent"]}" opacity=".42"/>', '</g>']
    p, cursor = lettering('My work ', regular, 95, 0, 76, c['ink'])
    body.append(p)
    p, cursor = lettering('starts', italic, 95, cursor, 76, c['accent'])
    body.append(p)
    p, cursor = lettering(' where', regular, 95, cursor, 76, c['ink'])
    body.append(p)
    p, cursor = lettering('the playbook ', regular, 95, 250, 190, c['ink'])
    body.append(p)
    p, cursor = lettering('ends.', italic, 95, cursor + 2, 190, c['accent'])
    body.append(p)
    (ROOT / 'assets' / f'masthead-{mode}.svg').write_text(svg('\n'.join(body), 1000, 240,
        'My work starts where the playbook ends.',
        'An offset editorial headline. Warm italic words are accompanied by three small tapered strokes of light in the open margin.'))
    for slug, label, font, width in [
        ('email', 'Say hello', footer_italic, 100),
        ('linkedin', 'LinkedIn', footer_regular, 106),
    ]:
        path, end = lettering(label, font, 22, 1, 25, c['accent'])
        assert end < width, (label, end, width)
        (ROOT / 'assets' / f'link-{slug}-{mode}.svg').write_text(svg(path, width, 36, label,
            f'{label}, set in the same serif as the masthead.'))
print('Built two mastheads and four contact labels.')
